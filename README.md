
# meals
apt-get install git    
apt-get install mysql    
apt-get install python-dev nginx    
apt-get install libmysqlclient-dev    
apt-get install mysql-server    
apt-get install python-pip python-dev build-essential    
修改python path    
pip install -r requirement    
create database meals    


---

## API documents

### 登录

key | value | 备注
---|---|---
url | api/login/ |
method | post|
request | ```{"user_name": "admin", "password": "123456"}```|
response | ```{"admin_type": 1, "user_id": 1, "company_id": 1}```| admin_type, 0: 员工，1：餐厅，2：企业管理员，3：系统管理员
need permission| - |


### 登出

key | value | 备注
---|---|---
url | api/logout/ |
method | post|
request |```{}```|
response |```{}```|
need permission| 0,1,2,3 |

### 重置密码

key | value | 备注
---|---|---
url | api/user/reset/ |
method | post|
request |```{"user_id": 1, "password": "123456", "new_password": "abcdefg"}```|
response |```{}```|
need permission| 0,1,2,3 |

### 公司账号列表

key | value | 备注
---|---|---
url | api/company/admin/|
method | get|
request |```{}```|
response |```{"company_id": 1, "user_id": 2, "user_name": "admin001", "phone_number": "123456789", "company_name": "XXX公司"}```|
need permission| 3 |

### 添加公司及管理员

key | value | 备注
---|---|---
url | api/company/add/|
method | post|
request |```{"company_name": "XXX公司", "province": "北京市", "address": "知春路致真大厦", "phone_number": "12345678"}```|
response |```{"company_id": 1, "admin_name": "admin001", "password": "123456"}```|
need permission| 3 |

### 公司列表
key | value | 备注
---|---|---
url | api/company/list/ |
method | get |
request |```{}```|
response |```[{"company_id": 1, "company_name": "xxx公司"}, ...]```|
need permission| 3 |

### 添加公司管理员
key | value | 备注
---|---|---
url |api/company/admin/add/ |
method | post |
request |```{"company_id": 1, "admin_name": "admin", "password": "123456"}```|
response |```{"company_id": 1, "admin_name": "admin", "password": "123456", }```|
need permission| 3 |

### 重置管理员密码
key | value | 备注
---|---|---
url | api/company/admin/reset/ |
method | post |
request |```{"user_id": 1, "password": "123456"}```|
response |```{"user_id": 1, "password": "123456"}```|
need permission| 3 |

### 创建公司部门
key | value | 备注
---|---|---
url | api/company/department/add/ |
method | post |
request |```{"company_id": 1, "department_name": "研发部"}```|
response |```{"department_id": 2, "department_name": "研发部", "company_id": 1}```|
need permission| 2, 3 |

### 部门列表
key | value | 备注
---|---|---
url | api/company/department/list/ |
method | get |
request |```{"company_id": 1}```|
response |```[{"department_id": 1, "department_name": "研发部"}, ...]```|
need permission| 2, 3 |


### 添加员工账号
key | value | 备注
---|---|---
url | api/user/add/ |
method | post |
request |```{"user_name": "zhangsan", "real_name": "张三", "company_id": 1, "department_id": 2, "gender": 1, "phone_number": "123456", "password": "123456"}```| gender 性别, 0: 位置, 1: 男, 2: 女
response |```{"user_id": 1, "user_name": "zhangsan", "real_name": "张三", "company_id": 1, "department_id": 2, "gender": 1, "phone_number": "123456", "admin_type": 0, "password": "123456"}```|
need permission| 2,3 |

### 员工列表
key | value | 备注
---|---|---
url | api/user/list/ |
method | get |
request |```{"company_id": 1}```|
response |```[{"user_id": 1, "department_id": 1, "department_name": "研发部", "real_name": "张三", "left_rmb": 0, "to_settle": 0}, ...]```|
need permission| 2, 3 |

### 添加菜品
key | value | 备注
---|---|---
url | api/restaurant/dish/add/ |
method | post |
request |```{"name": "狮子头", "price": 20.0, "restaurant_id": 1, "image_url": "", "support_times": "[1,2,3]"}```| support_times: 供餐时间段，时间段id的list
response |```{"dish_id": 1, "name": "狮子头", "price": 20.0, "restaurant_id": 1, "image_url": "", "support_times": "[1,2,3]"}```|
need permission| 3  |

### 菜品清单
key | value | 备注
---|---|---
url | api/restaurant/dish/list/ |
method | get |
request |```{"restaurant_id": 1, "time_range_id": 1}```|
response |```[{"dish_id": 1, "name": "狮子头", "price": 20.0, "image_url": "", "support_times": "[1,2,3]"}, ...]```|
need permission| 0,1,2,3 |

### 查询用餐时间段
key | value | 备注
---|---|---
url | api/restaurant/time_range/list/ |
method | get |
request |```{}```|
response |```[{"time_range_id": 1, "name": "午餐", "start_time": "10:00:00", "end_time": "14:00:00"}, ...]```|
need permission| 0,1,2,3 |

### 新建用餐时间段
key | value | 备注
---|---|---
url | api/restaurant/time_range/add/ |
method | post |
request |```{"name": "下午茶", "start_time": "14:00:00", "end_time": "16:00:00"}```|
response |```{"time_range_id": 2, "name": "下午茶", "start_time": "14:00:00", "end_time": "16:00:00"}```|
need permission| 3 |

### 启用用餐时间段
key | value | 备注
---|---|---
url | api/restaurant/time_range/enable/ |
method | post |
request |```{"dish_id": 1, "time_range_id": 2}```|
response |```{"dish_id": 1, "name": "狮子头", "price": 20.0, "image_url": "", "support_times": "[1,2,3]"}```|
need permission| 3  |

### 取消用餐时间段
key | value | 备注
---|---|---
url | api/restaurant/time_range/disable/ |
method | post |
request |```{"dish_id": 1, "time_range_id": 2}```|
response |```{"dish_id": 1, "name": "狮子头", "price": 20.0, "image_url": "", "support_times": "[1,2,3]"}```|
need permission| 3  |


### 创建餐厅
key | value | 备注
---|---|---
url | api/restaurant/add/ |
method | post |
request |```{"restaurant_name": "红红火火餐厅", "phone_number": "123456", "address": "海淀区XXXX"}```|
response |```{"restaurant_id": 1, "restaurant_name": "红红火火餐厅", "phone_number": "123456", "address": "海淀区XXXX"}```|
need permission| 3 |

### 餐厅列表
key | value | 备注
---|---|---
url | api/restaurant/list/ |
method | get |
request |```{}```|
response |```[{"restaurant_id": 1, "restaurant_name": "红红火火餐厅", "phone_number": "123456", "address": "海淀区XXXX"}, ...]```|
need permission| 0,1,2,3  |

### 删除餐厅
key | value | 备注
---|---|---
url | api/restaurant/delete/ |
method | post |
request |```{"restaurant_id": 1}```|
response |```{}```|
need permission| 3 |

### 订餐
key | value | 备注
---|---|---
url | api/user/meals/order/ |
method | post |
request |```{"user_id": 1, "order_list": "[{'dish_id': 1, 'count': 1}, ...]"}```|
response |```{"user_id": 1, "order_id": 1, "order_list": "[{'dish_id': 1, 'count': 1}, ...]", "order_total_price": 99.99}```|
need permission| 0,1,2,3  |

###
key | value | 备注
---|---|---
url | |
method | |
request |```{}```|
response |```{}```|
need permission|  |
