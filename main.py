import telebot
from dotenv import load_dotenv
from os import getenv
import json
from telebot import types
from random import choice

load_dotenv()
token = getenv('TOKEN')
bot = telebot.TeleBot(token=token)


# counter = 1


def main():
    bot.polling()


@bot.message_handler(commands=['start'])
def start(message):
    # data = load_data()
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! "
                          "Я тестовый Iq бот /start_adventure".format(message.from_user))
    q = register(message)
    print(q)
    print(message.text)
    # preface(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = make_button('/continue_preface🏁')
    btn2 = make_button('/rules🏁')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, 'Чтобы начать квест напишите команду "/continue_preface🏁"\n'
                                      'Чтобы посмотреть, как проходить квест напишите команду "/rules🏁"',
                     reply_markup=markup)


@bot.message_handler(commands=['register'])
def register(message):
    if str(message.chat.id) not in load_data('database'):
        data = load_data('database')
        data[str(message.chat.id)] = {
            'user_name': '{0.first_name}'.format(message.from_user),
            'registered': True,
            'counter': 1,
            'preface': False,
            '1_level': False,
            '2_level': [False, ''],
            '3_level': False,
        }
        change_data(data, 'database')
        bot.send_message(message.chat.id, 'Регистрация завершена!')
    else:
        return True


@bot.message_handler(commands=['help'])
def help(message):
    if register(message):
        bot.send_message(message.chat.id, 'Help')
    else:
        bot.send_message(message.chat.id, '')


def change_data(data: dict, path: str) -> None:
    with open(f'{path}.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def load_data(path: str) -> dict:
    try:
        with open(f'{path}.json', 'r', encoding='utf8') as file:
            data = json.load(file)
            return data
    except json.decoder.JSONDecodeError:
        return {}


def make_button(dicts):
    return types.KeyboardButton(f"{dicts}")


@bot.message_handler(commands=['continue_preface🏁', 'continue_preface'])
def preface(message):
    if register(message):
        data = load_data('database1')
        datas = load_data('database')
        counter = datas[str(message.chat.id)]['counter']
        try:
            with open(data['preface'][str(counter)][1], 'rb') as img:
                bot.send_photo(message.chat.id, img)
        except Exception as error:
            print(str(error) + ' preface')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = make_button('/continue_preface🏁')
        markup.row(btn1)
        bot.send_message(message.chat.id, data['preface'][str(counter)][0],
                         reply_markup=markup)
        counter += 1
        datas[str(message.chat.id)]['counter'] = counter
        change_data(datas, 'database')
        if datas[str(message.chat.id)]['counter'] >= len(data['preface']) + 1:
            counter = 1
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = make_button('/continue_1_level🏁')
            markup.row(btn1)
            datas[str(message.chat.id)]['preface'] = True
            datas[str(message.chat.id)]['counter'] = counter
            change_data(datas, 'database')
            bot.send_message(message.chat.id, 'Чтобы начать 1 уровень напишите команду "/continue_1_level🏁"',
                             reply_markup=markup)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = make_button('/register')
        markup.row(btn1)
        bot.send_message(message.chat.id, 'Пройдите регистрацию написав команду "/register"',
                         reply_markup=markup)


@bot.message_handler(commands=['continue_1_level🏁', 'continue_1_level'])
def level_1(message):
    if register(message):
        data = load_data('database1')
        datas = load_data('database')
        counter = datas[str(message.chat.id)]['counter']
        if datas[str(message.chat.id)]['preface']:
            print(counter)
            try:
                with open(choice(data['1_level'][str(counter)][1]), 'rb') as img:
                    bot.send_photo(message.chat.id, img)
            except Exception as error:
                print(str(error) + ' 1_level')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            if counter >= len(data['1_level']):
                btn1 = make_button('/continue_underwater_city🏁')
                btn2 = make_button('/continue_abandoned_mine🏁')
                markup.row(btn1, btn2)
                datas[str(message.chat.id)]['1_level'] = True
                change_data(datas, 'database')
                bot.send_message(message.chat.id, data['1_level'][str(counter)][0],
                                 reply_markup=markup)
                counter = 1
                datas[str(message.chat.id)]['counter'] = counter
                change_data(datas, 'database')

            else:
                btn1 = make_button('/continue_1_level🏁')
                markup.row(btn1)
                bot.send_message(message.chat.id, data['1_level'][str(counter)][0],
                                 reply_markup=markup)
                counter += 1
                datas[str(message.chat.id)]['counter'] = counter
                change_data(datas, 'database')
        else:
            bot.send_message(message.chat.id, 'Пройдите предыдущие уровни',
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = make_button('/register')
        markup.row(btn1)
        bot.send_message(message.chat.id, 'Пройдите регистрацию написав команду "/register"',
                         reply_markup=markup)


@bot.message_handler(commands=['continue_underwater_city🏁', 'continue_underwater_city'])
def underwater_city(message):
    if register(message):
        data = load_data('database1')
        datas = load_data('database')
        counter = datas[str(message.chat.id)]['counter']
        if datas[str(message.chat.id)]['1_level']:
            print(counter)
            try:
                with open(data['underwater_city'][str(counter)][1], 'rb') as img:
                    bot.send_photo(message.chat.id, img)
            except Exception as error:
                print(str(error) + ' underwater_city')
            if counter >= len(data['underwater_city']):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = make_button('/continue_castle_on_mountain🏁')
                btn2 = make_button('/continue_dark_forest🏁')
                markup.row(btn1, btn2)
                bot.send_message(message.chat.id, data['underwater_city'][str(counter)][0],
                                 reply_markup=markup)
                counter = 1
                datas[str(message.chat.id)]['counter'] = counter
                datas[str(message.chat.id)]['2_level'][0] = True
                datas[str(message.chat.id)]['2_level'][1] = 'underwater_city'
                change_data(datas, 'database')
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = make_button('/continue_underwater_city🏁')
                markup.row(btn1)
                bot.send_message(message.chat.id, data['underwater_city'][str(counter)][0],
                                 reply_markup=markup)
                counter += 1
                datas[str(message.chat.id)]['counter'] = counter
                change_data(datas, 'database')
        else:
            bot.send_message(message.chat.id, 'Пройдите предыдущие уровни',
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = make_button('/register')
        markup.row(btn1)
        bot.send_message(message.chat.id, 'Пройдите регистрацию написав команду "/register"',
                         reply_markup=markup)


@bot.message_handler(commands=['continue_abandoned_mine🏁', 'continue_abandoned_mine'])
def abandoned_mine(message):
    if register(message):
        data = load_data('database1')
        datas = load_data('database')
        counter = datas[str(message.chat.id)]['counter']
        if datas[str(message.chat.id)]['2_level']:
            print(counter)
            try:
                with open(data['abandoned_mine'][str(counter)][1], 'rb') as img:
                    bot.send_photo(message.chat.id, img)
            except Exception as error:
                print(str(error) + ' abandoned_mine')
            if datas[str(message.chat.id)]['counter'] >= len(data['abandoned_mine']):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = make_button('/continue_city_edge_world🏁')
                btn2 = make_button('/continue_lost_city🏁')
                markup.row(btn1, btn2)
                counter = 1
                datas[str(message.chat.id)]['counter'] = counter
                datas[str(message.chat.id)]['2_level'][0] = True
                datas[str(message.chat.id)]['2_level'][1] = 'abandoned_mine'
                change_data(datas, 'database')
                bot.send_message(message.chat.id, data['abandoned_mine'][str(counter)][0],
                                 reply_markup=markup)

            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = make_button('/continue_abandoned_mine🏁')
                markup.row(btn1)
                bot.send_message(message.chat.id, data['abandoned_mine'][str(counter)][0],
                                 reply_markup=markup)
                counter += 1
                datas[str(message.chat.id)]['counter'] = counter
                change_data(datas, 'database')
        else:
            bot.send_message(message.chat.id, 'Пройдите предыдущие уровни',
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = make_button('/register')
        markup.row(btn1)
        bot.send_message(message.chat.id, 'Пройдите регистрацию написав команду "/register"',
                         reply_markup=markup)


def commands(data: dict) -> list:
    command = []
    for i in data:
        if len(data[i]) == 1:
            command.append(f'continue_{i}🏁')
            command.append(f'continue_{i}')
    return command


@bot.message_handler(commands=commands(load_data('database1')))
def another(message):
    if register(message):
        data = load_data('database1')
        datas = load_data('database')
        if datas[str(message.chat.id)]['2_level'][0]:
            print('true')
            if '🏁' in message.text:
                item = message.text[10:-1]
            else:
                item = message.text[10:]
            print(item)
            try:
                with open(data[item]['1'][1], 'rb') as img:
                    bot.send_photo(message.chat.id, img)
            except:
                pass
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # btn1 = make_button(f'/continue_{item}🏁')
            # markup.row(btn1)
            bot.send_message(message.chat.id, data[item]['1'][0], reply_markup=types.ReplyKeyboardRemove())
            if data[item]['1'][2]:
                lose(message)
            else:
                win(message)
            datas[str(message.chat.id)]['3_level'] = True
            change_data(datas, 'database')
        else:
            bot.send_message(message.chat.id, 'Пройдите предыдущие уровни',
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = make_button('/register')
        markup.row(btn1)
        bot.send_message(message.chat.id, 'Пройдите регистрацию написав команду "/register"',
                         reply_markup=markup)


def lose(message):
    try:
        with open('Images/img/end/i.webp', 'rb') as img:
            bot.send_photo(message.chat.id, img)
    except:
        pass
    bot.send_message(message.chat.id, 'You lose!!!!!!!!!!', reply_markup=types.ReplyKeyboardRemove())


def win(message):
    try:
        with open('Images/img/end/i (1).webp', 'rb') as img:
            bot.send_photo(message.chat.id, img)
    except:
        pass
    bot.send_message(message.chat.id, 'You win!!!!!!!!!!', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['rules', 'rules🏁'])
def rules(message):
    bot.send_message(message.chat.id, 'Суть игры в том чтобы выбирать '
                                      'локации которые вы освободите от враждебной '
                                      'рассы.')


if __name__ == "__main__":
    main()
# else:
#
#     main()
