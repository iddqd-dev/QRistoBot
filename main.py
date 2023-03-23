import threading
from asyncio import set_event_loop, new_event_loop
from time import sleep
from aiogram import Bot, Dispatcher, types
from web.app import app
from aiogram.utils import executor
from core.config import *
from services.compare_images import compare_file_hashes
from services.qr_generator import qr_generator_h
from services.qr_reader import qr_reader
import os

if not os.path.exists:
    os.mkdir('codes')  # Папка для хранения кукодов


@dispatcher.message_handler(commands=['start'])
async def basic_start(message: types.Message):
    if os.path.exists(f'web\static\images\\{message.from_id}'):
        print(message)
        await bot.send_message(chat_id=message.chat.id, text='Одного раза хватит :-)')
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    else:
        os.mkdir(f'codes\\{message.from_id}')
        await message.reply('Welcome!')


@dispatcher.message_handler(commands=['help'])
async def basic_help(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Напиши текст (не более 500 символов) чтобы получить QR или скинь QR чтобы его расшифровать. \nПока что принимаю только PNG и JPEG')
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dispatcher.message_handler(content_types=['document'])
async def qr_recognize_document(message: types.Message):
    print(message)
    path = os.path.join(os.path.dirname(fr'{os.getcwd()}\web\static\images\{message.from_id}\\'))
    filename = f'\\{message.document.file_unique_id}.png'
    try:
        if message.document.mime_type == 'image/png' or message.document.mime_type == 'image/jpeg':
            await message.document.download(destination_file=path + filename)
            filename = compare_file_hashes(f'{message.document.file_unique_id}.png', path)
            image = os.path.join(path, filename)
            await message.reply(qr_reader(image))
            logger.info(message.document)
        else:
            await message.reply('Only PNG or JPEG images.')
    except Exception as ex:
        logger.warning(ex)
        await bot.send_message(chat_id=message.chat.id,
                               text='Чет пошло не так. \nДавани-ка /start \nЕсли не поможет пиши @iddqd649')
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dispatcher.message_handler(content_types=['photo'])
async def qr_recognize_photo(message: types.Message):
    path = os.path.join(os.path.dirname(fr'{os.getcwd()}\web\static\images\{message.from_id}\\'))
    filename = f'\\{message.photo[1].file_unique_id}.png'
    try:
        await message.photo[-1].download(destination_file=path + filename)
        filename = compare_file_hashes(f'{message.photo[1].file_unique_id}.png', path)
        image = os.path.join(path, filename)
        await message.reply(qr_reader(image))
        logger.info(message)
    except Exception as ex:
        logger.warning(ex)
        await bot.send_message(chat_id=message.chat.id,
                               text='Чет пошло не так. \nДавани-ка /start \nЕсли не поможет пиши @iddqd649')
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dispatcher.message_handler(content_types=['text'])
async def qr_generate(message: types.Message):
    chat_id = message.chat.id
    id = message.message_id
    print(message)
    path = os.path.join(os.path.dirname(fr'{os.getcwd()}\web\static\images\{message.from_id}\\'), f'{message.message_id}.png')
    print(path)
    if len(message.text) > 500:
        await bot.send_message(chat_id=message.chat.id,
                               text='Слишком много инфы. Максимум 500 символов!')
        await bot.delete_message(chat_id=chat_id, message_id=id)
    else:
        try:
            qr_generator_h(message.text).save(path)
            img = types.InputFile(path_or_bytesio=path)
            await bot.send_photo(chat_id=chat_id, photo=img, caption=message.text)
            await bot.delete_message(chat_id=chat_id, message_id=id)
            logger.info(message)
        except Exception as ex:
            logger.warning(ex)
            await bot.send_message(chat_id=message.chat.id,
                                   text='Чет пошло не так. \nДавани-ка /start \nЕсли не поможет пиши @iddqd649')
            await bot.delete_message(chat_id=chat_id, message_id=id)


def app_run():
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as ex:
        print(ex)


def bot_polling():
    try:
        set_event_loop(new_event_loop())
        executor.start_polling(dispatcher, skip_updates=True)
    except Exception as ex:
        print(ex)


bot_thread = threading.Thread(target=bot_polling)
bot_thread.daemon = True
bot_thread.start()

app_thread = threading.Thread(target=app_run)
app_thread.daemon = True
app_thread.start()

if __name__ == "__main__":
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            break
