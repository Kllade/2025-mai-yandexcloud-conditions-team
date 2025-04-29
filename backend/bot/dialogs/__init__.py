from aiogram_dialog import Dialog
from bot.dialogs.main_menu.windows import (
    main_menu_window,
    start_question_window,
    question_history_window,
    start_window
)
from bot.dialogs.main_menu.states import MainMenu


def menu_dialogs(): 
    return [
        Dialog(
            start_window(),
            main_menu_window(),
            start_question_window(),
            question_history_window(),
        )
    ]