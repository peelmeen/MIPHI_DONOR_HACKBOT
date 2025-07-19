import aiosqlite
# import asyncio
# import logging
# from datetime import datetime
import json


DB_NAME = "MIPHI_Donor.db"


async def init_db():
    """Создание таблицы пользователей"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                phone TEXT UNIQUE DEFAULT '-',
                FNS TEXT DEFAULT '-',
                type TEXT DEFAULT '-',
                agree INTEGER DEFAULT '-',
                DON INTERER DEFAULT '-',
                last_blood_center TEXT DEFAULT '-',
                last_don TEXT DEFAULT '-',
                date TEXT DEFAULT '-',         
                blood_center TEXT DEFAULT '-'
            )
        """)
        await db.commit()
#type - студент, сотрудник, внешний донор


async def add_user(telegram_id: int, phone: str = None, FNS: str = None, type: str = None, group_num: int = None, agree: int = None, DON: int = None, last_blood_center: str = None, last_don: str = None, date: str = None, blood_center: str = None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                phone INTEGER UNIQUE DEFAULT '-',
                FNS TEXT DEFAULT '-',
                type TEXT DEFAULT '-',
                agree INTEGER DEFAULT '-',
                DON INTERER DEFAULT '-',
                last_blood_center TEXT DEFAULT '-',
                last_don TEXT DEFAULT '-',
                date TEXT DEFAULT '-',         
                blood_center TEXT DEFAULT '-'
            )
        """)
        await db.commit()


        cursor = await db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        existing_user = await cursor.fetchone()

        if existing_user:
            return False  # Юзер уже есть

        await db.execute("INSERT INTO users (telegram_id, phone, FNS, type, agree, DON, last_blood_center, last_don, date, blood_center) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",  #  ?
                        (telegram_id, '-', '-', '-', '-', '-', '-', '-', '-', '-')) # , '-'
        await db.commit()
        return True




async def edit_FNS(FNS, telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET FNS = ? WHERE telegram_id = ?", (FNS, telegram_id))
        await db.commit()




async def edit_phone(phone, telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET phone = ? WHERE telegram_id = ?", (phone, telegram_id))
        await db.commit()








async def edit_Date(Date, telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET date = ? WHERE telegram_id = ?", (Date, telegram_id))
        await db.commit()






async def edit_last_don(Date, telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET last_don = ? WHERE telegram_id = ?", (Date, telegram_id))
        await db.commit()







async def edit_two_fields(phone, FNS, telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET phone = ?, FNS = ? WHERE telegram_id = ?", (phone, FNS, telegram_id)
        )
        await db.commit()





async def get_data(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT FNS, phone, date, blood_center FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cursor.fetchall()
        return row[0]
    

async def edit_agree(telegram_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET agree = 1 WHERE telegram_id = ?",(telegram_id,))
        await db.commit()






async def edit_FNS(FNS, telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET FNS = ? WHERE telegram_id = ?", (FNS, telegram_id))
        await db.commit()



async def get_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT telegram_id FROM users")
        rows = await cursor.fetchall()
        return [int(row[0]) for row in rows if row[0] is not None]
        # return rows #[int(rows[0]) for row in rows]




async def get_agree(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT agree FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cursor.fetchone()
        return row[0] if row else 0



async def edit_blood_center(CB, telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET blood_center = ? WHERE telegram_id = ?", (CB, telegram_id))
        await db.commit()





async def edit_last_blood_center(CB, telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET last_blood_center = ? WHERE telegram_id = ?", (CB, telegram_id))
        await db.commit()



async def get_date(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT date FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cursor.fetchone()
        return row[0] if row else 0
    


async def get_CB(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT blood_center FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cursor.fetchone()
        return row[0] if row else 0
    

async def edit_type_stuff(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET type = stuff WHERE telegram_id = ?", (telegram_id))
        await db.commit()
        


async def edit_type_different(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET type = stuff WHERE telegram_id = ?", (telegram_id))
        await db.commit()



async def edit_group(group, telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET type = ? WHERE telegram_id = ?", (group, telegram_id))
        await db.commit()



async def get_contact(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT phone FROM users WHERE telegram_id = ?", (telegram_id,))
        rows = await cursor.fetchall()
        return [row[0] for row in rows if row[0] is not None]
