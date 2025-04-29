from aiogram_dialog import Window, StartMode
from aiogram.types import ContentType
from aiogram.filters import StateFilter
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Button, Back, SwitchTo, Row, Next






#def admin_projects_menu_window():
    # return Window(
    #     Const(text="Главное меню"),
    #     Button(Const("Задать вопрос"), id="go_to_all_projects_menu", on_click=on_all_projects_click),
    #     Button(Const("Поиск проекта"), id="search_project", on_click=on_project_search_click),
    #     # goto("Общая статистика", "admin_projects_stats", AdminMain.projects_main_stats),
    #     Row(
    #         Button(
    #             Const("Добавить"),
    #             id="admin_projects_add",
    #             on_click=on_add_projects_click,
    #         ),
    #         Button(
    #             Const("Удалить"),
    #             id="admin_projects_delete",
    #             on_click=on_delete_projects_click,
    #         ),
    #     ),
    #     goto_main_menu,
    #     state=AdminMain.projects_main_menu,
    # )

