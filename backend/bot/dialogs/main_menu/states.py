from aiogram.fsm.state import State, StatesGroup

class MainMenu(StatesGroup):
    start = State()
    main_menu = State()
    start_question = State()
    question_history = State()
    often_questions = State()
    support = State()

