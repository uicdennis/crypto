from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def formPage():
    example = '''9c0100\
5f2a020840\
5f360102\
9f0206000000000001\
9f0306000000000000
'''
    return render_template('crypto.html', mode='ECB Mode')

@app.route('/crypto-test', methods=['GET', 'POST'])
def crypto_test():
    if request.method == 'POST':
        function = request.form['function']
        des_mode = request.form['des_mode']
        mode = request.form['mode']
        key = request.form['key']
        data = request.form['data']

        # 在此處加入您的加密演算法實現
        result = f"Encrypted/Decrypted data: {data}"

        return render_template('crypto.html', function=function, des_mode=des_mode, mode=mode, key=key, data=data, result=result)

    return render_template('crypto.html')
