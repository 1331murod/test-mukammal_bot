from aiogram import types,executor,Bot,Dispatcher
from config import TOKEN
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
import re
from database_bot import connect_db,create_user, get_all_users






PHONE_PATTERN = re.compile ("^\+998[0-9]{9}")

class ProfileState(StatesGroup):
    name = State()
    age = State()
    phone = State()
    email = State()
    photo = State()
   # bio = State()



storage = MemoryStorage()



bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot,storage=storage)


async def on_startup(_):
    await connect_db()
    print("Bot muvofaqiyatli ishga tushirildi")



reply_button = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton(text="/create")
btn2 = KeyboardButton(text="/start")
reply_button.add(btn1,btn2)

def inline_btn() -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Ha", callback_data="ha")
    btn2 = InlineKeyboardButton(text="Yo'q", callback_data='yoq')
    btn.add(btn1, btn2)
    return btn



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
     print(message.chat.id)
     await message.answer(text=f"Assalom alekum,profil yaratish uchun /create so'zini kiriting",reply_markup=reply_button)



@dp.message_handler(commands=['create'])
async def create_command(message:types.Message):
    await message.answer(text="profil toldirish boshlandi!  ismingizni kiriting:")
    await ProfileState.name.set()



@dp.message_handler(state=ProfileState.name)
async def set_name(message:types.Message,state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text="yoshingizni kiriting:")
    await ProfileState.next()

@dp.message_handler(lambda message: not message.text.isdigit(),state=ProfileState.age)
async def not_allow_age(message: types.Message,state:FSMContext):
    await message.answer("siz kiritgan habar faqat sonlardan iborat bolishi kerak")







@dp.message_handler(state=ProfileState.age)
async def set_age(message:types.Message,state:FSMContext):
    await state.update_data(age=message.text)
    await message.answer(text="telefon raqamingizni kriting:")
    await ProfileState.next()

@dp.message_handler(lambda message:not PHONE_PATTERN.match(message.text),state=ProfileState.phone)
async def not_allow_phone(message:types.Message,state:FSMContext):
    await message.answer("siz jonatgan habar sonlardan iborat bolishi kerak")







@dp.message_handler(state=ProfileState.phone)
async def set_phone(message:types.Message, state:FSMContext):
    await state.update_data(phone = message.text)
    await message.answer(text='pochtangizni kiriting:')
    await ProfileState.next()



@dp.message_handler(state=ProfileState.email) 
async def set_email(message:types.Message,state: FSMContext):
    await state.update_data(email = message.text)
    await message.answer(text='rasm jonating:') 
    await ProfileState.next()  

@dp.message_handler(content_types=['photo'], state=ProfileState.photo)
async def set_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id) 
    data = await state.get_data()
    await bot.send_photo(chat_id=message.chat.id, photo=data['photo'], caption=f"Kiritilgan ma'lumotlar to'g'riligini tasdiqlang: \nIsmingiz: {data['name']}, Yoshingiz: {data['age']}", reply_markup=inline_btn())
    await message.delete()
    await state.reset_state(with_data=False)







@dp.callback_query_handler(lambda callback:callback.data == "ha")
async def callback_func(callback:types.CallbackQuery,state:FSMContext, message:types.Message):
    data = await state.get_data()
    data = await state.get_data()
    await bot.send_photo(chat_id= "2145973351", photo=data['photo'], caption=f"Arizachi: \nIsmingiz: {data['name']}, Yoshingiz: {data['age']}")
    await create_user(data['name'],data['age'],data['phone'],data['email'],data['photo'])
    text =""
    for user in get_all_users():
        text += f"Id:{user[0]},Ism: {user[1]},Telefon raqam:{user[3]}\n"
    await message.answer(text)
    
    await state.reset_state(with_data=False)


@dp.message_handler(content_types=['photo'],state=ProfileState.photo)
async def set_photo(message:types.Message,state:FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    data = await state.get_data()
    await bot.send_photo(chat_id=message.chat.id,photo=data['photo'],caption=f"ismingiz:{data['name']},yoshingiz:{data['age']}")



if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup)

#AgACAgIAAxkBAANHZNo-BXkLC7H5T2Zps3hhU9If5Q0AAvjLMRt1Y9hKt3Dhc2ELHbwBAAMCAAN4AAMwBA