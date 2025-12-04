from tlv import TLV, TLVParser
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def formPage():
    example = '''9c0100\
5f2a020840\
5f360102\
9f0206000000000001\
9f0306000000000000
'''
    return render_template('form.html', Value=example)

@app.route("/submit", methods=['POST'])
def submit():
    if request.method == 'POST':
        form_data = request.form
        # print(type(form_data['TLV']))
        print(form_data['TLV'])
        parser = TLVParser(form_data['TLV'].strip())
        parser.parse()
        result = parser.dumpList()
        # # 將結果轉換為以 <br> 分隔的字符串
        # tlv_result = '<br>'.join(result)  # 使用 <br> 分隔行
        # html = tlv_result.replace('  ', '&nbsp;&nbsp;').replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')

        # # 將結果轉換為樹狀結構的HTML列表
        # html = '<ul>'
        # for item in result:
        #     html += f'<li>{item}</li>'  # 每個項目作為列表項
        # html += '</ul>'

        # 將結果轉換為樹狀結構的HTML列表
        html = '<ul>'
        stack = []  # 用於跟蹤當前層級的堆疊
        current_level = 0  # 當前層級

        for item in result:
            # 計算當前項目的層級
            level = item.count('  ')  # 每兩個空白字符表示一個層級
            item = item.strip()  # 去掉前後空白

            # 如果層級高於當前層級，則添加子列表
            if level > current_level:
                html += '<ul>' * (level - current_level)  # 開始新的子列表
            elif level < current_level:
                html += '</ul>' * (current_level - level)  # 結束多餘的子列表

            html += f'<li>{item}</li>'  # 添加當前項目
            current_level = level  # 更新當前層級

        html += '</ul>' * current_level  # 關閉所有開啟的子列表

    return render_template('form.html', Value=form_data['TLV'].strip(), Result=html)

if __name__ == "__main__":
    app.run()
