from flask import Flask
from flask import request
from flask import Response
from flask_sqlalchemy import SQLAlchemy
import requests
import uuid
import urllib.parse
 
app = Flask(__name__)

__BOT_TOKEN = "YOUR TOKEN"
URL = 'https://189f-89-41-121-123.ngrok-free.app'
HELP = ''' Commands Available:
/start  - start the session with bot
/latest_news [args]   - get latest news on a topic or in general
/save_news  url   - save one url
/saved_news   - see saved news
/delete_news  url   - delete the url from saved news
/fun_fact_cat    - get a fun fact about cats
'''

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///telegram_bot.db"
db = SQLAlchemy(app)

requests.get(f'https://api.telegram.org/bot{__BOT_TOKEN}/setWebhook?url={URL}')

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

def delete_news(user_id,url):
    select_list = News.query.filter_by(URL = url, USER_ID = str(user_id)).all()
    if not select_list:
        return send_msg(user_id,"No such URL saved.")
    for record in select_list:
        db.session.delete(record)
    db.session.commit()
    return send_msg(user_id,"URL deleted succesfully.")

def get_saved_news(user_id):
    select = News.query.filter_by(USER_ID = str(user_id)).all()
    if not select:
        return send_msg(user_id,"No news saved.")
    text = "You have saved the following news: \n\n"
    id = 1
    for row in select:
        text += f'News{id}: {row.URL} \n\n'
        id += 1
    return send_msg(user_id,text)

def send_msg(chat_id,message):
    url = f'https://api.telegram.org/bot{__BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text':message
    }
    return requests.post(url,json=data)

def get_news(args):
    if len(args) > 0 :
        args_safe = []
        for word in args:
            args_safe.append(urllib.parse.quote(word, safe=''))
        query = '%20'.join(args_safe)
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
        if data['totalResults'] == 0:
            return []
        else:
            news_nr = min(data['totalResults'],5)
        articles = data['articles'][0:news_nr+1]
        news = []
        for i in range(news_nr):
            add = articles[i]['url']
            news.append(add)
        return news
    else:
        return []

def send_news(chat_id,news):
    if not news:
        send_msg(chat_id,"No news on the chosen topic.")
    for article in news:
        send_msg(chat_id,article)
    return []

def get_fun_fact_cat(chat_id):
    response = requests.get('https://catfact.ninja/fact')
    fact = response.json()
    return send_msg(chat_id,f'Fun fact: {fact["fact"]}')


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        if 'message' in msg:
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
            elif command == '/save_news' and len(args)>0:
                save_news(chat_id,args[0])
            elif command == '/saved_news':
                get_saved_news(chat_id)
            elif command == '/delete_news' and len(args)>0:
                delete_news(chat_id,args[0])
            elif command == '/fun_fact_cat':
                get_fun_fact_cat(chat_id)
            elif command == '/help':
                send_msg(chat_id,HELP)
            else:
                send_msg(chat_id,f'Unrecognised command --> {command} \n Type /help for a list of available commands.')
        
            return Response('ok', status=200)
        else:
            return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1><h3>To try my new bot, find him -> <a href='https://t.me/faf202_Gilca_Constantina_bot'>HERE</a> <-</h3>"


if __name__ == '__main__':
   app.run(debug=False)
