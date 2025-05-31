import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ChatMemberHandler,
    filters,
    CallbackContext,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

API_URL_TEMPLATE = "https://api.coingecko.com/api/v3/simple/price?ids={id}&vs_currencies=usd"

async def get_crypto_price(id_name: str):
    try:
        response = requests.get(API_URL_TEMPLATE.format(id=id_name))
        data = response.json()
        logging.info(f"API response for {id_name}: {data}")
        return data.get(id_name, {}).get('usd')
    except Exception as e:
        logging.error(f"Error fetching {id_name} price: {e}")
        return None

async def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    keyboard = [
        [
            InlineKeyboardButton("𝗗𝗘𝗩👨🏼‍💻", url="tg://resolve?domain=GuSt3bDo"),
            InlineKeyboardButton("𝗢𝗪𝗡𝗘𝗥🕶", url="tg://resolve?domain=GuSt3bDo")
        ],
        [InlineKeyboardButton("𝗛𝗘𝗟𝗣", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_message = (
        f"Welcome, {user_name}!\n"
        "~ Start search and get info from NFT user\n"
        "~ Use HELP to see commands"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def help_button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    help_text = (
        "COMMANDS:\n"
        "~ /start to see start message\n"
        "~ /mode to change use mode for sudo\n\n"
        "USAGE:\n"
        "~ add bot to group or channel & send user with @\n"
        "~ send user with @ in bot private"
    )
    await query.edit_message_text(text=help_text, reply_markup=reply_markup)

async def handle_messages(update: Update, context: CallbackContext):
    text = update.message.text.lower().strip()

    if text in ["id", "/id", "أيدي", "ايدي"]:
        user_id = update.effective_user.id
        keyboard = [[InlineKeyboardButton("انسخ الايدي👆", callback_data='copy_id')]]
        await update.message.reply_text(
            f"الايدي بتاعك:\n`{user_id}`", parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if text == "منصه":
        await update.message.reply_text("https://fragment.com/")
        return

    if text in ["مطور البوت", "المطور"]:
        keyboard = [[InlineKeyboardButton("𝗮𝗯𝗱𝗲𝗹𝗿𝗮𝗵𝗺𝗮𝗻", url="https://t.me/GuSt3bDo")]]
        caption = (
            "❲ Developers Bot ❳\n"
            "— — — — — — — — —\n"
            "𖥔 Dev Name : ˛ 𝗮𝗯𝗱𝗲𝗹𝗿𝗮𝗵𝗺𝗮𝗻\n"
            "𖥔 Dev Bio : لٰا شۨيٰء يـدۅم."
        )
        await update.message.reply_photo(
            photo="https://pin.it/27R70Jvvs",
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if text == 'بوت':
        await update.message.reply_text("اسمي (nft)")
        return

    if text == 'nft':
        await update.message.reply_text("عايز اي يروحي")
        return

    crypto_triggers = {
        'تون': 'the-open-network',
        'ton': 'the-open-network',
        'ايثريم': 'ethereum',
        'الايثريم': 'ethereum',
        'ethereum': 'ethereum',
        'eth': 'ethereum',
        'بيتكوين': 'bitcoin',
        'bitcoin': 'bitcoin'
    }
    if text in crypto_triggers:
        coin_id = crypto_triggers[text]
        price = await get_crypto_price(coin_id)
        if price is not None:
            await update.message.reply_text(f"{price}$")
        else:
            await update.message.reply_text("حدث خطأ في جلب السعر!")
        return

async def greet_on_my_chat_member(update: Update, context: CallbackContext):
    result = update.my_chat_member
    new_status = result.new_chat_member.status
    old_status = result.old_chat_member.status
    if old_status in ('left', 'kicked') and new_status in ('member', 'administrator'):
        await context.bot.send_message(
            chat_id=result.chat.id,
            text="𝚑𝚎𝚕𝚕𝚘, 𝚒 𝚊𝚖(𝚗𝚏𝚝)\n𝚖𝚢 𝚞𝚜𝚎𝚛:- @G_E_QBOT"
        )

def main():
    application = Application.builder().token("7733750721:AAHleGIYGoAE3N0-7sA2-R6FbDyQUGjzU6A").build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(help_button, pattern='help'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    application.add_handler(ChatMemberHandler(greet_on_my_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    application.run_polling()

if __name__ == '__main__':
    main()