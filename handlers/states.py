from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    start = State()
    set_language = State()
    main = State()
    regiser_first = State()
    last_name = State()
    age = State()
    phone_number = State()
    address = State()
