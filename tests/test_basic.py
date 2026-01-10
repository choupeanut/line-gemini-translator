import pytest
from fastapi.testclient import TestClient
from src.main import app
import os

client = TestClient(app)

def test_health_check():
    """測試健康檢查接口"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_db_service_basic():
    """測試資料庫基本存取邏輯"""
    from src.services.db_service import db_service
    import os
    
    # 使用測試用的資料庫路徑
    test_db = "data/test_translator.db"
    if os.path.exists(test_db):
        os.remove(test_db)
        
    import src.services.db_service
    src.services.db_service.DB_PATH = test_db
    
    await db_service.init_db()
    
    # 測試寫入偏好
    await db_service.set_user_pref("group123", "user456", "Thai")
    
    # 測試讀取偏好
    prefs = await db_service.get_group_prefs("group123")
    assert prefs["user456"] == "Thai"
    
    # 清理測試資料
    if os.path.exists(test_db):
        os.remove(test_db)
