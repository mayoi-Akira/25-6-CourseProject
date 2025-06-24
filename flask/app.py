import pymysql
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import random

from user.login import login_bp, register_bp
from user.get_data import stati_bp, name_bp, video_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(stati_bp)
app.register_blueprint(name_bp)
app.register_blueprint(video_bp)

st = []


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
