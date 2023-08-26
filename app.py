from flask import Flask, render_template, request, flash, make_response,redirect
from flask_sqlalchemy import SQLAlchemy
import re
import search_number
import send_email

app = Flask(__name__, static_folder = "static")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user_data.db"
app.config['SQLALCHEMYTRACKMODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

def email_valid(email):
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        print("The string is a valid email")
        return True
    else:
        print("Invalid email")
        return False


def check_user(email,password):
    alluserdata = Todo.query.all()
    found_data = False
    for user in alluserdata:
        if user.email == email:
            print("email found")
            if user.password == password:
                print("password also mathced")
                found_data=True
    if found_data:
        print("user found login success...")
        return True
    else:
        print("user not found")
        return False
    
def register_user(username,email,password):
    alluserdata = Todo.query.all()
    username_exist = False
    for data_name in alluserdata:
        if data_name.username == username or data_name.email == email:
            username_exist = True
        else:
            username_exist = False
    return username_exist

def send_mail(user_username,user_email):
    Subject = "Account Successfully Created"
    Body = f"Dear, {user_username} your account for Truecaller Clone has been successfully created.\n Thanks for trying our service and feel free to contact us in case of any issues..."
    try:
        send_email.send_gmail(Subject,Body,user_email)
        return True
    except:
        return "An error occured !!!"

        
        


@app.route("/",methods=["GET","POST"])
def index():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        user_exist = check_user(email,password)
        print(user_exist)
        if user_exist:
            res = make_response(render_template('index.html'))
            res.set_cookie('registered', 'True', max_age=360000000)
            return res
        else:
            return "Username or Password not found ! ! !"
    else:
        cookies = request.cookies
        registered = cookies.get("registered")
        if registered:
            return render_template("index.html")
        else:
            return redirect("/register")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        check_email = email_valid(email)
        password = request.form['password']
        if username == "":
            return "You forgot to fill the USERNAME !!!"
        elif email == "":
            return "Your forgot to fill the EMAIL !!!"
        elif password == "":
            return "You forgot to fill the PASSWORD !!!"
        elif check_email==False:
            return "Invalid email address !!!"
        else:
            user_exist = register_user(username, email, password)
            if user_exist:
                return "This username or Email already exist !!!"
            else:
                send_mail(username,email)
                nothing = Todo(username=username,email=email,password=password)
                db.session.add(nothing)
                db.session.commit()
                return redirect("/")


    alluser_data = Todo.query.all()
    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
    return render_template("register.html")

        
    

@app.route('/search', methods=["POST","GET"])
def nothing():
    try:
        user_number = str(request.form['name_input'])
        contact_info = search_number.search(user_number)
        phone_name = contact_info[0]
        phone_carrier = contact_info[1]
        if contact_info[2] == "":
            return render_template("index.html", name=phone_name, carrier=phone_carrier)    
        else:
            phone_email = contact_info[2]
        return render_template("index.html", name=phone_name, carrier=phone_carrier, email=phone_email)
    except Exception as e:
        print(e)
        return "You can't go here directly ! ! !"


if __name__ == '__main__':
    app.run(debug=True)
