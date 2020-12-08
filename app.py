import datetime
import random
import time

from flask import Flask
from flask import render_template
from flask import request

from sqlalchemy import create_engine
from sqlalchemy import delete
from sqlalchemy import Column, Integer, Text, MetaData, Table, select
from sqlalchemy.exc import OperationalError

# virtualenv env # создание вирт. окружение
# source env/bin/activate
# pip install Flask

app = Flask(__name__)

metadata = MetaData()

messages = Table(
    'messages', metadata,
    Column('id', Integer, primary_key=True),
    Column('timestamp', Integer),
    Column('username', Text),
    Column('message', Text),
    )
db_engine = create_engine('sqlite:///base.db')
try:
    messages.create(bind=db_engine)
except OperationalError as error:
    print(str(error).split('\n')[0])


@app.route('/')
def index():
    stmt = select([messages])
    bruh = db_engine.execute(stmt).fetchall()
    msgs = [{'id': idx, 'timestamp': ts, 'author': au, 'message': msg} for idx, ts, au, msg in bruh]
    padding = 'style="padding:10px"'
    message_table_head = '<table align="center" border="2"><tr><th {0}>ID</th><th {0}>Время</th><th {0}>Автор</th><th {0}>Сообщение</th></tr>'.format(padding)
    message_table_content = ['<tr><td {0}>{1}</td><td {0}>{2}</td><td {0}>{3}</td><td {0}>{4}</td></tr>'.format(padding, msg['id'], datetime.datetime.utcfromtimestamp(msg['timestamp']).strftime('%Y-%m-%dT%H:%M:%SZ'), msg['author'], msg['message']) for msg in msgs]
    message_table_tail = '</table>'
    message_table = ''.join(
        [message_table_head,
        ''.join(message_table_content),
        message_table_tail]
        )

    return render_template('index.html', appname='Чат', content=message_table)


def command(id):
    return f'running command with {id}'


app.add_url_rule('/command/<id>', 'command', command)


@app.route('/add/message', methods=['POST'])
def add_message():
    insert_message = messages.insert().values(id=random.randint(1, 99999999), timestamp=int(time.time()), username=request.form['username'], message=request.form['msgtxt'])
    db_engine.execute(insert_message)

    stmt = select([messages])
    bruh = db_engine.execute(stmt).fetchall()
    msgs = [{'id': idx, 'timestamp': ts, 'author': au, 'message': msg} for idx, ts, au, msg in bruh]
    padding = 'style="padding:10px"'
    message_table_head = '<table align="center" border="2"><tr><th {0}>ID</th><th {0}>Время</th><th {0}>Автор</th><th {0}>Сообщение</th></tr>'.format(padding)
    message_table_content = ['<tr><td {0}>{1}</td><td {0}>{2}</td><td {0}>{3}</td><td {0}>{4}</td></tr>'.format(padding, msg['id'], datetime.datetime.utcfromtimestamp(msg['timestamp']).strftime('%Y-%m-%dT%H:%M:%SZ'), msg['author'], msg['message']) for msg in msgs]
    message_table_tail = '</table>'
    message_table = ''.join(
        [message_table_head,
        ''.join(message_table_content),
        message_table_tail]
        )

    return render_template('index.html', appname='Чат', content=message_table)


@app.route('/remove/message', methods=['POST'])
def remove_message():
    delete_message = delete(messages).where(messages.c.id == int(''.join(i for i in request.form['id'] if i.isdigit())))
    db_engine.execute(delete_message)

    stmt = select([messages])
    bruh = db_engine.execute(stmt).fetchall()
    msgs = [{'timestamp': ts, 'author': au, 'message': msg} for idx, ts, au, msg in bruh]
    padding = 'style="padding:10px"'
    message_table_head = '<table align="center" border="2"><tr><th {0}>Время</th><th {0}>Автор</th><th {0}>Сообщение</th></tr>'.format(padding)
    message_table_content = ['<tr><td {0}>{1}</td><td {0}>{2}</td><td {0}>{3}</td></tr>'.format(padding, datetime.datetime.utcfromtimestamp(msg['timestamp']).strftime('%Y-%m-%dT%H:%M:%SZ'), msg['author'], msg['message']) for msg in msgs]
    message_table_tail = '</table>'
    message_table = ''.join(
        [
    	    message_table_head,
            ''.join(message_table_content),
            message_table_tail
			]
        )

    return render_template('index.html', appname='Чат', content=message_table)


if __name__ == '__main__':
    app.run()

