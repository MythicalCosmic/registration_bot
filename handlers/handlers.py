from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from .states import UserStates
from utils.utils import *
from config.settings import get_button_text, get_translation
from keyboards.keyboards import *
import traceback
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import re
import os
ADMIN_ID = 6589960007  

router = Router()

CHANNEL_ID = "@SMARTENGLISH2016" 


DOCS_PATH = "documents"   


async def send_results(chat_id: int, bot: Bot):
    """Send all Excel files from documents folder to the user."""
    for file_name in os.listdir(DOCS_PATH):
        if file_name.endswith(".xlsx"):
            file_path = os.path.join(DOCS_PATH, file_name)
            await bot.send_document(chat_id, FSInputFile(file_path))

async def is_subscribed(user_id: int, bot: Bot) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except TelegramForbiddenError:
        return False
    except Exception:
        return False


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
            await message.reply(get_translation("start_message", 'en'), reply_markup=language_keyboard(), parse_mode="HTML")
            await state.set_state(UserStates.set_language)
    except Exception as e:
        await message.reply(f'Error occured in start handler: {e}')

@router.message(lambda message: message.text == get_button_text('about_us', get_user_language(message.from_user.id)), StateFilter(UserStates.main))
async def main_about_us_input(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)

        photo = FSInputFile("media/photos/photo_2025-09-22_23-44-46.jpg")


        about_text = get_translation('about_us_message', language=language)

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=about_text,
            parse_mode="HTML",
            reply_markup=main_keyboard(language=language)
        )

    except Exception as e:
        await message.reply(f"⚠️ Error in About Us section: {e}")

@router.message(lambda message: message.text == get_button_text('contact_us_button', get_user_language(message.from_user.id)), StateFilter(UserStates.main))
async def main_contact_us_input(message: Message, state: FSMContext, bot: Bot):
    try:
        language = get_user_language(message.from_user.id)
        caption = get_translation('contact_us', language=language)
        photo_path = FSInputFile("media/photos/qr_code.jpg")


        await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo_path,
                caption=caption,
                parse_mode="HTML",
                reply_markup=main_keyboard(language=language)
        )
    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")

@router.message(lambda message: message.text == get_button_text('results_button', get_user_language(message.from_user.id)), StateFilter(UserStates.main))
async def main_contact_us_input(message: Message, state: FSMContext, bot: Bot):
        try:
            language = get_user_language(message.from_user.id)
            results = [
                {
                    "file": "1.jpg",
                    "caption": """🏆 <b>Akramov Muhammad Siddiq</b>\n
⭐ Overall Band: <b>7.0</b>\n
🎧 Listening: 7.0\n
📖 Reading: 7.5\n
✍️ Writing: 5.5\n
🗣 Speaking: 7.5"""
                },
                {
                    "file": "2.jpg",
                    "caption": """🏆 <b>Karimov Abdulaziz</b>\n
⭐ Overall Band: <b>6.5</b>\n
🎧 Listening: 6.5\n
📖 Reading: 7.0\n
✍️ Writing: 6.0\n
🗣 Speaking: 6.0"""
                },
                {
                    "file": "3.jpg",
                    "caption": """🏆 <b>Egamberdiev Nodirbek</b>\n
⭐ Overall Band: <b>7.0</b>\n
🎧 Listening: 8.0 ✅\n
📖 Reading: 7.0\n
✍️ Writing: 6.5\n
🗣 Speaking: 7.0"""
                },
                {
                    "file": "4.jpg",
                    "caption": """🏆 <b>Nurmahammatova Sadoqatxon</b>\n
⭐ Overall Band: <b>7.0</b>\n
🎧 Listening: 8.5 🌟\n
📖 Reading: 6.5\n
✍️ Writing: 6.5\n
🗣 Speaking: 6.5"""
                },
                {
                    "file": "5.jpg",
                    "caption": """🏆 <b>Orifjonova Nozanin</b>\n
⭐ Overall Band: <b>6.5</b>\n
🎧 Listening: 6.0\n
📖 Reading: 6.5\n
✍️ Writing: 6.0\n
🗣 Speaking: 6.5"""
                },
                {
                    "file": "6.jpg",
                    "caption": """🏆 <b>Malikov Abdulloh</b>\n
⭐ Overall Band: <b>6.5</b>\n
🎧 Listening: 7.5\n
📖 Reading: 6.5\n
✍️ Writing: 7.0 🌟\n
🗣 Speaking: 5.5"""
                },
                {
                    "file": "7.jpg",
                    "caption": """🏆 <b>Abdugopporov Boburjon</b>\n
⭐ Overall Band: <b>6.5</b>\n
🎧 Listening: 8.0 🌟\n
📖 Reading: 6.5\n
✍️ Writing: 6.0\n
🗣 Speaking: 6.0"""
                },
                {
                    "file": "main.jpg",
                    "caption": """🏆 <b>Abrorbek Qodirjonov</b>\n
⭐ Overall Band: <b>6.5</b>\n
🎧 Listening: 7.0\n
📖 Reading: 6.5\n
🗣 Speaking: 6.0\n
✍️ Writing: 6.0"""
                }
            ]

            for result in results:
                photo = FSInputFile(f"media/photos/results/{result['file']}")
                
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption=result["caption"],
                    parse_mode="HTML",
                    reply_markup=main_keyboard(language=language)
                )

        except Exception as e:
            await message.reply(f"⚠️ Error occurred while sending results: {e}")
    

@router.message(lambda message: message.text == get_button_text('settings_button', get_user_language(message.from_user.id)), StateFilter(UserStates.main))
async def main_settings_input(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        set_user_state(user_id=user_id, state=UserStates.set_language.state)
        await message.reply(get_translation("start_message", 'en'), reply_markup=language_keyboard(), parse_mode="HTML")
        await state.set_state(UserStates.set_language)
    except Exception as e:
        await message.reply(f"⚠️ Error occurred while settings results: {e}")

@router.message(lambda message: message.text == get_button_text('exam_results', get_user_language(message.from_user.id)), StateFilter(UserStates.main))
async def exam_results_handler(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id

    if await is_subscribed(user_id, bot):
        await message.answer("✅ Siz obuna bo‘lgansiz!\n\n📌 Olimpiada natijalari yuklanmoqda...")
        await send_results(message.chat.id, bot)
    else:
        kb = InlineKeyboardBuilder()
        kb.button(text="📢 Subscribe", url="https://t.me/SMARTENGLISH2016")
        kb.button(text="✅ Check Again", callback_data="check_sub")
        await message.answer(
            "⚠️ Iltimos, avval kanalimizga obuna bo‘ling!\n\n"
            "👉 <a href='https://t.me/SMARTENGLISH2016'>SMART ENGLISH 2016</a>",
            reply_markup=kb.as_markup(),
            disable_web_page_preview=True,
            parse_mode="HTML"
        )


@router.callback_query(F.data == "check_sub")
async def check_subscription(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id

    if await is_subscribed(user_id, bot):
        await call.message.edit_text("✅ Rahmat! Siz obuna bo‘lgansiz.\n\n📌 Olimpiada natijalari yuklanmoqda...")
        await send_results(call.message.chat.id, bot)
    else:
        kb = InlineKeyboardBuilder()
        kb.button(text="📢 Subscribe", url="https://t.me/SMARTENGLISH2016")
        kb.button(text="✅ Check Again", callback_data="check_sub")

        await call.answer("❌ Siz hali obuna bo‘lmadingiz!", show_alert=True)

        await call.message.edit_text(
            "⚠️ Iltimos, avval kanalimizga obuna bo‘ling!\n\n"
            "👉 <a href='https://t.me/SMARTENGLISH2016'>SMART ENGLISH 2016</a>\n\n"
            "🔄 Tekshirish uchun quyidagi tugmadan foydalaning 👇",
            reply_markup=kb.as_markup(),
            disable_web_page_preview=True,
            parse_mode="HTML"
        )

            
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

@router.message(lambda message: message.text == get_button_text("back_button", get_user_language(message.from_user.id)), StateFilter(UserStates.regiser_first.state, UserStates.main, UserStates.last_name, UserStates.age, UserStates.phone_number, UserStates.address, UserStates.course, UserStates.level))
async def handle_back(message: Message, state: FSMContext, bot: Bot):
    try:
        current_state = await state.get_state()
        print(current_state)
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

        async def go_to_phone_number():
            await state.set_state(UserStates.phone_number)
            set_user_state(user_id=user_id, state=UserStates.phone_number.state)
            await message.answer(
                get_translation('phone_number_message', language=language), 
                reply_markup=phone_number_keyboard(language),
                parse_mode='HTML'
            )
        async def go_to_address():
            await state.set_state(UserStates.address)
            set_user_state(user_id=user_id, state=UserStates.address.state)
            await message.reply(
                get_translation('address_message', language=language), 
                reply_markup=back_keyboard(language),
                parse_mode='HTML'
            )
        async def go_to_course():
            await state.set_state(UserStates.course)
            set_user_state(user_id=user_id, state=UserStates.course.state)
            await message.reply(
                get_translation('course_message', language=language), 
                reply_markup=course_keyboard(language),
                parse_mode='HTML'
            )
        state_actions = {
            UserStates.regiser_first: go_to_main,
            UserStates.main.state: go_to_main,
            UserStates.last_name: go_to_first_name,
            UserStates.age: go_to_last_name,
            UserStates.phone_number: go_to_age,
            UserStates.address: go_to_phone_number,
            UserStates.course: go_to_address,
            UserStates.level: go_to_course,

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


        if message.contact and message.contact.phone_number:
            phone_number = message.contact.phone_number
        elif message.text:
            phone_number = message.text.strip()
        else:
            phone_number = None

 
        if phone_number:
            phone_number = re.sub(r"[^\d+]", "", phone_number)

            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number

        if not phone_number or not re.fullmatch(r"\+\d{7,15}", phone_number):
            await message.reply(
                get_translation('phone_number_invalid', language=language),
                reply_markup=phone_number_keyboard(language=language),
                parse_mode='HTML'
            )
            return


        set_student_phone_number(user_id=user_id, phone_number=phone_number)
        set_user_state(user_id, state=UserStates.address.state)
        await state.set_state(UserStates.address)

        await message.reply(
            get_translation('address_message', language=language),
            reply_markup=back_keyboard(language),
            parse_mode='HTML'
        )

    except Exception as e:
        await message.reply(f"Error occurred on handle number: {e}")



@router.message(StateFilter(UserStates.address))
async def handle_address_input(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        address = message.text.strip()
        set_user_state(user_id=user_id, state=UserStates.course.state)
        set_student_address(user_id=user_id, address=address)
        await message.reply(
            get_translation('course_message', language=language),
            reply_markup=course_keyboard(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.course)
    except Exception as e:
        await message.reply(f"Error occured on address input: {e}")

@router.message(lambda message: message.text == get_button_text('english_button', get_user_language(message.from_user.id)), StateFilter(UserStates.course))
async def handle_course_input(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=UserStates.level.state)
        set_student_course(user_id=user_id, course='English')
        await message.reply(
            get_translation('level_message', language=language),
            reply_markup=english_levels_keyboard(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.level)
    except Exception as e:
        await message.reply(f"Error occured on course input: {e}")

@router.message(lambda message: message.text == get_button_text('it_button', get_user_language(message.from_user.id)), StateFilter(UserStates.course))
async def handle_course_it_input(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=UserStates.time.state)
        set_student_course(user_id=user_id, course='IT')
        await message.reply(
            get_translation('time_message', language=language),
            reply_markup=back_keyboard(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.time)
    except Exception as e:
        await message.reply(f"Error occured on course input: {e}")

@router.message(StateFilter(UserStates.level))
async def handle_level_input(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        level = message.text.strip()

        valid_levels = [
            get_button_text('elementary_button', language),
            get_button_text('beginner_button', language),
            get_button_text('intermediate_button', language),
            get_button_text('upper_intermediate_button', language),
            get_button_text('advanced_button', language),
        ]

        if level in valid_levels:
            set_student_level(user_id=user_id, level=f'English|{level}')

            await state.set_state(UserStates.time)  

            await message.reply(
                get_translation('time_message', language=language),
                reply_markup=back_keyboard(language=language),
                parse_mode='HTML'
            )
        else:
            await message.reply(
                get_translation('level_invalid', language=language),
                reply_markup=english_levels_keyboard(language),
                parse_mode='HTML'
            )

    except Exception as e:
        await message.reply(f"Error occurred on level input: {e}")


@router.message(StateFilter(UserStates.time))
async def handle_time_input(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        time = message.text.strip()

        set_student_time(user_id=user_id, time=time)

        db = SessionLocal()
        student = db.query(Student).filter(Student.telegram_user_id == user_id).first()
        db.close()

        if student:
            student_info = (
                f"<b>New Student Registered ✅</b>\n\n"
                f"<b>First Name:</b> {student.first_name or '-'}\n"
                f"<b>Last Name:</b> {student.last_name or '-'}\n"
                f"<b>Age:</b> {student.age or '-'}\n"
                f"<b>Phone:</b> {student.phone_number or '-'}\n"
                f"<b>Address:</b> {student.address or '-'}\n"
                f"<b>Course:</b> {student.course or '-'}\n"
                f"<b>Level:</b> {student.level or '-'}\n"
                f"<b>Time:</b> {student.time or '-'}\n"
                f"<b>Telegram ID:</b> {student.telegram_user_id}"
            )

            await bot.send_message(
                ADMIN_ID,
                student_info,
                parse_mode="HTML"
            )
        await state.set_state(UserStates.main)


        await message.reply(
            get_translation('approved_message', language=language),
            reply_markup=main_keyboard(language=language),
            parse_mode='HTML'
        )

    except Exception as e:
        await message.reply(f"Error occurred on time input: {e}")


@router.message(StateFilter(UserStates.set_language, UserStates.main, UserStates.course, UserStates.level))
async def handle_unrecognized_input(message: Message, state: FSMContext, bot: Bot):
    try:
        current_state = await state.get_state()
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        state_responses = {
            UserStates.set_language: {
                "text": get_translation('start_message', language=language),
                "keyboard": language_keyboard()
            },
            UserStates.course: {
                "text": get_translation('course_message', language=language),
                "keyboard": course_keyboard(language)
            },
            UserStates.level: {
                "text": get_translation('level_message', language=language),
                "keyboard": english_levels_keyboard(language)
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
