import aiosqlite
import datetime as dat
import configparser

# Настройки конфигурации
config = configparser.ConfigParser()
config.read('config.ini')
DATABASE_PATH = config.get('Settings', 'PATH_BASE')


async def av_in_db(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT user_id FROM Users WHERE user_id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            return bool(result)


async def new_user(user_id, user_name, subscription_end_date):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'INSERT INTO Users (user_id, user_name, gpt3_usage_count, subscription_end_date, gpt4_usage_count, model_mode, context_saved, dalle3_usage_count) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (user_id, user_name, 0, subscription_end_date, 0, 3, 0, 0))
        await db.commit()


async def set_quantity_gpt_3(user_id, user_name, gpt3_usage_count):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('UPDATE Users SET user_name = ?, gpt3_usage_count = ? WHERE user_id = ?',
                         (user_name, gpt3_usage_count, user_id))
        await db.commit()


# Пример функции для получения контекста
async def get_context(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT user_context FROM Users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else []


# Пример функции для установки контекста
async def set_context_gpt(user_context, user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('UPDATE Users SET user_context = ? WHERE user_id = ?', (user_context, user_id))
        await db.commit()


async def set_quantity_gpt_4(user_id, user_name, gpt4_usage_count):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('UPDATE Users SET user_name = ?, gpt4_usage_count = ? WHERE user_id = ?',
                         (user_name, gpt4_usage_count, user_id))
        await db.commit()


async def set_quantity_dalle_3(user_id, user_name, dalle3_usage_count):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('UPDATE Users SET user_name = ?, dalle3_usage_count = ? WHERE user_id = ?',
                         (user_name, dalle3_usage_count, user_id))
        await db.commit()


async def update_subscription_end_date(user_id, user_name, subscription_end_date):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('UPDATE Users SET user_name = ?, subscription_end_date = ? WHERE user_id = ?',
                         (user_name, subscription_end_date, user_id))
        await db.commit()


async def get_quantity_gpt_3(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT gpt3_usage_count FROM Users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return int(result[0]) if result else 0


async def get_quantity_gpt_4(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT gpt4_usage_count FROM Users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return int(result[0]) if result else 0


async def get_quantity_dalle_3(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT dalle3_usage_count FROM Users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return int(result[0]) if result else 0


async def date_p_s(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        try:
            async with db.execute('SELECT subscription_end_date FROM Users WHERE user_id = ?', (user_id,)) as cursor:
                result = await cursor.fetchone()
                return dat.datetime.strptime(result[0], '%Y-%m-%d').date() if result else None
        except Exception as e:
            print(e)


async def new_all_quantity_gpt(quantity):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('UPDATE Users SET gpt3_usage_count = ?, gpt4_usage_count = ?, dalle3_usage_count = ?',
                         (quantity, quantity, quantity))
        await db.commit()


async def set_save_context_gpt(context_saved, user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('UPDATE Users SET context_saved = ? WHERE user_id = ?', (context_saved, user_id))
        await db.commit()


async def set_mode_model_gpt(model_mode, user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('UPDATE Users SET model_mode = ? WHERE user_id = ?', (model_mode, user_id))
        await db.commit()


async def get_mode_model_gpt(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT model_mode FROM Users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return int(result[0]) if result else None


async def get_mode_model_gpt_and_save_context(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT model_mode, context_saved FROM Users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                model_mode, context_saved = result
                return int(model_mode), int(context_saved)
            else:
                return None, None


async def get_settings_statistics(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
                'SELECT model_mode, context_saved, gpt3_usage_count, gpt4_usage_count, dalle3_usage_count FROM Users '
                'WHERE user_id = ?',
                (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                model_mode, context_saved, gpt3_usage_count, gpt4_usage_count, dalle3_usage_count = result
                return int(model_mode), int(context_saved), int(gpt3_usage_count), int(gpt4_usage_count), int(
                    dalle3_usage_count)
            else:
                return None, None, None, None, None


async def delete_context_gpt(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('UPDATE Users SET user_context = NULL WHERE user_id = ?', (user_id,))
        await db.commit()
