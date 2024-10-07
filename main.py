import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, Dispatcher, types
import asyncio

# Настройки
API_TOKEN = ''
GOOGLE_SHEETS_CREDENTIALS_FILE = 'deliverysaves-702cc766d001.json'
SPREADSHEET_ID = '1YKI0CMHQ22rqEdTzsV0lAIWYl2j1b1fmVUC-Z4ZKMpM'
SHEET_NAME = 'S'
TOPIC_NAME = 7

# Настройка логирования
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS_FILE, scope)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)


# Обработчик новых сообщений
@dp.message()
async def save_message(message: types.Message):
    print(message.message_thread_id)
    try:
        if message.is_topic_message and message.message_thread_id is not None:
            topic_name = message.message_thread_id  # Здесь нужно получить имя топика, если это возможно
            if topic_name == TOPIC_NAME:
                user_first_name = message.from_user.first_name
                user_message = message.text

                # Сохранение в Google Sheets
                sheet.append_row([user_first_name, user_message])

                logging.info(f"Сохранено: {user_first_name} - {user_message}")
    except:
        print('Иди нахуй')

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
