# Project: Line Gemini Translator

## Project Overview
這是一個基於 Python FastAPI 與 Line Bot SDK v3 開發的智慧翻譯機器人。其核心功能是加入 LINE 群組後，利用 Google Gemini 3 Flash 模型提供極速、精準的雙向翻譯服務。

## Tech Stack
- **Language:** Python 3.14+
- **Framework:** FastAPI (Asynchronous)
- **Line SDK:** Line Bot SDK v3 (WebhookHandler, MessagingApi)
- **AI Model:** Google Gemini 3 Flash (via `google-generativeai`)
- **Deployment:** Docker & Docker Compose

## Architecture & Conventions
採用 **Clean Architecture** 精神：
- **Interface Layer:** FastAPI 處理 Webhook 進入點。
- **Service Layer:** 獨立的 `GeminiService` 與 `LineService` 處理外部 API 通訊。
- **Handler Layer:** 封裝 Line 事件邏輯（Message, Join）。
- **Containerization:** 所有的執行環境皆封裝於 Docker 中，不依賴本地 Python 環境。

## Key Features
1.  **群組自動歡迎:** 
    - 當機器人被加入群組時，自動發送功能說明。
    - 主動詢問使用者要翻譯哪幾種語言，作為該群組的基礎設定。(此設定應為Gemini直接理解翻譯)
2.  **智慧雙向翻譯:** 
    - **指令式設定:** 使用 `!` 或 `！` 開頭作為設定指令。
        - 例如: `! 我想看中文` 或 `! Set to English`。
        - 機器人僅對以此符號開頭的訊息進行意圖分析，節省資源並防止誤判。
    - 簡易資料庫紀錄群組ID，並紀錄該群組的翻譯設定。
    - 使用 **Gemini 3 Flash** (model="gemini-3-flash-preview") 確保低延遲回應。
    - 翻譯時自動將群組內使用者的語言轉換為對應語言，可能是多語言翻譯。
    - 根據使用者進行設定其要閱讀的語言，而不是設定兩種語言的互相轉換。
3.  **非同步處理:** 確保在高併發群組訊息中保持回應穩定。

## Directory Structure (Planned)
```text
line-gemini-translator/
├── src/
│   ├── main.py             # FastAPI 入口
│   ├── config.py           # 環境變數與設定
│   ├── handlers/           # 事件處理 (Message, Join)
│   └── services/           # 外部服務 (Gemini, Line API)
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── GEMINI.md               # 本文件
```

## Setup & Development
1. 複製 `.env.example` 並填入 `LINE_CHANNEL_SECRET`, `LINE_CHANNEL_ACCESS_TOKEN` 與 `GEMINI_API_KEY`。
2. 使用 `docker-compose up --build` 啟動服務。
3. 使用 ngrok 將本地 8000 端口映射至公網以接收 Line Webhook。
