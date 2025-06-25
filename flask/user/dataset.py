import pymysql
import re
from flask import Flask, request, Blueprint, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import zipfile
from sql_connect import connect
import hashlib
import os
import time
import shutil

dataset_bp = Blueprint('dataset', __name__)

path = './flask/Roaming'
unzip_path = './flask/dataset'
allowed = {'zip'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed


def hash_filename(filename: str, algorithm: str = 'md5') -> str:
    """
    根据原文件名生成一个哈希后的文件名，并保留原扩展名。

    :param filename: 原始文件名（可以包含路径，也可以只包含文件名）
    :param algorithm: 使用的哈希算法，可选 'md5', 'sha1', 'sha256' 等
    :return: 哈希后的文件名，格式为 "<hash>_<timestamp>.<ext>"
    """
    # 分离文件名和扩展名
    base, ext = os.path.splitext(os.path.basename(filename))
    # 构造要哈希的字符串（可以加入时间戳以增强唯一性）
    to_hash = f"{base}_{time.time()}"
    # 选择哈希算法
    try:
        hasher = hashlib.new(algorithm)
    except ValueError:
        raise ValueError(f"不支持的哈希算法: {algorithm}")
    # 更新哈希
    hasher.update(to_hash.encode('utf-8'))
    hash_str = hasher.hexdigest()
    # 返回哈希文件名
    return f"{hash_str}{ext}"


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

    file.stream.seek(0, 2)
    size = file.stream.tell()
    file.stream.seek(0)

    filename = secure_filename(file.filename)
    name = request.form.get('name')
    description = request.form.get('description')
    # print(size)
    if name == None:
        name = filename

    save_path = path + '/' + filename

    os.makedirs(path, exist_ok=True)
    no_ex_filename = filename[:-4]
    try:
        file.save(save_path)
        unzip_save_path = unzip_path + '/' + hash_filename(no_ex_filename)
        try:
            with zipfile.ZipFile(save_path, 'r') as zip_ref:
                zip_ref.extractall(path=unzip_save_path)
        except:
            os.remove(save_path)
            return jsonify({'error': '解压失败'}), 500
        os.remove(save_path)
        con = connect()
        cur = con.cursor()
        sql = '''
            select id from now
        '''
        cur.execute(sql)
        now_id = cur.fetchone()[0]
        sql = f'''
            insert into datasets (user_id, name, path, size, description, create_at)
            values({now_id}, "{name}", "{unzip_save_path}", {size/1024/1024}, "{description}", NOW())
            '''
        cur.execute(sql)
        con.commit()
        cur.close()
        return jsonify({'message': '文件上传成功'})

    except Exception as e:
        return jsonify({'error': f'文件保存失败: {str(e)}'}), 500


@dataset_bp.route('/datasets', methods=['GET'])
def list_datasets():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    search = request.args.get('search', '', type=str)
    offset = (page - 1) * size

    # print(page, size, search, offset)
    con = connect()
    cur = con.cursor()
    sql = '''
        select id from now
    '''
    try:
        cur.execute(sql)
    except:
        return jsonify({'error': '数据库错误'}), 500
    user_id = cur.fetchone()[0]
    like_pattern = f"%{search}%"
    sql = f"""
        select id, user_id, name, size,description, create_at
        from datasets
        where user_id = {user_id} and  name like "{like_pattern}"
        order by id desc
        limit {size} offset {offset}
    """
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        cur.execute(
            f'select count(*), sum(size) from datasets where user_id = {user_id} and name like "{like_pattern}"'
        )
        total, total_size = cur.fetchone()
        # if total_size == None:
        #     total_size = 0
        # print(total, total_size)
        # print(total_size)
    except Exception as e:
        cur.close()
        con.close()
        return jsonify({'error': '数据库错误', 'details': str(e)}), 500
    datasets = []
    cur.close()
    con.close()
    for row in rows:
        datasets.append({
            'id': row[0],
            'user_id': row[1],
            'name': row[2],
            'size': row[3],
            'description': row[4],
            'created_at': row[5]
        })
    # print(datasets)
    return jsonify({
        'list': datasets,
        'total': total,
        'total_size': total_size
    }), 200


@dataset_bp.route('/datasets/<int:dataset_id>', methods=['DELETE'])
def remove(dataset_id):
    con = connect()
    cur = con.cursor()
    sql = f'''
        select path from datasets
        where id = {dataset_id}
    '''
    try:
        cur.execute(sql)
    except:
        cur.close()
        con.close()
        return jsonify({'error': '数据库错误'}), 500
    path = cur.fetchone()[0]
    ab_path = os.path.abspath(path)
    shutil.rmtree(ab_path)
    sql = f'''
            delete from datasets
            where id = {dataset_id}
        '''
    try:
        cur.execute(sql)
    except:
        cur.close()
        con.close()
        return jsonify({'error': '数据库错误'}), 500

    con.commit()
    cur.close()
    con.close()
    return jsonify({'status': 'success'})
