from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()


class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(255), unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    fullname=db.Column(db.String)
    qualification=db.Column(db.String)
    dob=db.Column(db.Date)
    role=db.Column(db.Integer, nullable=False, default=1)

    user_quizzes=db.relationship("UserQuiz",backref="user",lazy=True, cascade="all,delete")


class Subject(db.Model):
    __tablename__="subjects" 
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(300),nullable=True)
    
    chapters=db.relationship("Chapter", backref="subject", cascade="all,delete", lazy=True)
   


class Chapter(db.Model):
    __tablename__="chapters" 
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(300),nullable=True)
    subject_id=db.Column(db.Integer,db.ForeignKey('subjects.id', ondelete="CASCADE"),nullable=False)

    quizzes=db.relationship("Quiz", backref="chapter", cascade="all,delete", lazy=True)
  


class Quiz(db.Model):
    __tablename__='quizzes'
    id=db.Column(db.Integer,primary_key=True)
    chapter_id=db.Column(db.Integer,db.ForeignKey('chapters.id', ondelete="CASCADE"),nullable=False)
    date=db.Column(db.Date,nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    
    questions=db.relationship('Question',backref='quiz', cascade="all,delete", lazy=True)
    user_quizzes=db.relationship('UserQuiz', backref="quiz", cascade="all,delete", lazy=True)


class Question(db.Model):
    __tablename__='questions'
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer,db.ForeignKey('quizzes.id', ondelete="CASCADE"),nullable=False)
    question_title=db.Column(db.String(200),nullable=False)
    question_statement=db.Column(db.Text,nullable=False)
    option1=db.Column(db.String(200),nullable=False)
    option2=db.Column(db.String(200),nullable=False)
    option3=db.Column(db.String(200),nullable=False)
    option4=db.Column(db.String(200),nullable=False)
    correct_option=db.Column(db.String,nullable=False)


class UserQuiz(db.Model):
    __tablename__="user_quiz"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    quiz_id=db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete="CASCADE"), nullable=False)
    score=db.Column(db.Integer, nullable=False, default=0)