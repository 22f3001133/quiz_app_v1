# quiz_app_v1
This is a Quiz Application for MAD 1 Project of IITM.

## Run these command in Command Prompt
Step1:- pip install -r requirements.txt
Step2:- from backend.models import*
Step3:- from app import*
Step4:- db.create_all()
Step5:- u1=User(email="admin@gmail.com", password="Admin123@", role="0")
Step6:- db.session.add(u1)
Step7:- db.session.commit()
Step8:- exit()
Step9:- python app.py