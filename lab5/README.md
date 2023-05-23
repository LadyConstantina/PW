# Lab 5 - Backend development

## Story

Imagine, you're a developer at Newsroom SRL, a local company which runs a site for business news. On a regular meeting you propose to launch an Telegram bot along with the web site. Your idea looks nice, but the CTO has requested a proof-of-concept application before main development starts.

## Task

1. Follow [this basic tutorial](https://core.telegram.org/bots/tutorial) to create a Telegram bot using [@BotFather](https://t.me/botfather) bot - name it using the format `faf20x_<your name>_<your surname>_bot` and save the __token__ in a safe place;
2. Pick a backend framework and programming language of your choice;
3. Your application should use Telegram [webhooks](https://core.telegram.org/bots/api#setwebhook) to respond to updates from chats;
4. Use a reverse proxy to establish a secure communication between your local web server and Telegram e.g. Ngrok;
5. Your bot should implement at least the following commands:
  - `/start` - to show a greeting;
  - `/latest_news` with optional parameter `topic` - to search for latest news on some topic (up to 5 links);
  - `/save_news` with required parameter `url` - to add the URL to the saved news for the given user;
  - `/saved_news` - to show a list of saved news for the given user.

6. Your application should send HTTP requests to some news API aggregators (e.g. Google News API, NYT API) to fetch the news;

## Special conditions

No special conditions.

## Grading

Points:
  - basic Telegram bot with `/start` - `7` point
  - the bot implements `/latest_news` command - `+1` point
  - the bot implements `/save_news` command - `+1` point
  - the bot implements `/saved_news` command - `+1` point

You can get `+1` point for implementing other non-trivial functions (up to 2 functionalities)

## Hints

- Have a look on the official [FAQ](https://core.telegram.org/bots/faq#general-questions) on Telegram.
- If you already know a backend framework - use it!
- If you don't, use Flask, Sinatra or Express.
- Use SQLite3 as RDBMS, if you're unsure what DBMS to use. Other good choices - PostgreSQL, MongoDB.
