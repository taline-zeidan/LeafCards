from flask import Flask, redirect, request, session, render_template, url_for, current_app
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import talk_to_db as ttd
import sqlite3
from flask import jsonify
import threading



app = Flask(__name__)
app.secret_key='8fc1a05cf18fd2b60d3befb6e475a0008f0e55568bffd4b3d45b6fb699465338'
#app.config['MAIL_SERVER'] = 'outlook.office365.com'
#app.config['MAIL_PORT'] = 993
#app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_USERNAME'] = 'leafcards123@gmail.com'
#app.config['MAIL_PASSWORD'] = 'ILoveCroi$$ant5'

mail_settings = {
    "MAIL_SERVER": 'outlook.office365.com',
    "MAIL_PORT": 993,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'leafcards@hotmail.com' ,
    "MAIL_PASSWORD": '$2a$04$7CdMYGwieBdN3ffuecmotejZ/pX2dbmips83pqGy1WTqIiy.O/gHi'
}

app.config.update(mail_settings)
mail = Mail(app)


print("All routes:", app.url_map)  # This will print all registered routes
#print("URL for signup:", url_for('signup'))  # This checks if the 'signup' route can be resolved

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm-salt')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='email-confirm-salt',
            max_age=expiration
        )
    except:
        return False
    return email

#this code WILL crash
@app.route('/')
def home():
    return redirect("/index")

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/discover")
def discover():
    return render_template('discover.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/signup', methods=['POST','GET'])
def register():
    msg = ''
    if request.method == "POST" and 'email' in request.form and 'password' in request.form and 'username' in request.form and 'confirm_password'in request.form:
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password!=confirm_password:
            msg='The passwords you entered do not match!'
            return render_template('signup.html',msg=msg)
        ttd.register_user(email,password)
        msg='Check your email to confirm your sign up!'
        thread = threading.Thread(target=send_signup_email_async, args=(current_app._get_current_object(), email, username))
        thread.start()
        return render_template('login.html', msg=msg)
    return render_template('signup.html',msg=msg)

@app.route('/MyLeafsets')
def open_leafsets():
    if "user" not in session:
        return redirect("/login")
    else:
        return render_template('MyLeafsets.html')
    
@app.route('/create')
def create_leaf():
    if "user" not in session:
        return redirect("/login")
    else:
        return render_template('create.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ''
    if request.method == "POST" and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        try:
            authentication = ttd.authenticate(email, password) 
        except Exception as e:
            print("Authentication failed:", e)  # Logging the exception can help in debugging
            authentication = False

        if authentication:
            session["user"] = ttd.get_user_by_email(email) 
            session["user_id"] = ttd.get_user_id(email)  # Assuming get_user_id is correctly fetching user ID
            session["email"] = email
            return redirect("/home")
        else:
            msg = "Incorrect username or password"
    return render_template("login.html", msg=msg)


@app.route('/home',methods= ['GET'])
def go_home():
    if "user" not in session:
        return redirect("/login")
    else:
        return render_template("landing-upon-login.html",user=session["user"])


def send_signup_email_async(app, email, username):
    with app.app_context():
        subject = 'Account Creation'
        body = f"Dear {username},\n\nWelcome to our platform! We are thrilled to have you join us."
        message = Message(subject, recipients=[email], body=body, sender='leafcards@hotmail.com')
        try:
            mail.send(message)
            msg = "Email sent successfully!"
        except Exception as e:
            msg = "Failed to send email:" + str(e)
        return msg

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
        if email:
            # Here, implement the logic to update the user's status as 'verified'
            ttd.update_user_status(email, 'verified')
            return 'You have confirmed your account. Thanks!'
        else:
            return 'The confirmation link is invalid or has expired.'
    except Exception as e:
        return str(e)  # for debugging, better log this in production
    

@app.route('/get_user_leafsets/<int:user_id>')
def get_user_leafsets(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized or not logged in'}), 401

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = """
        SELECT Leaf_Set_ID, FolderName, Label
        FROM Leaf_Sets
        WHERE UserID = ?
        """
        cursor.execute(query, (user_id,))
        leafsets = cursor.fetchall()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
        return jsonify({'error': 'Database error'}), 500
    finally:
        if conn:
            conn.close()

    return jsonify(leafsets)

@app.route('/get_leafset_cards/<int:folderId>')
def get_leafset_cards(folderId):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = """
        SELECT Leaf_Card_ID, Leaf_Card_Name, Question, Answer, Knowledge
        FROM Leaf_Cards
        WHERE FolderID = ?
        """
        cursor.execute(query, (folderId,))
        cards = cursor.fetchall()
        return jsonify(cards)
    except sqlite3.Error as error:
        print("Failed to read cards from sqlite table", error)
        return jsonify({'error': 'Database error'}), 500
    finally:
        if conn:
            conn.close()



@app.route('/save_leafset', methods=['POST'])
def save_leafset():
    leafset_name = request.form.get('leafsetName')
    questions = request.form.getlist('questions[]')
    answers = request.form.getlist('answers[]')
    cards = [{'key': q, 'value': a} for q, a in zip(questions, answers)]
    

    if not leafset_name or not cards:
        return jsonify({'error': 'Missing name or cards'}), 400
    
    try:
        with sqlite3.connect('database.db') as conn:
            
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Leaf_Sets (FolderName) VALUES (?)", (leafset_name,))
            
            leafset_id = cursor.lastrowid
            cursor.executemany("INSERT INTO Leaf_Cards (FolderID, Question, Answer, Knowledge) VALUES (?,?,?,0)",
                               [(leafset_id, card['key'], card['value']) for card in cards])
            
            conn.commit()
    except sqlite3.Error as e:
        error_info = str(e)
        print(error_info)  
        return jsonify({'error': 'Database error', 'details': error_info}), 500

    return jsonify({'success': True, 'leafset_id': leafset_id}), 200


@app.route('/update_knowledge', methods=['POST'])
def update_knowledge():
    # Extract card ID and knowledge value from the POST request
    card_id = request.json.get('cardId')
    knowledge = request.json.get('knowledge')

    # Connect to the database and update the knowledge field
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = "UPDATE Leaf_Cards SET Knowledge = ? WHERE Leaf_Card_ID = ?"
        cursor.execute(query, (knowledge, card_id))
        conn.commit()
    except sqlite3.Error as error:
        print("Failed to update knowledge", error)
        return jsonify({'error': 'Database error'}), 500
    finally:
        if conn:
            conn.close()

    # Return a success message
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
