import asyncio
from datetime import datetime, timedelta
from db_operations import *


async def run_tests():
    # Пример user_id и user_name
    user_id = 1
    user_name = "test_user"
    subscription_end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    # Проверка наличия пользователя в базе данных
    exists = await av_in_db(user_id)
    print(f"Результат функции `av_in_db`: Пользователь существует: {exists}")

    # Добавление нового пользователя
    if not exists:
        await new_user(user_id, user_name, subscription_end_date)
        print("Результат функции `new_user`: Пользователь добавлен")

    # Обновление количества GPT-3 запросов
    await set_quantity_gpt_3(user_id, user_name, 5)
    print("Результат функции `set_quantity_gpt_3`: Количество запросов GPT-3 обновлено")

    # Получение контекста пользователя
    context = await get_context(user_id)
    print(f"Результат функции `get_context`: Контекст пользователя: {context}")

    # Установка нового контекста
    await set_context_gpt("New context data", user_id)
    print("Результат функции `set_context_gpt`: Контекст обновлен")

    # Обновление количества GPT-4 запросов
    await set_quantity_gpt_4(user_id, user_name, 10)
    print("Результат функции `set_quantity_gpt_4`: Количество запросов GPT-4 обновлено")

    # Обновление количества DALL-E запросов
    await set_quantity_dalle_3(user_id, user_name, 7)
    print("Результат функции `set_quantity_dalle_3`: Количество запросов DALL-E обновлено")

    # Обновление даты окончания подписки
    new_end_date = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
    await update_subscription_end_date(user_id, user_name, new_end_date)
    print("Результат функции `update_subscription_end_date`: Дата окончания подписки обновлена")

    # Получение количества запросов GPT-3
    gpt3_count = await get_quantity_gpt_3(user_id)
    print(f"Результат функции `get_quantity_gpt_3`: Количество запросов GPT-3: {gpt3_count}")

    # Получение количества запросов GPT-4
    gpt4_count = await get_quantity_gpt_4(user_id)
    print(f"Результат функции `get_quantity_gpt_4`: Количество запросов GPT-4: {gpt4_count}")

    # Получение количества запросов DALL-E
    dalle3_count = await get_quantity_dalle_3(user_id)
    print(f"Результат функции `get_quantity_dalle_3`: Количество запросов DALL-E: {dalle3_count}")

    # Получение даты окончания подписки
    sub_end_date = await date_p_s(user_id)
    print(f"Результат функции `date_p_s`: Дата окончания подписки: {sub_end_date}")

    # Установка одинакового количества для всех запросов
    await new_all_quantity_gpt(15)
    print("Результат функции `new_all_quantity_gpt`: Все количества установлены в 15")

    # Установка сохранения контекста
    await set_save_context_gpt(1, user_id)
    print("Результат функции `set_save_context_gpt`: Флаг сохранения контекста установлен")

    # Установка режима модели
    await set_mode_model_gpt(2, user_id)
    print("Результат функции `set_mode_model_gpt`: Режим модели установлен")

    # Получение режима модели
    model_mode = await get_mode_model_gpt(user_id)
    print(f"Результат функции `get_mode_model_gpt`: Режим модели: {model_mode}")

    # Получение режима модели и флага сохранения контекста
    mode_model, context_saved = await get_mode_model_gpt_and_save_context(user_id)
    print(f"Результат функции `get_mode_model_gpt_and_save_context`: Режим модели: {mode_model}, Сохранение контекста: {context_saved}")

    # Получение статистики настроек
    stats = await get_settings_statistics(user_id)
    print(f"Результат функции `get_settings_statistics`: Статистика настроек: {stats}")

    # Удаление контекста пользователя
    await delete_context_gpt(user_id)
    print("Результат функции `delete_context_gpt`: Контекст пользователя удален")


# Запуск тестов
if __name__ == "__main__":
    asyncio.run(run_tests())
