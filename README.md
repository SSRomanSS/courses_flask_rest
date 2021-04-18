# *FLASK COURSES DB* (test project)

## Installation
<br/>

Make directory for the project:
```
$ mkdir <project_dir>
```
Create virtual environment into project directory:
```
$ python3 -m venv <env_dir>
```
 
and activate it:
```
source <env_dir>/bin/activate
```
Clone git repository into environment directory:
```
$ git clone https://github.com/SSRomanSS/courses_flask_rest
```
Change directory:
```
$ cd courses_flask_rest/
```
Install all dependencies:
```
$ pip install -r requirements.txt
```
Run
```
$ flask run
```

## Links
GET all courses
```
http://localhost:5000/api/courses
```
GET courses with search parameters
```
http://localhost:5000/api/courses?params1=value1&params2=value2
```
> allowed params: title, date, start_date, end_date (format for date: dd/mm/yyyy)

title: search courses by title
<br>
date: search all courses which take place on a specified data
<br>
start_date & end_date: search courses between two dates


GET method for getting single course by id
```
http://localhost:5000/api/courses/<id>
```

POST method for creating a new course
```
http://localhost:5000/api/courses
```
> fields: title, start_date, end_date, lectures_number (format for date: dd/mm/yyyy)

PUT method for updating an existing course by id
```
http://localhost:5000/api/courses/<id>
```
> fields: title, start_date, end_date, lectures_number (format for date: dd/mm/yyyy)

DELETE method for deleting course by id
```
http://localhost:5000/api/courses/<id>
```
