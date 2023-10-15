import telebot, datetime, json, random, urllib.request

HOST = '62.217.177.120'
PORT = 8069
DB = 'odoo'
USER = 'k@lmyk.ru'
PASS = 'Kalmyk244kk_'

BOT_TOKEN = "5704394405:AAEQcpb0t8GJ69imJXVbn7d2fdAbc0hScmE"

bot = telebot.TeleBot(BOT_TOKEN)


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type": "application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]


def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})


# log in the given database
url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    my_task = str(datetime.datetime.fromtimestamp(message.date).strftime('%d-%m %H:%M')), str(message.text)

    # create a new note
    args = {
        'company_id': 1,
        'kanban_state': 'normal',
        'name': my_task
    }

    note_id = call(url, "object", "execute", DB, uid, PASS, 'project.task', 'create', args)


bot.infinity_polling()
