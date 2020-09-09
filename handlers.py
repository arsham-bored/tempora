import utils
from helpers.dataLeak import (
    search_id,
    send_to_database
)
from memory.annoy import annoy_memory
from memory.contact import contact_memory
from memory.captcha import bot_memory
from datetime import datetime

async def bot_started(bot, event):
    await utils.welcome_message(bot, event)


@utils.bot_protect
async def search_on_database(bot, event):
    await utils.searching(bot, event)

    try:

        start = datetime.now()
        result = search_id(event.from_id)
        end = datetime.now()

        total = end - start
        total = f"{total.total_seconds():.3f}"

        if result is None:
            await utils.reply_user_not_exists(bot, event)

        else:
            await utils.reply_user_exists(bot, event, result, total)
            bot_memory.clear(event)


    except:
        await utils.invalid_message(bot, event)



@utils.bot_protect
async def add_phone_number_database(bot, event):
    contact_memory.add(event)
    await utils.ask_to_share_contacts(bot, event)


@utils.bot_protect
async def add_contact_to_database(bot, event):
    try:
        userid, phone, username = await utils.get_data_from_media(bot, event)

        username = "" if username is None else username
        phone = str(phone).split("+")[-1]

        await event.reply("در حال بارگذاری...⏳")

        already_exists = send_to_database(userid, phone, username)

        if already_exists:
            await utils.contact_already_been(bot, event)

        else:
            await utils.contact_added(bot, event)

    except:
        await utils.invalid_contact(bot, event)


@utils.bot_protect
async def action_handler(bot, event):
    in_contact_action = contact_memory.check(event)
    in_annoy_detection_action = annoy_memory.check(event)

    try:
        if in_contact_action:
            await add_contact_to_database(bot, event)

        elif in_annoy_detection_action:
            await utils.get_info_from_phone(bot, event)

        else:
            await utils.send_username_result(bot, event)

    except Exception as error:
        print(error)
        bot_memory.record(event)
        await utils.invalid_message(bot, event)
