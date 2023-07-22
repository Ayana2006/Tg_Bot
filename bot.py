# from aiogram import Bot, Dispatcher, executor, types 
 
# from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# bot = Bot(token = "5721472259:AAGls_VpeHQJfXyL71oORkzYK9S_FPnjs9w") 
# dp = Dispatcher(bot)

# button_hi = KeyboardButton('Привет! 👋')

# greet_kb = ReplyKeyboardMarkup()
# greet_kb.add(button_hi)

# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.reply("Привет!", reply_markup=greet_kb)

# @dp.message_handler(commands = ['help'])
# async def help(message: types.Message):
#     await message.reply("Наши команды: /start")

# @dp.message_handler(text = 'Привет')
# async def hello(message: types.Message):
#     await message.reply_sticker('https://img5.lalafo.com/i/posters/original_webp/2e/14/1d/083e3518c12c2d14b5cd81f353.webp')

# @dp.message_handler(text = 'Аудио')
# async def hello(message: types.Message):
#     await message.reply_audio('https://cdn8.sefon.pro/prev/LjUUhoeWcV0c1u4IHzICgg/1666135639/73/The%20Weeknd%20-%20Call%20Out%20My%20Name%20%28192kbps%29.mp3')

# @dp.message_handler(text = 'Локация')
# async def hello(message: types.Message):
#     await message.reply_location(40.538822, 72.8018676)
    
# executor.start_polling(dp)


from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import os
import logging
from pytube import YouTube
bot =  Bot(token = "5721472259:AAGls_VpeHQJfXyL71oORkzYK9S_FPnjs9w")
dp = Dispatcher(bot, storage=MemoryStorage)
logging.basicConfig(level = logging.INFO)
storage = MemoryStorage()

@dp.message_handler(commands = 'start') 
async def start(message: types.Message): 
    await message.answer(f"Здраствуйте {message.from_user.full_name}, напишите комманду /help что-бы узнать что может бот") 
 
@dp.message_handler(commands='help') 
async def help(message: types.Message): 
    await message.answer('Комманды бота /audio - скачать видео с ютуба в mp3 формате, /video - скачать видео с ютуба') 
 
class DownloadAudio(StatesGroup): 
    download = State() 
 
def download_audio(url, type = 'audio'): 
    yt = YouTube(url) 
    if type == 'audio': 
        yt.streams.filter(only_audio=True).first().download('audio', f'{yt.title}.mp3') 
        return f'{yt.title}.mp3' 
 
@dp.message_handler(commands='audio') 
async def audio(message: types.Message): 
    await message.reply("Отправьте ссылку на видео в ютубе") 
    await DownloadAudio.download.set() 
 
@dp.message_handler(state=DownloadAudio.download) 
async def down_audio(message: types.Message, state: FSMContext): 
    await message.reply("Скачиваем файл ожидайте...") 
    title = download_audio(message.text) 
    audio = open(f"audio/{title}", 'rb') 
    await message.answer("Все скачалось, вот держи") 
    try: 
        await bot.send_audio(message.chat.id, audio) 
    except: 
        await message.answer("Повторите попытку") 
    await state.finish() 
 
executor.start_polling(dp)