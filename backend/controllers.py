from flask import Flask, render_template,request,redirect,session,url_for,flash,jsonify
from flask import current_app as app
from sqlalchemy import func
from backend.models import*
from backend.models import db,Subject,Quiz,Question,Chapter
from datetime import datetime, date

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
    query=request.args.get('query','').strip().lower()
    current_date=date.today().strftime("%Y-%m-%d")
    print(current_date)
    if query:
        quizzes=Quiz.query.filter(func.lower(Quiz.date).ilike(f"%{query}%"))
    else:
        quizzes=Quiz.query.all()
    return render_template("userDashboard.html", quizzes=quizzes, current_date=current_date)
    
    
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
    query=request.args.get("query","").strip().lower()
    if query:
        subject_info=Subject.query.filter(func.lower(Subject.name).ilike(f"%{query}%")).all()
    else:
        subject_info=fetch_subjects()
    chapter_info=fetch_chapters()
    return render_template("AdminDashboard.html",subjects=subject_info,chapters=chapter_info)

    

@app.route("/logout")
def logout():
    session.pop('user_id',None)
    flash("logged out successfully!","success")
    return redirect(url_for("login"))



@app.route("/subject_form",methods=["GET","POST"])
@app.route("/subject_form/<int:subject_id>",methods=["GET","POST"])
def subject_form(subject_id=None):
    subject=Subject.query.get(subject_id) if subject_id else None
    
    if request.method=="POST":
        name=request.form.get("name")
        description=request.form.get("description")

        if subject:
            subject.name=name
            subject.description=description
        else:
            subject=Subject(name=name,description=description)
            db.session.add(subject)
            
        db.session.commit()
        return redirect(url_for("admin_dashboard"))
    return render_template("newSubject.html", subject=subject)


@app.route('/delete_subject/<int:subject_id>', methods=["POST"])
def delete_subject(subject_id):
    subject=Subject.query.get(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


def fetch_subjects():
    subjects=Subject.query.all()
    subject_list=[]
    for subject in subjects :
        subject_info={"id":subject.id,"name":subject.name,"description":subject.description}
        subject_list.append(subject_info)
    return subject_list 


                                    

@app.route("/chapter_form/<int:subject_id>",methods=["GET","POST"])
@app.route("/chapter_form/<int:subject_id>/<int:chapter_id>",methods=["GET","POST"])
def chapter_form(subject_id, chapter_id=None):
    chapter = Chapter.query.get(chapter_id) if chapter_id else None
    
    if request.method=="POST":
        name=request.form.get("name")
        description=request.form.get("description")

        if chapter:
            chapter.name=name
            chapter.description=description
        else:
            chapter=Chapter(name=name,description=description,subject_id=subject_id)
            db.session.add(chapter)
        
        db.session.commit()
        return redirect(url_for("admin_dashboard"))
    return render_template("newchapter.html", subject_id=subject_id, chapter=chapter)


@app.route("/delete_chapter/<int:chapter_id>", methods=["POST"])
def delete_chapter(chapter_id):
    chapter=Chapter.query.get(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


def fetch_chapters():
    chapters=Chapter.query.all()
    chapter_list=[]
    for chapter in chapters:
        chapter_info={"id":chapter.id,"name":chapter.name,"description":chapter.description,"subject_id":chapter.subject_id}
        chapter_list.append(chapter_info)
    return chapter_list



@app.route("/subject/<int:subject_id>/chapter/<int:chapter_id>")
def quiz_management(subject_id,chapter_id):
    chapters=Chapter.query.filter_by(id=chapter_id,subject_id=subject_id).all()
    quizzes=fetch_quizzes(chapter_id)
    for quiz in quizzes:
        quiz.questions=fetch_question(quiz.id)
    return render_template("quizmanagement.html",chapters=chapters,quizzes=quizzes)



@app.route("/quiz_form/<int:chapter_id>",methods=["GET","POST"])
@app.route("/quiz_form/<int:chapter_id>/<int:quiz_id>",methods=["GET","POST"])
def quiz_form(chapter_id, quiz_id=None):
    quiz=Quiz.query.get(quiz_id) if quiz_id else None
    
    if request.method=="POST":
        date=datetime.strptime(request.form.get('date'),'%Y-%m-%d')
        duration=int(request.form.get('duration'))

        if quiz:
            quiz.date=date
            quiz.duration=duration
        else:
            quiz=Quiz(chapter_id=chapter_id,date=date,duration=duration)
            db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('quiz_management', subject_id=quiz.chapter.subject_id, chapter_id=chapter_id))
    return render_template("newquiz.html", quiz=quiz)


@app.route("/delete_quiz/<int:quiz_id>", methods=["POST"])
def delete_quiz(quiz_id):
    quiz=Quiz.query.get(quiz_id)
    subject_id=quiz.chapter.subject_id
    chapter_id=quiz.chapter_id
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('quiz_management', subject_id=subject_id, chapter_id=chapter_id))



def fetch_quizzes(chapter_id):
    quizzes=Quiz.query.filter_by(chapter_id=chapter_id).all()
    return quizzes
    

@app.route('/new_question/<int:quiz_id>',methods=['GET','POST'])
@app.route('/new_question/<int:quiz_id>/<int:question_id>',methods=['GET','POST'])
def new_question(quiz_id,question_id=None):

        question=Question.query.get(question_id) if question_id else None
        
        if request.method=='POST':
            question_title=request.form.get('question_title')
            question_statement=request.form.get('question_statement')
            option1=request.form.get('option1')
            option2=request.form.get('option2')
            option3=request.form.get('option3')
            option4=request.form.get('option4')
            correct_option=request.form.get('correct_option')
            
            quiz=Quiz.query.get(quiz_id)
            chapter_id=quiz.chapter_id
            subject_id=quiz.chapter.subject_id
            
            if question:
                question.question_title=question_title
                question.question_statement=question_statement
                question.option1=option1
                question.option2=option2
                question.option3=option3
                question.option4=option4
                question.correct_option=correct_option
            else:
                question=Question(
                    quiz_id=quiz_id,
                    question_title=question_title,
                    question_statement=question_statement,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    correct_option=correct_option)
                db.session.add(question)
            db.session.commit()
            return redirect(url_for('quiz_management', chapter_id=chapter_id, subject_id=subject_id))
        return render_template('newQuestion.html',quiz_id=quiz_id,question=question)
    
    

@app.route("/delete_question/<int:quiz_id>/<int:question_id>",methods=["POST"])
def delete_question(quiz_id,question_id):
    question=Question.query.get(question_id)
    quiz=question.quiz
    chapter_id=quiz.chapter_id
    subject_id=quiz.chapter.subject_id
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('quiz_management', chapter_id=chapter_id, subject_id=subject_id))
    

def fetch_question(quiz_id):
    questions=Question.query.filter_by(quiz_id=quiz_id).all()
    return questions


@app.route("/quizzes")
def quizzes():
    query=request.args.get('query','').strip().lower()
    if query:
        quizzes=Quiz.query.filter(func.lower(Quiz.date).ilike(f"%{query}%"))
    else:
        quizzes=Quiz.query.all()
    return render_template('quiz.html',quizzes=quizzes)


@app.route("/quiz/<int:quiz_id>")
def get_question(quiz_id):
    quiz=Quiz.query.get(quiz_id)
    
    questions=Question.query.filter_by(quiz_id=quiz_id).all()
    quiz_data={
        'id':quiz.id,
        'date':quiz.date,
        'duration':quiz.duration,
        'questions':[{
            'id':q.id,
            'text':q.question_statement,
            'options':[q.option1, q.option2, q.option3, q.option4],
            'correct_option':q.correct_option
        }for q in questions]
    }
    return jsonify(quiz_data)


@app.route("/submit_quiz", methods=['POST'])
def submit_quiz():
    data=request.json
    quiz_id=data.get('quiz_id')
    user_id=session.get('user_id')
    score=data.get('score')
    submitted_at=datetime.now()
    new_score=UserQuiz(user_id=user_id, quiz_id=quiz_id, score=score, submitted_at=submitted_at)
    db.session.add(new_score)
    db.session.commit()
    return jsonify({'message':'Quiz Submited'})


@app.route("/scores")
def scores():
    user_id=session.get('user_id')
    user_score=UserQuiz.query.filter_by(user_id=user_id).all()
    return render_template("scores.html", scores=user_score)


@app.route("/summary")
def admin_summary():
    user_id=session['user_id']
    role=session.get('role')
    
    if role == 0:
        quizzes=Quiz.query.all()
        quiz_attempts={quiz.id:UserQuiz.query.filter_by(quiz_id=quiz.id).count() for quiz in quizzes}
        quiz_top_scores={}
        for quiz in quizzes:
            top_score=db.session.query(db.func.max(UserQuiz.score)).filter_by(quiz_id=quiz.id).scalar() or 0
            quiz_top_scores[quiz.id]=top_score
        return render_template("AdminSummary.html", quiz_attempts=quiz_attempts, quiz_top_scores=quiz_top_scores)
    elif role == 1:
        user_scores=UserQuiz.query.filter_by(user_id=user_id).all()
        scores_data={quiz.quiz_id:quiz.score for quiz in user_scores}
        return render_template("UserSummary.html", scores_data=scores_data)
        