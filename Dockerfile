# 使用 Python 3.13 穩定版
FROM python:3.13-slim

# 設定工作目錄
WORKDIR /app

# 設定環境變數
# 防止 Python 產生 pyc 檔案
ENV PYTHONDONTWRITEBYTECODE 1
# 強制標準輸出直接顯示在 Log 中，不緩存
ENV PYTHONUNBUFFERED 1

# 安裝系統依賴 (如果需要的話)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案程式碼
COPY . .

# 啟動 FastAPI 服務
# 預設使用 8000 端口
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
