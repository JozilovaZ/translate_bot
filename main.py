import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator
from deep_translator import GoogleTranslator

BOT_TOKEN = "7743118893:AAES8ZaCsDmsRl4lO3ZyVwPX9Xry3blqsDM"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
translator = Translator()


languages = {
    "English": "en",
    "Русский": "ru",
    "O'zbek": "uz",
    "Turk":"tr",
    "Arab":"ar"
}

valyuta={

}


language_keyboard = InlineKeyboardMarkup()
for lang, code in languages.items():
    language_keyboard.add(InlineKeyboardButton(text=lang, callback_data=f"lang_{code}"))


user_languages = {}


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Assalomu alykum, tarjima tilini tanlang", reply_markup=language_keyboard)


@dp.callback_query_handler(lambda call: call.data.startswith("lang_"))
async def set_language(call: types.CallbackQuery):
    lang_code = call.data.split("_")[1]
    user_languages[call.from_user.id] = lang_code
    await call.message.answer("Menga matn yuboring")
    await call.answer()


@dp.message_handler()
async def translate_message(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_languages:
        await message.reply("Tarjima tilini tanlang", reply_markup=language_keyboard)
        return

    lang_code = user_languages[user_id]
    translated_text = GoogleTranslator(source='auto', target=lang_code).translate(message.text)

    await message.reply(f"Tarjima ({languages.get(lang_code, lang_code)}): {translated_text}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
