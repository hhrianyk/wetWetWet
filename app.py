from flask import Flask, render_template, request  # Flask — веб-фреймворк, render_template — для рендерингу HTML, request — для отримання даних з форм
import requests  # Для HTTP-запитів до API погоди
import os  # Для роботи з файловою системою та поточною директорією
from datetime import datetime  # Для формування часу оновлення даних

# Ініціалізація Flask-додатку
# template_folder і static_folder встановлюються як поточна директорія, щоб шаблони та стилі знаходилися в одному місці
app = Flask(__name__, template_folder=os.getcwd(), static_folder=os.getcwd())


def get_weather(city):
    """
    Отримує дані про погоду з API wttr.in для заданого міста.
    :param city: Назва міста
    :return: Словник з погодними даними або None, якщо запит не вдався
    """
    # Формуємо URL для запиту у форматі JSON
    url = f"https://wttr.in/{city}?format=j1"

    # Виконуємо GET-запит
    response = requests.get(url)

    # Якщо API повернув успішну відповідь
    if response.status_code == 200:
        data = response.json()  # Отримуємо JSON як Python-словник

        # Поточні умови погоди
        current = data["current_condition"][0]

        # Прогноз на перший день
        weather = data["weather"][0]

        # Формуємо словник з даними, які передамо в шаблон
        return {
            "city": city.capitalize(),  # Назва міста з великої літери
            "country": data["nearest_area"][0]["country"][0]["value"],  # Країна
            "temperature": current["temp_C"],  # Температура зараз
            "feels_like": current["FeelsLikeC"],  # Відчувається як
            "description": current["weatherDesc"][0]["value"],  # Опис погоди
            "icon": current["weatherIconUrl"][0]["value"],  # URL до іконки погоди
            "humidity": current["humidity"],  # Вологість у %
            "wind": current["windspeedKmph"],  # Швидкість вітру у км/год
            "pressure": current["pressure"],  # Атмосферний тиск у гПа
            "sunrise": weather["astronomy"][0]["sunrise"],  # Час сходу сонця
            "sunset": weather["astronomy"][0]["sunset"],  # Час заходу сонця
            "clouds": current["cloudcover"],  # Хмарність у %
            "precipitation": current["precipMM"],  # Опади у мм
            "update_time": datetime.now().strftime("%H:%M:%S")  # Поточний час оновлення
        }
    else:
        # Якщо API не відповів, повертаємо None
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Головний маршрут веб-додатку.
    Якщо користувач вводить місто (POST), показуємо його погоду.
    Якщо відкриває сторінку вперше (GET) — показуємо погоду в Києві.
    """
    if request.method == "POST":
        # Отримуємо назву міста з форми
        city = request.form.get("city")
        weather_data = get_weather(city)
    else:
        # За замовчуванням показуємо погоду в Києві
        weather_data = get_weather("Київ")

    # Передаємо дані в HTML-шаблон
    return render_template("index.html", weather=weather_data)


    # Запускаємо Flask-додаток на 0.0.0.0 (доступ з усіх IP)
port = int(os.environ.get('PORT', 5000))  # Можна змінити через змінну середовища PORT
app.run(host="0.0.0.0", port=port, debug=False)
