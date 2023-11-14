with open(".env", "r") as file:
    buffer = file.read()
    line_pos = buffer.find("BOT_TOKEN")
    TOKEN = buffer[buffer.find("=", line_pos) + 1:buffer.find("\n", line_pos)]
FILE = "data.json"
# Supported countries
countries = [
            {'emoji': '🇺🇸','name': 'США'}, {'emoji': '🇷🇺','name': 'Россия'}, 
            {'emoji': '🇵🇱','name': 'Польша'}, {'emoji': '🇨🇳','name': 'Китай'}, 
            {'emoji': '🇦🇽','name': 'Швеция'}, {'emoji': '🇦🇲','name': 'Армения'}, 
            {'emoji': '🇨🇿','name': 'Чехия'}, {'emoji': '🇩🇰','name': 'Дания'}, 
            {'emoji': '🇯🇴','name': 'Палестина'}, {'emoji': '🇪🇪','name': 'Эстония'}, 
            {'emoji': '🇪🇬','name': 'Египет'}, {'emoji': '🇧🇾','name': 'Беларусь'}, 
            {'emoji': '🇧🇷','name': 'Бразилия'}, {'emoji': '🇨🇦','name': 'Канада'}, 
            {'emoji': '🇫🇮','name': 'Финляндия'}, {'emoji': '🇫🇷','name': 'Франция'}, 
            {'emoji': '🇬🇷','name': 'Греция'}, {'emoji': '🇩🇪','name': 'Германия'}, 
            {'emoji': '🇬🇪','name': 'Грузия'}, {'emoji': '🇧🇬','name': 'Болгария'}, 
            {'emoji': '🇷🇴','name': 'Румыния'}, {'emoji': '🇹🇷','name': 'Турция'}, 
            {'emoji': '🇮🇹','name': 'Италия'}, {'emoji': '🇸🇰','name': 'Словакия'}, 
            {'emoji': '🇸🇦','name': 'Саудовская аравия'}
]
# Supported types of jobs
works = [
        "IT", "Завод", "Финансы, банкинг",
        "Строительство", "Добыча ископаемых",
        "Обслуживание", "Медицина", "Работа с персоналом", "Преподавание"
]
# Age of people
ages = [
    "от 0 до 18",
    "от 18 до 25",
    "от 26 до 35",
    "от 36 до 50",
    "от 50 до смерти",
]
sexes = [
    "Мужчина",
    "Женщина"
]
cars = [
    "Есть машина",
    "Нет машины"
]
menu = [
    "Начать опрос",
    "Показать статистику",
    "Настроить статистику"
]
format_settings_menu = [
    "в абсолютных числах",
    "в процентах",
]
division_type = format_settings_menu[0]
