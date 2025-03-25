from flask import Flask
from backend.models import*


def init_app():

    quiz_app=Flask(__name__)

    quiz_app.debug=True
    quiz_app.secret_key="treta"
    quiz_app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///treta.sqlite"
    quiz_app.app_context().push()
    db.init_app(quiz_app)
    print("quiz app started")
    return quiz_app


app=init_app()
from backend.controllers import*



if __name__=="__main__":
    app.run()