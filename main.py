# -*- coding: UTF-8 -*-
import re
import urllib
import pymysql
import time
import sys,time
from bs4 import BeautifulSoup

for i in range(100):
    sys.stdout.write('>')
    sys.stdout.flush()
    time.sleep(0.1)

url_temp = 'http://sportsapp.aipao.me/Manage/UserDomain_SNSP_Records.aspx/MyResutls?userId='


def password():
    return "a123456789"


def time_mark():
    return 'day' + time.strftime('%Y%m%d', time.localtime(time.time()))


db = pymysql.connect(
    host="localhost",
    user="root",
    password=password(),
    db="Run_Data",
    charset='utf8',
    port=3306
)

cur = db.cursor()
table_name = str(time_mark())
create_table = '''CREATE TABLE IF NOT EXISTS {}(person VARCHAR(20),sex VARCHAR(20),class VARCHAR(20),times VARCHAR(20),whether_finish VARCHAR(20),whether_ok VARCHAR(20));'''

try:
    cur.execute(create_table.format(table_name))  # 创建表
    db.commit()  # 要记得写这句话，提交请求。
except Exception as e:
    db.rollback()  # 表存在就回滚操作

sql_insert = '''INSERT INTO {} (person,sex,class,times,whether_finish,whether_ok) VALUES('{}','{}','{}','{}','{}','{}');'''  # 插值模板


# 解析并生成列表
def scf(i):  # i为id
    # 获取html
    url = url_temp + str(i)
    page = urllib.request.urlopen(url)
    html_code = page.read().decode('UTF-8')
    html = BeautifulSoup(html_code, 'html.parser')

    # 解析器（查找标签）
    data_1 = str(html.find_all('a', 'item box-col')[3])
    data_2 = str(html.find_all('span')[2])
    data_3 = str(html.find_all('span')[4])
    data_4 = str(html.find_all('span')[3])

    # 解析器（正则取值）
    school = re.findall(r'''<a class="item box-col">(.*)</a>''', data_1)
    name = re.findall(r'''<span class="name">(.*)</span>''', data_2)
    run_times = re.findall(r'''<span>(.*)</span>''', data_3)
    sex = re.findall(r'''<span class="Gender">(.*)</span>''', data_4)

    # 判断是否满分
    if int(run_times[0]) >= 30:
        mark = 'Full marks'
    else:
        mark = 'No Full marks'

    if int(run_times[0]) >= 20:
        fin = 'Finish'
    else:
        fin = 'Not Finish'

    # 生成并返回list

    list_main = [name[0], sex[0], school[0], run_times[0], fin, mark]
    return list_main


# 遍历并commit mysql

def main_loop():
    a = 0
    for i in range(558591, 566302):
        li = scf(i)  # 传入id
        cur.execute(sql_insert.format(table_name, li[0], li[1], li[2], li[3], li[4], li[5]))
        db.commit()
        a += 1
        print('第{}/7711个完成了'.format(a))


if __name__ == '__main__':
    main_loop()
