# AI DOC QUERY

An application that allows users to upload pdf files to the server. User can then query the chatbot regarding the pdf files.
## Features
1. Login/SignUp
2. User Authentication (JWT tokens)
3. Create/Delete Chats.
4. Upload Files
5. Question Chatbot regarding the content of pdf

## Technologies Used
1. Django (Backend)
2. React (Frontend)
3. MongoDB (Database)

## Pre-requisits
1. Django
2. Node.js
3. npm
4. Python 3.x


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