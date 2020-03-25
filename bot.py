import logging

import telegram.error as tg_error
from telegram import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler, Updater

from utils import get_server_list
from settings import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Keep track of last message sent
last_welcome_msg = None


def start(update, context):
    """Send starting message"""
    update.message.reply_text(f"Ciao! Sono il bot di supporto🤖\nConsulta il menù " \
                               "delle azioni per sapere cosa posso fare per te!")

def contribute(update, context):
    """Send some links"""
    update.message.reply_text(f"Se vuoi contribuire al progetto consulta questa " \
                               "[pagina](https://iorestoacasa.work/voglio-contribuire.html) o le " \
                               "[issues](https://github.com/iorestoacasa-work/iorestoacasa.work/issues) " \
                               "presenti su GitHub 🖥", parse_mode=ParseMode.MARKDOWN)

def info(update, context):
    """Send infoz about project"""
    update.message.reply_text(f"Questo progetto è stato realizzato dall'associazione " \
                               "[PDP Free Software User Group](pdp.linux.it) in collaborazione con " \
                               "[beFair](befair.it).\nOltre a loro ci sono altri che hanno contribuito!\n" \
                               "Puoi trovare la lista completa ed aggiornata "\
                               "[qua](https://iorestoacasa.work/crediti.html) 💪", parse_mode=ParseMode.MARKDOWN)

def server_list(update, context):
    """Return the available server list"""
    msg, reply_markup = prepare_server_list()

    update.message.reply_text(msg,
                              reply_markup=reply_markup,
                              parse_mode=ParseMode.MARKDOWN,
                              disable_web_page_preview=True)

def add_group(update, context):
    """Send message to new group members"""
    global last_welcome_msg

    for member in update.message.new_chat_members:
        # Delete last msg
        if last_welcome_msg:
            last_welcome_msg.delete()

        # Send new!
        last_welcome_msg = update.message.reply_text(f"Ciao *{member.name}*! Benvenuto nel gruppo di supporto😁\n" \
                                                      "Se vuoi contribuire al progetto consulta questa " \
                                                      "[pagina](https://iorestoacasa.work/voglio-contribuire.html) o le " \
                                                      "[issues](https://github.com/iorestoacasa-work/iorestoacasa.work/issues) " \
                                                      "presenti su GitHub.\n\nSe invece hai bisogno di aiuto scrivi pure qua, " \
                                                      "qualcuno in questo gruppo sicuramente ti saprà aiutare🛠",
                                                      parse_mode=ParseMode.MARKDOWN,
                                                      disable_web_page_preview=True)

def error(update, context):
    """Log errors caused by updates"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def change_page(update, context):
    """Callback for page change on server list"""
    query = update.callback_query

    msg, reply_markup = prepare_server_list(int(query.data))
    query.edit_message_text(text=msg,
                            reply_markup=reply_markup,
                            parse_mode=ParseMode.MARKDOWN,
                            disable_web_page_preview=True)

def prepare_server_list(page=0):
    """
    Prepare server list message and keyboard

    :param page: Page to be shown
    """
    msg = "🛠 *Server disponibili* 🛠\n\n"

    server_list = sorted(get_server_list(), key=lambda k: k.get('cpu_usage', -1))

    for server in server_list[(page*5):(page*5+5)]:
        # Check server type
        if server['software'] == "JITSI":
            msg += f"🔌 [{server['name']}]({server['url']})\n"
        else:
            msg += f"📚 [{server['name']}]({server['url']})\n"

        msg += f"❤️ *Offerto da*: [{server['by']}]({server['by_url']})\n"

        # Check if metrics are enabled
        if server.get('cpu_usage') != None and server.get('user_count') != None:
            msg += f"👩🏻‍💻 *Utenti connessi*: {server['user_count']}\n"
            msg += f"⚙️ *Carico*: {int(server['cpu_usage']*100)}%\n"

        # Add space between servers
        msg += "\n"

    msg += f"🔌 = *Jitsi*\n"
    msg += f"📚 = *Multiparty-Meeting* (Beta)\n\n"
    msg += f"📖 *Pagina*: {page+1}"

    # Create a inline keyboard based on current page
    if page == 0:
        keyboard = [[
            InlineKeyboardButton("➡️", callback_data=page+1)
        ]]
    elif ((page+1)*5) >= len(server_list):
        keyboard = [[
            InlineKeyboardButton("⬅️", callback_data=page-1),
        ]]
    else:
        keyboard = [[
            InlineKeyboardButton("⬅️", callback_data=page-1),
            InlineKeyboardButton("➡️", callback_data=page+1)
        ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    return msg, reply_markup

def main():
    """Starts the bot"""
    print("Starting bot :D")

    # Create the Updater
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("servers", server_list))
    dp.add_handler(CommandHandler("contribute", contribute))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, add_group))
    dp.add_handler(CallbackQueryHandler(change_page))

    # Register error handler
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
