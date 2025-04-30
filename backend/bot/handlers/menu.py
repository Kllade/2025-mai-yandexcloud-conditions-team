from aiogram import Router, types, F
from aiogram.filters import Command
from bot.dialogs.main_menu.states import MainMenu
from aiogram_dialog import DialogManager, StartMode
from bot.handlers.on_click.main_menu import process_question, on_support
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline_menu import main_menu_kb, close, support_kb
from sqlalchemy.ext.asyncio import AsyncSession
from api.cache.redis import redis_client, set_redis_value
from bot.core.loader import bot
import logging
logger = logging.getLogger(__name__)

router = Router(name="menu")


@router.message(Command("menu"))
async def start_handler(message: types.Message, state: FSMContext) -> None:
    if message.reply_markup:
        await message.edit_reply_markup(reply_markup=None)
    await message.answer(
        "Главное меню",
        reply_markup=main_menu_kb()
    )
    await state.set_state(MainMenu.main_menu)


@router.callback_query(MainMenu.main_menu, F.data.startswith("ask_question"))
async def cmd_ask_question(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainMenu.start_question)
    await c.message.edit_text("✍️ Напишите ваш вопрос:", reply_markup=close())
    await c.answer()


@router.callback_query(MainMenu.start_question, F.data.startswith("close"))
async def cmd_close_question(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainMenu.main_menu)
    await c.message.edit_text("Главное меню", reply_markup=main_menu_kb())
    await c.answer()

@router.callback_query(MainMenu.main_menu, F.data.startswith("support"))
async def start_support(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainMenu.start_support)
    await on_support(c.from_user.id, c.message)


@router.callback_query(MainMenu.start_support, F.data.startswith("take_"))
async def take_chat(callback: types.CallbackQuery, state: FSMContext):
    operator_id = callback.from_user.id
    user_id = int(callback.data.split("_")[1])
    user_key = f"support:user:{user_id}"
    status = await redis_client.get(user_key)
    logger.info(f"status: {status}\n type: {type(status)}")
    if status != "waiting":
        await callback.answer("Чат уже взят другим оператором или закрыт.", show_alert=True)
        return
    
    await set_redis_value(user_key, str(operator_id))
    await set_redis_value(f"support:operator:{operator_id}", str(user_id))

    # Уведомление
    await bot.send_message(
        operator_id,
        f"Вы подключились к чату с пользователем <a href=\"tg://user?id={user_id}\">{user_id}</a>. Для завершения напишите /close.",
        parse_mode="HTML"
    )
    await bot.send_message(
        user_id,
        f"Оператор <a href=\"tg://user?id={operator_id}\">{callback.from_user.full_name}</a> подключился к чату. Задавайте ваши вопросы.",
        parse_mode="HTML", reply_markup=support_kb()
    )
    
    await state.set_state(MainMenu.support)
    await callback.message.edit_reply_markup(reply_markup=None)

@router.message(MainMenu.support)
async def route_messages(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Если сообщение от оператора
    op_key = f"support:operator:{user_id}"
    if await redis_client.exists(op_key):
        cust_id = int(await redis_client.get(op_key))
        await bot.send_message(cust_id, f"Оператор: {message.text}")
        return
    # Если сообщение от поддерживаемого пользователя
    user_key = f"support:user:{user_id}"
    val = await redis_client.get(user_key)
    if val and val.isdigit():
        op_id = int(val)
        await bot.send_message(op_id, f"Пользователь: {message.text}")
        return

@router.message(MainMenu.start_question)
async def handle_question_message(message: types.Message, state: FSMContext, session: AsyncSession):
    """Обработчик обычных текстовых сообщений в состоянии start_question"""
    await state.set_state(MainMenu.waiting_answer)
    await process_question(message, state, message.text, session)


@router.message(F.text.not_.startswith("/"))
async def handle_question_message(message: types.Message, state: FSMContext, session: AsyncSession):
    """Обработчик обычных текстовых сообщений в состоянии start_question"""
    await state.set_state(MainMenu.waiting_answer)
    await process_question(message, state, message.text, session)



