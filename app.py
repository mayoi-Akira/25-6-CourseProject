import pymysql
import re
from flask import Flask, request, jsonify
'''
错误码：
 
0：成功
1：两次密码不匹配
2：密码不合法
3：用户名不合法
4：用户已存在
5：未获取到JSON
6：用户不存在
7：密码不匹配
10：数据库错误
'''

con = pymysql.connect(host='localhost',
                      port=3306,
                      user='root',
                      password='112358',
                      database='root',
                      charset='utf8')

app = Flask(__name__)

now_user = 0


@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()
    if not data:
        return jsonify({'code': 5})

    username, password, confirm_password, role = \
    data.get('username'), data.get('password'), data.get('confirm_password'), data.get('role')

    if (password != confirm_password):
        return jsonify({'code': 1})

    password_pattern = re.compile(r'^[\x20-\x7E]{6,20}$')
    username_pattern = re.compile(r'^[A-Za-z0-9_]{6,20}$')

    if not bool(password_pattern.fullmatch(password)):
        return jsonify({'code': 2})
    if not bool(username_pattern.fullmatch(username)):
        return jsonify({'code': 3})

    cur = con.cursor()

    #检查用户名是否存在
    sql = f'''
        select 1 from users
        where username="{username}"
    '''
    try:
        cur.execute(sql)
    except:
        return jsonify({'code': 10})

    if cur.fetchone():
        return jsonify({'code': 4})

    #加入新用户
    sql = f'''
        insert into users(username, password, role)
        values("{username}", "{password}", "{role}")
    '''

    try:
        cur.execute(sql)
    except:
        return jsonify({'code': 10})
    con.commit()
    cur.close()
    return jsonify({'code': 0})


@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'code': 5})

    username = data.get('username')
    password = data.get('password')

    #查找该用户的密码
    cur = con.cursor()
    sql = f'''
        select id, password from users
        where username="{username}"
    '''
    try:
        cur.execute(sql)
    except:
        return jsonify({'code': 10})

    result = cur.fetchone()

    #未找到
    if not result:
        return jsonify({'code': 6})

    if result[1] != password:
        return jsonify({'code': 7})

    global now_user
    now_user = result[0]
    return jsonify({'code': 0, 'id': now_user})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
