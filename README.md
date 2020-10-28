# Guide to organize file in this project

## Directory
database (database and classes)

&ensp;- user

&emsp;&emsp;user_schema.py

&ensp;- session
 
&ensp;- contact
 
&ensp;- event

&ensp;- organization

&ensp;- receipt

&ensp;- notification

product (API calls)

&nbsp;&nbsp; - api_functions

&emsp; - user

&emsp;&emsp; get_apis.py

&emsp;&emsp; post_apis.py

&emsp;&emsp; put_apis.py

&emsp;&emsp; delete_apis.py  

&emsp;...

&nbsp;&nbsp; - helper_functions

&emsp; user_helper.py

&emsp; ...

tests

&ensp;- database

&ensp;- api



## Write clean code:

- Make code readable for people (indentation) 
- Use meaningful names for variables, functions and methods (short but descriptive)
- Let one function or method perform only one task
- Use comments for clarification
- Be consistent
- Review your code regularly
- Write a function / class:

&emsp;&emsp; Start with comments:

&emsp;&emsp;&emsp; What does this function / class do? 

&emsp;&emsp;&emsp; What kinds of parameters is taken as input? (function) 

&emsp;&emsp;&emsp; What variables should we store in class? (class)

&emsp;&emsp;&emsp; What kinds of output will be? (function)

- Make comments/notes as you progress

## Set up the project:

git clone the repo

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

Follow this the upper website on installing packages

You should have done these after the website:

install / upgrade pip if needed

create a virtual environment

activate the env

(make sure you have the correct "python" running. py or python or python3)

Your dir should be: (env) yourdirectory

Run: py install -r requirements.txt

Run the init_db.py to initialize database

Run main.py to start the server

## Set up requirements packages:

Will add more into this as we go.
  
Flask==1.1.2

psycopg2-binary==2.8.6

Flask-Migrate==2.5.3

Flask-SQLAlchemy==2.4.4

flask-marshmallow==0.14.0

python-dotenv==0.14.0

argon2-cffi==20.1.0 

zxcvbn==4.4.28

email-validator==1.1.1

marshmallow-sqlalchemy==0.24.0

marshmallow-enum==1.5.1
