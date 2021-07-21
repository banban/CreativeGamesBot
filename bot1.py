from datetime import MINYEAR
import constants as C
import os
import logging
import random

from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, Update, MessageEntity, InlineQueryResultGame) #,Game, InputTextMessageContent
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
PLAY, TRADER, MINER, PAGE_MASSAGES = map(chr, range(4))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END


class Bot:
    # instance members
    #constractor
    def __init__(self):
        self.games =['MinerVsTrader']
        self.title = 'Python-telegram-bot Test Game'
        self.description = 'description'
        self.photo = [{'width': 640, 'height': 360, 'file_id': 'Blah', 'file_size': 0}]
        self.text = 'Other description'
        self.text_entities = [{'offset': 13, 'length': 17, 'type': MessageEntity.URL}]
        self.animation = {'file_id': 'Blah'}

    def stop(self, update: Update, context: CallbackContext) -> int:
        """End Conversation by command."""
        context.user_data.clear()
        #self.remove_page_messages(update,  context)
        if bool(update.callback_query):
            return update.callback_query.message.reply_text('🏁Okay, bye')
            #context.chat_data[PAGE_MASSAGES].append(bye_message.message_id)
        elif bool(update.message):
            return update.message.reply_text('🏁Okay, bye')
            #context.chat_data[PAGE_MASSAGES].append(bye_message.message_id)
        
        self.remove_page_messages(update, context)
        #return END

    def remove_page_messages(self, update: Update, context: CallbackContext):
        #print("remove_page_messages")
        try:
            _chat_id = update.callback_query.message.chat_id
        except:
            _chat_id = update.message.chat_id

        #print("remove_page_messages: 2")
        chat_data = context.chat_data
        if PAGE_MASSAGES in chat_data and _chat_id:
            #print("remove_page_messages: 3")
            for _id in chat_data[PAGE_MASSAGES]:
                try:
                    context.bot.delete_message(chat_id=_chat_id, message_id=_id)
                except:
                    pass
        chat_data[PAGE_MASSAGES] = []

    def start(self, update: Update, context: CallbackContext):
        #print("start is started")
        if bool(update.callback_query):
            #print('start update.callback_query')
            if update.callback_query.data == str(END):
                return self.stop(update, context)
            if update.callback_query.data == str(TRADER):
                return update.callback_query.message.reply_text('Good luck in trading!')
            if update.callback_query.data == str(MINER):
                return update.callback_query.message.reply_text('Good luck in mining!')
            if (update.callback_query.data is None):
                context.chat_data[PAGE_MASSAGES] = []
                return self.game(update, context)
        elif bool(update.message):
            #print('start update.message')
            #game = Game(title=self.title,description=self.description,photo=self.photo,text=self.text,text_entities=self.text_entities,animation=self.animation)
            update.message.reply_game("MinerVsTrader")#.set_game_score(user_id = update.message.from_user.id, score=100)
            #context.bot.send_game(game)
        """Send a message when the command /start is issued."""
        #update.message.reply_text('Hello, play games!')


    def shuffleDish(self):
        A = ['APPLE', 'PUMKIN', 'STRAWBERRY', 'BANANA', 'CHOCOLATE']
        B = ['PIE', 'ICE-CREAM', 'CAKE', 'SHAKE']
        dish = random.choice(A)+" "+random.choice(B)
        return dish

    def play_shuffle(self, update: Update, context: CallbackContext):
        #print("play_shuffle is started")
        """Send a message when the command /play is issued."""
        update.message.reply_text(self.shuffleDish())

    def game(self, update: Update, context: CallbackContext):
        """Start the game when Play button is pressed."""
        #print("game is started")
        if bool(update.callback_query):
            #print("game:"+ str(update.callback_query.data))
            _text = "Let's play! Choose your role"
            update.callback_query.set_game_score(user_id = update.message.from_user.id, score=100)
            buttons = [
                [
                    InlineKeyboardButton(text='Trader', callback_data=str(TRADER)),
                    InlineKeyboardButton(text='Miner', callback_data=str(MINER)),
                ],
                # [
                #     InlineKeyboardButton(text=f"🔎Trading", callback_data=str(SEARCHING)),
                #     InlineKeyboardButton(text=f"⛓Trades History", callback_data=str(TRACKING)),
                # ],
                [
                    InlineKeyboardButton(text='⏹Exit', callback_data=str(END)),
                ],
            ]
            keyboard = InlineKeyboardMarkup(buttons)

            if (_text != update.callback_query.message.text):
                update.callback_query.answer()
                update.callback_query.edit_message_text(text=_text, reply_markup=keyboard)

    def inlinequery(self, update: Update, context: CallbackContext):
        #print("inlinequery")
        query = context.inline_query.query
        results = []
        for game in self.games:
            if query.lower() in game.lower():
                results.append(InlineQueryResultGame(id=str('uuid4()'),game_short_name=game))
        context.inline_query.answer(results)

    def play_button(self, update: Update, context: CallbackContext):
        #print("play button")
        #print(update)
        query = update.callback_query
        if query.message:
            buttons = [
                [
                    InlineKeyboardButton(text='Trader', callback_data=str(TRADER)),
                    InlineKeyboardButton(text='Miner', callback_data=str(MINER)),
                ],
                # [
                #     InlineKeyboardButton(text=f"🔎Trading", callback_data=str(SEARCHING)),
                #     InlineKeyboardButton(text=f"⛓Trades History", callback_data=str(TRACKING)),
                # ],
                [
                    InlineKeyboardButton(text='⏹Exit', callback_data=str(END)),
                ],
            ]
            keyboard = InlineKeyboardMarkup(buttons) #, reply_markup=keyboard
            return query.message.reply_text(text=f"Please choose your role...", reply_markup=keyboard)

        game = query.game_short_name
        uid = str(query.from_user.id)
        url = "https://yenots.itch.io/crypto-catch"
            #"https://cdno.itch.io/flappy-coin" #https://bitcoinsv.itch.io/bitcoin-versus-crypto #https://playcurious.games/games/blockchain-battle/
            #https://playcurious.games/games/blockchain-battle/

        if query.message:
            mid = str(query.message.message_id)
            cid = str(query.message.chat.id)
            url += f"?game={game}uid={uid}&mid={mid}&cid={cid}"
        else:
            imid = update.callback_query.inline_message_id
            url += f"?game={game}uid={uid}&imid={imid}"

        return context.bot.answer_callback_query(query.id, text=game, url=url)

        #if (game): #is not None
        #    query.message.set_game_score(user_id = uid, score=0)

        #query.answer()
        #query.edit_message_text(text="starting {game}...", reply_markup=keyboard) #.reply(text=f"starting {game}...")
        #scores = query.message.get_game_high_scores(uid)
        #query.message.reply_text(text=f"starting {game} with to top score {scores[0].score}...")
        #.reply_game(game).game.title caption="" #set_game_score(user_id = uid, score=10) #
        #context.bot.setGameScore(user_id = uid, score=76, message_id=query.message.message_id)
        # try:
        #     query.message.set_game_score(user_id = uid, score=10)
        # except:
        #     print(context.error)
        #     pass

        #query.message.reply_game(game).set_game_score(user_id = uid, score=100)
        # host = "localhost"
        # port = "8080"
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

    def run(self) -> None:
        """Run the bot."""
        # Create the Updater and pass it your bot's token.
        updater = Updater(C.TELEGRAM_TOKEN)
        # Get the dispatcher to register handlers
        dp = updater.dispatcher
        
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler('stop', self.stop))
        dp.add_handler(CommandHandler("shuffle", self.play_shuffle))

        dp.add_handler(CallbackQueryHandler(self.start, pattern='^' + str(TRADER) + '|'+ str(MINER) + '|'+ str(END) + '$')) #End button
        dp.add_handler(CallbackQueryHandler(self.play_button))
        #dp.add_handler(CallbackQueryHandler(Filters.game, self.start, pattern=r'.*'))  #^' + str(PLAY) + '$
        #dp.add_handler(CallbackQueryHandler(self.game, pattern=r'.*'))  #, pattern=r'.*') ^' + str(PLAY) + '$
        #dp.add_handler(InlineQueryHandler(self.inlinequery)) #, pattern=Filters.regex('^(File|Coupon|Other)$')

        #updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))
        #updater.dispatcher.add_handler(CallbackQueryHandler(button))

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

        # on noncommand i.e message - echo the message on Telegram
        #dp.add_handler(MessageHandler(Filters.text, self.play))
        dp.add_error_handler(self.error)


        # Run bot
        if C.HEROKU_APP_NAME == "":  #pooling mode
            #logger.info("Can't detect 'HEROKU_APP_NAME' env. Running bot in pooling mode.")
            updater.start_polling(1)
        else:  #webhook mode
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
