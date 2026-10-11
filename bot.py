import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- НАСТРОЙКИ ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
PHOTO_PATH = "photo.jpg"

if not BOT_TOKEN:
    raise RuntimeError("Переменная окружения BOT_TOKEN не задана")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- КЛАВИАТУРА ---
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Продлить подписку", callback_data="extend_sub")
    builder.button(text="Тарифы", callback_data="tariffs")
    builder.button(text="Профиль", callback_data="profile")
    builder.button(text="Документация", callback_data="docs")
    builder.button(text="Поддержка", callback_data="support")
    # 1 кнопка в первом ряду, далее по 2 в ряд
    builder.adjust(1, 2, 2)
    return builder.as_markup()


# --- ОБРАБОТЧИКИ ---

@dp.message(CommandStart())
async def cmd_start(message: Message):
    caption_text = (
        "<b>ГЛЕБ ЗАРОВНЯЕВ Service</b>\n\n"
        "Командой разработали сервис по изменению вашего местоположения, "
        "после включения которого вы сможете беспроблемно пользоваться "
        "Telegram, Youtube, TikTok и другие популярные медиа пространства.\n\n"
        "Для взаимодействия с панелью используйте кнопки под данным сообщением."
    )

    try:
        photo = FSInputFile(PHOTO_PATH)
        await message.answer_photo(
            photo=photo,
            caption=caption_text,
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML,
        )
    except Exception:
        await message.answer(
            text=f"Не найден файл {PHOTO_PATH}.\n\n{caption_text}",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML,
        )


# Заглушки для кнопок — пока ничего не делают
@dp.callback_query(F.data == "extend_sub")
async def process_extend_sub(callback: CallbackQuery):
    await callback.answer()


@dp.callback_query(F.data == "tariffs")
async def process_tariffs(callback: CallbackQuery):
    await callback.answer()


@dp.callback_query(F.data == "profile")
async def process_profile(callback: CallbackQuery):
    await callback.answer()


@dp.callback_query(F.data == "docs")
async def process_docs(callback: CallbackQuery):
    await callback.answer()


@dp.callback_query(F.data == "support")
async def process_support(callback: CallbackQuery):
    await callback.answer()


# --- ЗАПУСК ---
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
