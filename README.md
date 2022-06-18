# Udacity Trivia API

This project is a trivia game for Udacity students. As a part of the Fullstack Nanodegree, completing this trivia app will give us the ability to structure, plan, implement, and test an API. Which are skills essential for enabling future applications to communicate with others.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## About the Application

This application performs the following actions:
1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Add categories
3) Delete categories
4) Add questions and require that they include question and answer text.
5) Delete questions.
6) Search for questions based on a text query string.
7) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Fetches a dictionary of categories with ids as keys and category type as values
    - Returns: True and a list of categories
- Sample: `curl http://127.0.0.1:5000/categories`

* Example Response:
```
{
    'success': True,
    'categories': {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
        }
}
```

#### POST /categories
- General:
    - Creates a category
    - Returns: True if successful and success message
* Request Body:
```
{
    type:string
}
```
* Example Response:
```
{
    'success': True,
    'message': 'Category created sucessfully'
}
```
#### DELETE /categories/{category_id}
- General:
    - Deletes a category from the categories list.
    - Request parameters: `category_id`
    - Returns: True if successfully deleted and the id of deleted category
* Example Response:
```
{
    'success': True,
    'deleted': '2',
}
```
#### GET /questions?page={page_number}
- General:
    - Fetches a dictionary of questions with questions, answers, difficulty, ids and category as keys
    - Fetches a dictionary of categories with ids as keys and the category types as values
    - Request arguments: `page_number`
    - Returns: True, list of questions, categories and total questions
- Sample: `curl http://127.0.0.1:5000/questions?page=1`

* Example Response:
```
{
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    'categories': {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
        }
    "success": true,
    "total_questions": 19
}
```

#### GET /categories/{category_id}/questions
- General:
    - Fetches lists of questions based on a category
    - Request parameters: `category_id` 
    - Returns: True, a list of questions,total number of questions and the current category
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

* Example Response:
```
{
    "current_category": 1,
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "total_questions": 19
}
```
#### POST /questions
- General:
    - Creates question
    - Returns: True if successful and success message
* Request Body:
```
{
    question: string,
    answer: string,
    category: integer,
    difficulty: integer
}
```
* Example Response:
```
{
    'success': True,
    'message': 'Question created sucessfully'
}
```
#### POST /questions/search
- General:
    - Fetches questions based on the search term
    - Returns: True and a list of questions if succesful
* Request Body:
```
{
    search_term: string
}
```
* Example Response:
```
{
    'success': True,
    'questions': [
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ]
```
#### DELETE /questions/{question_id}
- General:
    - Deletes a question from the questions list.
    - Request parameters: `question_id`
    - Returns: True if successfully deleted and the id of deleted question
* Example Response:
```
{
    'success': True,
    'deleted': '9',
}
```
#### POST /play_quiz
- General:
    - Plays the trivia quiz by fetching questions
* Request Body:
```
{
    "quiz_category": string,
    "previous_questions": []
}
```
* Example Response:
```
{
    "question":{
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
        },
    "success": True
}
```

## Deployment N/A

## Authors
* Udacity
* lilstex [lilstex4good@gmail.com]

## Acknowledgements 
The awesome team at Udacity and all of my fellow students especially the full stack gurus!  