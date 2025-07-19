from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, web_app_info, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

Edit = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Изменить ФИО", callback_data="edit_name")],
                                            #  [InlineKeyboardButton(text="Выбрать Дату", callback_data="edit_date")],
                                            [InlineKeyboardButton(text="Изменить Номер телефона", callback_data="edit_phone")],
                                            [InlineKeyboardButton(text="Написать админу", callback_data="mess_admin")],
                                            [InlineKeyboardButton(text="✅ Все верно", callback_data="good")]])

Date = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="20 июля 2025", callback_data="20.07.2025")],
                                             [InlineKeyboardButton(text="30 июля 2025", callback_data="30.07.2025")]])

admin = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Рассылка пользователей", callback_data="message")],
            [InlineKeyboardButton(text="Изменить информацию пользователей", callback_data="edit_info")]])


admin_edit = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Изменить ФИО", callback_data="admin_edit_name")],
                                            [InlineKeyboardButton(text="Изменить Номер телефона", callback_data="admin_edit_phone")],
                                            [InlineKeyboardButton(text="Изменить тип Донора", callback_data="admin_edit_type")],
                                            [InlineKeyboardButton(text="Изменить количество донорства", callback_data="admin_edit_DON")],
                                            [InlineKeyboardButton(text="Изменить последнее донорство", callback_data="admin_edit_last_don")],
                                            [InlineKeyboardButton(text="Изменить ЦК", callback_data="admin_edit_CB")],
                                            [InlineKeyboardButton(text="Изменить последней ЦК", callback_data="admin_edit_last_CB")]])



admin_message = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✉️Написать пользователю", callback_data="wr_user")],
            [InlineKeyboardButton(text="✉️Рассылка всем", callback_data="wr_all")]])


Meds = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Не уверен, Написать админу", callback_data="mess_admin")],
            [InlineKeyboardButton(text="✅ Все верно", callback_data="goods")]])




Editss = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Изменить ФИО", callback_data="edit_name")],
                                             [InlineKeyboardButton(text="Выбрать Дату", callback_data="edit_date")],
                                             [InlineKeyboardButton(text="Написать админу", callback_data="mess_admin")]])




Agree = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Согласен на обработку ПД", callback_data="agree")]])




Donor = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Студент", callback_data="student")],
                                             [InlineKeyboardButton(text="Сотрудник", callback_data="stuff")],
                                             [InlineKeyboardButton(text="Внешний донор", callback_data="different")]])



CS = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="ЦК 1", callback_data="CB1")],
                                             [InlineKeyboardButton(text="ЦК 2", callback_data="CB2")]])



Info = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="1. Требования к донорам", callback_data="Donor")],
                                            [InlineKeyboardButton(text="2. Подготовка к донации (за 2-3 дня)", callback_data="Need")],
                                            [InlineKeyboardButton(text="3. Рацион донора за 2-3 дня до донации", callback_data="Food")],
                                            [InlineKeyboardButton(text="4. Абсолютные противопоказания", callback_data="infect")],
                                            [InlineKeyboardButton(text="5. Временные противопоказания", callback_data="Vremen")],
                                            [InlineKeyboardButton(text="6. Важность донорства костного мозга", callback_data="Donor_brain")],
                                            [InlineKeyboardButton(text="7. Процедура вступления в регистр доноров костного мозга", callback_data="Postupi")],
                                            [InlineKeyboardButton(text="8. Процедура донации", callback_data="Donate")]])
