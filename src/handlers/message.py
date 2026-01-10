from linebot.v3.webhooks import MessageEvent, TextMessageContent
from src.services.gemini import gemini_service
from src.services.line_service import line_service
from src.services.db_service import db_service

async def handle_message_event(event: MessageEvent):
    if not isinstance(event.message, TextMessageContent):
        return

    user_text = event.message.text
    group_id = getattr(event.source, 'group_id', getattr(event.source, 'room_id', None))
    user_id = event.source.user_id

    if not group_id:
        # 非群組訊息，執行基本翻譯
        translated = await gemini_service.translate_text(user_text)
        await line_service.reply_text(event.reply_token, translated)
        return

    # 1. 偵測是否為「設定語言」意圖
    detected_lang = await gemini_service.detect_setting_intent(user_text)
    if detected_lang:
        await db_service.set_user_pref(group_id, user_id, detected_lang)
        await line_service.reply_text(
            event.reply_token, 
            f"👌 沒問題！我記住了，之後我會將別人的訊息翻譯成 {detected_lang} 給你閱讀。"
        )
        return

    # 2. 執行翻譯邏輯
    # 獲取群組內所有人的設定
    prefs = await db_service.get_group_prefs(group_id)
    
    # 找出除了發送者以外，其他人想看的語言
    target_langs = [lang for uid, lang in prefs.items() if uid != user_id]
    
    if not target_langs:
        # 如果還沒有人設定語言，不執行動作或執行預設翻譯（這裡選擇不動作以避免干擾）
        return

    # 3. 呼叫 Gemini 進行多語言翻譯
    translated_payload = await gemini_service.translate_for_recipients(user_text, target_langs)
    
    if translated_payload:
        await line_service.reply_text(event.reply_token, translated_payload)
