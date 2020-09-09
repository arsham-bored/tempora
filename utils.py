from telethon import Button
from datetime import datetime
from helpers.dataLeak import (
    search_id,
    search_username,
    get_data_from_phone
)
import logging
import memory
from memory import (
    captcha
)

from emoji import UNICODE_EMOJI

logging.basicConfig(level=logging.INFO)

channel_invite = [
    Button.url("عضویت در کانال", "https://t.me/Badhunters")
]

captcha_ask = [
    Button.text("من ربات نیستم 😊", resize=True, single_use=True)
]

general_options = [
    [
        Button.text('شماره من👤', resize=False, single_use=True),
        Button.text('افزودن شماره ➕', resize=False, single_use=True),
        Button.text('مزاحم یاب ☎️', resize=False, single_use=True),
    ],
    [
        Button.text('ارتباط با ما 📩', resize=False, single_use=True),
        Button.text('ساخت ربات مشابه 🤖', resize=True, single_use=True),
        Button.text('سوالات متداول ❓', resize=True, single_use=True),
    ],
]

use_bot = """
🔹 برای جستجو می‌توانید نام کاربری، شناسه تلگرام (آیدی عددی‌) و یا پیغام فوروارد شده از سوی کاربر مورد نظرتان را در صورتی که فوروارد آن کاربر بسته (مخفی) نشده باشد برای ربات ارسال کنید. با توجه به این که بسیاری از مخاطبین آیدی یوزرنیم خود را عوض می‌کنند یا اصلا یوزرنیم ندارند برای قطعیت حتما از شناسه عددی استفاده کنید. همچنين میتوانید پیامی از کاربر مورد نظرتان را به ربات فوروارد کنید، در صورتی که فوروارد کاربر مورد نظر بسته نباشد ربات روند سرچ و نتیجه آن را اعلام می‌کند. برای به دست آوردن شناسه عددی یک اکانت در سوالات متداول روش های مختلفی ذکر شده است که می‌توانید از آنها استفاده‌ کنید. 


🔹در بخش مزاحم یاب کافیست شماره مورد نظرتان را (بدون صفر یا با صفر فرقی نمی‌کند) ارسال کنید تا اطلاعات آن شماره برای شما ارسال شود. از جمله اطلاعات دریافتی از سوی ربات شامل اسم و فامیل،محل سکونت، کد پستی و... می‌شود. همچنین می‌توانید از طریق تلگرام با ارسال آیدی کاربری ، شناسه عددی و یا پیغام فورواردی در صورت بسته (مخفی) نبودن فوروارد آن شخص شماره به همراه‌ اطلاعات موجود شماره آن اکانت تلگرامی را به دست آورید.
"""

what_is_userid = """
🔹 آیدی عددی تلگرام که برای هر کاربر ثابت است. ترفند های به دست آوردن شناسه عددی در بخش سوالات متداول قرار دارد.
"""

what_is_username = """
🔹 آیدی، یوزرنیم یا همان نام کاربری که با @ شروع می‌شود.
"""

android_text = """
    1- برنامه تلگرام پلاس را نصب کنید.
2- مانند عکس به صفحه پروفایل مخاطب مورد نظر بروید.
3- عدد مشخص شده در تصویر شناسه عددی کاربر است / آن را در ربات وارد کنید.

لینک نصب از پلی استور 👇

https://play.google.com/store/apps/details?id=org.telegram.plus
"""

ios_text = """
🔹 برای به دست آوردن آیدی عددی در پلتفرم IOS کافیست اکانت مورد نظرتان را در تلگرام به کانتکت (مخاطبین) خود اضافه کرده و یک نام دلخواه برای او نیز انتخاب کنید بعد از پایان کار به مخاطبین تلفن خود بروید و با سرچ نام انتخابی در هنگام اضافه کردن به مخاطبین تلگرام آن را پیدا کرده و با کلیک بر روی آن میتوانید شناسه عددی اکانت را مشاهده کنید و اعداد را به بات ارسال و نتیجه را دریافت کنید.
"""

questions = {
    'bot': use_bot,
    'android': android_text,
    'ios': ios_text,
    'username': what_is_username,
    'userid': what_is_userid,
    'broken': "🔹ربات حاوی 42 میلیون شماره به همراه اطلاعات اکانت میباشد / ربات فقط در صورتی می‌تواند شماره را ارسال کند که شماره هدف مد نظر شما جزو این لیست بلند بالا باشد",
    'get_userid': """
    🔹 از طریق ربات های زیر میتوانید با ارسال یوزرنیم یا همان آیدی شناسه عددی صاحب آیدی را دریافت کنید:

@useridgetbot
@gibinfobot
    """,
    'notice_userid': """
    باید بگم که کار اشتباهی میباشد ❌
 
🔹 ممکن است شخص مورد نظر شما آیدی کاربری خود را تغییر داده باشد و ربات امکان پیدا کردن آن را نداشته باشد، البته که راهی برای این مورد هم هست. شناسه عددی! شما برای نتیجه قطعی بهتره همیشه با شناسه عددی جستجو کنید. این شناسه بر خلاف آیدی یوزرنیم قابل تغییر نیست و فقط با دیلیت و حذف اکانت کاربری از بین می‌رود.
    """
}

question_options = [
    [Button.inline("چطوری از ربات استفاده کنم ❓", b'bot')],
    [Button.inline("شناسه عددی یا یوزر آیدی چیست❓", b'userid')],
    [Button.inline("نام کاربری چیست❓", b'username')],
    [Button.inline("دریافت شناسه عددی (اندروید) ❓", b'android')],
    [Button.inline("دریافت شناسه عددی در آیفون (iOS) ❓", b'ios')],
    [Button.inline("چرا ربات شماره نمیده❓خراب شده❓", b'broken')],
    [Button.inline("دریافت شناسه عددی (با ربات)❓", b'get_userid')],
    [Button.inline("شما با آیدی جستجو میکنید⁉️", b"notice_userid")]
]

async def question_handler(bot, event):
    await bot.send_message(event.chat_id, "💭سوالات متداول", buttons=question_options)


turn_back_option = [
    Button.text("بازگشت 🔙", resize=True, single_use=True)
]

welcome_text = """
به ربات هویج خوش آمدید 👋 لطفا برای استفاده از ربات ابتدا در چنل اسپانسر ربات عضو شوید🙂
"""

search_text = """
    در حال جستجو در سامانه شکار⏳
"""

user_exists = lambda phone, time: f"""
متاسفانه اطلاعات اکانت شما در دیتابیس سامانه شکار موجود است 😱

👤result: {phone}
⏰search time: {time}

🔍 برای جستجو های بیشتر می‌توانید نام کاربری ،شناسه تلگرام و یا پیغامی فورواردی از سوی اکانت مورد نظرتان را برای ربات ارسال کنید.

🔹 همچنین برای دریافت اطلاعات شماره مورد نظرتان میتوانید آن شماره را به لاتین در قسمت "مزاحم یاب" ارسال کنید.
"""

user_not_exists = """
خوشبختانه اطلاعات اکانت شما در دیتابیس سامانه شکار نیست🙂

🔍 برای جستجو های بیشتر می‌توانید نام کاربری ،شناسه تلگرام و یا پیغامی فورواردی از سوی اکانت مورد نظرتان را برای ربات ارسال کنید.

🔹 همچنین برای دریافت اطلاعات شماره مورد نظرتان میتوانید آن شماره را به لاتین در قسمت "مزاحم یاب" ارسال کنید.
"""

invalid_contact_text = """
یه مشکلی پیش اومد! بنظرم نمیاد بصورت مخاطب تلگرامی شماره رو فرستاده باشید🧐

شماره مورد نظر رو به صورت مخاطب تلگرام ارسال کنید📱
"""

valid_contact_text = """
مخاطب با موفقیت به دیتابیس اضافه شد✅
"""

contact_already_been_text = """
مخاطب از قبل در دیتابیس وجود دارد!😃
"""

create_copy_of_bot_text = """
تیم Badhunters اولین سازنده ربات ارسال اطلاعات‌ شماره و آیدی تلگرامی با بالاترین حجم دیتابیس قصد اجاره api از دیتابیس های موجود و یا پیاده سازی 0 تا 100 ربات مشابه @havij_robot را به صورت ماهانه، سالانه و... دارد 🥳

ویژگی های ربات:

1- دیتابیس بیش از 50 میلیون شماره ♨️

2- دریافت شماره در مدت زمان کمتر از 1 ثانیه 🤩

3- جذب ممبر فوقالعاده عالی👥

4- قابلیت قفل روی چنل به تعداد دلخواه با جذب بسیار بالا (1k در روز)🙀

5- پنل مدیریتی با قابلیت آمارگیری و بکاپ گیری👌

6- قابلیت فوروارد در ربات با سرعت عالی🚀

7- 🔺(بدون آفی) 💯

#توجه 👇

🔹 ساخت، راه اندازی و پشتیبانی فنی ربات به عهده ادمین های ما بوده و هیچگونه نیازی به دانش برنامه نویسی نیست❗️

🔹 هزینه اجاره با توجه به تایم مورد نظر خریدار گفته می‌شود و مبلغ صرفا معادل بیت کوین گرفته می‌شود / جهت خرید و اطلاعات بیشتر با این اکانت @in_pod در ارتباط باشید
"""

user_may_not_exists_text = """
این یوزرنیم در دیتابیس لو رفته سامانه شکار موجود نیست! 🙂

#توصیه:

🔹 با توجه به اینکه بیشتر اکانت های تازه وارد شده بدون یوزرنیم هستند و یا یوزرنیم قبلی خود را تغییر داده اند حتما با شناسه عددی جستجو کنید.

🔹 این شناسه را میتوانید با آیدی و یا پیام فورواردی در صورتی که فوروارد از سوی کاربر مد نظرتون بسته (مخفی) نباشد به این ربات @useridgetbot ارسال و شناسه را دریافت کنید. در صورت‌ عدم وجود آیدی در اکانت مورد نظر و بسته بودن فوروارد آن از ترفند های ذکر شده در سوالات متداول کمک بگیرید."""

async def create_copy(bot, event):
    await bot.send_message(event.chat_id, create_copy_of_bot_text, buttons=general_options)


async def welcome_message(bot, event):
    await bot.send_message(event.chat_id, welcome_text, buttons=channel_invite)


async def invalid_message(bot, event):
    await bot.send_message(event.chat_id, "بنظر نمیاد (شناسه کاربری، یوزرنیم و یا پیغام فوروارد شده از سوی کاربر) فرستاده باشيد 🧐", buttons=general_options)


async def searching(bot, event):
    text = """در حال جستجو اطلاعات اکانت شما در سامانه شکار⏳
    """
    await bot.send_message(event.chat_id, text, buttons=general_options)


async def reply_user_exists(bot, event, phone, time):
    logging.info("user exist")
    text = user_exists(phone, time)
    await bot.send_message(event.chat_id, text, buttons=general_options)


async def reply_user_not_exists(bot, event):
    logging.info("user does not exist")
    await bot.send_message(event.chat_id, user_not_exists, buttons=general_options)


async def in_development(bot, event):
    await bot.send_message(event.chat_id, "این بخش در دست ساخت است", buttons=general_options)


async def ask_to_share_contacts(bot, event):
    await bot.send_message(event.chat_id, "شماره مورد نظر رو به صورت مخاطب تلگرام ارسال کنید📱",
                           buttons=turn_back_option)


async def cancel_action(bot, event):
    await bot.send_message(event.chat_id, "کنسل شد✅", buttons=general_options)


async def user_search_t(bot, event):
    
    await bot.send_message(event.chat_id, search_text, buttons=general_options)


async def send_username_result(bot, event):
    try:
        start = datetime.now()
        userid = await get_id_from_forward(event)

        if userid == 0:
            return

        result = search_id(userid)

        if result is None:
            await event.reply("اطلاعات کاربر در دیتابیس سامانه شکار وجود ندارد ☹️")
            return

        end = datetime.now()


        total_search_time = end - start

        body = f"""
👤result: {result}
⏰search time: {total_search_time.total_seconds():.3f}s
"""

        await event.reply(body)        

    except:
        start_point = datetime.now()
        text = event.message.message

        string = list(text)

        for char in string:
            if char in UNICODE_EMOJI.keys():
                raise Exception("emoji in string")
        
        if "@" in text:
            text = str(text).split("@")[-1]

        await user_search_t(bot, event)
        is_id = text.isdigit()

        if is_id:
            result = search_id(text)

            if result is None:
                await event.reply("اطلاعات کاربر در دیتابیس سامانه شکار وجود ندارد ☹️")
                return

        else:
            result = search_username(text)

            if result is None:
                await event.reply(user_may_not_exists_text)
                return

        end_point = datetime.now()
        total_search_time = end_point - start_point

        body = f"""
👤result: {result}
⏰search time: {total_search_time.total_seconds():.3f}s
"""

        await event.reply(body)


async def get_data_from_media(bot, event):
    userid = event.original_update.message.media.user_id
    phone_number = event.original_update.message.media.phone_number
    entity = await bot.get_entity(userid)
    username = entity.username

    return userid, phone_number, username


async def invalid_contact(bot, event):
    await bot.send_message(event.chat_id, invalid_contact_text, buttons=turn_back_option)


async def contact_added(bot, event):
    await bot.send_message(event.chat_id, valid_contact_text, buttons=general_options)


async def contact_already_been(bot, event):
    await bot.send_message(event.chat_id, contact_already_been_text, buttons=turn_back_option)


async def ask_to_share_phone(bot, event):
    text = """
    لطفا شماره فرد مورد نظر را بفرستید📞

🔵 همچنین می‌توانید از طریق ارسال یوزرنیم، شناسه عددی و یا پیام فورواردی از سوی کاربر مد نظرتان در تلگرام به این بخش از ربات هم شماره را به دست آورید و هم اسم و فامیل مرتبط با آن شماره!
    """
    await bot.send_message(event.chat_id, text, buttons=turn_back_option)


async def invalid_phone(bot, event):
    await bot.send_message(event.chat_id, "بنظر نمیاد شماره فرستاده باشید⁉️", buttons=turn_back_option)


async def nothing_found(bot, event):
    await bot.send_message(event.chat_id, "متاسفانه اطلاعای در دیتابیس وجود ندارد", buttons=turn_back_option)

def generate_list(title, iter):
    text_name = f"{title}:"
    iter = [i for i in iter if i != None and i != ""]

    if len(iter) == 0:
        text_name += "\n-"
        return text_name


    for i in iter:
        if i != None:
            text_name += f"\n - {i}"

    return text_name

async def get_data_from_forward(event):
    user_id = event.fwd_from.from_id
    if user_id is None:
        await event.reply("""
        شخص مورد نظر فوروارد خودشو مخفی کرده ❌

#توصیه:

🔹 درصد زیادی از اکانت های موجود در تلگرام به دلیل توجه به حریم خصوصی  فوروارد خود را می‌بندند (مخفی می‌کنند) در نتیجه باید شناسه کاربری (همان آیدی عددی) شخص مورد نظر و یا آیدی اکانت آن را در صورت موجودیت ارسال کنید

🔹 همچنین این شناسه را میتوانید با ارسال آیدی و یا پیام فورواردی در صورتی که فوروارد بسته (مخفی) نباشد از سوی کاربر مد نظرتون به این ربات @useridgetbot ارسال کنید و شناسه را به دست آورید.در صورت بسته بودن فوروارد و عدم موجود آیدی در اکانت مورد نظرتان، از ترفند های ذکر شده در سوالات متداول کمک بگیرید.
        """)

        return 0    

    phone = search_id(user_id)

    return phone


async def get_id_from_forward(event):
    user_id = event.fwd_from.from_id
    if user_id is None:
        await event.reply("""
        شخص مورد نظر فوروارد خودشو مخفی کرده ❌

#توصیه:

🔹 درصد زیادی از اکانت های موجود در تلگرام به دلیل توجه به حریم خصوصی  فوروارد خود را می‌بندند (مخفی می‌کنند) در نتیجه باید شناسه کاربری (همان آیدی عددی) شخص مورد نظر و یا آیدی اکانت آن را در صورت موجودیت ارسال کنید

🔹 همچنین این شناسه را میتوانید با ارسال آیدی و یا پیام فورواردی در صورتی که فوروارد بسته (مخفی) نباشد از سوی کاربر مد نظرتون به این ربات @useridgetbot ارسال کنید و شناسه را به دست آورید.در صورت بسته بودن فوروارد و عدم موجود آیدی در اکانت مورد نظرتان، از ترفند های ذکر شده در سوالات متداول کمک بگیرید.
        """)

        return 0    
    return user_id


forward_limit_text = """
شخص مورد نظر فروارد خودشو محدود کرده !
متاسفیم! شماره اکانت مورد نظر شما برای جستجو اسم و فامیل در دیتابیس موجود نیست / در صورت موجود بودن شماره نزد شما، برای دریافت اطلاعاتش آن شماره را ارسال کنید تا ربات مستقیما از طریق شماره جستجو را انجام دهد
"""

async def get_info_from_phone(bot, event):

    try:
        phone = await get_data_from_forward(event)

        if phone is None:
            await event.reply(forward_limit_text)
            return

        if phone == 0:
            return

        need_phone = True

    except:
        phone = event.original_update.message.message
        need_phone = False

        
    if phone and str(phone).isdigit():
        names, families, cities, addresses = get_data_from_phone(phone)
        
        if not (names and families and cities and addresses):
            await event.reply("متاسفیم! ☹️ شماره اکانت مورد نظر شما برای جستجو اسم و فامیل در دیتابیس یافت نشد/ در صورت موجود بودن شماره نزد شما، برای دریافت اطلاعاتش آن شماره را ارسال کنید تا ربات مستقیما از طریق شماره جستجو را انجام دهد🦾")
            return

        names = generate_list("👤names", names)
        families = generate_list("👥 family names", families)
        cities = generate_list("🏡 cities", cities)
        addresses = generate_list("🚔 addresses", addresses)

        text = f"""
{names}

{families}

{cities}

{addresses}
        """

        if need_phone:
            text = f"""
phone: {phone}
{text}
            """

        await bot.send_message(event.chat_id, text, buttons=turn_back_option)


    else:
        await invalid_phone(bot, event)


def remove_all_memories(event):
    memory.contact.contact_memory.remove(event)
    memory.annoy.annoy_memory.remove(event)


async def captcha_message(bot, event):
    await bot.send_message(event.chat_id, "آیا شما ربات هستید؟ 🤖", buttons=captcha_ask)


async def back_to_service(bot, event):
    await bot.send_message(event.chat_id, "عالیه ✅", buttons=general_options)


async def stop_spam(bot, event):
    await bot.send_message(event.chat_id, "🚫اسپم ممنوع🚫", buttons=general_options)

async def limit_time(time, bot, event):
    await bot.send_message(event.chat_id, f"لطفا {int(time)} ثانیه صبر کنید⏰", buttons=general_options)


def bot_protect(handler):
    async def wrapper(bot, event):
        is_bot = captcha.bot_memory.check(event)


        captcha.bot_memory.clear_by_time(event)

        if is_bot:
            await captcha_message(bot, event)

        elif captcha.bot_memory.raise_warn(event):
            await stop_spam(bot, event)

            start_point = captcha.bot_memory.time[captcha.bot_memory.get_id(event)]
            now = datetime.now()

            difference = now - start_point
            difference = difference.total_seconds()
            print(difference)

            time = 60 - difference

            await limit_time(time, bot, event)

        else:
            await handler(bot, event)
            captcha.bot_memory.record(event)

    return wrapper

async def send_image(bot, event):
    await bot.send_message(event.chat_id, questions['android'], file="./assets/video.mp4")