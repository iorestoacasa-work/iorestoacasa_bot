import logging
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


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

def add_group(update, context):
    """Send message to new group members"""
    for member in update.message.new_chat_members:
        update.message.reply_text(f"Ciao *{member.username}*! Benvenuto nel gruppo di supporto😁\n" \
                                   "Se vuoi contribuire al progetto consulta questa " \
                                   "[pagina](https://iorestoacasa.work/voglio-contribuire.html) o le " \
                                   "[issues](https://github.com/iorestoacasa-work/iorestoacasa.work/issues) " \
                                   "presenti su GitHub.\n\nSe invece hai bisogno di aiuto scrivi pure qua, " \
                                   "qualcuno in questo gruppo sicuramente ti saprà aiutare🛠", parse_mode=ParseMode.MARKDOWN)

def error(update, context):
    """Log errors caused by updates"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Starts the bot"""
    print("Starting bot :D")

    # Create the Updater
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("contribute", contribute))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, add_group))

    # Register error handler
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
