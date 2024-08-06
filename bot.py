> Oleg:
import random
import telebot
from telebot import types
import random
import time

TOKEN = '' # Заменить TOKEN
bot = telebot.TeleBot(TOKEN)

questions = [
    {
        'question': 'Операционная система на которой вам предстоит работать',
        'options': ['Linux', 'Windows', 'MacOS'],
        'correct_answer': 'MacOS'
    },
    {
        'question': 'Пароль от wi-fi в кампусе',
        'options': ['school21', 's21kzn', 'school21kzn', 'peer2peer', 'peertopeer'],
        'correct_answer': 'peer2peer'
    },
    {
        'question': 'Сколько лет казанскому кампусу?',
        'options': ['2 года', '3 года', '4 года', '5 лет'],
        'correct_answer': '3 года'
    },
    {
        'question': 'В каком месяце мы празднуем день рождения нашего кампуса?',
        'options': ['Декабрь', 'Январь', 'Февраль', 'Март', 'Апрель'],
        'correct_answer': 'Февраль'
    },
    {
        'question': 'Скольо рабочих мест у нас в кампусе?',
        'options': ['567 мест', '613 места', '543 места', '498 мест'],
        'correct_answer': '567 мест'
    },
    {
        'question': 'Правильное написаниие сайта с вашими заданиями, проверками, календарем и всем остальным',
        'options': ['kzn-edu.21-school.ru', 'edu.21-school.ru', 'edu-21-school.ru', 'edu.21.school.ru', 'edu-kzn.21-school.ru', 'edu.kazan.21-school.ru'],
        'correct_answer': 'edu.21-school.ru'
    },
    {
        'question': 'Корректный формат ввода логина на сайте',
        'options': ['login@student-21.school.ru', 'login@student.21-school.ru', 'login@21-student.school.ru', 'login@21-school.student.ru'],
        'correct_answer': 'login@student.21-school.ru'
    }
]

compile_results = []
quiz_active = False
user_scores = {}

@bot.message_handler(commands=['start'])
def start(message):
    global quiz_active
    if not quiz_active:
        bot.send_message(message.chat.id, "Привет! Введите свой никнейм:")
        bot.register_next_step_handler(message, start_quiz)
    else:
        bot.send_message(message.chat.id, "Викторина уже активна.")

def start_quiz(message):
    global quiz_active, user_scores
    if not quiz_active:
        username = message.text
        user_id = message.from_user.id
        start_time = time.time()

        if user_id not in user_scores:
            user_scores[user_id] = {
                'username': username,
                'score': 0,
                'start_time': start_time,
                'current_question': 0
            }
            bot.send_message(message.chat.id, f"Начинаем викторину, {username}!")
            ask_question(user_id)
        else:
            bot.send_message(message.chat.id, "Вы уже участвуете в викторине.")
    else:
        bot.send_message(message.chat.id, "Викторина уже активна.")

def ask_question(user_id):
    if user_id in user_scores:
        question_index = user_scores[user_id]['current_question']
        if question_index < len(questions):
            question = questions[question_index]['question']
            options = questions[question_index]['options']
            random.shuffle(options)  

            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for option in options:
                callback_button = types.InlineKeyboardButton(text=option, callback_data=option)
                keyboard.add(callback_button)

            bot.send_message(user_id, question, reply_markup=keyboard)
        else:
            finish_quiz(user_id)


@bot.callback_query_handler(func=lambda call: True)
@bot.callback_query_handler(func=lambda call: True)
def process_answer(call):
    user_id = call.from_user.id
    response = call.data

> Oleg:
if user_id in user_scores:
        current_question_index = user_scores[user_id]['current_question']
        if current_question_index < len(questions):
            if response == questions[current_question_index]['correct_answer']:
                user_scores[user_id]['score'] += 1
            user_scores[user_id]['current_question'] += 1
            ask_question(user_id)
        else:
            finish_quiz(user_id)

def finish_quiz(user_id):
    global quiz_active
    if user_id in user_scores:
        score = user_scores[user_id]['score']
        start_time = user_scores[user_id]['start_time']
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        user_scores[user_id]['end_time'] = end_time
        bot.send_message(user_id, f"Викторина окончена!\n"
                                  f"Никнейм: {user_scores[user_id]['username']}\n"
                                  f"Время выполнения: {elapsed_time} сек\n"
                                  f"Количество правильных ответов: {score}")
        send_results()
        quiz_active = False

def send_results():
    results = []
    for user_id, user_data in user_scores.items():
        username = user_data['username']
        score = user_data['score']
        start_time = user_data['start_time']
        end_time = user_data.get('end_time')
        elapsed_time = round(end_time - start_time, 2) if end_time is not None else None
        result = f"<b>Никнейм:</b> {username}\n" \
                 f"<b>Время выполнения:</b> {elapsed_time} сек\n" \
                 f"<b>Количество правильных ответов:</b> {score}"
        results.append(result)

    chat_id1 = '864251663'  # Заменить ID
    chat_id2 = '683033190'  # Заменить ID
    message = "\n\n".join(results)
    bot.send_message(chat_id1, f"<b>Результаты викторины:</b>\n\n{message}", parse_mode='HTML')
    bot.send_message(chat_id2, f"<b>Результаты викторины:</b>\n\n{message}", parse_mode='HTML')

    

@bot.message_handler(commands=['results'])
def send_quiz_results(message):
    if user_scores:
        send_results()
    else:
        bot.send_message(message.chat.id, "Нет доступных результатов викторины.")
