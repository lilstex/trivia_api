import os
import sys
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTION"
        )
        return response

    QUESTIONS_PER_PAGE = 10


    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions


    #  Categories
    #  ----------------------------------------------------------------
    #  ----------------------------------------------------------------
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    #  Get Categories
    #  ----------------------------------------------------------------
    @app.route("/categories", methods=["GET"])
    def get_categories():
        try:
            categories = Category.query.all()
            category_list = { category.id: category.type for category in categories }
            if len(categories) == 0:
                return jsonify(
                {
                    "success": True,
                    "categories": len(categories),
                    "Message": "No categories found"
                }
            )

            return jsonify(
                {
                    "success": True,
                    "categories": category_list
                }
            )
        except:
            abort(422)


    #  Create Category
    #  ----------------------------------------------------------------
    @app.route("/categories", methods=["POST"])
    def create_categories():
        body = request.get_json()
        new_category = body.get("category", None)
        try:
            # Check if category already exists
            check_category = Category.query.filter_by(type=new_category).first()
            if check_category:
                return jsonify(
                {
                    "success": False,
                    "message": "Category already exist",
                }
            )
            category = Category(type=new_category)
            category.insert()
            
            return jsonify(
                {
                    "success": True,
                    "message": "Category created sucessfully",
                }
            )

        except:
            abort(422)


    #  Delete Category
    #  ----------------------------------------------------------------
    @app.route("/categories/<int:category_id>", methods=["DELETE"])
    def delete_category(category_id):
        try:
            category = Category.query.get(category_id)
            if category is None:
                abort(404)
            
            category.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": category_id,
                }
            )

        except:
            abort(422)


    #  Questions
    #  ----------------------------------------------------------------
    #  ----------------------------------------------------------------
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.


    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    #  Get Questions
    #  ----------------------------------------------------------------
    @app.route("/questions", methods=["GET"])
    def get_questions():
        try:
            question_list = Question.query.order_by('id').all()
            categories = Category.query.order_by('id').all()
            if len(categories) == 0:
                abort(404)
            if len(question_list) == 0:
                return jsonify(
                {
                    "success": True,
                    "questions": len(question_list),
                    "Message": "No questions yet"
                }
            )
            category_list = { category.id: category.type for category in categories }
            current_questions = paginate_questions(request, question_list)
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(question_list),
                    "categories": category_list
                }
            )
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    # Delete Question  
    # ----------------------------------------------------------------
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)
            
            question.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                }
            )

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    # Create Questions
    # ----------------------------------------------------------------
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        answer = body.get("answer", None)
        category = body.get("category", None)
        difficulty = body.get("difficulty", None)
        rating = body.get("rating", None)

        if not (new_question and answer and category and difficulty and rating):
            return abort(400)

        try:
            question = Question(
                question = new_question, 
                answer = answer, 
                category_id = category,
                difficulty = difficulty,
                rating = rating
            )
            question.insert()

            return jsonify(
                {
                    "success": True,
                    "message": "Question created sucessfully",
                }
            )

        except:
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    # Search Questions
    # ----------------------------------------------------------------
    @app.route("/questions/search", methods=["POST"])
    def search_question():
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        try:
            question_list = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            if not question_list:
                return abort(404)

            current_questions = paginate_questions(request, question_list)
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(question_list)                
                }
            )

        except:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    # Get Questions By Categories
    # ----------------------------------------------------------------
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        try:
            categories = Category.query.order_by('id').all()
            if len(categories) == 0:
                abort(404, 'Categories not found')
            for category in categories:
                if category.id == category_id:
                    current_category = category.type
                    quest_list = [question.format() for question in category.questions]
               
            return jsonify(
                {
                    "success": True,
                    "questions": quest_list,
                    "total_questions": len(quest_list),
                    "current_category": current_category,
                }
            )
        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    # Play Quiz
    # ----------------------------------------------------------------
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        body = request.get_json()
        quiz_category = body.get("quiz_category", None)
        previous_questions = body.get("previous_questions", None)
        try:
            if quiz_category['id'] == 0:
                if len(previous_questions) == 0:
                    questions = Question.query.all()
                else:
                    questions = Question.query.filter(
                        Question.id.notin_(previous_questions)
                        ).all()

            else:
                if len(previous_questions) == 0:
                    questions = Question.query.filter(
                        Question.category_id == quiz_category['id']
                        ).all()
                else:
                    questions = Question.query.filter(
                        Question.category_id == quiz_category['id'],
                        Question.id.notin_(previous_questions)
                        ).all()

            if len(questions) > 0:
                question = random.choice(questions).format()
            else:
                question = []

            return jsonify({
                'success': True,
                'question': question
            })

        except:
            abort(422)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 404, 
                "message": "resource not found"
                }), 404
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({
                "success": False, 
                "error": 405, 
                "message": "method not allowed"
                }), 405
        )


    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False, 
                "error": 422, 
                "message": "unprocessable"
                }), 422
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400, 
            "message": "bad request"
            }), 400


    return app

