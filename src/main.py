from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from contextlib import asynccontextmanager
from linebot.v3.webhook import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, JoinEvent
import uvicorn

from src.config import settings
from src.handlers.message import handle_message_event
from src.handlers.join import handle_join_event
from src.services.db_service import db_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時初始化資料庫
    await db_service.init_db()
    yield

app = FastAPI(title="Line Gemini Translator", lifespan=lifespan)

parser = WebhookParser(settings.line_channel_secret)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")
    
    body = await request.body()
    body_str = body.decode("utf-8")
    
    try:
        events = parser.parse(body_str, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    for event in events:
        if isinstance(event, JoinEvent):
            await handle_join_event(event)
        elif isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessageContent):
                await handle_message_event(event)
                
    return "OK"

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
