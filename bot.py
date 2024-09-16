import telebot
from telebot import types

bot = telebot.TeleBot('')

user_data = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я чат-бот для сбора информации. Используйте команду /collect для ввода данных и /show для просмотра последних 5 блоков.")

@bot.message_handler(commands=['collect'])
def collect_info(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        user_data[chat_id] = []

    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(chat_id, "Введите вашу фамилию:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_lastname_step)

def process_lastname_step(message):
    chat_id = message.chat.id
    user_data[chat_id].append({'lastname': message.text})
    
    msg = bot.send_message(chat_id, "Введите ваше имя:")
    bot.register_next_step_handler(msg, process_firstname_step)

def process_firstname_step(message):
    chat_id = message.chat.id
    user_data[chat_id][-1]['firstname'] = message.text

    msg = bot.send_message(chat_id, "Введите вашу дату рождения (в формате ДД.ММ.ГГГГ):")
    bot.register_next_step_handler(msg, process_birthday_step)

def process_birthday_step(message):
    chat_id = message.chat.id
    user_data[chat_id][-1]['birthday'] = message.text

    bot.send_message(chat_id, "Информация успешно собрана!")

@bot.message_handler(commands=['show'])
def show_info(message):
    chat_id = message.chat.id

    if chat_id in user_data:
        last_five_blocks = user_data[chat_id][-5:]

        for i, user_info in enumerate(last_five_blocks, 1):
            info_str = f"Блок {i}:\nФамилия: {user_info['lastname']}\nИмя: {user_info['firstname']}\nДата рождения: {user_info['birthday']}\nПочта: {user_info['email']}\n"
            bot.send_message(chat_id, info_str)
    else:
        bot.send_message(chat_id, "Вы еще не ввели информацию. Используйте команду /collect для ввода данных.")

bot.polling(none_stop=True)