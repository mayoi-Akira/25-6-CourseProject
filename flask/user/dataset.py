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
    if 'zip_file' not in request.files:
        return jsonify({'error': '未找到文件'}), 400

    file = request.files['zip_file']

    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    if not (file and allowed_file(file.filename)):
        return jsonify({'error': '仅支持 ZIP 文件'}), 400
    filename = secure_filename(file.filename)
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
            values({now_id}, "{filename}", "{unzip_save_path}", 0)
            '''
        cur.execute(sql)
        con.commit()
        cur.close()
        return jsonify({'message': '文件上传成功'})

    except Exception as e:
        return jsonify({'error': f'文件保存失败: {str(e)}'}), 500
