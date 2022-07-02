from webbrowser import get
from flask_wtf.csrf import CSRFProtect
from flask import Flask, render_template, request, flash, redirect, session, Blueprint, Response
from web import Data
from routes import *
from secure import SecureHeaders
import os
import sys


app=Flask(__name__)
app.register_blueprint(routes)
data=Data() #Instancee de class Data to manage app data

app_data=data.load_data()

SESSION_TYPE='redis'
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
PERMANENT_SESSION_LIFETIME=1800

app.config.update(
SECRET_KEY=os.urandom(24)
)
if app_data:
    app.config['keys'] = data.valid_keys(app_data["api_keys"])
    app.config['virus_key'] = app_data["virustotalkey"]

csrf = CSRFProtect()
csrf.init_app(app)

secure_headers = SecureHeaders()
@app.after_request
def set_secure_headers(response):
    secure_headers.flask(response)
    return response

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    r.headers["X-Frame-Options"] = "SAMEORIGIN"

    return r


@app.route('/')
def index():
    if 'user' in session:
        return render_template("account.html")
    else:
         return render_template("login.html")



@app.route('/virus', methods=["GET","POST"])
def virus():
    if 'user' in session:
        VT_key=app_data.get("virustotalkey")
        if request.method == 'POST':
            if request.form["VT_api_key"]:
                virus_key=request.form["VT_api_key"]
                app_data["virustotalkey"]=virus_key
                app.config['virus_key'] = virus_key
                data.update_data(app_data)
                flash("Virus Total API key updated")
        
        
        VT_key=app_data.get("virustotalkey")            
        return render_template("virus.html",VT_api_key=VT_key)
    else:
        flash("You must be logged in")
    
    return redirect("login")



@app.route('/changeaccount', methods=["POST", "GET"])
def changeaccount():
    if 'user' in session:
        if request.method == 'POST':
            if "newuser" in request.form and "password" in request.form:
                password=request.form.get("password")
                hash= app_data.get("admin").get("password")
                if data.check_password(hash, password):
                    new_user=request.form.get("newuser")
                    app_data["admin"]["user"]=new_user
                    data.update_data(app_data)
                    flash(f"User changed to {new_user}")
                else:
                    flash("Not authorized")

            if "oldpassword" in request.form and "newpassword" in request.form:
                password=request.form.get("oldpassword")
                hash= app_data.get("admin").get("password")
                if data.check_password(hash, password):
                    new_pass=request.form.get("newpassword")
                    new_pass=data.argon_hash(new_pass)
                    app_data["admin"]["password"]=new_pass
                    flash("Password changed")
                    data.update_data(app_data)
                else:
                    flash("Not authorized")

                    
        return render_template("account.html")
    else:
        flash("You must be logged in")
    
    return redirect("login")



@app.route('/apikey', methods=["POST", "GET"])
def apikey():
    if 'user' in session:
        #api_keys={"12ghsdgshdghsgd": "algo", "hsdg735463rfyweg":"test"}
        api_keys=app_data.get("api_keys")
        if request.method == 'POST' and  "id" in request.form:
            id=request.form["id"]
            if id in api_keys:
                del app_data["api_keys"][id]
                api_keys=app_data.get("api_keys")
                valid_keys=data.valid_keys(api_keys)
                app_data["valid_keys"]=valid_keys
                app.config['keys'] = valid_keys
                data.update_data(app_data)

                return render_template('APIkey.html', api_keys=api_keys)

        return render_template('APIkey.html', api_keys=api_keys)
    else:
        flash("You must be logged in")
    
    return redirect("login")



@app.route('/craete_api', methods=["POST"])
def craete_api():
    if 'user' in session:
        if "name" in request.form:
            name=request.form["name"]
            id=app_data.get('id')
            app_data['id']=id+1
            api_key=data.create_api_key()
            app_data["api_keys"][str(id)]=[api_key,name]
            api_keys=app_data.get("api_keys")
            valid_keys=data.valid_keys(api_keys)
            app.config["keys"] = valid_keys
            app_data["valid_keys"]=valid_keys
            data.update_data(app_data)

            return render_template('APIkey.html', api_keys=api_keys, key=api_key)

    else:
        flash("You must be logged in")
    
    return redirect("login")



@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        if "user" in request.form and "password" in request.form:
            user= request.form["user"]
            password= request.form["password"]

            print(data.argon_hash(password))

            hash= app_data.get("admin").get("password")
            print(data.check_password(hash, password))

            if user==app_data.get("admin").get("user") and data.check_password(hash, password):
                session["user"] = user
                return redirect("/changeaccount")
            else:
                flash("Invalid credentials")
        else:
            flash("Bad Request")
            
    return render_template("login.html")



@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/login')

if __name__ == "__main__":
    args = sys.argv
    if len(args)==4 and args[1]=='setup':
        data=Data()
        user=args[2]
        password=data.argon_hash(args[3])
        print(user, password)
        base_data={
                    "admin":{"user":user, "password":password},
                    "salt":"Ww7-.WJEK2334nmh18*-%",
                    "api_keys":{},
                    "valid_keys":[],
                    "virustotalkey":"",
                    "id":1
                    }
        status=data.update_data(base_data)
        if not status:
            sys.exit(56)
        else:
            sys.exit(0)
    from waitress import serve
    serve(app, host="127.0.0.1", port=5000)