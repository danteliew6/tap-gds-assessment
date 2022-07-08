# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from ..models.Quiz import Quiz
# from ..models.Question import Question
# from ..models.Answer import Answer
# from flask_cors import CORS
# from sqlalchemy import not_, func
# from src.football_competition import db
# from ..models.Lesson import Lesson
# from ..models.CompletedLesson import CompletedLesson

# class LessonController():
#     def getLessonForClass():
#         try:
#             data = request.args
#             lessons = Lesson.query.filter(Lesson.class_name==data['class_name'], Lesson.course_name==data['course_name']).all()
#             return jsonify({
#                 "data": {
#                     "lessons": [lesson.to_dict() for lesson in lessons]
#                 }
#             }), 201
#         except Exception as e:
#             return jsonify({
#                 "message": str(e)
#             }), 401

#     def addQuizToLesson():
#         try:
#             data = request.get_json()
#             quiz = Quiz(class_name=data['class_name'],course_name=data['course_name'],lesson_no=data['lesson_no'],passing_percentage=data['passing_percentage'])
#             db.session.add(quiz)
#             db.session.flush()

#             for question in data['questions']:
#                 question_obj = Question(quiz_id=quiz.quiz_id, question_description=question['question_description'])
#                 db.session.add(question_obj)
#                 db.session.flush()
#                 for answer in question['answers']:
#                     answer_obj = Answer(question_id=question_obj.question_id, answer_description=answer['answer_description'], is_correct=answer['is_correct'])
#                     db.session.add(answer_obj)  

#             questions_and_answers = []
#             for question in quiz.questions:
#                 temp = question.to_dict()
#                 temp['answers'] = [answer.to_dict() for answer in question.answers]
#                 questions_and_answers.append(temp)
#             db.session.commit()
#             return jsonify({
#                 "data": {
#                     "quiz": quiz.to_dict(),
#                     "questions": questions_and_answers
#                 }
#             }), 201
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({
#                 "message": str(e)
#             }), 401

#     def markQuiz():
#         try:
#             data = request.get_json()
#             quiz = Quiz.query.filter(Quiz.class_name==data['class_name'], Quiz.course_name==data['course_name'], Quiz.lesson_no==data['lesson_no']).first()
#             answers = {}
#             for question in quiz.questions:
#                 for answer in question.answers: 
#                     if answer.is_correct:
#                         answers[question.question_description] = answer.answer_description
            
#             score = 0
#             for answer in data['answers']:
#                 if answers[answer['question_description']] == answer['answer_description']:
#                     score += 1
            
#             total_percentage = score / len(quiz.questions) * 100
#             has_passed = total_percentage >= quiz.passing_percentage

#             if has_passed:
#                 lesson = Lesson.query.filter(Lesson.class_name==data['class_name'], Lesson.course_name==data['course_name'], Lesson.lesson_no==data['lesson_no']).first()
#                 completedLesson = CompletedLesson(class_name=data['class_name'], course_name=data['course_name'], lesson_no=data['lesson_no'], is_last_lesson=lesson.is_last_lesson, engineer_username=data['engineer_username'])
#                 db.session.add(completedLesson)
#                 db.session.commit()

#             return jsonify({
#                 "data": {
#                     "quiz": quiz.to_dict(),
#                     "score": score,
#                     "total_points": len(quiz.questions), 
#                     "scoring_percentage": total_percentage,
#                     "passed": has_passed  
#                 }
#             }), 201
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({
#                 "message": str(e)
#             }), 401

#     def getQuiz():
#         try:
#             data = request.args
#             quiz = Quiz.query.filter(Quiz.lesson_no==data['lesson_no'], Quiz.class_name==data['class_name'], Quiz.course_name==data['course_name']).first()
#             questions = quiz.questions
#             question_list = []
#             for question in questions:
#                 answers = question.answers
#                 question = question.to_dict()
#                 question['answers'] = [answer.to_dict() for answer in answers]
#                 question_list.append(question)
#             return jsonify({
#                 "data": {
#                     "quiz": quiz.to_dict(),
#                     "questions": question_list
#                 }
#             }), 201
#         except Exception as e:
#             return jsonify({
#                 "message": str(e)
#             }), 401