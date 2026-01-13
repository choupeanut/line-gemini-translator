from google import genai
from google.genai import types
from src.config import settings

class GeminiService:
    def __init__(self):
        # 初始化新的 Client
        self.client = genai.Client(api_key=settings.gemini_api_key)
        # 設定模型名稱，使用 Gemini 3 Flash Preview
        self.model_name = 'gemini-3-flash-preview'
        
    async def parse_command_language(self, text: str) -> str | None:
        """
        解析指令中的目標語言。
        已知 text 是一個設定指令（已移除 ! 前綴）。
        """
        prompt = (
            "The user is issuing a command to set their preferred reading language. "
            "Extract the target language from the text. "
            "Output ONLY the language name in English (e.g., 'Thai', 'Traditional Chinese', 'English'). "
            "If the text does not contain a valid language setting request, output 'NONE'.\n\n"
            f"Command Text: {text}"
        )
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            result = response.text.strip()
            return None if "NONE" in result.upper() else result
        except Exception as e:
            print(f"Gemini Intent Error: {e}")
            return None

    async def translate_for_recipients(self, text: str, target_langs: list[str]) -> str:
        """
        將文字翻譯給多個目標語言。
        """
        if not target_langs:
            return ""
        
        langs_str = ", ".join(set(target_langs))
        prompt = (
            f"You are a translator in a group chat. The sender just said: '{text}'\n"
            f"There are other members who read different languages: {langs_str}.\n"
            "Please translate the sender's message into these languages. "
            "Output format:\n"
            "LanguageName: [Translation]\n\n"
            "If there is only one target language, just output the translation directly. "
            "Output ONLY the translations."
        )
        
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"翻譯出錯: {e}"

    async def translate_text(self, text: str) -> str:
        # 基本翻譯邏輯
        prompt = f"Translate to Traditional Chinese if not, else to English: {text}"
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"翻譯出錯: {e}"

# Singleton instance
gemini_service = GeminiService()