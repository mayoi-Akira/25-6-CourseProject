import pymysql
import re
from flask import Flask, request, Blueprint, jsonify
from flask_cors import CORS
from sql_connect import connect
import hashlib

login_bp = Blueprint('login', __name__)
register_bp = Blueprint('register', __name__)


@login_bp.route('/login', methods=['POST'])
def login():
    con = connect()
    cur = con.cursor()
    sql = '''
        select id, name, role from now
    '''
    try:
        cur.execute(sql)
    except:
        return jsonify({'message': '数据库错误'})
    now_user, now_role, now_id = cur.fetchone()
    cur.close()
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'message': "未获取到JSON"}), 304

    username = data.get('username')
    password = data.get('password')
    hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    #查找该用户的密码
    cur = con.cursor()
    sql = '''
        select id, password, role from users
        where username=%s
    '''
    try:
        cur.execute(sql, (username, ))
    except:
        return jsonify({'message': "数据库错误"}), 500

    result = cur.fetchone()
    #未找到
    if not result:
        return jsonify({'message': "用户不存在"}), 403

    if result[1] != hash:
        return jsonify({'message': "密码错误"}), 403

    now_id, now_role, now_user = result[0], result[2], username
    sql = '''
        update now
        set id = %s,
            name = %s,
            role = %s
    '''
    try:
        cur.execute(sql, (now_id, now_user, now_role))
    except:
        return jsonify({'message': "数据库错误"}), 500
    con.commit()
    cur.close()
    print(now_id)
    return jsonify({
        'message': 0,
        'id': now_id,
        'username': username,
        'role': now_role
    }), 200


@register_bp.route('/register', methods=['POST'])
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
        return jsonify({'message': "用户名长度需在5-20之间，且仅能包含字母数字以及'_'"}), 403
    if not bool(password_pattern.fullmatch(password)):
        return jsonify({'message': "密码长度需在5-20之间，且仅能包含可见字符"}), 403
    con = connect()
    cur = con.cursor()

    #检查用户名是否存在
    sql = '''
        select 1 from users
        where username=%s
    '''
    try:
        cur.execute(sql, (username, ))
    except:
        return jsonify({'message': "数据库错误"}), 500

    if cur.fetchone():
        return jsonify({'message': "用户名已存在"}), 403
    #加入新用户
    hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    sql = '''
        insert into users(username, password, role)
        values(%s, %s, %s)
    '''

    try:
        cur.execute(sql, (username, hash, role))
    except:
        return jsonify({'message': "数据库错误"}), 500
    con.commit()
    cur.close()
    return jsonify({'message': "成功"}), 200
