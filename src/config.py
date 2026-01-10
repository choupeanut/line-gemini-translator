from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # LINE settings
    line_channel_secret: str
    line_channel_access_token: str
    
    # Gemini settings
    gemini_api_key: str
    
    # App settings
    app_port: int = 8000
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
