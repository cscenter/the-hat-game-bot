import json
import logging
import random

import telegram

from built_dict import build_dict

TOKEN = '173396560:AAH6D6_z-Dik1HFmFNM2PktTkrahDSyMurY'

words = {}
games = {}
LAST_UPDATE_ID = None
LAST_MESSAGE = None
commands = [['/start'], ['/more'], ['/exit']]
markup_ingame = [['Еще подсказку!'], ['Закончить игру']]
markup_newgame = [['Начать!'], ['Нет, спасибо']]

##TODO: execute commands


def give_a_hint(bot, chat_id):
    global markup_ingame, markup_newgame

    if (games[chat_id]['attempts'] == games[chat_id]['hints_amount']):
        bot.sendMessage(chat_id=chat_id, text='Подсказки закончились!')
        offer_new_game(bot, chat_id)
    else:
        cur_hints = games[chat_id]['hints']
        games[chat_id]['attempts'] += 1
        games[chat_id]['hint'] = cur_hints.pop(random.randrange(len(cur_hints)))
        bot.sendMessage(chat_id=chat_id, text='Подсказка №' + str(games[chat_id]['attempts']) + ': ' +
                                               games[chat_id]['hint'],
                        reply_markup =telegram.ReplyKeyboardMarkup(keyboard = markup_ingame))


def start_a_game(bot, chat_id):
    global markup_ingame, markup_newgame
    bot.sendMessage(chat_id=chat_id,
                    text='Начинаем игру!')
    cur_word = random.choice(list(words.keys()))
    cur_hints = words[cur_word]
    hints_amount = len(cur_hints)
    attempts = 1

    cur_hint = cur_hints.pop(random.randrange(len(cur_hints)))
    logging.info('user ' + str(chat_id) + ' has just started a game. The word is ' + cur_word)
    bot.sendMessage(chat_id=chat_id, text='Подсказка №' + str(attempts) + ': ' +
                                          cur_hint,
                   reply_markup =telegram.ReplyKeyboardMarkup(keyboard = markup_ingame))
    games[chat_id] = {'word': cur_word, 'hint': cur_hint, 'hints': cur_hints, 'attempts': attempts, 'ingame' : 1,
                      'hints_amount': hints_amount}

def offer_new_game(bot, chat_id):
    global ingame, markup_newgame
    games[chat_id]['ingame'] = 0
    bot.sendMessage(chat_id=chat_id, text="Начать новую игру?",
                        reply_markup =telegram.ReplyKeyboardMarkup(keyboard = markup_newgame))

def execute(cmd, bot, chat_id):

    if cmd.startswith('/start') or (cmd.startswith('Начать') and games[chat_id]['ingame'] == 0):
        start_a_game(bot, chat_id)

    elif cmd.startswith('Еще подсказку!'):
        logging.info('user ' + str(chat_id) + ' asked for another hint on the ' + str(games[chat_id]['attempts']) +
                     'th attempt, right word is ' + games[chat_id]['word'] + ', last hint was ' + games[chat_id]['hint'])
        give_a_hint(bot, chat_id)

    elif cmd.startswith('Закончить'):
        bot.sendMessage(chat_id=chat_id, text="Игра закончена!", reply_markup=telegram.ReplyKeyboardHide())
        offer_new_game(bot, chat_id)

    elif cmd.startswith('Нет, спасибо') and games[chat_id]['ingame'] == 0:
        bot.sendMessage(chat_id=chat_id, text="Спасибо за игру!",
                        reply_markup =telegram.ReplyKeyboardHide())
        logging.info('user ' + str(chat_id) + ' has just ended a game.')


    else:
        if (cmd.lower() == games[chat_id]['word']):
            bot.sendMessage(chat_id=chat_id, text="Поздравляем, вы угадали слово!")
            logging.info('user ' + str(chat_id) + ' guessed a word ' + games[chat_id]['word'] + ' with '
                         + str(games[chat_id]['attempts']) + 'th attempt')
            offer_new_game(bot, chat_id)
        elif cmd.startswith('/'):
            bot.sendMessage(chat_id=chat_id, text="Unknown command")
        else:
            bot.sendMessage(chat_id=chat_id, text="Вы не угадали!")
            logging.info('user ' + str(chat_id) + ' said ' + cmd +
                         ' on the ' + str(games[chat_id]['attempts']) + 'th attempt, right word is ' +
                         games[chat_id]['word'] +  ', last hint was ' + games[chat_id]['hint'])
            give_a_hint(bot, chat_id)


def answer(bot):
    global LAST_UPDATE_ID, LAST_MESSAGE, IS_KEYBOARD_WORKING, words
    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        chat_id = update.message.chat_id
        message = update.message.text.encode('utf-8')
        dec_message = message.decode('utf-8')
        if message:
            reply_markup = {'keyboard': commands[1::],
                            'resize_keyboard': True, 'one_time_keyboard': False}
            reply_markup = json.dumps(reply_markup)
            execute(dec_message, bot, chat_id)

            LAST_UPDATE_ID = update.update_id + 1


def main():
    logging.basicConfig(filename='hat_game.log',level=logging.INFO)
    logging.getLogger("telegram").setLevel(logging.WARNING)
    global LAST_UPDATE_ID, words
    words = build_dict()
    bot = telegram.Bot(TOKEN)
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        answer(bot)


if __name__ == '__main__':
    main()
