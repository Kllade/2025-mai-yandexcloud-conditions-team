from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.dialogs.main_menu.states import MainMenu
from aiogram_dialog import DialogManager, StartMode

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: types.Message, dialog_manager: DialogManager) -> None:
    # Удаляем клавиатуру, если она есть
    if message.reply_markup:
        await message.edit_reply_markup(reply_markup=None)
    await dialog_manager.start(MainMenu.start, mode=StartMode.NEW_STACK)
    
