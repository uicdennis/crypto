要將您的Flask Web應用程序打包成Docker映像並使用Docker Compose來管理它，您需要創建一個`Dockerfile`和一個`docker-compose.yml`文件。以下是這些文件的內容示例。

### 1. Dockerfile

首先，您需要創建一個名為`Dockerfile`的文件，這個文件將定義如何構建您的Flask應用程序的Docker映像。

```dockerfile
# 使用官方的 Python 基礎映像
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 複製需求文件並安裝依賴
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程序代碼，包括 tlv.py
COPY . .

# 暴露應用程序運行的端口
EXPOSE 5000

# 設置環境變量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 啟動Flask應用
CMD ["flask", "run"]
```

### 2. 確保文件結構

確保您的項目結構如下：

```
/your-project-directory
│
├── app.py          # Flask 應用程序
├── tlv.py          # 自行開發的模組
├── requirements.txt # 依賴項文件
└── Dockerfile      # Dockerfile 文件
```

### 3. requirements.txt

確保您有一個名為`requirements.txt`的文件，列出Flask及其依賴項。例如：

```
Flask==2.0.1
```

### 4. docker-compose.yml

接下來，創建一個名為`docker-compose.yml`的文件，這個文件將定義如何運行您的Docker容器。

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
```

### 5. 構建和運行容器

在終端中，導航到包含`Dockerfile`和`docker-compose.yml`的目錄，然後運行以下命令來構建和啟動您的應用程序：

```bash
# 構建Docker映像
docker-compose build

# 啟動應用程序
docker-compose up
```

### 說明

- **Dockerfile**:
  
  - `FROM python:3.9-slim`：使用輕量級的Python基礎映像。
  - `WORKDIR /app`：設置工作目錄為`/app`。
  - `COPY requirements.txt requirements.txt`：將需求文件複製到容器中。
  - `RUN pip install --no-cache-dir -r requirements.txt`：安裝依賴。
  - `COPY . .`：將應用程序的所有代碼複製到容器中。
  - `EXPOSE 5000`：暴露5000端口，Flask默認使用此端口。
  - `CMD ["flask", "run"]`：啟動Flask應用。

- **docker-compose.yml**:
  
  - `version: '3.8'`：指定Docker Compose的版本。
  - `services`：定義服務，這裡只有一個名為`web`的服務。
  - `build: .`：從當前目錄構建映像。
  - `ports`：將容器的5000端口映射到主機的5000端口。
  - `volumes`：將當前目錄掛載到容器的`/app`目錄，便於開發時即時更新。
  - `environment`：設置環境變量，這裡設置Flask為開發模式。

這樣，您就可以將Flask應用程序打包到Docker容器中，並使用Docker Compose進行管理。



### 總結

只要確保在 Dockerfile 中使用 `COPY . .` 將整個應用程序目錄中的所有文件（包括 `tlv.py`）複製到 Docker 容器的工作目錄中，您的 Flask 應用就能夠正常找到並使用 `tlv.py` 模組。這樣，您就不需要在 `requirements.txt` 中引入它。