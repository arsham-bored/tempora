from telethon import TelegramClient
from telethon.sync import events
import socks
import handlers
import utils

import memory
from memory import (
    captcha
)

api_id = 719906
api_hash = "5bde80cc5d05e175ee24462a729802dc"
# 1101709847:AAFwjL2-BIYxhFublsn1b_-VvhIJO9rcW3Y
bot_token = "1207287485:AAHhOWVNJifSaBwm8AEKcFwPqNgFqoDyFH4"

# 
bot = TelegramClient('bot', api_id, api_hash, proxy=(socks.SOCKS5, '127.0.0.1', 9050)).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='(?i)/start'))
async def handle_message(event):
    captcha.bot_memory.add(event)
    utils.remove_all_memories(event)
    await handlers.bot_started(bot, event)
    await handlers.search_on_database(bot, event)


@bot.on(events.NewMessage(pattern='(?i)شماره من👤'))
async def search_phone_number(event):
    utils.remove_all_memories(event)
    await handlers.search_on_database(bot, event)


@bot.on(events.NewMessage(pattern='من ربات نیستم 😊'))
async def user_validated(event):
    utils.remove_all_memories(event)
    captcha.bot_memory.remove(event)
    await utils.back_to_service(bot, event)
    await handlers.search_on_database(bot, event)


@bot.on(events.NewMessage(pattern='(?i)افزودن شماره ➕'))
async def add_new_number(event):
    utils.remove_all_memories(event)
    await handlers.add_phone_number_database(bot, event)


@bot.on(events.NewMessage(pattern='(?i)مزاحم یاب ☎️'))
async def find_person(event):
    utils.remove_all_memories(event)
    memory.annoy.annoy_memory.add(event)
    await utils.ask_to_share_phone(bot, event)


@bot.on(events.NewMessage(pattern='(?i)بازگشت'))
async def search_phone_number(event):
    utils.remove_all_memories(event)
    await utils.cancel_action(bot, event)


@bot.on(events.NewMessage(pattern='(?i)ارتباط با ما 📩'))
async def in_development(event):
    await event.reply("""
ارتباط با ما 📬

➡️ Contact us: @in_pod
    """)

@bot.on(events.NewMessage(pattern='(?i)ساخت ربات مشابه 🤖'))
async def in_development(event):
    await utils.create_copy(bot, event)

@bot.on(events.NewMessage(pattern='(?i)سوالات متداول ❓'))
async def in_development(event):
    await utils.question_handler(bot, event)

@bot.on(events.NewMessage(
    pattern="(?!(/start|شماره من👤|بازگشت|ارتباط با ما 📩|ساخت ربات مشابه 🤖|سوالات متداول ❓|مزاحم یاب ☎️|من ربات نیستم 😊|افزودن شماره ➕))"))
async def action_keeper(event):
    await handlers.action_handler(bot, event)

@bot.on(events.CallbackQuery)
async def callback_handler(event):
    case = event.original_update.data
    
    for question_key in utils.questions:
        if case == b'android':
            await utils.send_image(bot, event)
            return

        if case == bytes(question_key, 'ascii'):
            answer = utils.questions[question_key]
            await event.reply(answer)

print("bot is running..")
bot.run_until_disconnected()
