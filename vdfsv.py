import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = '8286575871:AAFK32MDZJsGetWk5YO7ad-CiF9voCLBBzs'  # Вставь токен
OWNER_ID = 7459210893  # 🔒 Вставь СВОЙ Telegram user ID (не username!)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

participants = set()

join_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎉 Беру участь", callback_data="join")]
    ]
)

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! Натисни кнопку нижче, щоб взяти участь у розіграші:",
        reply_markup=join_button
    )

@dp.message(F.text == "/list")
async def cmd_list(message: types.Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("⛔ Ця команда доступна лише організатору.")
        return

    if participants:
        text = "Список учасників:\n" + "\n".join(participants)
    else:
        text = "Ще ніхто не бере участі."
    await message.answer(text)

@dp.callback_query(F.data == "join")
async def process_join(callback: types.CallbackQuery):
    user = callback.from_user
    user_info = f"{user.full_name} (@{user.username})"
    if user_info not in participants:
        participants.add(user_info)
        await callback.answer("Ти береш участь 🎉")
        await callback.message.answer(f"{user_info} долучився!")
    else:
        await callback.answer("Ти вже береш участь 😉")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())