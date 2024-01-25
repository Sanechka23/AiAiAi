from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


# Main menu set up

main_menu = [
    [InlineKeyboardButton(text="🎶 Загрузить аудиодорожку", callback_data="upload_audio")],

    [InlineKeyboardButton(text="Помощь", callback_data="help"),
    InlineKeyboardButton(text="Связаться", callback_data="support")]

]
main_menu = InlineKeyboardMarkup(inline_keyboard=main_menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu")]])


# Audio menu set up
audio_menu = [
    [InlineKeyboardButton(text="Разложение аудиофайла", callback_data="decomposition"), InlineKeyboardButton(text="Выделение звуковой дорожки", callback_data="selection")],
    [InlineKeyboardButton(text="Основное меню", callback_data="return_1")]
]
audio_menu = InlineKeyboardMarkup(inline_keyboard=audio_menu)
exit_audio_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в  аудио меню")]], resize_keyboard=True)
iexit_audio_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в аудио меню", callback_data="audio_menu")]])


# # Selection menu set up
# select_menu = [
#     [InlineKeyboardButton(text="🥁 Ударные", callback_data="dram"), InlineKeyboardButton(text="👨‍🎤 Вокал", callback_data="vocals")],
#     [InlineKeyboardButton(text="🔊 Басс", callback_data="bass"), InlineKeyboardButton(text="🎹 Пианино", callback_data="piano")],
#     [InlineKeyboardButton(text="Другое", callback_data="other"), InlineKeyboardButton(text="Меню выбора", callback_data="return_2")] 
# ]
# select_menu = InlineKeyboardMarkup(inline_keyboard=select_menu)
# exit_select_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню  выбора")]], resize_keyboard=True)
# iexit_select_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню выбора", callback_data="select_menu")]])