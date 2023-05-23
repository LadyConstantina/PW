from flask import Flask
from flask import request
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
import requests
import uuid
 
app = Flask(__name__)

__BOT_TOKEN = '6112376366:AAGg6qRTZR_smiL3sTafCGL7tCN6MOaXbrQ'
URL = 'https://b1be-89-41-121-123.ngrok-free.app/'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///telegram_bot.db"
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)

class News(db.Model):
    ID = db.Column(db.String(64), primary_key = True)
    USER_ID = db.Column(db.String(64), unique = False)
    URL = db.Column(db.String(32), unique = False)

class Users(db.Model):
    USER_ID = db.Column(db.String(64), primary_key = True)
    NAME = db.Column(db.String(64), unique = False)

@app.before_first_request
def create_tables():
    db.create_all()

def save_user(user_id,name):
    user = Users.query.filter_by(USER_ID = user_id).first()
    if user:
        return "User already saved."
    else:
        new_user = Users(
            USER_ID = user_id,
            NAME = name
        )
        db.session.add(new_user)
        db.session.commit()
        return "New user added."

def save_news(chat_id,url):
    new_save = News(
        ID = str(uuid.uuid1()),
        USER_ID = chat_id,
        URL = url
    )
    db.session.add(new_save)
    db.session.commit()
    return send_msg(chat_id,"News saved succesfully!")

def send_msg(chat_id,message):
    url = f'https://api.telegram.org/bot{__BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text':message
    }
    return requests.post(url,json=data)

def get_news(args):
    if len(args) > 0 :
        query = '%20'.join(args)
        url = (f'https://newsapi.org/v2/everything?'
            f'q="{query}"&'
            f'language=en&'
            f'sortBy=publishedAt&'
            f'apiKey=2fa21cb27174422d9d062d3840529d2b')
    else:
        url = (f'https://newsapi.org/v2/top-headlines?'
            f'sources=google-news&'
            f'apiKey=2fa21cb27174422d9d062d3840529d2b')
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'ok':
        articles = data['articles'][0:6]
        news = []
        for i in range(5):
            title = articles[i]['title']
            add = articles[i]['url']
            news.append((title,add))
        return news
    else:
        return []

def send_news(chat_id,news):
    text = ""
    for article in news:
        title, url = article
        text = f'Title: {title} \n Access at {url} \n'
        send_msg(chat_id,url)
    return []


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id = msg['message']['chat']['id']
        text = msg['message']['text'].split(' ')
        command = text[0]
        args = []
        if len(text) > 1 :
            args = text[1:]

        if command == '/start':
            print(save_user(chat_id,msg["message"]["from"]["first_name"]))
            send_msg(chat_id,f'Hello, {msg["message"]["from"]["first_name"]}! What can I do for you today?')
        elif command == '/latest_news':
            news = get_news(args)
            send_news(chat_id,news)
        else:
            send_msg(chat_id,f'Unrecognised command --> {command} \n Type /help for a list of available commands.')
        
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"

@app.route('/webhook/')
def setwebhook():
    response = requests.get(f'https://api.telegram.org/bot{__BOT_TOKEN}/setWebhook?url={URL}')
    if response:
        return "OK"
    else:
        return "Error"







if __name__ == '__main__':
   app.run(debug=True)