from datetime import MINYEAR
import constants as C
import os
import logging
import random

from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, Update)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    InlineQueryHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)
from telegram.utils import helpers

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING
)

logger = logging.getLogger(__name__)
# State definitions for top level conversation
TRADER, MINER, SALING, BUYING, PROCESSING, FARMING, PAGE_MASSAGES = map(chr, range(7))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

class Bot:
    # constractor
    def __init__(self):
        self.games = ['MinerVsTrader']
        #list of games to play randomly
        self.html5_games = [
            "https://t.me/WorldOfCryptoCurrencyBot?start",
            "https://yenots.itch.io/crypto-catch",
            "https://cdno.itch.io/flappy-coin",
            "https://bitcoinsv.itch.io/bitcoin-versus-crypto",
            "https://playcurious.games/games/blockchain-battle/",
        ]

    def stop(self, update: Update, context: CallbackContext) -> int:
        """End Conversation by command."""
        context.user_data.clear()
        #self.remove_page_messages(update,  context)
        if bool(update.callback_query):
            return update.callback_query.message.reply_text('🏁Okay, bye')
            # context.chat_data[PAGE_MASSAGES].append(bye_message.message_id)
        elif bool(update.message):
            return update.message.reply_text('🏁Okay, bye')
            # context.chat_data[PAGE_MASSAGES].append(bye_message.message_id)

        self.remove_page_messages(update, context)
        # return END

    def remove_page_messages(self, update: Update, context: CallbackContext):
        # print("remove_page_messages")
        try:
            _chat_id = update.callback_query.message.chat_id
        except:
            _chat_id = update.message.chat_id
        chat_data = context.chat_data
        if PAGE_MASSAGES in chat_data and _chat_id:
            for _id in chat_data[PAGE_MASSAGES]:
                try:
                    context.bot.delete_message(
                        chat_id=_chat_id, message_id=_id)
                except:
                    pass
        chat_data[PAGE_MASSAGES] = []

    def start(self, update: Update, context: CallbackContext):
        """Send a message when the command /start is issued."""
        #print("user entered")
        if bool(update.callback_query):
            if update.callback_query.data == str(END):
                try:
                    # return the score of the specified user and several of their neighbors in a game.
                    scores = context.bot.get_game_high_scores(chat_id=update.callback_query.message.chat_id,
                                                            message_id=update.callback_query.message.message_id,
                                                            user_id=update.callback_query.message.from_user.id)
                    _text = "Here is top list of players:"
                    for score in scores:
                        _text += f"\n No: {score.position}, User: {score.user.first_name +' '+ score.user.last_name}, Score: {score.score}"
                    top_list_message = update.message.reply_text(text=_text)
                    context.chat_data[PAGE_MASSAGES].append(top_list_message.message_id)
                except:
                    pass
                #return self.stop(update, context)

            elif update.callback_query.data == str(TRADER):
                image_path = "./trading.gif"
                if (os.path.isfile(image_path)):
                    image_message = context.bot.send_animation(
                        chat_id=update.callback_query.message.chat_id, 
                        reply_to_message_id=update.callback_query.message.message_id,
                        animation=open(image_path, 'rb'),
                        caption="https://coinmarketcap.com/"
                    )
                    context.chat_data[PAGE_MASSAGES].append(image_message.message_id)
                update.callback_query.message.reply_text('Good luck in trading!')

            elif update.callback_query.data == str(MINER):
                image_path = "./mining.gif"
                if (os.path.isfile(image_path)):
                    image_message = context.bot.send_animation(
                        chat_id=update.callback_query.message.chat_id, 
                        reply_to_message_id=update.callback_query.message.message_id,
                        animation=open(image_path, 'rb'),
                        caption="https://www.nicehash.com/marketplace"
                    )
                    context.chat_data[PAGE_MASSAGES].append(image_message.message_id)
                update.callback_query.message.reply_text('Good luck in mining!')

            elif update.callback_query.data in [str(SALING),str(BUYING),str(PROCESSING),str(FARMING)]:
                # grant player random score
                try:
                    context.bot.set_game_score(
                        chat_id=update.callback_query.message.chat_id, 
                        user_id=update.callback_query.message.from_user.id,
                        message_id=update.callback_query.message.message_id,
                        score=random.randint(0, 100),
                        force=True)
                except:
                    print(f"Error:{context.error}")
                    pass
            return None
        elif bool(update.message):
            replay_game = update.message.reply_game(self.games[0])
            return replay_game

    def play_shuffle(self, update: Update, context: CallbackContext):
        """Play shuffle dish game mixing A and B randomly"""
        #print("play_shuffle is started")
        A = ['APPLE', 'PUMKIN', 'STRAWBERRY', 'BANANA', 'CHOCOLATE']
        B = ['PIE', 'ICE-CREAM', 'CAKE', 'SHAKE']
        dish = random.choice(A)+" "+random.choice(B)
        update.message.reply_text(dish)

    def play_button(self, update: Update, context: CallbackContext):
        #print("play button pressed in chut group")
        query = update.callback_query
        
        # HTML5 mode in group
        if query.inline_message_id:
            game = query.game_short_name
            ilmid = query.inline_message_id
            uid = query.from_user.id

            # grant player random score
            try:
                context.bot.set_game_score(
                    inline_message_id=ilmid,
                    user_id=uid,
                    score=random.randint(0, 100),
                    force=True)
            except:
                pass

            # redirect to random game
            url = random.choice(self.html5_games)
            return context.bot.answer_callback_query(query.id, text=game, url=url)

        # direct dialogue mode
        elif query.message:
            buttons = [
                [
                    InlineKeyboardButton(
                        text='📉Trader', callback_data=str(TRADER)),
                    InlineKeyboardButton(
                        text='⛏Miner', callback_data=str(MINER)),
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔽Sale", callback_data=str(SALING)),
                    InlineKeyboardButton(
                        text=f"🔼Buy", callback_data=str(BUYING)),
                    InlineKeyboardButton(
                        text=f"⛓Mine", callback_data=str(PROCESSING)),
                    InlineKeyboardButton(
                        text=f"🔋Farm", callback_data=str(FARMING)),
                ],
                [
                    InlineKeyboardButton(text='⏹Exit', callback_data=str(END)),
                ],
            ]
            keyboard = InlineKeyboardMarkup(buttons)  # , reply_markup=keyboard
            return query.message.reply_text(text=f"Please choose your role...", reply_markup=keyboard)
        # if query.message:
        #     mid = str(query.message.message_id)
        #     cid = str(query.message.chat.id)
        #     url += f"?game={game}uid={uid}&mid={mid}&cid={cid}"
        # else:
        #     imid = update.callback_query.inline_message_id
        #     url += f"?game={game}uid={uid}&imid={imid}"
        # host = "your_game_server_address"
        # port = "433"
        # if query.message:
        #     mid = str(query.message.message_id)
        #     cid = str(query.message.chat.id)
        #     url = "https://" + host + ":"+port + "/" + game + "?uid="+uid+"&mid="+mid+"&cid="+cid
        #     query.answer(text=game, url=url)
        # else:
        #     imid = update.callback_query.inline_message_id
        #     url = "https://" + host + ":"+port + "/" + game + "?uid="+uid+"&imid="+imid
        #     update.callback_query.answer(text=game, url=url)
        # print(url)
        # context.bot.answer_callback_query(query.id, text=game, url=url)

    def error(update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def help(self, update: Update, context: CallbackContext):
        #chat_id = update.message.chat_id
        message_id = update.message.message_id
        reply = update.message.reply_text(
            "Type one of the following commands:"
            "\n/start - initiate guided session"
            "\n/stop - terminate conversation"
            "\n/shuffle - play shuffle dish game"
            "\nThere are some rules behind the scene:"
            "\n-Player has to choose role: Miner or Trader"
            "\n-Trader generates transactions in blockchain and choose which Miner will process them"
            "\n-Miner promotes commission rates for Traders, process transactions, and collect coins commission."
            "\n-The winner is the player with maximum coins scored."
        )
        chat_data = context.chat_data
        if PAGE_MASSAGES not in chat_data:
            chat_data[PAGE_MASSAGES] = []
        chat_data[PAGE_MASSAGES].append(reply.message_id)

    def handle_message(self, update: Update, context: CallbackContext):
        user_message = str(update.message.text).lower()
        if user_message.strip('!') in ("hello", "hi"):
            response = f"🤟G'Day {update.message.from_user.first_name}!"
        else:
            response = "😏hmm, looks like you need some /help"
        update.message.reply_text(response)

    def run(self) -> None:
        """Run the bot."""
        # Create the Updater and pass it your bot's token.
        updater = Updater(C.TELEGRAM_TOKEN)
        # Get the dispatcher to register handlers
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler('stop', self.stop))
        dp.add_handler(CommandHandler("shuffle", self.play_shuffle))
        dp.add_handler(CallbackQueryHandler(self.start, pattern='^' +
                       str(TRADER) + '|' + str(MINER) + '|' +
                       str(SALING) + '|' + str(BUYING) + '|' +
                       str(PROCESSING) + '|' + str(FARMING) + '|' +
                       str(END) + '$'))
        dp.add_handler(CallbackQueryHandler(self.play_button))
        #dp.add_handler(MessageHandler(Filters.text, self.handle_message))
        dp.add_error_handler(self.error)

        # # Callback handlers
        # hit_callback_handler = CallbackQueryHandler(game.hit_callback, pattern=r"^hit_[0-9]{7}$")
        # stand_callback_handler = CallbackQueryHandler(game.stand_callback, pattern=r"^stand_[0-9]{7}$")
        # join_callback_handler = CallbackQueryHandler(game.join_callback, pattern=r"^join_[0-9]{7}$")
        # start_callback_handler = CallbackQueryHandler(game.start_callback, pattern=r"^start_[0-9]{7}$")
        # newgame_callback_handler = CallbackQueryHandler(game.newgame_callback, pattern=r"^newgame$")
        # language_callback_handler = CallbackQueryHandler(settings.language_callback, pattern=r"^lang_([a-z]{2}(?:-[a-z]{2})?)$")
        # handlers = [banned_user_handler,
        #             start_command_handler, stop_command_handler, join_callback_handler, hit_callback_handler,
        #             stand_callback_handler, start_callback_handler, language_command_handler, stats_command_handler,
        #             newgame_callback_handler, reload_lang_command_handler, language_callback_handler, users_command_handler,
        #             comment_command_handler, comment_text_command_handler, answer_command_handler, ban_command_handler,
        #             unban_command_handler, bans_command_handler]
        # __all__ = ['handlers', 'error_handler']

        # Run bot
        if C.HEROKU_APP_NAME == "":  # pooling mode
            #logger.info("Can't detect 'HEROKU_APP_NAME' env. Running bot in pooling mode.")
            updater.start_polling(1)
        else:  # webhook mode
            PORT = int(os.environ.get('PORT', C.HEROKU_PORT))
            updater.start_webhook(
                listen="0.0.0.0",
                port=PORT,
                url_path=C.TELEGRAM_TOKEN,
                webhook_url=f"https://{C.HEROKU_APP_NAME}.herokuapp.com/{C.TELEGRAM_TOKEN}"
            )

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()


if __name__ == '__main__':
    bot = Bot()
    bot.run()
