from flask import Flask, redirect, request, session, render_template

app = Flask(__name__)
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
            authentication = authenticate(username=email, password=password)
        except Exception as e:
            authentication = False

        if authentication:
            
            session["user"] = 'name'
            session["email"] = email
            return redirect("/home")
        else:
            msg = "Incorrect username or password"

    return render_template("index.html", msg = msg)


if __name__ == '__main__':
    app.run(debug=True)