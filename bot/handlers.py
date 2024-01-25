from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile
import requests
import os
import csv
import datetime
import pandas as pd
import threading

from bot import kb
from bot import text
from bot.config import BOT_TOKEN
from models.zero_shot.zero_shot import run_zero_shot
from models.combined_model.combined_model import run_combined_model

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    '''
    Message '/start' -> main menu 
    '''
    with open('data.csv', 'a', newline="", encoding='UTF-8') as fil:
        wr = csv.writer(fil, delimiter=',')
        wr.writerow([msg.chat.id, msg.text])
    print([msg.chat.id, msg.text])
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.main_menu)
@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def main_menu(msg: Message):
    await msg.answer(text.main_menu, reply_markup=kb.main_menu)


@router.callback_query(F.data == 'upload_audio')
async def audio_menu(callback: types.CallbackQuery):
    '''
    After pushing '🎶 Загрузить аудиодорожку' button raises audio menu
    '''
    await callback.message.answer(text.audio_menu, reply_markup=kb.audio_menu)
    await callback.answer()

@router.callback_query(F.data == "help")
async def help_button(callback: types.CallbackQuery):
    await callback.message.answer("Данный бот позволяет разложить песню на составляющие или выделить нужный тебе инструмент")
    await callback.answer()

@router.callback_query(F.data == 'support')
async def support_button(callback: types.CallbackQuery):
    await callback.message.answer(" Связаться с создателей:\
                                   \n @sasha_doroshkevich") 
    await callback.answer()

@router.callback_query(F.data ==  "return_1")
async def audio_to_main(callback: types.CallbackQuery):
    await callback.message.answer(text.main_menu, reply_markup=kb.main_menu)
    await callback.answer()

@router.callback_query(F.data ==  "selection")
async def audio_to_select(callback: types.CallbackQuery):
    await callback.message.answer(text=text.select_menu)
    await callback.message.answer('Отправьте первый файл')
    global nn_model
    nn_model = 2 # тип используемой нейронки
    global first_file
    first_file = True # "трюк" для того, чтобы по-разному отвечать в дальнейшем на первый и второй файл
    await callback.answer()


# @router.callback_query(F.data ==  "return_2")
# async def select_to_audio(callback: types.CallbackQuery):
#     await callback.message.answer(text.audio_menu, reply_markup=kb.audio_menu)
#     await callback.answer()

@router.callback_query(F.data == "decomposition")
async def audio_decomp(callback: types.CallbackQuery):
    await callback.message.answer("Можешь прислать в чат песню, которую хотел бы разложить")
    global nn_model
    nn_model = 1  # тип используемой нейронки
    await callback.answer()

URI_INFO = f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id='
URI = f'https://api.telegram.org/file/bot{BOT_TOKEN}/'

@router.message(F.audio)
async def doc_handler(message: types.Message):
  if threading.active_count()>1:
    print('гг')
  else:
    global first_file
    if not os.path.exists('input_files'):
        os.mkdir('input_files')

    if not os.path.exists('predict_outputs'):
        os.mkdir('predict_outputs')

    file_id=message.audio.file_id
    response = requests.get(URI_INFO + file_id)
    file_path = response.json()['result']['file_path']
    audio = requests.get(URI + file_path)

    if nn_model == 2:
        if first_file:
            with open('input_files/mix.mp3', 'wb') as f:
                f.write(audio.content)
            first_file = False
            await message.answer('Отправьте второй файл')

        else:
            with open('data.csv', 'a', newline="", encoding='UTF-8') as fil:
              wr = csv.writer(fil, delimiter=',')
              rer = 'Выделение'
              wr.writerow([message.chat.id, rer])
              print([message.chat.id, rer])
            with open('input_files/query.mp3', 'wb') as f:
                f.write(audio.content)
            first_file = True
            await message.answer('Идет процесс обработки. Может занять продолжительное время')

            out_path = run_zero_shot('input_files/mix.mp3', 'input_files/query.mp3')
            audio = FSInputFile(out_path)
            await message.answer_audio(audio=audio) 
            os.remove('input_files/mix.mp3')
            os.remove('input_files/query.mp3')
            os.remove(out_path)
    
    elif nn_model == 1:
        with open('data.csv', 'a', newline="", encoding='UTF-8') as fil:
          wr = csv.writer(fil, delimiter=',')
          rek = 'Разделение'
          wr.writerow([message.chat.id, rek])
          print([message.chat.id, rek])
        with open('input_files/mix.mp3', 'wb') as f:
            f.write(audio.content)
        run_combined_model('input_files/mix.mp3')

        audio = FSInputFile('predict_outputs/drums.mp3')
        await message.answer_audio(audio=audio)
        audio = FSInputFile('predict_outputs/vocals.mp3')
        await message.answer_audio(audio=audio)  
        audio = FSInputFile('predict_outputs/bass.mp3')
        await message.answer_audio(audio=audio) 
        audio = FSInputFile('predict_outputs/other.mp3')
        await message.answer_audio(audio=audio) 

        os.remove('input_files/mix.mp3')
        os.remove('predict_outputs/drums.mp3')
        os.remove('predict_outputs/vocals.mp3')
        os.remove('predict_outputs/bass.mp3')
        os.remove('predict_outputs/other.mp3')
        


        
        



