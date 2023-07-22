from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import os
import logging
from pytube import YouTube

bot = Bot(token = "5721472259:AAGls_VpeHQJfXyL71oORkzYK9S_FPnjs9w")
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    await message.answer(f"Здраствуйте {message.from_user.full_name}, напишите комманду /help что-бы узнать что может бот")

@dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.answer('Комманды бота /audio - скачать видео с ютуба в mp3 формате, /video - скачать видео с ютуба')

class DownloadAudio(StatesGroup):
    download = State()

class DownloadVideo(StatesGroup):
    download = State()

def download_audio_video(url, type):
    yt = YouTube(url)
    if type == 'audio':
        yt.streams.filter(only_audio=True).first().download('audio', f'{yt.title}.mp3')
        return f'{yt.title}.mp3'
    elif type == 'video':
        yt.streams.filter(adaptive=True, file_extension='mp4').first().download('video', f'{yt.title}.mp4')
        return f'{yt.title}.mp4'

@dp.message_handler(commands='audio')
async def audio(message: types.Message):
    await message.reply("Отправьте ссылку на видео в ютубе")
    await DownloadAudio.download.set()

@dp.message_handler(state=DownloadAudio.download)
async def down_audio(message: types.Message, state: FSMContext):
    await message.reply("Скачиваем файл ожидайте...")
    title = download_audio_video(message.text, 'audio')
    audio = open(f"audio/{title}", 'rb')
    await message.answer("Все скачалось, вот держи")
    try:
        await bot.send_audio(message.chat.id, audio)
    except:
        await message.answer("Повторите попытку")
    await state.finish()

@dp.message_handler(commands=['video'])
async def video(message: types.Message):
    await message.answer("Отправьте ссылку на видео в ютубе и я вам его скачаю")
    await DownloadVideo.download.set()

@dp.message_handler(state = DownloadVideo.download)
async def down_video(message: types.Message, state: FSMContext):
    await message.reply("Скачиваем видео файл ожидайте...") 
    title = download_audio_video(message.text, 'video')
    video = open(f"video/{title}", 'rb')
    await message.answer("Все скачалось, вот держи")
    try:
        await bot.send_video(message.chat.id, video = video)
    except:
        await message.answer("Повторите попытку")
    await state.finish()
    
# @dp.message_handler(commands=['TikTok'])
# async def tiktok(message: types.Message):
#     await message.answer("Отправьте ссылку на видео в тиктоке и я вам его скачаю")
#     await DownloadVideo.download.set()
    
executor.start_polling(dp)