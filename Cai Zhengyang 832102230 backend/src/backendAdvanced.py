from flask import Flask, request, jsonify
from flask_cors import *
import re
import pymysql
import numpy as np
import math
app = Flask(__name__)


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = '*'
    return environ


@app.route('/calculate_result', methods=['POST'])
def get_result():
    data = request.form.get("formula")
    data = data.replace("^", "**")
    data = data.replace("√(", "math.sqrt(")
    data = data.replace("sin(", "np.sin(np.pi/180*")
    data = data.replace("cos(", "np.cos(np.pi/180*")
    data = data.replace("tan(", "np.tan(np.pi/180*")
    data = data.replace("π", "np.pi")
    data = data.replace("e", "np.exp(1)")
    data = data.replace("mod", "%")
    data = data.replace("log(", "np.log10(")
    data = data.replace("ln(", "np.log(")
    data = re.sub(
        "(\d+)!", lambda x: "np.math.factorial("+str(x.group(1))+")", data)
    data = eval(data)
    print(data)
    return jsonify({'result': data, 'message': 'success'})


@app.route('/set_history', methods=['POST'])
def set_history():
    data = request.form.get("data")
    try:
        conn = pymysql.connect(
            host='127.0.0.1', port=3306, user='root', password='1234', db='calculatorhistory'
        )
        print('Setting the data SUCCESSFULLY(设置数据成功)')
        cur = conn.cursor()
        sql = "INSERT INTO history(forumla) VALUES(%s)"
        value = (data)
        cur.execute(sql, value)
        conn.commit()
        return jsonify({'message': 'success'})
    except pymysql.Error as e:
        print('Setting the data FAIL(设置数据失败)'+str(e))

    conn.close()


@app.route('/read_history', methods=['POST'])
def read_history():
    try:
        conn = pymysql.connect(
            host='127.0.0.1', port=3306, user='root', password='1234', db='calculatorhistory'
        )
        print('reading the recordings from the history SUCCESSFULLY(数据读取成功)')
        cur = conn.cursor()
        sql = "SELECT * FROM history ORDER BY id DESC LIMIT 0,10"
        cur.execute(sql)
        results = cur.fetchall()

        return jsonify({'result': results, 'message': 'success'})
    except pymysql.Error as e:
        print('reading the recordings from the history FAIL(数据读取失败)'+str(e))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)
