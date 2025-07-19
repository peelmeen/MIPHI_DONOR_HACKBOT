#import sys
#from pathlib import Path
#sys.path.append(str(Path(__file__).parent.parent))
import asyncio
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.types import Message, FSInputFile, CallbackQuery
from src.config import config
from src.DB import *
from src.BOT import *
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logging
import aiofiles
from aiogram.methods import DeleteWebhook
from mistralai import Mistral

Admins = [config.Admin]

class Form(StatesGroup):
    waiting_for_message = State()

class Form1(StatesGroup):
    waiting_for_mess = State()


logging.basicConfig(level=logging.INFO)

photo0="Donor.jpeg"


router = Router()
bot = Bot(config.Bot_Tocken.get_secret_value())
Api_Key=config.API_KEY.get_secret_value()
dp = Dispatcher()
model = "mistral-small-latest"
client = Mistral(api_key=Api_Key)
dp.include_router(router)


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer_photo(photo=FSInputFile(photo0), caption='''🚀 Привет! Я Автоматизированный ИИ бот для взаимодействия с донорами в ВУЗе! Здесь ты можешь узнать все про донорское движение и задавать вопросы.    
                                   
Для продолжения подтвержи свое согласие на обработку своих персональных данных ниже👇''', reply_markup=Agree) # /check 📌 Отправь мне свое ФИО, медицинские отводы если есть в произвольном формате.
    telegram_id = message.from_user.id
    await add_user(telegram_id)








@dp.callback_query(F.data == "agree")
async def edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    telegram_id = callback.from_user.id
    # await callback.message.answer(f"{telegram_id}")
    await callback.message.answer("Вы дали согласие на обработку персональных данных")
    await edit_agree(telegram_id)

    # info = await get_contact(telegram_id)
    # await callback.message.answer(f"{info}")
    # if info == '-' or info == '':
    await callback.message.answer("Введите ваше ФИО и номер телефона(в формате: 71234567890, без +, строго 11 цифр) в произвольном формате")
    await state.update_data(last_command="start")
    await state.set_state(Form.waiting_for_message)





@dp.message(Form.waiting_for_message)
async def cmd_start(message: Message, state: FSMContext):
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "system",
                "content": "Твоя задача достать из сообщения ФИО, Номер телефона(без + просто 11 цифр). Вывести информация в формате: ФИО:\n Номер телефона:\n",
            },
            {
                "role": "user",
                "content": message.text,
            },
        ]
    )

    # если медицинских отводов нет, то в БД пойдет - 0, иначе 1

    telegram_id = message.from_user.id
    FNS = chat_response.choices[0].message.content.split('\n')[0].split(':')[1]
    Phone_num = chat_response.choices[0].message.content.split('\n')[1].split(':')[1]
    
    await message.answer(f"Номер телефона: {Phone_num}\nФИО: {FNS}", reply_markup=Edit)
    await edit_two_fields(Phone_num, FNS, telegram_id)

    await state.clear()










@dp.callback_query(F.data == "edit_name")
async def edit(callback: CallbackQuery, state: FSMContext):
    await state.update_data(last_command="edit_name")
    await callback.message.answer("Введите корректные данные ФИО")
    await state.set_state(Form1.waiting_for_mess)


@dp.callback_query(F.data == "edit_phone")
async def edit(callback: CallbackQuery, state: FSMContext):
    await state.update_data(last_command="edit_phone")
    await callback.message.answer("Введите корректные данные Номера телефона")
    await state.set_state(Form1.waiting_for_mess)




@dp.callback_query(F.data == "good")
async def edit(callback: CallbackQuery):
    await callback.message.answer("Отлично, все данные сохранены, выберите удобную для вас дату ниже👇\n\n(P.S. если вы ввели неверные данные или сомневаетесь - можете поменять данные командой /edit, а так же написать админу - /help)", reply_markup=Date)



@dp.callback_query(F.data == "20.07.2025")
async def edit(callback: CallbackQuery):
    date = callback.data
    telegram_id = callback.from_user.id

    if await get_date(telegram_id) != date:
        edit_last_blood_center(await get_date(telegram_id), telegram_id)

    telegram_id = callback.from_user.id
    await callback.message.answer("Отлично, данные сохранены!\n\nВы выбрали 20.07.2025 в качестве даты", reply_markup=CS)
    date = "20.07.2025"
    await edit_Date(date, telegram_id)



@dp.callback_query(F.data == "30.07.2025")
async def edit(callback: CallbackQuery):
    date = callback.data
    telegram_id = callback.from_user.id

    if await get_date(telegram_id) != date:
        edit_last_blood_center(await get_date(telegram_id), telegram_id)

    await callback.message.answer("Отлично, данные сохранены!\n\nВы выбрали 30.07.2025 в качестве даты", reply_markup=CS)
    date = "30.07.2025"
    await edit_Date(date, telegram_id)






@dp.callback_query(F.data == "CB1")
async def edit(callback: CallbackQuery):
    CB = callback.data
    telegram_id = callback.from_user.id

    if await get_CB(telegram_id) != CB:
        edit_last_blood_center(await get_CB(telegram_id), telegram_id)

    await callback.message.answer("Отлично, данные сохранены!\n\nВы выбрали ЦК 1 в качестве Центра Крови, выберите какой вы тип донора", reply_markup=Donor)
    CB = "CB1"
    await edit_blood_center(CB, telegram_id)



@dp.callback_query(F.data == "CB2")
async def edit(callback: CallbackQuery):
    CB = callback.data
    telegram_id = callback.from_user.id

    if await get_CB(telegram_id) != CB:
        edit_last_blood_center(await get_CB(telegram_id), telegram_id)
        
    await callback.message.answer("Отлично, данные сохранены!\n\nВы выбрали ЦК 2 в качестве Центра Крови, выберите какой вы тип донора", reply_markup=Donor)
    CB = "CB2"
    await edit_blood_center(CB, telegram_id)




















@dp.callback_query(F.data == "mess_admin")
async def edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Вы выбрали опцию написать админу, напишите ниже ваше сообщение")
    await state.update_data(last_command="mess_admin")
    await state.set_state(Form1.waiting_for_mess)




@dp.callback_query(F.data == "edit_date")
async def edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите дату", reply_markup=Date)




@dp.message(Command("admin_panel"))
async def edit(message: Message):
    if message.from_user.id in Admins:
        await message.answer("Admin панель, выберите что хотите сделать", reply_markup=admin)
    else:
        await message.answer("Вы не админ:(")
        return



@dp.callback_query(F.data == "message")
async def edit(callback: CallbackQuery):
    if callback.from_user.id in Admins:
        await callback.message.answer("Admin панель, выберите какую рассылку хотите сделать", reply_markup=admin_message)
    else:
        await callback.message.answer("Вы не админ:(")
        return



@dp.callback_query(F.data == "edit_info")
async def edit(callback: CallbackQuery):
    if callback.message.from_user.id in Admins:
        await callback.message.answer("Admin панель, выберите какую информацию хотите поменять пользователю", reply_markup=admin_edit)
    else:
        await callback.message.answer("Вы не админ:(")
        return










@dp.callback_query(F.data == "admin_edit_name")
async def edit(callback: CallbackQuery, state: FSMContext):
    if callback.message.from_user.id in Admins:
        await callback.message.answer("Admin, напишите какому пользователю хотите поменять данные в формате: 215346356(telegramid), значение занасимое в таблицу", reply_markup=admin_edit)
        await state.update_data(last_command="admin_edit_name")
        await state.set_state(Form1.waiting_for_mess)
    else:
        await callback.message.answer("Вы не админ:(")
        return
    

@dp.callback_query(F.data == "admin_edit_phone")
async def edit(callback: CallbackQuery, state: FSMContext):
    if callback.message.from_user.id in Admins:
        await callback.message.answer("Admin, напишите какому пользователю хотите поменять данные в формате: 215346356(telegramid), значение занасимое в таблицу", reply_markup=admin_edit)
        await state.update_data(last_command="admin_edit_phone")
        await state.set_state(Form1.waiting_for_mess)
    else:
        await callback.message.answer("Вы не админ:(")
        return

@dp.callback_query(F.data == "admin_edit_type")
async def edit(callback: CallbackQuery, state: FSMContext):
    if callback.message.from_user.id in Admins:
        await callback.message.answer("Admin, напишите какому пользователю хотите поменять данные в формате: 215346356(telegramid), значение занасимое в таблицу", reply_markup=admin_edit)
        await state.update_data(last_command="admin_edit_type")
        await state.set_state(Form1.waiting_for_mess)
    else:
        await callback.message.answer("Вы не админ:(")
        return

    
@dp.callback_query(F.data == "admin_edit_DON")
async def edit(callback: CallbackQuery, state: FSMContext):
    if callback.message.from_user.id in Admins:
        await callback.message.answer("Admin, напишите какому пользователю хотите поменять данные в формате: 215346356(telegramid), значение занасимое в таблицу", reply_markup=admin_edit)
        await state.update_data(last_command="admin_edit_DON")
        await state.set_state(Form1.waiting_for_mess)
    else:
        await callback.message.answer("Вы не админ:(")
        return
    

@dp.callback_query(F.data == "admin_edit_last_don")
async def edit(callback: CallbackQuery, state: FSMContext):
    if callback.message.from_user.id in Admins:
        await callback.message.answer("Admin, напишите какому пользователю хотите поменять данные в формате: 215346356(telegramid)| значение занасимое в таблицу", reply_markup=admin_edit)
        await state.update_data(last_command="admin_edit_last_don")
        await state.set_state(Form1.waiting_for_mess)
    else:
        await callback.message.answer("Вы не админ:(")
        return
    
@dp.callback_query(F.data == "admin_edit_CB")
async def edit(callback: CallbackQuery, state: FSMContext):
    if callback.message.from_user.id in Admins:
        await callback.message.answer("Admin, напишите какому пользователю хотите поменять данные в формате: 215346356(telegramid), значение занасимое в таблицу", reply_markup=admin_edit)
        await state.update_data(last_command="admin_edit_CB")
        await state.set_state(Form1.waiting_for_mess)    
    else:
        await callback.message.answer("Вы не админ:(")
        return
    

@dp.callback_query(F.data == "admin_edit_last_CB")
async def edit(callback: CallbackQuery, state: FSMContext):
    if callback.message.from_user.id in Admins:
        await callback.message.answer("Admin, напишите какому пользователю хотите поменять данные в формате: 215346356(telegramid), значение занасимое в таблицу", reply_markup=admin_edit)
        await state.update_data(last_command="admin_edit_last_CB")
        await state.set_state(Form1.waiting_for_mess)    
    else:
        await callback.message.answer("Вы не админ:(")
        return





























@dp.callback_query(F.data == "student")
async def edit(callback: CallbackQuery, state: FSMContext):
    
    await callback.message.answer("Отлично вы выбрали тип донора - Студент, введите название вашей группы")
    await state.update_data(last_command="edit_group")
    await state.set_state(Form1.waiting_for_mess)



@dp.callback_query(F.data == "stuff")
async def edit(callback: CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id

    await callback.message.answer("Отлично вы выбрали тип донора - Сотрудник, введите название вашей группы")
    await edit_type_stuff(telegram_id)



@dp.callback_query(F.data == "different")
async def edit(callback: CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id

    await callback.message.answer("Отлично вы выбрали тип донора - Внешний донор, введите название вашей группы")
    await edit_type_different(telegram_id)



















@dp.callback_query(F.data == "wr_user")
async def edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите Telegram id пользователя, которому пишем\n\nВ формате: 111111111, сообщение пользователю")
    await state.update_data(last_command="get_id")
    await state.set_state(Form1.waiting_for_mess)





@dp.callback_query(F.data == "wr_all")
async def edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите сообщение для всех пользователей")
    await state.update_data(last_command="wr_all")
    await state.set_state(Form1.waiting_for_mess)




@dp.callback_query(F.data == "student")
async def student(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название вашей группы")
    await state.update_data(last_command="edit_group")
    await state.set_state(Form1.waiting_for_mess)





@dp.message(Command("help"))
async def edit(message: Message, state: FSMContext):
    # await message.answer(f"{await get_agree(message.from_user.id)}")
    if await get_agree(message.from_user.id) != 1:
        await message.answer("Сначала нужно согласиться на обработку данных!")
        return

    await message.answer("Вы выбрали опцию написать админу, напишите ниже ваше сообщение")
    await state.update_data(last_command="mess_admin")
    await state.set_state(Form1.waiting_for_mess)




@dp.message(Command("edit"))
async def edit(message: Message, state: FSMContext):
    if await get_agree(message.from_user.id) != 1:
        await message.answer("Сначала нужно согласиться на обработку данных!")
        return

    telegram_id = message.from_user.id
    info = await get_data(telegram_id)
    await message.answer(f"Вы выбрали опцию изменить информацию\n\nФИО:{info[0]}\nТелефон: {info[1]}\nДата: {info[2]}\nЦентр Крови: {info[3]}\n\nвыберите ниже что хотите изменить👇", reply_markup=Editss)





@dp.message(Form1.waiting_for_mess)#(Form1.waiting_for_mess, F.text, F.photo)
async def handle_user_media(message: Message, state: FSMContext): # , state: FSMContext
    req = message.text
    telegram_id = message.from_user.id

    state_data = await state.get_data()
    last_command = state_data.get('last_command')

    if last_command == "mess_admin":
    
        group=-1002762829858# id вашей группы

        info = await get_data(telegram_id)

        await bot.send_message(group, f"ФИО:{info[0]}\nТелефон: {info[1]}\nДата: {info[2]}\n\n{req}")

        await message.answer("✅ Ваш ответ получен! Админ ответит вам скоро.")


    elif last_command == "edit_name":
        await edit_FNS(req, telegram_id)
        await message.answer(f"Имя успешно изменено на {req}")



    elif last_command == "wr_all":
        users = await get_users()

        for id in users:
            await bot.send_message(chat_id=id, text=req)
            # await message.answer(f"{id}")
    

    elif last_command == "get_id":
        user = req.split("|")[0]
        mess = req.split("|")[1]
        await bot.send_message(user, mess)


    elif last_command == "edit_phone":
        await edit_phone(req, telegram_id)
        if edit_phone:
            await message.answer(f"Номер телефона успешно изменен на {req}")
        else:
            await message.answer(f"Повторите попытку позднее")


    elif last_command == "edit_group":
        await edit_group(req, telegram_id)
        if edit_phone:
            await message.answer(f"Название группы успешно изменено на {req}")
        else:
            await message.answer(f"Повторите попытку позднее")


    elif last_command == "admin_edit_name":
        telegram_id = req.strip(',')[0]
        data = req.strip(',')[1]
        await edit_FNS(data, telegram_id)


    elif last_command == "admin_edit_phone":
        telegram_id = req.strip(',')[0]
        data = req.strip(',')[1]
        await edit_phone(data, telegram_id)


    elif last_command == "admin_edit_type":
        telegram_id = req.strip(',')[0]
        data = req.strip(',')[1]
        await edit_group(data, telegram_id)

    # elif last_command == "admin_edit_DON":
    #     telegram_id = req.strip(',')[0]
    #     data = req.strip(',')[1]
    #     await edit_don(data, telegram_id)

    elif last_command == "admin_edit_last_don":
        telegram_id = req.strip(',')[0]
        data = req.strip(',')[1]
        await edit_last_don(data, telegram_id)


    elif last_command == "admin_edit_CB":
        telegram_id = req.strip(',')[0]
        data = req.strip(',')[1]
        await edit_blood_center(data, telegram_id)


    elif last_command == "admin_edit_last_CB":
        telegram_id = req.strip(',')[0]
        data = req.strip(',')[1]
        await edit_last_blood_center(data, telegram_id)


    await state.clear()








@dp.message(Command('myinfo'))
async def send_my_info(message: types.Message):
    if await get_agree(message.from_user.id) != 1:
        await message.answer("Сначала нужно согласиться на обработку данных!")
        return

    # telegram_id = message.from_user.id
    # info = await get_data(telegram_id)
    # await message.answer(f"{info}")#ФИО:{info[0]}\nДата: {info[1]}", reply_markup=Editss)

    telegram_id = message.from_user.id
    info = await get_data(telegram_id)
    await message.answer(f"ФИО:{info[0]}\nТелефон: {info[1]}\nДата: {info[2]}\nЦентр Крови: {info[3]}\n\nвыберите ниже что хотите изменить👇", reply_markup=Editss)





@dp.message(Command('info'))
async def send_my_info(message: types.Message):
    if await get_agree(message.from_user.id) != 1:
        await message.answer("Сначала нужно согласиться на обработку данных!")
        return

    # telegram_id = message.from_user.id
    # info = await get_data(telegram_id)
    # await message.answer(f"{info}")#ФИО:{info[0]}\nДата: {info[1]}", reply_markup=Editss)


    await message.answer(f"Выберите ниже информацию, которая вас интересует", reply_markup=Info)








@dp.callback_query(F.data == 'Need')
async def info1(callback: CallbackQuery):    
    file = "src/Need.txt"

    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        content = await f.read()


    await callback.message.answer(f"{content}")









@dp.callback_query(F.data == 'Donor')
async def info1(callback: CallbackQuery):    
    file = "src/Donor.txt"

    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        content = await f.read()


    await callback.message.answer(f"{content}")



@dp.callback_query(F.data == 'Donor')
async def info1(callback: CallbackQuery):    
    file = "src/Donor.txt"

    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        content = await f.read()


    await callback.message.answer(f"{content}")





@dp.callback_query(F.data == 'Food')
async def info1(callback: CallbackQuery):    
    file = "src/Food.txt"

    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        content = await f.read()


    await callback.message.answer(f"{content}")




@dp.callback_query(F.data == 'Infect')
async def info1(callback: CallbackQuery):    
    file = "src/Infect.txt"

    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        content = await f.read()


    await callback.message.answer(f"{content}")





@dp.callback_query(F.data == 'Vremen')
async def info1(callback: CallbackQuery):    
    file = "src/Vremen.txt"

    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        content = await f.read()


    await callback.message.answer(f"{content}")




@dp.callback_query(F.data == 'Donor_brain')
async def info1(callback: CallbackQuery):    
    file = "src/Donor_brain.txt"

    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        content = await f.read()


    await callback.message.answer(f"{content}")






@dp.callback_query(F.data == 'Donor_brain')
async def info1(callback: CallbackQuery):    
    file = "src/Donor_brain.txt"

    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        content = await f.read()


    await callback.message.answer(f"{content}")









@dp.callback_query(F.data == 'Postupi')
async def info1(callback: CallbackQuery):    
    file = "src/Postupi.txt"

    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        content = await f.read()


    await callback.message.answer(f"{content}")





@dp.callback_query(F.data == 'Donate')
async def info1(callback: CallbackQuery):    
    file = "src/Donate.txt"

    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        content = await f.read()

    file1 = "src/Donate1.txt"

    async with aiofiles.open(file1, 'r', encoding='utf-8') as f:
        content1 = await f.read()

    await callback.message.answer(f"{content}")
    await callback.message.answer(f"{content1}")










async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    
    webhook_info = await bot.get_webhook_info()
    print(f"Webhook status: {webhook_info.url or 'NOT ACTIVE'}")
    
    await dp.start_polling(bot)





#____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
if __name__ == "__main__":
    # asyncio.run(dp.start_polling(bot))
    asyncio.run(main())
