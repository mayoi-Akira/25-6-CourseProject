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
10：数据库错误
'''

con = pymysql.connect(host='localhost',
                      port=3306,
                      user='root',
                      password='112358',
                      database='test',
                      charset='utf8')

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()
    if not data:
        return jsonify({'code': 5})

    user_name, password, confirm_password, role = \
    data.get('user_name'), data.get('password'), data.get('confirm_password'), data.get('role')

    if (password != confirm_password):
        return jsonify({'code': 1})

    password_pattern = re.compile(r'^[\x20-\x7E]{6,20}$')
    user_name_pattern = re.compile(r'^[A-Za-z0-9_]{6,20}$')

    if not bool(password_pattern.fullmatch(password)):
        return jsonify({'code': 2})
    if not bool(user_name_pattern.fullmatch(user_name)):
        return jsonify({'code': 3})

    cur = con.cursor()

    sql = f'''
        select 1 from user
        where name="{user_name}"
    '''
    cur.execute(sql)
    if cur.fetchone():
        return jsonify({'code': 4})

    sql = f'''
        insert into user(name, password, role)
        values("{user_name}", "{password}", "{role}")
    '''

    try:
        cur.execute(sql)
    except:
        return jsonify({'code': 10})
    con.commit()
    cur.close()
    return jsonify({'code': 0})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
