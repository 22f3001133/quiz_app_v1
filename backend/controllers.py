from flask import Flask, render_template,request,redirect,session,json,url_for,flash
from flask import current_app as app
from backend.models import*
from backend.models import db,Subject,Quiz,Question,Chapter
from datetime import datetime

@app.route('/',methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        role=int(request.form.get("login-type"))
        user=None
        user=User.query.filter_by(email=email,password=password).first()
        print(user)
        if user and user.role==role:
            session["user_id"]=user.id
            session["role"]=user.role
            if role==0:
                return redirect(url_for("admin_dashboard"))
            elif role==1:
                return redirect(url_for("user_dashboard"))
        else:
            return render_template("login.html")
    return render_template("login.html")
    

@app.route("/user_dashboard")
def user_dashboard():
    if "user_id" not in session or session.get("role")!=1:
        return redirect(url_for("login"))
    return render_template("userDashboard.html")
    
    
@app.route("/user_Register",methods=["GET","POST"])
def user_Register():
    if request.method=="POST":
        email=request.form.get("email")
        fullname=request.form.get("fullname")
        password=request.form.get("password")
        qualification=request.form.get("qualification")
        dob1=request.form.get("dob")
        dob=datetime.strptime(dob1,"%Y-%m-%d").date()
        user=User.query.filter_by(email=email).first()
        if not user:
            new_user=User(email=email,fullname=fullname,password=password,qualification=qualification,dob=dob)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            return render_template("registration.html")
    return render_template("registration.html")




@app.route("/admin_dashboard")
def admin_dashboard():
    if "user_id" not in session or session.get("role")!=0:
        return redirect(url_for("login"))
    return render_template("AdminDashboard.html")

    

@app.route("/logout")
def logout():
    session.pop('user_id',None)
    flash("logged out successfully!","success")
    return redirect(url_for("login"))


