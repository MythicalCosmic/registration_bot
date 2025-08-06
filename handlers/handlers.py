from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from .states import UserStates
from utils.utils import *
from config.settings import get_button_text, get_translation
from keyboards.keyboards import *
import traceback

router = Router()



@router.message(Command('start'))
async def start_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        if user_exists(user_id=user_id) and language is not None:
            await message.reply(get_translation('main_message', language=language), reply_markup=main_keyboard(language=language), parse_mode="HTML")
            await state.set_state(UserStates.main)
            set_user_state(user_id=user_id, state=UserStates.main.state)
        else:
            await message.reply(get_translation("start_message", 'uz'), reply_markup=language_keyboard(), parse_mode="HTML")
            await state.set_state(UserStates.set_language)
    except Exception as e:
        await message.reply(f'Error occured in start handler: {e}')
            
@router.message(lambda message: message.text in [EN, RU, UZ], StateFilter(UserStates.set_language))
async def set_language_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language_map = {
            "🇺🇸 English": "en",
            "🇺🇿 O'zbek Tili": "uz",
            "🇷🇺 Русский язык": "ru" 
        }
        language = language_map.get(message.text, "ru")
        set_user_state(user_id=user_id, state=UserStates.set_language.state)
        set_user_language(user_id=user_id, language=language)
        user_language = get_user_language(user_id=user_id)
        await message.reply(get_translation('main_message', user_language), reply_markup=main_keyboard(user_language), parse_mode="HTML")
        set_user_state(user_id=user_id, state=UserStates.main.state)
        await state.set_state(UserStates.main)
    except Exception as e:
        await message.reply(f'Error occurred: {e}')

@router.message(lambda message: message.text == get_button_text("back_button", get_user_language(message.from_user.id)), StateFilter(UserStates.regiser_first.state, UserStates.main, UserStates.last_name, UserStates.age, UserStates.phone_number))
async def handle_back(message: Message, state: FSMContext, bot: Bot):
    try:
        current_state = await state.get_state()
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)

        async def go_to_main():
            await state.set_state(UserStates.main)  
            set_user_state(user_id, UserStates.main.state) 
            await message.answer(                      
                get_translation("main_message", language=language),
                reply_markup=main_keyboard(language=language),
                parse_mode="HTML"
            )
        async def go_to_first_name():
            await state.set_state(UserStates.regiser_first)
            set_user_state(user_id, UserStates.regiser_first.state)
            await message.answer(
                get_translation("first_name_message", language=language),
                reply_markup=back_keyboard(language),
                parse_mode='HTML'
            )
        
        async def go_to_last_name():
            await state.set_state(UserStates.last_name)
            set_user_state(user_id, UserStates.last_name.state)
            await message.answer(
                get_translation('last_name_message', language=language), 
                reply_markup=back_keyboard(language),
                parse_mode='HTML'
            )

        async def go_to_age():
            await state.set_state(UserStates.age)
            set_user_state(user_id, UserStates.age.state)
            await message.answer(
                get_translation('age_message', language=language), 
                reply_markup=back_keyboard(language),
                parse_mode='HTML'
            )

        state_actions = {
            UserStates.regiser_first: go_to_main,
            UserStates.main.state: go_to_main,
            UserStates.last_name: go_to_first_name,
            UserStates.age: go_to_last_name,
            UserStates.phone_number: go_to_age,
        }

        action = state_actions.get(current_state)
        if action:
            await action()
        else:
            await message.answer("Unknown state. Please try again.")

    except Exception as e:
        await message.reply(f'Error occured on handle back: {e}')


@router.message(lambda message: message.text == get_button_text('register_button', language=get_user_language(message.from_user.id)), StateFilter(UserStates.main))
async def regiser_button_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=UserStates.regiser_first.state)
        await message.reply(get_translation('first_name_message', language=language), reply_markup=back_keyboard(language=language), parse_mode="HTML")
        await state.set_state(UserStates.regiser_first)
    except Exception as e:
        await message.reply(f'Error occured on regiser button handler: {e}')

@router.message(StateFilter(UserStates.regiser_first))
async def handle_first_name(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        first_name = message.text.strip()
        set_student_first_name(user_id=user_id, first_name=first_name)
        set_user_state(user_id=user_id, state=UserStates.last_name.state)
        await message.reply(get_translation('last_name_message', language=language), reply_markup=back_keyboard(language=language), parse_mode='HTML')
        await state.set_state(UserStates.last_name)
    except Exception as e:
        await message.reply(f"Error occured on handle first name handler:\n<code>{traceback.format_exc()}</code>", parse_mode="HTML")


@router.message(StateFilter(UserStates.last_name))
async def handle_last_name(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        last_name = message.text.strip()
        set_student_last_name(user_id=user_id, last_name=last_name)
        set_user_state(user_id=user_id, state=UserStates.age.state)
        await message.reply(get_translation('age_message', language=language), reply_markup=back_keyboard(language=language), parse_mode='HTML')
        await state.set_state(UserStates.age)
    except Exception as e:
        await message.reply(f'Error occured on handle last name: {e}')


@router.message(StateFilter(UserStates.age))
async def handle_age(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        age = message.text.strip()

        if not age.isdigit() or not (5 <= int(age) <= 100): 
            await message.reply(
                get_translation('age_message', language=language),
                reply_markup=back_keyboard(language),
                parse_mode='HTML'
            )
            return

        set_student_age(user_id=user_id, age=int(age))
        set_user_state(user_id=user_id, state=UserStates.phone_number.state)
        await message.reply(
            get_translation('phone_number_message', language=language),
            reply_markup=phone_number_keyboard(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.phone_number)

    except Exception as e:
        await message.reply(f'Error occurred: {e}')

@router.message(StateFilter(UserStates.phone_number))
async def handle_phone_number(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)

        phone_number = None
        if message.contact and message.contact.phone_number:
            phone_number = message.contact.phone_number
        elif message.text:
            phone_number = message.text.strip()
        if not phone_number or not phone_number.startswith('+') or not phone_number[1:].isdigit():
            await message.reply(
                get_translation('phone_number_invalid', language=language),
                reply_markup=phone_number_keyboard(language=language),
                parse_mode='HTML'
            )
            return

        set_student_phone_number(user_id=user_id, phone_number=phone_number)

        set_user_state(user_id=user_id, state=UserStates.address.state) 
        await message.reply(
            get_translation('registration_complete', language=language),
            reply_markup=back_keyboard(language),
            parse_mode='HTML'
        )

    except Exception as e:
        await message.reply(f"Error occurred on handle number: {e}")





@router.message(StateFilter(UserStates.set_language, UserStates.main))
async def handle_unrecognized_input(message: Message, state: FSMContext):
    try:
        current_state = await state.get_state()
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        state_responses = {
            UserStates.set_language: {
                "text": get_translation('start_message', language=language),
                "keyboard": language_keyboard()
            }
        }
        response = state_responses.get(current_state, {
            "text": get_translation('main_message', language=language),
            "keyboard": main_keyboard(language=language)
        })

        await message.reply(
            response['text'],
            reply_markup=response['keyboard'],
            parse_mode='HTML'
        )

    except Exception as e:
        await message.reply(f'Error occured on handle_unrecognized_input handler: {e}')

@router.message(StateFilter(UserStates.main))
async def main_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        await message.reply(get_translation('main_message', language=language), reply_markup=main_keyboard(language=language), parse_mode="HTML")
        set_user_state(user_id=user_id, state=UserStates.main.state)
    except Exception as e:
        await message.reply(f"Error occured: {e}")



@router.message()
async def fallback_handler(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        if user_exists(user_id=user_id) and language is not None:
            await message.reply(get_translation('main_message', language=language), reply_markup=main_keyboard(language=language), parse_mode="HTML")  
            await state.set_state(UserStates.main)
            set_user_state(user_id=user_id, state=UserStates.main.state)

        else:
            await message.reply(get_translation('start_message', 'uz'), reply_markup=language_keyboard(), parse_mode='HTML')
            await state.set_state(UserStates.start)
            await set_user_state(user_id=user_id, state=UserStates.main.state)          
    except Exception as e:
        await message.reply(f"Error occured on fallback_handler: {e}")
