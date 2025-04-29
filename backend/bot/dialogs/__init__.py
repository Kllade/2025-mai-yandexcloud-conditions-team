from aiogram_dialog import Dialog
from bot.dialogs.main_menu.windows import (
    admin_projects_menu_window, start_question_window, 
    question_history_window
)
from bot.dialogs.main_menu.states import MainMenu


def menu_dialogs():
    return [
        Dialog(
            admin_projects_menu_window(),
            start_question_window(),
            question_history_window(),
        )
    ]