from linebot.v3.webhooks import JoinEvent
from src.services.line_service import line_service

async def handle_join_event(event: JoinEvent):
    welcome_message = (
        "大家好！我是 Gemini 翻譯機器人 🤖\n\n"
        "請使用驚嘆號 (!) 來設定你想看的語言：\n\n"
        "例如：\n"
        "❗ 「! 我想看繁體中文」\n"
        "❗ 「! Set my language to Thai」\n\n"
        "設定好後，別人的訊息我就會自動翻譯給你聽囉！"
    )
    await line_service.reply_text(event.reply_token, welcome_message)

