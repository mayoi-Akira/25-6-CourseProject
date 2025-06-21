import pymysql
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

con = pymysql.connect(host='localhost',
                      port=3306,
                      user='root',
                      password='112358',
                      database='root',
                      charset='utf8')

app = Flask(__name__)
CORS(app, resources={r"/login": {"origins": "*"}})
CORS(app, resources={r"/register": {"origins": "*"}})

now_user = 0
now_role = ""


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'message': "未获取到JSON"}), 304

    username, password, password_Confirm, role = \
    data.get('username'), data.get('password'), data.get('passwordConfirm'), data.get('role')

    if (password != password_Confirm):
        return jsonify({'message': "两次密码不一致!"}), 403

    username_pattern = re.compile(r'^[A-Za-z0-9_]{5,20}$')
    password_pattern = re.compile(r'^[!-~]{5,20}$')

    if not bool(username_pattern.fullmatch(username)):
        return jsonify({'message': "用户名长度需在5-20之间，且仅能包含字母数字以及\'_\'"}), 403
    if not bool(password_pattern.fullmatch(password)):
        return jsonify({'message': "密码长度需在5-20之间，且不能含有特殊字符"}), 403

    cur = con.cursor()

    #检查用户名是否存在
    sql = f'''
        select 1 from users
        where username="{username}"
    '''
    try:
        cur.execute(sql)
    except:
        return jsonify({'message': "数据库错误"}), 500

    if cur.fetchone():
        return jsonify({'message': "用户名已存在"}), 403
    #加入新用户
    sql = f'''
        insert into users(username, password, role)
        values("{username}", "{password}", "{role}")
    '''

    try:
        cur.execute(sql)
    except:
        return jsonify({'message': "数据库错误"}), 500
    con.commit()
    cur.close()
    return jsonify({'message': "成功"}), 200


@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'message': "未获取到JSON"}), 304

    username = data.get('username')
    password = data.get('password')

    #查找该用户的密码
    cur = con.cursor()
    sql = f'''
        select id, password, role from users
        where username="{username}"
    '''
    try:
        cur.execute(sql)
    except:
        return jsonify({'message': "数据库错误"}), 500

    result = cur.fetchone()

    #未找到
    if not result:
        return jsonify({'message': "用户不存在"}), 403

    if result[1] != password:
        return jsonify({'message': "密码错误"}), 403

    global now_user, now_role
    now_user, now_role = result[0], result[2]
    return jsonify({
        'message': 0,
        'id': now_user,
        'username': username,
        'role': now_role
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
