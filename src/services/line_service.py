from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
# 注意：最新 SDK v3 的 Async 功能通常是透過 ApiClient 的 context manager 自動處理
# 或者是使用 AsyncApiClient (如果版本支援)
try:
    from linebot.v3.messaging import AsyncApiClient, AsyncMessagingApi
    HAS_ASYNC = True
except ImportError:
    HAS_ASYNC = False

from src.config import settings

class LineService:
    def __init__(self):
        self.configuration = Configuration(
            access_token=settings.line_channel_access_token
        )
        
    async def reply_text(self, reply_token: str, text: str):
        if HAS_ASYNC:
            async with AsyncApiClient(self.configuration) as api_client:
                line_bot_api = AsyncMessagingApi(api_client)
                await line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text=text)]
                    )
                )
        else:
            # Fallback to sync if async classes are not found
            with ApiClient(self.configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text=text)]
                    )
                )

# Singleton instance
line_service = LineService()