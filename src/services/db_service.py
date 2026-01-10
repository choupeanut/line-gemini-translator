import aiosqlite
import os

DB_PATH = "data/translator.db"

class DBService:
    def __init__(self):
        # 確保資料夾存在
        os.makedirs("data", exist_ok=True)

    async def init_db(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_prefs (
                    group_id TEXT,
                    user_id TEXT,
                    target_lang TEXT,
                    PRIMARY KEY (group_id, user_id)
                )
            """)
            await db.commit()

    async def set_user_pref(self, group_id: str, user_id: str, lang: str):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                INSERT OR REPLACE INTO user_prefs (group_id, user_id, target_lang)
                VALUES (?, ?, ?)
            """, (group_id, user_id, lang))
            await db.commit()

    async def get_group_prefs(self, group_id: str):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT user_id, target_lang FROM user_prefs WHERE group_id = ?",
                (group_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return {row[0]: row[1] for row in rows}

db_service = DBService()
