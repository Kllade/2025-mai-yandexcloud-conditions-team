from aiogram import Router, types
from aiogram.filters import Command
from bot.dialogs.main_menu.states import MainMenu
from aiogram_dialog import DialogManager, StartMode

router = Router(name="menu")


@router.message(Command("menu"))
async def start_handler(message: types.Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainMenu.main_menu, mode=StartMode.NEW_STACK)
    
