# messages.py

START_BUY_MESSAGE = (
    "Вы начали процесс покупки. Пройдите шаги 1-6 до конца или прервите процесс нажатием /stop\n\nШаг 1/6. Введите "
    "вашу фамилию и имя на английском языке: "
)

ERROR_MESSAGE = "Произошла ошибка, обратитесь в поддержку /help"

STEP1_MESSAGE = "Шаг 2/6. Введите дату, когда нужна проходка (в формате ДД.ММ.ГГГГ):"

STEP2_MESSAGE = "Шаг 3/6. Напишите юзернейм или номер телефона в телеграме. Туда мы отправим проходку:"

STEP3_MESSAGE = "Шаг 4/6. Введите страну, город и название аэропорта, в котором нужна проходка:"

STEP4_MESSAGE = (
    "Шаг 5/6. Пришлите скриншот выбранного бизнес-зала пройдя по ссылке https://m.everylounge.app/home и нажав "
    "«Выбрать бизнес-зал» . \nСайт открывается несколько секунд.\nРегистрироваться на сайте не нужно.\nВнимательно "
    "проверяйте режим работы выбранного бизнес зала и терминал. "
)

STEP4_INSTRUCTION_MESSAGE = "Инструкция по выбору бизнес-зала."

STEP5_ERROR_MESSAGE = ("Пожалуйста, пришлите именно скриншот выбранного бизнес-зала. Если у вас возникли сложности, "
                        "напишите нам в поддержку /help. ")

ORDER_SAVED_MESSAGE = (
    "Ваш заказ №{order_number} сохранен.\n\nИмя: {name}\nАэропорт: {airport}\nДата: {date}\nЕсли все верно, "
    "перходим к оплате.\n "
)

STEP6_MESSAGE = (
    "Шаг 6/6. Пришлите скриншот оплаты на сумму 999 рублей по номеру карты 5280413752652326\nКоментарий при оплате "
    "добавлять не нужно.\n\nК каждому заказу обязательно должен быть приложен скриншот оплаты.\n\nПосле оплаты в "
    "течение 20-40 минут вы получите QR-код, который нужно показать на входе в бизнес-зал вместе с посадочным "
    "талоном.\n "
)

STEP6_ERROR_MESSAGE = "Пожалуйста, пришлите именно скриншот оплаты."

ORDER_ACCEPTED_MESSAGE = (
    "Ваш заказ №{order_number} принят. Ожидайте QR-код в течение 20-40 минут. В случае необходимости пишите "
    "администратору /help "
)

PRODUCTION_ORDER_CAPTION = "Бизнес зал заказа номер {order_number}"

START_MESSAGE = "Привет! Я Проходкин бот.\nИспользуйте команду /buy для покупки проходки в бизнес-зал, /stop для прекращения оформления проходки и /help для связи с администратором."

STOP_MESSAGE = "Процесс остановлен. Все данные очищены. Чтобы начать покупку нажмите /buy"

QR_CODE_ERROR_MESSAGE1 = "Подписи к фото нет. Подпишите фотографию и обязательно укажите номер заказа. Попробуйте еще раз."

QR_CODE_ERROR_MESSAGE2 = "Такого заказа не найти. Возможно вы не указали номер заказа. Попробуйте еще раз, или напишите администратору /help"

QR_CODE_THANK_YOU_MESSAGE = (
    "Спасибо, что воспользовались нашим сервисом. Приятного полета! \n"
    "Будем благодарны вам за фотоотзыв, а также за рекомендацию нашего сервиса вашим друзьям и знакомым ❤\n\n"
    "Подписывайтесь на наш канал @proxodkin и Инстаграм https://www.instagram.com/proxodkin. Там много полезной информации и анонсы распродаж от авиакомпаний!\n"
)

QR_CODE_ORDER_NOT_FOUND_MESSAGE = "Такого заказа не найти. Попробуйте еще раз, или напишите администратору /help"

START_HELP_MESSAGE = "Шаг 1. Напишите, что случилось:"

SUPPLIER_MESSAGE_TEMPLATE = "!!!ОБРАЩЕНИЕ ОТ ПОСТАВЩИКА!!!\nПользователь @{username} ({user_id}) сообщил:\n{issue}"

SUPPORT_MESSAGE_TEMPLATE = "!!!ОБРАЩЕНИЕ В ПОДДЕРЖКУ!!!\nПользователь @{username} ({user_id}) сообщил:\n{issue}"

CONFIRMATION_MESSAGE = "Ваше сообщение отправлено диспетчеру. Ожидайте ответ в ближайшие 20 минут."
