from flask import Flask, redirect, request, session, render_template, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import talk_to_db as ttd


app = Flask(__name__)
app.config['SECRET_KEY']='8fc1a05cf18fd2b60d3befb6e475a0008f0e55568bffd4b3d45b6fb699465338'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'leafcards123@gmail.com'
app.config['MAIL_PASSWORD'] = 'ILoveCroi$$ant5'
mail = Mail(app)

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
    return redirect("/login")

@app.route('/login', methods = ['POST', 'GET'] )
def login():
    msg = ''
    if request.method == "POST" and 'email' in request.form and 'password' in request.form:
        email= request.form['email']
        password = request.form['password']
        try:
            authentication = ttd.authenticate(username=email, password=password)
        except Exception as e:
            authentication = False

        if authentication:
            session["user"] = ttd.get_username(email)
            session["email"] = email
            return redirect("/home")
        else:
            msg = "Incorrect username or password"

    return render_template("signup.html", msg = msg)

@app.route('/home',methods= ['GET'])
def go_home():
    if session["user"] == None:
        return redirect("/login")
    else:
        return render_template("landing-upon-login.html",user=session["user"])
    
@app.route('/signup', methods = ['POST','GET'])
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
        token = generate_confirmation_token(email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('confirm_template.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(email, subject, html)
        ttd.register_user(email,password)
        msg='Check your email to confirm your sign up!'
        return render_template('signup.html',msg=msg)
    return render_template('signup.html',msg=msg)

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


if __name__ == '__main__':
    app.run(debug=True)
