import pymysql
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import random

con = pymysql.connect(host='localhost',
                      port=3306,
                      user='root',
                      password='112358',
                      database='root',
                      charset='utf8')

app = Flask(__name__)
CORS(app)

now_user = ""
now_id = 0
now_role = ""

st = []


@app.route('/stati', methods=['GET'])
def get_stai():
    try:
        sql = '''
            select count(*) from users
        '''
        cur = con.cursor()
        cur.execute(sql)
        user_num = cur.fetchone()[0]

        sql = f'''
            select count(*) from models
            where user_id = {now_id}
        '''
        cur.execute(sql)
        model_num = cur.fetchone()[0]

        sql = f'''select count(*), max(test_acc), avg(test_acc), sum(train_time)  from experiments
            where user_id = {now_id}
            '''
        cur.execute(sql)
        exp_num, max_acc, avg_acc, train_time = cur.fetchone()
        if max_acc == None:
            max_acc = 0
        if avg_acc == None:
            avg_acc = 0
        if train_time == None:
            train_time = 0
        print(exp_num, max_acc, avg_acc, train_time)
        return jsonify({
            'user_num': user_num,
            'model_num': model_num,
            'exp_num': exp_num,
            'max_acc': max_acc,
            'avg_acc': avg_acc,
            'train_time': train_time
        })
    except:
        return jsonify({'error': '数据库错误'}), 500


@app.route('/poem', methods=['GET'])
def poem():
    global st
    l = []
    with open('./assets/poem.txt', 'r', encoding='utf-8') as f:
        l = [i for i in f if i not in st]
        f.close()
    p = random.choice(l)
    st.append(p)
    if (len(st) * 2 >= 30):
        st.pop(0)
    p = p.split(' ')
    try:
        return jsonify({'first': p[0], 'second': p[1]})
    except:
        return jsonify({'first': 'error', 'second': p})


@app.route('/name', methods=['GET', 'POST'])
def oper():
    global now_user, now_role, now_id
    data = request.get_json()
    op = data.get('op')
    if op == 'cancel':
        now_id, now_role = 0, ""
        return jsonify({'status': 'success'})
    elif op == 'get':
        return jsonify({'name': now_user, "role": now_role, "id": now_id})


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

    global now_user, now_role, now_id
    now_id, now_role, now_user = result[0], result[2], username
    return jsonify({
        'message': 0,
        'id': now_user,
        'username': username,
        'role': now_role
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
