from typing import Dict, Any

from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from db.user import create_user

router = Router()


class GetPersonalData(StatesGroup):
    name = State()
    sec_name = State()
    age = State()
    contact = State()
    location = State()
    record = State()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        text="Botga Xush Kelibsiz!\n\nBotdan foydalanish uchun ismingizni kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(GetPersonalData.name)


@router.message(GetPersonalData.name, F.text.regexp(r"^[a-zA-Zа-яА-ЯёЁ]+$"))
async def get_sec_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    await message.answer(
        text="Familiyangizni kiriting:"
    )
    await state.set_state(GetPersonalData.sec_name)


@router.message(GetPersonalData.name)
async def get_name_incorrect(message: Message):
    await message.answer(
        text="Ism noto'g'ri kiritildi! To'g'irlab boshidan kiriting!"
    )


@router.message(GetPersonalData.sec_name, F.text.regexp(r"^[a-zA-Zа-яА-ЯёЁ]+$"))
async def get_age(message: Message, state: FSMContext):
    await state.update_data(sec_name=message.text.lower())
    await message.answer(
        text="Yoshingizni kiriting:"
    )
    await state.set_state(GetPersonalData.age)


@router.message(GetPersonalData.sec_name)
async def get_sec_name_incorrect(message: Message):
    await message.answer(
        text="Familiya noto'g'ri kiritildi! To'g'irlab boshidan kiriting!"
    )


@router.message(GetPersonalData.age, F.text.regexp(r"^[0-9]+$"), lambda message: 15 < int(message.text) < 70    )
async def get_contact(message: Message, state: FSMContext):
    await state.update_data(age=message.text)

    kb = [KeyboardButton(text="Telefon raqam", request_contact=True)]
    keyboard = ReplyKeyboardMarkup(keyboard=[kb], resize_keyboard=True, is_persistent=True)

    await message.answer(
        text="Telefon raqamingizni kiriting:",
        reply_markup=keyboard
    )
    await state.set_state(GetPersonalData.location)
    ReplyKeyboardRemove()


@router.message(GetPersonalData.age)
async def get_age_incorrect(message: Message):
    await message.answer(
        text="Yosh noto'g'ri kiritildi! To'g'irlab boshidan kiriting!"
    )


@router.message(GetPersonalData.location)
async def get_location(message: Message, state: FSMContext):
    await state.update_data(contact=message.contact)

    kb = [KeyboardButton(text="Lokatsiya", request_location=True)]
    keyboard = ReplyKeyboardMarkup(keyboard=[kb], resize_keyboard=True, is_persistent=True)

    await message.answer(
        text="Lokatsiyangizni jo'nating:",
        reply_markup=keyboard
    )
    await state.set_state(GetPersonalData.record)


@router.message(GetPersonalData.record)
async def records(message: Message, state: FSMContext):
    data: Dict[str, Any]
    await state.update_data(location=message.location)
    state_data = await state.get_data()
    await state.clear()

    await create_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        name=state_data['name'],
        sec_name=state_data['sec_name'],
        age=state_data['age'],
        contact=state_data['contact'].phone_number,
        long=message.location.longitude,
        latit=message.location.latitude,
        session_maker=data["session_maker"]
    )

