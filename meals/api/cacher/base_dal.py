# coding=utf8
import codecs
import threading
import time
import traceback
import MySQLdb
import json
from datetime import datetime, date

codecs.register(
    lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)


class BaseTypes(object):
    success = 0

    def __init__(self, __dict__={}):
        for k, v in __dict__.items():
            setattr(self, k, v)

class DefaultType(BaseTypes):
    pass

class SmartEncoder(json.JSONEncoder):
    '''
        只支持一层解析。
    '''
    def default(self, obj):
        # if isinstance(obj, datetime.datetime):
        #     return int(mktime(obj.timetuple()))
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def json_encode(obj):
    return json.dumps(obj, cls=SmartEncoder)

def get_where_op(k, v=''):
    '''
    >>> get_where_op('a')
    'a = %s'
    >>> get_where_op('a__ne')
    'a != %s'
    >>> get_where_op('a__lt')
    'a < %s'
    >>> get_where_op('a__isnull', False)
    'a is not null'
    >>> get_where_op('a__regexp')
    'a regexp %s'
    >>> get_where_op('a', [1, 2])
    'a in %s'
    '''

    op_map = dict(
        ne='!=',
        lt='<',
        lte='<=',
        gt='>',
        gte='>=',
        isnull='isnull',
        regexp='regexp'
        )

    parts = k.rsplit('__', 1)
    if len(parts) == 2:
        k, op = parts
        op = op_map[op]
    else:
        k = parts[0]
        op = 'in' if isinstance(v, (list, tuple)) else '='

    if op == 'isnull':
        return '%s is %s' % (k, 'null' if v else 'not null')
    else:
        return '%s %s %%s' % (k, op)


def get_where_sql(where):
    '''
    >>> get_where_sql(['a.b', 'c'])
    'a.b = %s and c = %s'
    >>> get_where_sql(['a__ne'])
    'a != %s'
    >>> get_where_sql(dict(a=[1,2], b='x'))
    'a in %s and b = %s'
    '''
    if isinstance(where, (list, tuple)):
        where_keys = where
        where = {x: '' for x in where}
    else:
        where_keys = where.keys()
    return ' and '.join(get_where_op(k, where[k]) for k in where_keys)


def get_insert_sql(
    table, keys, on_duplicate_update=False,
        ignore=False, dup_unupdate_keys=[], primary_key=''):
    '''
    >>> get_insert_sql('foo', ['a', 'b'])
    'insert into foo (a, b) values (%s, %s)'
    >>> get_insert_sql(
    ...     'foo', ['a', 'b'], on_duplicate_update=True, primary_key='id')
    'insert into foo (a, b) values (%s, %s) \
ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id), a=values(a), b=values(b)'
    >>> get_insert_sql(
    ...     'foo', ['a', 'b'], on_duplicate_update=True,
    ...     dup_unupdate_keys=['a', ])
    'insert into foo (a, b) values (%s, %s) \
ON DUPLICATE KEY UPDATE b=values(b)'
    '''
    sql = 'insert into %s (%s) values (%s)' % (
        table, ', '.join(keys), ', '.join(['%s'] * len(keys)))
    if on_duplicate_update:
        odu_clause = ', '.join(
            '%s=values(%s)' % (k, k) for k in keys
            if k not in dup_unupdate_keys
            )
        id_prefix = '%s=LAST_INSERT_ID(%s), ' % (primary_key, primary_key) \
            if primary_key else ''
        odu_clause = ' ON DUPLICATE KEY UPDATE %s' % (id_prefix + odu_clause, )
        sql = sql + odu_clause
    return sql


def get_update_sql(table, update_keys, where):
    '''
    >>> get_update_sql('foo', ['a', 'b'], dict(a=1, b=2))
    'update foo set a=%s, b=%s where a = %s and b = %s'
    >>> get_update_sql('foo', ['a'], dict(id__isnull=True))
    'update foo set a=%s where id is null'
    '''
    sql = 'update %s set %s where %s' % (
        table,
        ', '.join(x + '=%s' for x in update_keys),
        get_where_sql(where),
        )
    return sql


def get_delete_sql(table, where):
    '''
    >>> get_delete_sql('foo', dict(a=1, b=2))
    'delete from foo where a = %s and b = %s'
    >>> get_delete_sql('foo', dict(id__isnull=True))
    'delete from foo where id is null'
    '''
    sql = 'delete from %s where %s' % (
        table,
        get_where_sql(where),
        )
    return sql


def get_select_sql(
        table, keys, where=None, extra=None, order_by=None, limit=None):
    '''
    >>> get_select_sql('foo', ['a', 'b'], order_by='a asc', limit=1)
    'select a, b from foo order by a asc limit 1'
    >>> get_select_sql('foo', ['a', 'b'], extra="order by a asc", limit=1)
    'select a, b from foo order by a asc limit 1'
    >>> get_select_sql('foo', ['a', 'b'], extra="order by a asc", limit='1, 2')
    'select a, b from foo order by a asc limit 1, 2'
    >>> get_select_sql('foo', ['a', 'b'], ['b', 'c'])
    'select a, b from foo where b = %s and c = %s'
    >>> get_select_sql('foo', ['a', 'b'], where=dict(a__ne=5, b__isnull=True))
    'select a, b from foo where b is null and a != %s'
    '''

    sql = 'select %s from %s' % (', '.join(keys), table)
    if where:
        sql += ' where ' + get_where_sql(where)
    if order_by:
        sql += ' order by ' + order_by
    if extra:
        sql += ' ' + extra
    if limit:
        sql += ' limit %s' % limit
    return sql


def unfold_one(lst):
    if isinstance(lst, (list, tuple)) and len(lst) == 1:
        return lst[0]
    else:
        return lst

local_conn = None

class DAL(threading.local):
    def __init__(self, host, name, user, passwd, port=3306, charset='utf8'):
        self.host, self.port, self.name, self.user, self.passwd = \
            host, int(port), name, user, passwd
        self.conn_key = '%s:%s@%s:%s/%s' % (user, passwd, host, port, name)
        self.cursor = None
        self.conn = None
        self.charset = charset

    def open(self):
        global local_conn
        if not local_conn:
            local_conn = threading.local()
        if not hasattr(local_conn, 'connections'):
            local_conn.connections = {}
        conn = local_conn.connections.get(self.conn_key)
        if not conn:
            conn = MySQLdb.connect(
                host=self.host, port=self.port, user=self.user,
                passwd=self.passwd, db=self.name, charset=self.charset
                )
            conn.autocommit(True)
            local_conn.connections[self.conn_key] = conn

        self.conn = conn
        self.cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    def get_cursor(self):
        if not self.cursor:
            self.open()
        return self.cursor

    def execute(self, sql_fmt, *params):
        retry = 0
        while True:
            retry += 1
            try:
                # cursor = self.get_cursor() // 老代码
                self.get_cursor()
                self.cursor.execute(sql_fmt, params)
                break
            except:
                self.close()
                if retry >= 2:
                    raise

    def executemany(self, sql_fmt, *params):
        retry = 0
        while True:
            retry += 1
            try:
                # cursor = self.get_cursor() // 老代码
                self.get_cursor()
                self.cursor.executemany(sql_fmt, params)
                break
            except:
                self.close()
                if retry >= 2:
                    raise

    def close(self):
        global local_conn
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.conn:
            conn = local_conn.connections.pop(self.conn_key, None)
            if conn:
                conn.close()
            self.conn = None

    # 需要支持事务
    def begin(self, ):
        self.get_cursor()
        self.conn.begin()

    def commit(self, ):
        self.get_cursor()
        self.conn.commit()

    def rollback(self, ):
        self.get_cursor()
        self.conn.rollback()

class BaseDAL(DAL):
    def insert(
        self, table, info, on_duplicate_update=False,
            unique_keys={}, dup_unupdate_keys=[]):
        if not info:
            return None, 'no values'
        try:
            sql = get_insert_sql(
                table, info.keys(), on_duplicate_update,
                dup_unupdate_keys=dup_unupdate_keys,
                primary_key='id',
                )
            self.execute(sql, *info.values())
            return self.cursor.connection.insert_id(), 'new insert'
        except MySQLdb.IntegrityError:
            if unique_keys:
                rs = self.fetchone(table, ['id', ], where=unique_keys)
                if rs:
                    return rs['id'], 'already exist, insert error'
            raise
        except:
            raise

    def update(self, table, info, **where):
        if 'where' in where:
            where = where['where']
        if not info or not where:
            return
        # workaround: MySQLdb对于只有一个元素的list执行in操作有bug
        where = {k: unfold_one(v) for k, v in where.iteritems()}
        # isnull没有%s, 故需从values中去掉
        where_values = [
            v for k, v in where.iteritems()
            if not k.endswith('__isnull')]
        sql = get_update_sql(table, info.keys(), where)
        self.execute(sql, *(info.values() + where_values))

    def delete(self, table, **where):
        if 'where' in where:
            where = where['where']
        if not where:
            return
        # workaround: MySQLdb对于只有一个元素的list执行in操作有bug
        where = {k: unfold_one(v) for k, v in where.iteritems()}
        # isnull没有%s, 故需从values中去掉
        where_values = [
            v for k, v in where.iteritems()
            if not k.endswith('__isnull')]
        sql = get_delete_sql(table, where)
        self.execute(sql, *where_values)

    def _fetch(self, one, table, keys, order_by=None, limit=None, **where):
        if 'where' in where:
            where = where['where']
        # workaround: MySQLdb对于只有一个元素的list执行in操作有bug
        where = {k: unfold_one(v) for k, v in where.iteritems()}
        sql = get_select_sql(
            table, keys, where, order_by=order_by, limit=limit)
        # isnull没有%s, 故需从values中去掉
        where_values = [
            v for k, v in where.iteritems() if not k.endswith('__isnull')]
        self.execute(sql, *where_values)
        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def fetchone(self, table, keys, order_by=None, **where):
        return self._fetch(
            True, table, keys, order_by=order_by, limit=1, **where)

    def fetchall(self, table, keys, order_by=None, limit=None, **where):
        return self._fetch(
            False, table, keys, order_by=order_by, limit=limit, **where)

    def fetch_by_sql(self, sql, one=False):
        self.execute(sql)
        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()


class MealsBaseDAL(BaseDAL):
    _SLOW_QUERY_RUNNING_TIME_IN_SECONDS = 0.5

    def __init__(self, db_conn_args):
        super(MealsBaseDAL, self).__init__(**db_conn_args)

    def _db_get_table_record(self, table, columns, where, order_by=None):
        records = self.fetchall(table, columns, where=where, order_by=order_by)
        record = records[0] if records else {}
        return self._db_convert_record_to_object(record)

    def _db_convert_record_to_object(self, record):
        object = DefaultType(record)
        return json.loads(json_encode(object.__dict__))

    def _db_get_table_records(self, table, columns, where, order_by=None, limit=None):
        rs = self.fetchall(table, columns, where=where, order_by=order_by, limit=limit)
        return self._db_convert_rs_to_arr(rs)

    def _db_convert_rs_to_arr(self, rs):
        if not rs:
            return []
        else:
            records = [DefaultType(r) for r in rs]

            results = []
            for record in records:
                results.append(json.loads(json_encode(record.__dict__)))

            return results

    def execute(self, sql_fmt, *params):
        # Override to log SQL info and corresponding time info.
        begin_time = time.time()

        retry = 0
        while True:
            retry += 1
            try:
                # cursor = self.get_cursor() // 老代码
                self.get_cursor()
                self.cursor.execute(sql_fmt, params)
                break
            except:
                try:
                    self.close()
                except Exception as err:
                    traceback.print_exc()

                if retry >= 2:
                    raise

        end_time = time.time()
        latency = end_time - begin_time
        if latency > self._SLOW_QUERY_RUNNING_TIME_IN_SECONDS:
            try:
                tel_data = {
                    'begin_time': begin_time,
                    'latency': latency,
                    'sql': unicode(sql_fmt % params),
                    'params': unicode(params),
                }
            except Exception:
                traceback.print_exc()

    def begin(self):
        """
        This is used to avoid the MySQL server has gone away issue
        """
        retry = 0
        while True:
            retry += 1
            try:
                # cursor = self.get_cursor() // 老代码
                self.get_cursor()
                self.conn.begin()
                break
            except Exception:
                self.close()
                if retry >= 2:
                    raise
