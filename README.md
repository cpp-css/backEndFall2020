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

## Set up requirements packages:

Will add more into this as we go.
- Python3
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- PGAdmin4 (to look at database - not really a requirement)
