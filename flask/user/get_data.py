import pymysql
import re
from flask import Flask, request, Blueprint, jsonify
from flask_cors import CORS
from sql_connect import connect

stati_bp = Blueprint('stati', __name__)
name_bp = Blueprint('name', __name__)
video_bp = Blueprint('video', __name__)


@stati_bp.route('/stati', methods=['GET'])
def get_stati():
    try:
        con = connect()
        cur = con.cursor()
        sql = '''
            select id from now
        '''
        cur.execute(sql)
        now_id = cur.fetchone()[0]
        sql = '''
            select count(*) from users
        '''
        cur.execute(sql)
        user_num = cur.fetchone()[0]

        # print(now_id)
        sql = f'''
            select count(*) from models
            where user_id = {now_id}
        '''
        cur.execute(sql)
        model_num = cur.fetchone()[0]
        # print(model_num)
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
        # print(exp_num, max_acc, avg_acc, train_time)
        cur.close()
        return jsonify({
            'user_num': user_num,
            'model_num': model_num,
            'exp_num': exp_num,
            'max_acc': max_acc,
            'avg_acc': avg_acc,
            'train_time': train_time
        })
    except:
        return jsonify({'error': 'stati数据库错误'}), 500


@name_bp.route('/name', methods=['GET', 'POST'])
def oper():
    con = connect()
    cur = con.cursor()
    sql = '''
        select id, name, role from now
    '''
    try:
        cur.execute(sql)
    except:
        return jsonify({'message': 'op数据库错误'})
    now_id, now_user, now_role = cur.fetchone()
    cur.close()

    data = request.get_json()
    op = data.get('op')
    if op == 'cancel':
        cur = con.cursor()
        sql = '''
        update now
        set id = 0,
            role = "user"
        '''
        cur.execute(sql)
        con.commit()
        cur.close()
        return jsonify({'status': 'success'})
    elif op == 'get':
        return jsonify({'name': now_user, "role": now_role, "id": now_id})


@video_bp.route('/video', methods=['GET', 'POST'])
def video():
    data = request.get_json()
    con = connect()
    cur = con.cursor()
    sql = '''
        select id from now
    '''
    try:
        cur.execute(sql)
    except:
        return jsonify({'message': 'video数据库错误'})

    now_id = cur.fetchone()[0]
    if (now_id == 0):
        return jsonify({'error': '未登录'}), 200

    cur.close()
    print(now_id)
    try:
        if data.get('op') == 'update':
            url = data.get('bv')
            print(url)
            pattern = re.compile(
                r'^(?:https?://(?:www\.)?bilibili\.com/video/)?'
                r'(BV[0-9A-Za-z]{10})'
                r'(?:/)?'
                r'(?:\?.*)?$')
            m = pattern.search(url)
            # print(m)
            if m:
                bv = m.group(1)
                cur = con.cursor()
                sql = f'''
                    update users
                    set bv = "{bv}"
                    where id = {now_id}
                '''
                try:
                    cur.execute(sql)
                    con.commit()
                    cur.close()
                except:
                    return jsonify({'error': '数据库错误'}), 500
                return jsonify({'bv': bv})
            else:
                return jsonify({'error': "请按要求正确输入"}), 500
        elif data.get('op') == 'get':
            cur = con.cursor()
            sql = f'''
                select bv from users
                where id = {now_id}
            '''
            try:
                cur.execute(sql)
                bv = cur.fetchone()[0]
                cur.close()
                if not bv:
                    bv = 'BV11H4y1F7uH'
                return jsonify({'bv': bv})
            except:
                return jsonify({'error': '11数据库错误'}), 500

    except:
        return jsonify({'error': '未知错误'}), 500
