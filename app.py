from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

# Здесь мы будем хранить список тех, кто зашел
visitors = []

# Главная страница сайта (то, что видят пользователи)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Мой крутой сайт</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 50px; background: #282c34; color: white; }
        .box { padding: 30px; background: #444; display: inline-block; border-radius: 10px; }
        h1 { color: #61dafb; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Привет!</h1>
        <p>Ты находишься на моем сайте.</p>
        <p>Спасибо за посещение этого сайта</p>
    </div>
    <div style="margin-top: 20px;">
        <img src="https://i.postimg.cc/CK35DjxR/Atomic-Heart-sample.jpg" 
        alt="Моя фотография" 
        style="border-radius: 15px; max-width: 100%;">
    </div>
</body>
</html>
"""

# Страница для АДМИНА (только для тебя), где виден список IP
ADMIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Админка: Кто на сайте</title>
    <style>
        body { font-family: monospace; background: #1e1e1e; color: #00ff00; padding: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #333; padding: 10px; text-align: left; }
        th { background: #333; color: white; }
        .refresh { margin-bottom: 20px; color: #fff; }
    </style>
    <meta http-equiv="refresh" content="5"> <!-- Страница обновляется каждые 5 секунд -->
</head>
<body>
    <h1>👀 Список IP-адресов на сайте (обновляется каждые 5 сек)</h1>
    <table>
        <tr>
            <th>Время</th>
            <th>IP-адрес</th>
            <th>Браузер (User-Agent)</th>
        </tr>
        {% for v in visitors %}
        <tr>
            <td>{{ v.time }}</td>
            <td>{{ v.ip }}</td>
            <td>{{ v.agent[:50] }}...</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    # Получаем IP пользователя
    # Если сайт за прокси/Cloudflare, иногда IP может быть в заголовке X-Forwarded-For
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Добавляем в список (чтобы не было дублей подряд, можно проверять, но для простоты просто пишем)
    visitors.append({
        "ip": user_ip,
        "time": current_time,
        "agent": user_agent
    })

    # Ограничиваем список последними 50 визитами, чтобы не тормозило
    if len(visitors) > 50:
        visitors.pop(0)

    return HTML_PAGE

@app.route('/admin')
def admin():
    # Эта страница только для тебя (показываем всех, кто заходил)
    return render_template_string(ADMIN_PAGE, visitors=reversed(visitors)) # Выводим свежие сверху

if __name__ == '__main__':
    print("Сервер запущен!")
    print("Сайт для людей: http://127.0.0.1:5000")
    print("Твоя админка: http://127.0.0.1:5000/admin")
    app.run(host='0.0.0.0', port=5000, debug=True)
