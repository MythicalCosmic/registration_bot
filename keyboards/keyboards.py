from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.settings import get_button_text, get_translation

UZ = "🇺🇿 O'zbek Tili"
EN = "🇺🇸 English"
RU = "🇷🇺 Русский"


def language_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=UZ)],
            [KeyboardButton(text=EN)],
            [KeyboardButton(text=RU)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def main_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button_text('register_button', language))],
            [KeyboardButton(text=get_button_text('about_us', language)),
             KeyboardButton(text=get_button_text('results_button', language))],
            [KeyboardButton(text=get_button_text('contact_us_button', language)),
             KeyboardButton(text=get_button_text('settings_button', language))],
            [KeyboardButton(text=get_button_text('exam_results', language))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def back_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button_text('back_button', language=language))]
        ],
        resize_keyboard=True
    )

def phone_number_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button_text('phone_number_button', language), request_contact=True)],
            [KeyboardButton(text=get_button_text('back_button', language=language))]
        ],
        resize_keyboard=True
    )

def course_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button_text('english_button', language)),
             KeyboardButton(text=get_button_text('it_button', language))],
            [KeyboardButton(text=get_button_text('back_button', language=language))]
        ],
        resize_keyboard=True
    )

def english_levels_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button_text('elementary_button', language)),
             KeyboardButton(text=get_button_text('beginner_button', language))],
            [KeyboardButton(text=get_button_text('intermediate_button', language)),
             KeyboardButton(text=get_button_text('upper_intermediate_button', language))],
            [KeyboardButton(text=get_button_text('advanced_button', language))],
            [KeyboardButton(text=get_button_text('back_button', language=language))]
        ],
        resize_keyboard=True
    )
