from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(dbname="bot_db", user="test", password="test", host="31.129.105.17", port="5432")


bot = Bot(token=os.environ.get('TOKEN'))
dp = Dispatcher(bot)


# Обработчик команды /status
@dp.message_handler(commands=['status'])
async def on_status_command(message: types.Message):
    try:
        # Запрос к базе данных для получения статуса
        cur = conn.cursor()
        cur.execute('SELECT * FROM pg_stat_activity;') # SELECT * FROM pg_stat_activity;
        result = cur.fetchall()
        response = "" 
        for i, row in enumerate(result):
            response = f"id бд: {row[0]}\n\n"
            response += f'имя базы данных: {row[1]}\n\n'
            response += f'id процесса: {row[2]}\n\n'
            response += f'имя пользователя {row[5]}\n\n'
            response += f'ip адресс клиента {row[7]}\n\n'
            response += f'статус сеанса: {row[16]}\n\n'
            await message.answer(f'Сеанс {i}\n\n {response}\n\n')
            # response += f"Сеанс: {row}\n\n"
        # await message.answer(f"Статус базы данных: {response}")
        
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    # finally:
    #     cur.close()




# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
