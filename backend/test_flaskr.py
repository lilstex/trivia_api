import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://postgres:postgres@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))


    def test_create_categories(self):
        new_category = {
            "category": "Nodejs"
            }
        res = self.client().post('/categories', json=new_category)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_categories(self):
        new_category = {
            "category": "Sports"
            }
        res = self.client().post('/categories', json=new_category)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Category already exist')


    def test_delete_category(self):
        res = self.client().delete("/categories/10")
        data = json.loads(res.data)
        category = Category.query.filter(Category.id == 10).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 10)
        self.assertEqual(category, None)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))


    def test_delete_question(self):
        res = self.client().delete("/questions/20")
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 20).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 20)
        self.assertEqual(question, None)


    def test_create_question(self):
        new_question = {
            "question": "Who won the 2008 ballon d'or?",
            "answer": "Cristiano Ronaldo",
            "category": 6,
            "difficulty": 3,
            "rating": 4
            }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_question_by_search(self):
        res = self.client().post("/questions/search", json={"searchTerm": "Indian city"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
    

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["current_category"])

    def test_post_play_quiz(self):
        quiz = {
            'previous_questions':[],
            'quiz_category':{'id': 2,'type': 'Art'}
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["question"])

    def test_422_on_deleting_categories(self):
        res = self.client().delete('/categories/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_on_deleting_questions(self):
        res = self.client().delete('/categories/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_404_not_found_on_searching_questions(self):
        res = self.client().post("/questions/search", json={"searchTerm": "mumu"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_400_bad_request_on_creating_question(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_422_on_playing_quiz(self):
        quiz = {}
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],"unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()