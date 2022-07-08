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
from datetime import timedelta, datetime


# Done by: Dante Liew Zhen Ting
# Student ID: 01349305
# Team: G8 TEAM 1
class TestClasses(unittest.TestCase):
    def setUp(self):
        self.app =app
        app.config["TESTING"] = True
        app.testing=True
        app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://admin:XYBfSJxQJC5M9zwdbsZq@database-2.cmsaamavflox.us-east-2.rds.amazonaws.com:3306/coursecycle_test'
        #app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/coursecycle_test'
        app.app_context().push()
        db.create_all()
        db.session.rollback()
        start_date = datetime.today()+timedelta(1)
        course = Course(course_name="course1")
        class1 = Class(course_name="course1", class_name = "G1", start_date=start_date)
        engineer = Engineer(username="cindy123", engineer_username="cindy123")
        enrolledClass = EnrolledClass(course_name="course1", class_name="G1",engineer_username="cindy123", approved=True)
        db.session.add(course)
        db.session.add(class1)
        db.session.add(engineer)
        db.session.flush()
        db.session.add(enrolledClass)
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app = None

    def test_get_class_list(self):
        response = self.client.get('/classes/classlist', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(response_json['data']))
    
    def test_add_lesson_to_class(self):
        data_json = {
            "lesson_no": 1,
            "lesson_title": "something",
            "course_name":"course1",
            "class_name": "G1",
            "is_last_lesson": False,
            "lesson_materials_url": "drive.google.com"
        }
        # correct adding of lesson
        response = self.client.post('/classes/addlesson', data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response_json['data'],data_json)
        
        # duplicate entry of lesson -> 401 error
        response = self.client.post('/classes/addlesson', data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status_code,401)

        # insufficient/wrong data inserted
        data_json['lesson_no'] = 2
        data_json['is_last_lesson'] = "something else"
        response = self.client.post('/classes/addlesson', data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status_code,401)
        data_json.pop("class_name", None)
        response = self.client.post('/classes/addlesson', data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status_code,401)

    def test_get_all_classes(self):
        #get all classes for all courses
        response = self.client.get('/classes/allclasses', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(response_json['data']))

        #get class of non-existent course -> empty list returned
        response = self.client.get('/classes/allclasses?course_name=HP', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual([], response_json['data'])

    def test_get_learners_by_class(self):
        #get enrolled students
        response = self.client.get('/classes/getlearnersbyclass?course_name=course1&class_name=G1', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(response_json['data']['learners']))
        
        # get without inserting required parameters
        response = self.client.get('/classes/getlearnersbyclass')
        self.assertEqual(response.status_code,401)

        # get non-existent class/course -> return 201 but learners will be an empty list
        response = self.client.get('/classes/getlearnersbyclass?course_name=course2&class_name=G2', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual({
            "course_name": "course2",
            "class_name": "G2",
            "learners": []
        },response_json['data'])

