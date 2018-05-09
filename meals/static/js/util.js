(function() {
    var _cache = {};
    var _reg_space = /[\r\t\n]/g;
    var _reg_trim_left = /^\s+/;
    var _reg_trim_right = /\s+$/;
    var _reg_spaces = />\s*(.*?)\s*</g;
    var _reg_right = /((^|%>)[^\t]*)'/g;
    var _reg_equal = /\t=(.*?)%>/g;
    var _temp_year, _temp_month, _temp_date, _temp_hour, _temp_minute, _temp_second;
    function _to_two_digit(num) {
        return num < 10 ? "0" + num: num
    }
    function _get_date_part(part) {
        switch (part) {
        case "yyyy":
            return _temp_year;
        case "yy":
            return _temp_year.toString().slice( - 2);
        case "MM":
            return _to_two_digit(_temp_month);
        case "M":
            return _temp_month;
        case "dd":
            return _to_two_digit(_temp_date);
        case "d":
            return _temp_date;
        case "HH":
            return _to_two_digit(_temp_hour);
        case "H":
            return _temp_hour;
        case "hh":
            return _to_two_digit(_temp_hour > 12 ? _temp_hour - 12 : _temp_hour);
        case "h":
            return _temp_hour > 12 ? _temp_hour - 12 : tempHour;
        case "mm":
            return _to_two_digit(_temp_minute);
        case "m":
            return _temp_minute;
        case "ss":
            return _to_two_digit(_temp_second);
        case "s":
            return _temp_second;
        default:
            return part
        }
    }
    function _replace_string(str) {
        return "var p=[];" + "with(tmplData){p.push('" + str.replace(_reg_trim_left, "").replace(_reg_trim_right, "").replace(_reg_space, " ").replace(_reg_spaces, ">$1<").split("<%").join("\t").replace(_reg_right, "$1\r").replace(_reg_equal, "',$1,'").split("\t").join("');\n").split("%>").join("\np.push('").split("\r").join("\\'") + "');}return p.join('');"
    }
    function _tmpl(str, data) {
        var funcBody = "",
        tmplElem = document.getElementById("tmpl_" + str);
        var fn = !/\W\//.test(str) && tmplElem ? _cache[str] = _cache[str] || tmpl(tmplElem.innerHTML) : new Function("tmplData", "tmpl", _replace_string(str));
        if (data) {
            try {
                return fn(data, _format_by_tmpl)
            } catch(exp) {}
        }
        return fn
    }
    function _format_by_tmpl(str, data) {
        data = data || {};
        if (typeof str === "function") {
            return str(data)
        }
        return _tmpl(str, data)
    }
    window.util = {
        format: function(param) {
            if (typeof param == "undefined") {
                return ""
            }
            if (typeof param != "object") {
                throw new Error("data sended to the server must be 'object'")
            }
            var s = [];
            for (var j in param) {
                s.push(encodeURIComponent(j) + "=" + encodeURIComponent(param[j]))
            }
            return s.join("&").replace(/%20/g, "+")
        },
        strip_time: function(dateStr) {
            return dateStr.replace(/\+0800|\S\S\S\+0800|CST/g, "")
        },
        get_length: function(str) {
            return Math.ceil(str.replace(/[\uFE30-\uFFA0\u2E80-\u9FFF\uac00-\ud7ff\u3000‘“”’]/g, "**").length / 2);
        },
        get_left_length: function(str) {
            return Math.floor(str.replace(/[\uFE30-\uFFA0\u2E80-\u9FFF\uac00-\ud7ff\u3000‘“”’]/g, "**").length / 2);
        },
        get_size: function(str) {
            return str.replace(/[\uFE30-\uFFA0\u2E80-\u9FFF\uac00-\ud7ff\u3000‘“”’]/g, "**").length;
        },
        is_legal: function(str) {
            for (var i = 0; i < str.length; i++) {
                if (str.charCodeAt(i) > 255) return false;
            }
            return true;
        },
        parse: function(str, data) {
            return _format_by_tmpl(str, data)
        },
        bubble_node: function(elem, condition, callBack) {
            var con = false;
            do {
                if (condition(elem)) {
                    con = true;
                    break
                } else {
                    elem = elem.parentNode
                }
            } while ( elem . parentNode );
            con && callBack()
        },
        bubble_node_n: function(elem, condition, callBack) {
            var con = true;
            do {
                if (condition(elem)) {
                    con = false;
                    break
                } else {
                    elem = elem.parentNode
                }
            } while ( elem . parentNode );
            con && callBack()
        },
        get_select_text: function() {
            if (document.selection) {
                return function() {
                    return document.selection.createRange().text
                }
            } else {
                return function() {
                    return document.getSelection()
                }
            }
        } (),
        format_date: function(time, formation) {
            var date = new Date(time);
            _temp_year = date.getFullYear();
            _temp_month = date.getMonth() + 1;
            _temp_date = date.getDate();
            _temp_hour = date.getHours();
            _temp_minute = date.getMinutes();
            _temp_second = date.getSeconds();
            return formation.replace(/y+|m+|d+|h+|s+|H+|M+/g, _get_date_part)
        },
        load_script: function(url, func) {
            var source = document.createElement("script");
            source.language = "javascript";
            source.type = "text/javascript";
            source.charset = "UTF-8";
            source.onload = source.onreadystatechange = function() {
                if (!source.readyState || "loaded" == source.readyState || "complete" == source.readyState) {
                    func()
                }
            };
            source.src = url;
            document.getElementsByTagName("head")[0].appendChild(source)
        },
        get_url_strs: function(url) {
            var vars = [],
            hash,
            str;
            if (url.indexOf("?") != -1) {
                str = url.substr(url.indexOf("?") + 1);
                var hashes = str.split("&")
            } else {
                var hashes = []
            }
            for (var i = 0; i < hashes.length; i++) {
                hash = hashes[i].split("=");
                vars[hash[0]] = hash[1]
            }
            return vars
        },
        get_url_str: function(name, url) {
            var url = url || document.location.href;
            return util.getUrlStrs(url)[name]
        },
        toggle_img: function(node) {
            node.onload = function() {
                if (this.width > this.height) {
                    this.style.height = "100%";
                    this.style.width = "auto"
                }
            };
            node.onerror = function() {
                this.src = ""
            }
        },
        is_ios: function() {
            if (!navigator) {
                return false
            }
            if (!navigator.userAgent) {
                return false
            }
            return /(iPhone|iPad|iPod|iOS)/i.test(navigator.userAgent)
        },
        count_chars: function(str, len, flag) {
            var strLen = str.replace(/[\u4e00-\u9fa5\s]/g, "**").length,
            newStr = [],
            totalCount = 0;
            if (strLen <= len) {
                return str
            } else {
                for (var i = 0; i < strLen; i++) {
                    var nowValue = str.charAt(i);
                    if (/[^\x00-\xff]/.test(nowValue)) {
                        totalCount += 2
                    } else {
                        totalCount += 1
                    }
                    newStr.push(nowValue);
                    if (totalCount >= len) {
                        break
                    }
                }
                if (flag) {
                    return newStr.join("")
                } else {
                    return newStr.join("") + "..."
                }
            }
        },
        encode_special_html_char: function(str) {
            if (str) {
                var codingchar = ["&", "<", ">", '"'];
                var sepchar = ["&amp;", "&lt;", "&gt;", "&quot;"];
                var len = sepchar.length;
                for (var i = 0; i < len; i++) {
                    str = str.replace(new RegExp(codingchar[i], "g"), sepchar[i])
                }
                return str
            } else {
                return ""
            }
        },
        decode_special_html_char: function(str) {
            if (str) {
                var codingchar = ["&amp;", "&lt;", "&gt;", "&quot;", "&#quot", "&#rmrow", "&#lmrow", "&apos;"];
                var sepchar = ["&", "<", ">", '"', "'", "(", ")", "'"];
                var len = sepchar.length;
                for (var i = 0; i < len; i++) {
                    str = str.replace(new RegExp(codingchar[i], "g"), sepchar[i])
                }
                return str
            } else {
                return ""
            }
        },
        format_number: function(s, n) {
            n = n > 0 && n <= 20 ? n: 2;
            s = parseFloat((s + "").replace(/[^\d\.-]/g, "")).toFixed(n) + "";
            var l = s.split(".")[0].split("").reverse(),
            r = s.split(".")[1];
            t = "";
            for (i = 0; i < l.length; i++) {
                t += l[i] + ((i + 1) % 3 == 0 && i + 1 != l.length ? ",": "")
            }
            return t.split("").reverse().join("")
        },
        del_que_str: function(url, ref) {
            var str = "";
            if (url.indexOf("?") != -1) {
                str = url.substr(url.indexOf("?") + 1)
            } else {
                return url
            }
            var arr = "";
            var returnurl = "";
            var setparam = "";
            if (str.indexOf("&") != -1) {
                arr = str.split("&");
                for (i in arr) {
                    if (arr[i].split("=")[0] != ref) {
                        returnurl = returnurl + arr[i].split("=")[0] + "=" + arr[i].split("=")[1] + "&"
                    }
                }
                return url.substr(0, url.indexOf("?")) + "?" + returnurl.substr(0, returnurl.length - 1)
            } else {
                arr = str.split("=");
                if (arr[0] == ref) {
                    return url.substr(0, url.indexOf("?"))
                } else {
                    return url
                }
            }
        },
        get_hash_str: function(url) {
            var vars = {},
            hash, str;
            if (url.indexOf("#") != -1) {
                str = url.substr(url.indexOf("#") + 1);
                var hashes = str.split("&")
            } else {
                var hashes = []
            }
            for (var i = 0; i < hashes.length; i++) {
                hash = hashes[i].split("=");
                vars[hash[0]] = hash[1]
            }
            return vars
        },
        get_hash: function(name, url) {
            var url = url || document.location.href;
            return util.getHashStr(url)[name]
        },
        parse_lyric: function(lrc) {
            var lyrics = lrc.split("\n");
            var artistReg = /(.*)\[(by|ti|ar|al)\:(.+)\]+/m;
            var timearry = [];
            for (var i = 0; i < lyrics.length; i++) {
                var lyric = decodeURIComponent(lyrics[i]);
                var timeReg = /\[\d*:\d*((\.|\:)\d*)*\]/g;
                var timeRegExpArr = lyric.match(timeReg);
                if (!timeRegExpArr) {
                    continue
                }
                var clause = lyric.replace(timeReg, "");
                for (var k = 0,
                h = timeRegExpArr.length; k < h; k++) {
                    var t = timeRegExpArr[k];
                    var min = Number(String(t.match(/\[\d*/i)).slice(1)),
                    sec = Number(String(t.match(/\:\d*/i)).slice(1)),
                    milisec = Number(String(t.match(/\.\d*/i)).slice(1));
                    var time = min * 6e4 + sec * 1e3 + milisec;
                    timearry.push({
                        time: time,
                        clause: clause
                    })
                }
            }
            timearry.sort(function compare(a, b) {
                return a.time - b.time
            });
            return {
                time_ary: timearry,
                user: lrc.match(artistReg) ? lrc.match(artistReg)[3] : "no",
                length: lyrics.length
            }
        }
    }
})();