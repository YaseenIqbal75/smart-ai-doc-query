# SMART DOC QUERY

An application that assists user upload multiple files and take assistance from chatbot to get answers of their questions regarding uploaded files.

## Features
### Backend
1. Implemented RESTful apis for Login/Signup
2. Implemented RESTful apis for CRUD operations on Chats
3. Implemeted RESTful apis for create,delete,read operations on Files
5. Implemented RESTful apis for create operation on messages.
6. Integerated JWT varification for user authentication and authorization
### Frontend
1. Login/SignUp
2. User Authentication (JWT tokens)
3. Create/Delete Chats.
4. Upload Files
5. Question Chatbot regarding the content of pdf

## Technologies Used
1. Django 4.2.13 (Backend)
2. React 18.3.1 (Frontend)
3. MongoDB (Database)

## Pre-requisits
1. Django 4.2.13
2. Node.js 20.15.0
3. npm 10.7.0
4. Python 3.8.10


## Installation 
### Backend Setup:

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.

Install [MongoDB](https://www.mongodb.com/docs/manual/installation/) 

#### Create a vitual environment

```bash
python -m venv venv
```
#### Activate the virtual environment (Linux)
```bash
source venv/bin/activate
```

#### Install project dependencies
```bash
pip install -r requirements.txt
```
#### Make migrations for Django
```bash
python manage.py makemigrations
python manage.py migrate
```
#### Go to the project directory and run server
```bash
python manage.py runserver
```

### Frontend Setup:

#### Navigate to the Frontend Directory

```bash
cd Frontend
```

#### Install Frontend Dependencies
```bash
npm install
```
#### Start the Frontend Server
```bash
npm start
```