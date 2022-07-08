# Third party modules
import json
import unittest
# First party modules
from src.football_competition import app, db
from src.football_competition.models.Course import Course
from src.football_competition.models.Class import Class
from src.football_competition.models.Employee import Employee
from src.football_competition.models.Engineer import Engineer
from src.football_competition.models.Learner import Learner
from src.football_competition.models.Trainer import Trainer
from src.football_competition.models.EnrolledClass import EnrolledClass
from src.football_competition.models.Lesson import Lesson
from src.football_competition.models.CompletedLesson import CompletedLesson
from src.football_competition.models.PrerequisiteCourse import PrerequisiteCourse
from datetime import timedelta, datetime


# Done by: Koh Qi Yan Bryan
# Student ID: 01352837
# Team: G8 TEAM 1

class TestEnrollments1(unittest.TestCase):
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
        course2 = Course(course_name="course2")
        course3 = Course(course_name="course3")
        prerequisiteCourse1 = PrerequisiteCourse(course_name="course2", prerequisite_course_name="course1")
        prerequisiteCourse2 = PrerequisiteCourse(course_name="course3", prerequisite_course_name="course2")
        start_date = datetime.today()+timedelta(1)
        class1 = Class(course_name="course1", class_name = "G1", start_date = start_date, capacity = 10)
        lesson = Lesson(lesson_no = 1, course_name="course1",class_name="G1",is_last_lesson=True)
        engineer1 = Engineer(username="cindy123", engineer_username="cindy123")
        engineer2 = Trainer(username="brian123", engineer_username="brian123")
        engineer3 = Trainer(username="adam123", engineer_username="adam123")
        enrollment1 = EnrolledClass(course_name="course1", class_name="G1",engineer_username="brian123", approved=False)
        enrollment2 = EnrolledClass(course_name="course1", class_name="G1",engineer_username="adam123", approved=True)
        lesson = Lesson(lesson_no = 1, course_name="course1",class_name="G1",is_last_lesson=True)
        completedLesson = CompletedLesson(engineer_username="adam123",lesson_no = 1, course_name="course1",class_name="G1",is_last_lesson=True)

        db.session.add(course)
        db.session.add(course2)
        db.session.add(course3)
        db.session.add(class1)
        db.session.add(lesson)
        db.session.add(engineer1)
        db.session.add(engineer2)
        db.session.add(engineer3)
        db.session.flush()
        db.session.add(prerequisiteCourse1)
        db.session.add(prerequisiteCourse2)
        db.session.add(enrollment1)
        db.session.add(enrollment2)
        db.session.flush()
        db.session.add(completedLesson)
        db.session.commit()
        self.client = app.test_client()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app = None

    def test_enrol_for_class(self):
        data_json = {
            "course_name": "course1",
            "class_name": "G1",
            "engineer_username" : "cindy123"
        }
        #first enrollment
        response = self.client.post('/enrollment/enrolforclass',data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(201, response.status_code)

        #duplicate enrollment check
        response = self.client.post('/enrollment/enrolforclass',data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(401, response.status_code)

    def test_assign_learner_to_class(self):
        data_json = {
            "course_name": "course1",
            "class_name": "G1",
            "engineer_username" : "cindy123"
        }
        #first assignment
        response = self.client.post('/enrollment/assignlearnertoclass',data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(201, response.status_code)

        #duplicate assignment check
        response = self.client.post('/enrollment/assignlearnertoclass',data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(401, response.status_code)

    def test_assign_trainer_to_class(self):
        #assigning trainer to calss
        response = self.client.put('/enrollment/assigntrainertoclass?class_name=G1&course_name=course1&trainer_name=brian123', headers={"Content-Type":"application/json"})
        self.assertEqual(201, response.status_code)

    def test_approve_class_enrollment(self):
        data_json = {
            "course_name": "course1",
            "class_name": "G1",
            "engineer_username" : "brian123"
        }
        response = self.client.put('/enrollment/approveclassenrollment',data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(201, response.status_code)

    def test_get_learner_class(self):
        response = self.client.get('/enrollment/getlearnerclass?engineer_username=brian123', headers={"Content-Type":"application/json"})
        self.assertEqual(201, response.status_code)

    def test_get_all_engineers(self):
        response = self.client.get('/enrollment/getallengineers', headers={"Content-Type":"application/json"})
        self.assertEqual(201, response.status_code)

    def test_get_all_learners(self):
        response = self.client.get('/enrollment/getalllearners', headers={"Content-Type":"application/json"})
        self.assertEqual(201, response.status_code)







    
