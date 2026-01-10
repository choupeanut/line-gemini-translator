from linebot.v3.webhooks import JoinEvent
from src.services.line_service import line_service

async def handle_join_event(event: JoinEvent):
    welcome_message = (
        "大家好！我是 Gemini 翻譯機器人 🤖\n\n"
        "我現在變更聰明了！我可以針對每個人設定想看的語言。\n\n"
        "📢 請直接跟我說你想看什麼語言，例如：\n"
        "「我想看繁體中文」\n"
        "「Set my language to Thai」\n\n"
        "設定好後，當別人在群組說話時，我就會自動翻譯成你的語言給你閱讀喔！"
    )
    await line_service.reply_text(event.reply_token, welcome_message)

