init_menu_welcome = "Добро пожаловать в новую версию Либре-такси!\nИсходный код: https://github.com/ro31337/libretaxi\nЗапрограммировал Роман Пушкин и друзья\nЛицензия: AGPL-3.0"

ask_location_menu_click_next = "Нажмите \"Далее\" (с мессенжера в телефоне) чтобы установить локацию. Или 📎 скрепка -> 📍 Местоположение для большей приватности."

ask_location_menu_next_button = "Далее"

feed_menu_greeting = "Тут вы увидите 🚗 водителей и 👋 пассажиров."

feed_menu_search_button = "Найти 🚗 или 👋"

feed_menu_location_button = "📍 Сменить локацию"

feed_menu_location_changed = "👌 Новая локация установлена"

feed_menu_error = "😕 Не могу понять ваш выбор, попробуйте нажать 🔳 иконку ниже 👇"

post_menu_report_button = "☝️️Пожаловаться ⚠️"

post_menu_wait = "🕙 Подождите 5 минут"

# Do not translate /cancel
post_menu_copy_and_paste = "Скопируйте текст, который начинается с 🚗 (если вы водитель) или 👋 (если пассажир) и измените необходимые поля, или /cancel:"

post_menu_driver_example = "🚗 Подвезу\nОткуда: район Речного вокзала\nКуда: на Дубровку\nДата: сегодня\nВремя: сейчас\nОплата: наличные, на карту сбер\n"

post_menu_passenger_example = "👋 Ищу водителя\nОткуда: Дубровская улица, дом 1\nКуда: аэропорт\nДата: сегодня\nВремя: сейчас\nПассажиров: 1"

# Here is how we check if the user just copied the text or changed it. It's just a string from the previous postings.
# Note how we have "foobar" in both postings above. It's the magic string, non-existent address, you should think
# about an address that doesn't exist in your own language. Or you can leave "foobar" if you didn't get it ;)
# Keep it lowercased!
validation_dummy_addr_lowercase = "дубров"

post_menu_sent = "✅ Отправлено всем в радиусе 25 км и в @libretaxi_all"

# "Contact" is a verb here. For example, we'll have a posting where it says "blabla, I'm looking for ride, contact @username".
# So you're translating this verb "contact" below.
post_menu_via = "Контакт: "

# When we have an error we say something like:
# "Your input is invalid, try again or /cancel"
# So this "or" part needs to be translated below. Important: keep space at the end!
post_menu_or = "или"

validation_text_too_long = "🚫 Сообщение очень длинное, 300 букв максимум (у вас %d)"

validation_text_too_short = "🚫 Текст слишком короткий, 20 букв минимум (у вас %d)"

validation_prefix = "🚫 Текст должен начинаться с 🚗 или 👋"

validation_no_at = "🚫 Не указывайте символ @"

validation_no_offensive_language = "🚫 Уважайте культуру речи 🤦"

validation_change_from_to = "🚫 Еще раз, но измените \"Откуда\" и \"Куда\""

validation_empty_lines1 = "🚫 Две пустые строки максимум, если можно (у вас %d)"

validation_empty_lines2 = "🚫 Девять строк максимум пожалуйста (у вас %d)"

validation_min_lines = "🚫 Надо хотя бы пять строк (у вас %d)"

main_welcome_link = "https://telegra.ph/Novaya-versiya-Libre-taksi-vam-ponravitsya-02-08"