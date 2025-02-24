from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

main_router = Router()


@main_router.message(Command('start'))
async def welcome_message(message: Message):
    """
    send welcome message.
    """
    await message.answer('bot works!')
