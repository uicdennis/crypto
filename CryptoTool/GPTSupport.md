#### Question:

我想使用Flask提供如底下介面，template應該如何設計?

![](C:\Users\decar\AppData\Roaming\marktext\images\2025-12-04-17-34-05-image.png)

#### Answer:

根據提供的 Crypto Test 程式介面,我們可以設計一個簡單的 Flask 網頁模板。以下是一個基本的範例:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Crypto Test</title>
</head>
<body>
    <h1>Crypto Test - Ver. 0.1</h1>
    <form action="{{ url_for('crypto_test') }}" method="post">
        <h2>Function</h2>
        <input type="radio" name="function" value="XOR" {% if function == 'XOR' %}checked{% endif %}> XOR
        <input type="radio" name="function" value="DES" {% if function == 'DES' %}checked{% endif %}> DES
        <input type="radio" name="function" value="Triple-DES" {% if function == 'Triple-DES' %}checked{% endif %}> Triple-DES
        <input type="radio" name="function" value="DES-MAC" {% if function == 'DES-MAC' %}checked{% endif %}> DES-MAC
        <input type="radio" name="function" value="TDES-MAC" {% if function == 'TDES-MAC' %}checked{% endif %}> TDES-MAC
        <input type="radio" name="function" value="AES" {% if function == 'AES' %}checked{% endif %}> AES

        <h2>DES Encrypt/Decrypt</h2>
        <input type="radio" name="des_mode" value="Encryption" {% if des_mode == 'Encryption' %}checked{% endif %}> Encryption
        <input type="radio" name="des_mode" value="Descryption" {% if des_mode == 'Descryption' %}checked{% endif %}> Descryption

        <h2>Mode</h2>
        <input type="radio" name="mode" value="ECB Mode" {% if mode == 'ECB Mode' %}checked{% endif %}> ECB Mode
        <input type="radio" name="mode" value="CBC Mode" {% if mode == 'CBC Mode' %}checked{% endif %}> CBC Mode

        <h2>Key</h2>
        <input type="text" name="key" value="{{ key }}">

        <h2>Data</h2>
        <input type="text" name="data" value="{{ data }}">

        <button type="submit">DES Calculate</button>
    </form>

    <h2>Result</h2>
    <p>{{ result }}</p>
</body>
</html>
```

這個模板包含了以下元素:

1. 表單,包含了各種加密演算法、加解密模式、金鑰和資料輸入欄位。
2. 根據使用者的選擇,預設勾選對應的選項。
3. 提交表單後,將結果顯示在頁面上。

在 Flask 後端,您需要處理表單提交並計算加密結果,然後將結果傳遞給模板進行渲染。以下是一個簡單的 Flask 路由範例:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

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

        return render_template('crypto_test.html', function=function, des_mode=des_mode, mode=mode, key=key, data=data, result=result)

    return render_template('crypto_test.html')
```

這個路由處理 GET 和 POST 請求。在 POST 請求中,它會接收表單資料,進行加密計算,並將結果傳遞給模板進行渲染。

您可以根據實際需求,進一步完善加密演算法的實現,並調整模板以滿足更複雜的使用者介面需求。



#### Question:

若Function選擇為'AES'，Encrypt的標頭則改為AES，而非DES。也就是說要依Function的選擇，動態修改，這樣是否需要javascript在前端達成?或是有其他方法?

若希望在選擇的當下，立即修改，而非提出表單才修改。

#### Answer:

如果您希望在使用者選擇加密演算法時,立即修改表單內容,而不是等到提交表單,那麼您可以使用 JavaScript 來實現這個功能。

以下是修改後的 HTML 模板,使用 JavaScript 來動態更新表單:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Crypto Test</title>
    <script>
        function updateForm() {
            var functionSelect = document.getElementById("function");
            var encryptTitle = document.getElementById("encrypt-title");
            var encryptModeRadios = document.getElementsByName("mode");
            var calculateButton = document.getElementById("calculate-button");

            var selectedFunction = functionSelect.value;
            if (selectedFunction === "AES") {
                encryptTitle.textContent = "AES Encrypt/Decrypt";
                encryptModeRadios[0].value = "Encryption";
                encryptModeRadios[1].value = "Descryption";
                calculateButton.textContent = "AES Calculate";
            } else {
                encryptTitle.textContent = "DES Encrypt/Decrypt";
                encryptModeRadios[0].value = "Encryption";
                encryptModeRadios[1].value = "Descryption";
                calculateButton.textContent = "DES Calculate";
            }
        }
    </script>
</head>
<body>
    <h1>Crypto Test - Ver. 0.1</h1>
    <form action="{{ url_for('crypto_test') }}" method="post">
        <h2>Function</h2>
        <input type="radio" name="function" id="function" value="XOR" {% if function == 'XOR' %}checked{% endif %} onchange="updateForm()"> XOR
        <input type="radio" name="function" id="function" value="DES" {% if function == 'DES' %}checked{% endif %} onchange="updateForm()"> DES
        <input type="radio" name="function" id="function" value="Triple-DES" {% if function == 'Triple-DES' %}checked{% endif %} onchange="updateForm()"> Triple-DES
        <input type="radio" name="function" id="function" value="DES-MAC" {% if function == 'DES-MAC' %}checked{% endif %} onchange="updateForm()"> DES-MAC
        <input type="radio" name="function" id="function" value="TDES-MAC" {% if function == 'TDES-MAC' %}checked{% endif %} onchange="updateForm()"> TDES-MAC
        <input type="radio" name="function" id="function" value="AES" {% if function == 'AES' %}checked{% endif %} onchange="updateForm()"> AES

        <h2><span id="encrypt-title">DES Encrypt/Decrypt</span></h2>
        <input type="radio" name="mode" value="Encryption" {% if mode == 'Encryption' %}checked{% endif %}> Encryption
        <input type="radio" name="mode" value="Descryption" {% if mode == 'Descryption' %}checked{% endif %}> Descryption

        <h2>Key</h2>
        <input type="text" name="key" value="{{ key }}">

        <h2>Data</h2>
        <input type="text" name="data" value="{{ data }}">

        <button type="submit" id="calculate-button">DES Calculate</button>
    </form>

    <h2>Result</h2>
    <p>{{ result }}</p>
</body>
</html>
```

在這個範例中,我們添加了一個 JavaScript 函數 `updateForm()`。當使用者選擇不同的加密演算法時,會觸發 `onchange` 事件,從而調用這個函數。

這個函數會根據選擇的演算法,動態更新表單中的標題、加密/解密模式選項以及按鈕文字。

這樣,當使用者選擇不同的加密演算法時,表單內容就會立即更新,而不需要等到提交表單。這提供了更好的用戶體驗。
