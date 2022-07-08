# Third party modules
import json
import unittest
# First party modules
from src.football_competition import app, db
from src.football_competition.models.Course import Course
from src.football_competition.models.Class import Class
from src.football_competition.models.Employee import Employee
from src.football_competition.models.Engineer import Engineer
from src.football_competition.models.EnrolledClass import EnrolledClass
from src.football_competition.models.Lesson import Lesson
from src.football_competition.models.CompletedLesson import CompletedLesson
from src.football_competition.models.Quiz import Quiz
from src.football_competition.models.Question import Question
from src.football_competition.models.Team import Answer

# Done by: Remus Chan Koon Hong
# Student ID: 01366054
# Team: G8 TEAM 1

class TestLessons(unittest.TestCase):
    def setUp(self):
        self.app =app
        app.config["TESTING"] = True
        app.testing=True
        app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://admin:XYBfSJxQJC5M9zwdbsZq@database-2.cmsaamavflox.us-east-2.rds.amazonaws.com:3306/coursecycle_test'
        #app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/coursecycle_test'
        app.app_context().push()
        db.create_all()
        db.session.rollback()
        course = Course(course_name="course1")
        class1 = Class(course_name="course1", class_name = "G1")
        engineer1 = Engineer(username="cindy123", engineer_username="cindy123")
        engineer2 = Engineer(username="frank123", engineer_username="frank123")
        enrolledClass1 = EnrolledClass(course_name="course1", class_name="G1",engineer_username="cindy123", approved=True)
        enrolledClass2 = EnrolledClass(course_name="course1", class_name="G1",engineer_username="frank123", approved=True)
        lesson1 = Lesson(lesson_no = 1, course_name="course1",class_name="G1",is_last_lesson=False)
        lesson2 = Lesson(lesson_no = 2, course_name="course1",class_name="G1",is_last_lesson=True)
        completedLesson = CompletedLesson(engineer_username="cindy123",lesson_no = 1, course_name="course1",class_name="G1",is_last_lesson=False)
        quiz = Quiz(lesson_no = 1, course_name="course1",class_name="G1", passing_percentage=50)
        question1 = Question(question_description="Question 1")
        question2 = Question(question_description="Question 2")
        question1.answers = [Answer(answer_description="True", is_correct=True),Answer(answer_description="False", is_correct=False)]
        question2.answers = [Answer(answer_description="True", is_correct=True),Answer(answer_description="False", is_correct=False)]
        quiz.questions = [question1, question2]
        db.session.add(course)
        db.session.add(class1)
        db.session.add(engineer1)
        db.session.add(engineer2)
        db.session.flush()
        db.session.add(enrolledClass1)
        db.session.add(enrolledClass2)
        db.session.add(lesson1)
        db.session.add(lesson2)
        db.session.flush()
        db.session.add(quiz)
        db.session.add(completedLesson)
        db.session.commit()
        self.client = app.test_client()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app = None

    def test_get_lesson_for_class(self):
        response = self.client.get('/lessons/getlessons?class_name=G1&course_name=course1', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(2, len(response_json['data']['lessons']))

    def test_add_quiz_to_lesson(self):
        data_json = {
            "class_name": "G1",
            "course_name": "course1",
            "lesson_no": 1,
            "passing_percentage": 70,
            "questions":[
                {
                    "question_description": "What is the most expensive component of a printer?",
                    "answers": [
                        {
                            "answer_description": "Printer Ink",
                            "is_correct": True
                        },
                        {
                            "answer_description": "Scanner",
                            "is_correct": False
                        }
                    ]
                },
                {
                    "question_description": "Are papers biodegradeable?",
                    "answers": [
                        {
                            "answer_description": "True",
                            "is_correct": True
                        },
                        {
                            "answer_description": "False",
                            "is_correct": False
                        }
                    ]
                }
            ]
        }
        # Correct Json
        response = self.client.post('/lessons/addquiz',data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)

        # Invalid Class/Course
        data_json['class_name'] = "G2"
        response = self.client.post('/lessons/addquiz',data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(401, response.status_code)


    def test_mark_quiz(self):
        data_json = {
            "class_name": "G1",
            "course_name": "course1",
            "engineer_username": "frank123",
            "lesson_no": 1,
            "answers":[
                {
                    "question_description": "Question 1",
                    "answer_description": "True"
                },
                {
                    "question_description": "Question 2",
                    "answer_description": "False"
                }
            ]
        }
        # Passed -> 1 correct 1 wrong (50% score)
        response = self.client.post('/lessons/markquiz',data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(True, response_json['data']['passed'])
        self.assertEqual(50, response_json['data']['scoring_percentage'])


        # Failed -> 2 wrong (0% score)
        data_json = {
            "class_name": "G1",
            "course_name": "course1",
            "lesson_no": 1,
            "answers":[
                {
                    "question_description": "Question 1",
                    "answer_description": "False"
                },
                {
                    "question_description": "Question 2",
                    "answer_description": "False"
                }
            ]
        }
        response = self.client.post('/lessons/markquiz',data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(False, response_json['data']['passed'])
        self.assertEqual(0, response_json['data']['scoring_percentage'])

    def test_get_quiz(self):
        response = self.client.get('/lessons/getquiz?class_name=G1&course_name=course1&lesson_no=1', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)