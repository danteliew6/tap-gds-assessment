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
from datetime import timedelta, datetime

# Done by: Wang Weimin
# Student ID: 01367692
# Team: G8 TEAM 1
class TestCourses(unittest.TestCase):
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
        start_date = datetime.today()+timedelta(1)
        class1 = Class(course_name="course1", class_name = "G1", start_date = start_date, capacity = 10)
        engineer = Engineer(username="cindy123", engineer_username="cindy123")
        enrolledClass = EnrolledClass(course_name="course1", class_name="G1",engineer_username="cindy123", approved=True)
        lesson1 = Lesson(lesson_no = 1, course_name="course1",class_name="G1",is_last_lesson=False)
        lesson2 = Lesson(lesson_no = 2, course_name="course1",class_name="G1",is_last_lesson=True)
        completedLesson = CompletedLesson(engineer_username="cindy123",lesson_no = 1, course_name="course1",class_name="G1",is_last_lesson=False)
        db.session.add(course)
        db.session.add(class1)
        db.session.add(engineer)
        db.session.flush()
        db.session.add(enrolledClass)
        db.session.add(lesson1)
        db.session.add(lesson2)
        db.session.flush()
        db.session.add(completedLesson)
        db.session.commit()
        self.client = app.test_client()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app = None

    def test_get_course_list(self):
        response = self.client.get('/courses/getcourselist', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(["course1"], response_json['data'])

    def test_create_course(self):
        data_json = {
            "course_name": "course2"
        }
        # add course with no prerequisites
        response = self.client.post('/courses/createcourse',data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual("course2", response_json['data']['course_name'])

        # add course with prerequisites
        data_json['course_name'] = "course3"
        data_json['prerequisite_courses'] = ['course2']
        response = self.client.post('/courses/createcourse',data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual("course3", response_json['data']['course_name'])
        self.assertEqual(["course2"], response_json['data']['prerequisite_courses'])


    def test_get_all_available_course_and_class(self):
        response = self.client.get('/courses/getallcourses', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(response_json['data']))

    def test_get_lesson_progress(self):
        # Correct Parameters
        response = self.client.get('/courses/getlessonprogress?engineer_username=cindy123&course_name=course1&class_name=G1', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response_json['data']['lessons_completed'])

        # Invalid Engineer -> return 201 but contents show 0% progress
        response = self.client.get('/courses/getlessonprogress?engineer_username=wrong123&course_name=course1&class_name=G1', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(0, response_json['data']['lessons_completed'])

        # Invalid Course/Class -> return 201 but progress contents are null
        response = self.client.get('/courses/getlessonprogress?engineer_username=cindy123&course_name=course1&class_name=G2', headers={"Content-Type":"application/json"})
        response_json = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual({'lessons_completed': 0, 'lessons': [], 'total_lessons': 0}, response_json['data'])
