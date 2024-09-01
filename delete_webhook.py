import requests

TOKEN = '7392931002:AAEgffxxN2MptXKQ48mhQKY-HGc2SIhimes'  # Замість 'YOUR_BOT_TOKEN' вставте ваш фактичний токен бота
url = f'https://api.telegram.org/bot{TOKEN}/deleteWebhook'

response = requests.get(url)

if response.status_code == 200:
    print('Webhook успішно видалено.')
else:
    print('Помилка при видаленні Webhook:', response.text)
