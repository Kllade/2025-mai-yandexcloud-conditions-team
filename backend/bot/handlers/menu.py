from aiogram import Router, types, F
from aiogram.filters import Command
from bot.dialogs.main_menu.states import MainMenu
from aiogram_dialog import DialogManager, StartMode
from bot.handlers.on_click.main_menu import process_question

router = Router(name="menu")


@router.message(Command("menu"))
async def start_handler(message: types.Message, dialog_manager: DialogManager) -> None:
    # Удаляем клавиатуру, если она есть
    if message.reply_markup:
        await message.edit_reply_markup(reply_markup=None)
    await dialog_manager.start(MainMenu.main_menu, mode=StartMode.NEW_STACK)
    

@router.message()
async def handle_question_message(message: types.Message, dialog_manager: DialogManager):
    """Обработчик обычных текстовых сообщений в состоянии start_question"""
    print(f"Получен текст через обычное сообщение: {message.text}")
    
    # Передаем текст сообщения в функцию обработки вопроса
    await process_question(message, dialog_manager, message.text)


