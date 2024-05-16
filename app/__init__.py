from flask import Flask, render_template, request, flash,g, redirect, url_for
import sqlite3


app = Flask(__name__)
app.secret_key = 'your_secret_key' 
DATABASE = ("database.db")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def create_table():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS PhoneBook (
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                city TEXT NOT NULL,
                country TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        db.commit()

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        city = request.form['city']
        country = request.form['country']
        phone =  request.form['phone']

        with get_db() as users:
            cursor = users.cursor()
            cursor.execute("Insert into phonebook(name, email, city, country, phone) values(?,?,?,?,?)", (name, email,city, country, phone))
            users.commit()
            flash("Contact details successfully saved!")       
        return render_template("index.html")

    else:
        return render_template('index.html')
     


@app.route('/contacts')

def contacts():
    with  get_db() as db:
        cursor = db.execute('Select * from phonebook')
        data = cursor.fetchall()
    return render_template('contacts.html', data = data)

@app.route('/contacts/<name>', methods=['POST'])
def delete_entry(name):
    with  get_db() as db:
        db.execute('DELETE from phonebook where name = ?', (name,))
        db.commit()
        flash(f'Entry for {name} was successfully deleted.')
        return redirect(url_for('contacts'))



if __name__ == '__main__':
    app.run(debug=False)


