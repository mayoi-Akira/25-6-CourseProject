import pymysql
import re
from flask import Flask, request, Blueprint, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import zipfile
from sql_connect import connect

dataset_bp = Blueprint('dataset', __name__)

path = './flask/dataset_zip'
unzip_path = './flask/dataset'
allowed = {'zip'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed


@dataset_bp.route('/datasets', methods=['POST'])
def datasets():
    print(request.files)
    if 'file' not in request.files:
        return jsonify({'error': '未找到文件'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    if not (file and allowed_file(file.filename)):
        return jsonify({'error': '仅支持 ZIP 文件'}), 400
    filename = secure_filename(file.filename)
    name = request.form.get('name')

    if name == None:
        name = filename

    save_path = path + '/' + filename
    os.makedirs(path, exist_ok=True)
    print(save_path)
    no_ex_filename = filename[:-4]
    try:
        file.save(save_path)
        unzip_save_path = unzip_path + '/' + no_ex_filename
        try:
            with zipfile.ZipFile(save_path, 'r') as zip_ref:
                zip_ref.extractall(path=unzip_save_path)
        except:
            return jsonify({'error': '解压失败'}), 500
        print(filename)
        con = connect()
        cur = con.cursor()
        sql = '''
            select id from now
        '''
        cur.execute(sql)
        now_id = cur.fetchone()[0]
        sql = f'''
            insert into datasets (user_id, name, path, size)
            values({now_id}, "{name}", "{unzip_save_path}", 0)
            '''
        cur.execute(sql)
        con.commit()
        cur.close()
        return jsonify({'message': '文件上传成功'})

    except Exception as e:
        return jsonify({'error': f'文件保存失败: {str(e)}'}), 500


@dataset_bp.route('/datasets', methods=['GET'])
def list_datasets():
    user_id = request.args.get('user_id', type=int)
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    search = request.args.get('search', '', type=str)
    offset = (page - 1) * size

    con = connect()
    cur = con.cursor()
    like_pattern = f"%{search}%"
    sql = f"""
        select id, user_id, name, path, size
        from datasets
        where name like "{like_pattern}"
        order by id desc
        limit {size} offset {offset}
    """
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        # 新增：查询总数
        cur.execute(f'select count(*) from datasets where name like "{like_pattern}"')
        total = cur.fetchone()[0]
    except Exception as e:
        cur.close()
        con.close()
        return jsonify({'error': '数据库错误', 'details': str(e)}), 500

    datasets = []
    for row in rows:
        datasets.append({
            'id': row[0],
            'user_id': row[1],
            'name': row[2],
            'path': row[3],
            'size': row[4]
        })
    cur.close()
    con.close()
    return jsonify({'list': datasets, 'total': total}), 200
