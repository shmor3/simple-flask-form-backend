from flask import Flask, request, redirect
import os
import sqlite3
import cryptocode
import random
import string


app = Flask(__name__)
secret_key = os.urandom(24).hex()
app.config['SECRET_KEY'] = secret_key


@app.route('/$<a>', methods=('GET', 'POST'))
def formSubmition(a):
    connection = sqlite3.connect("messages.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS messages (id INTEGER, message TEXT)")
    if a == 'submit':
        if request.method == 'POST':
            try:
                rNum = []
                for x in range(8):
                    rNum.append(str(random.choice(list(string.digits))))
                messageId = ''.join(rNum)
                message = str(request.form).replace(
                    'ImmutableMultiDict', '').replace('>', '')
                cursor.execute("INSERT INTO messages VALUES ('" + messageId +
                               "', '" + cryptocode.encrypt(str(message), '0000') + "')")
                connection.commit()
                with open('new-messages', 'a') as file:
                    file.write(messageId + '\n')
                print(messageId + ': ' + str(message))
            except:
                pass
            return redirect('https://rstanford.com', code=302)
    else:
        if request.method == 'GET':
            fetchMessage = cryptocode.decrypt(str(cursor.execute(
                "SELECT message FROM messages WHERE id = ?", (a,)).fetchone()), '0000')
            return str(fetchMessage)
    return redirect('https://rstanford.com', code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9387)
