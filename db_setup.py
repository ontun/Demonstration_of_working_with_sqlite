import aiosqlite
import asyncio
from faker import Faker
import datetime
import configparser

# Настройки конфигурации
config = configparser.ConfigParser()
config.read('config.ini')
DATABASE_PATH = config.get('Settings', 'PATH_BASE')

fake = Faker()


async def create_database_and_table():
    """
    Создает базу данных и таблицу Users с необходимой структурой.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                gpt3_usage_count INTEGER CHECK(gpt3_usage_count BETWEEN -1 AND 1500),
                subscription_end_date TEXT,
                gpt4_usage_count INTEGER CHECK(gpt4_usage_count BETWEEN -1 AND 1500),
                model_mode INTEGER CHECK(model_mode BETWEEN -127 AND 128),
                context_saved INTEGER CHECK(context_saved IN (0, 1)),
                user_context TEXT,
                dalle3_usage_count INTEGER CHECK(dalle3_usage_count BETWEEN -1 AND 200)
            );
        ''')
        await db.commit()
        print("Таблица Users успешно создана или уже существует.")


async def fill_db_with_dummy_data():
    """
    Заполняет таблицу Users случайными данными, используя библиотеку Faker.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        used_ids = set()  # Хранение использованных идентификаторов, если не используете AUTOINCREMENT
        for _ in range(100):
            user_id = fake.random_int(min=1, max=1000)
            while user_id in used_ids:  # Убедитесь, что ID уникален
                user_id = fake.random_int(min=1, max=1000)
            used_ids.add(user_id)

            user_name = fake.user_name()
            gpt3_usage_count = fake.random_int(min=0, max=1500)
            gpt4_usage_count = fake.random_int(min=0, max=1500)
            dalle3_usage_count = fake.random_int(min=0, max=200)
            model_mode = fake.random_int(min=-127, max=128)
            context_saved = fake.random_int(min=0, max=1)
            user_context = fake.sentence()
            subscription_end_date = (
                    datetime.datetime.now() + datetime.timedelta(days=fake.random_int(min=1, max=365))
            ).strftime('%Y-%m-%d')

            await db.execute(
                'INSERT INTO Users (user_id, user_name, gpt3_usage_count, subscription_end_date, gpt4_usage_count, '
                'model_mode, context_saved, user_context, dalle3_usage_count) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) '
                'ON CONFLICT(user_id) DO NOTHING;',
                (user_id, user_name, gpt3_usage_count, subscription_end_date, gpt4_usage_count, model_mode,
                 context_saved, user_context, dalle3_usage_count)
            )
        await db.commit()
        print("Таблица Users успешно заполнена 100 строками случайных данных.")


async def main():
    await create_database_and_table()
    await fill_db_with_dummy_data()


# Запуск скрипта
if __name__ == "__main__":
    asyncio.run(main())
