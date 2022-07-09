# tap-gds-assessment

## Assumptions
1. Each round allows one team to versus another team only once. As such, in the case where "teamA teamB 0 1" and "teamB teamA 0 1" are entered, an error will be shown.
2. There are no restrictions to limit the number of teams that can be added although there is a fixed number of 12 teams.
3. Matches between teams from different groups are not allowed and is strictly enforced in the application.
4. All team and match inputs are assumed to be of correct format except for possible extra newline spaces.

## Notes
1. Since the application is still small, I decided to host both frontend and backend in the same deployed instance. However, for the purpose of scalability, I have designed the application architecture to follow the MVC framework while modularising the frontend and backend so as to loosen the coupling between the two.
2. The application instance is hosted on heroku while the database is an AWS RDS database. Deployed application is in this link: https://tap-gds-assessment.herokuapp.com/
3. As Heroku tends to switch off applications that are not in use frequently, please contact me through telegram(@danteliew6) if the above link does not work so that I can reboot the deployed application.
4. I have also attached my postman collection in this repository for your perusal on my APIs.

## How to Set Up
### 1. After cloning repository, navigate to 'config.py' and edit the database configuration code line below

```
Do ensure that the DB Schema indicated is a valid schema as flask will not create the schema and will throw an error.

Without Password:
SQLALCHEMY_DATABASE_URI = environ.get('dbURL') or 'mysql+mysqlconnector://<DB_USERNAME>@<DB_ENDPOINT>:3306/<DB_SCHEMA>'

With Password:
SQLALCHEMY_DATABASE_URI = environ.get('dbURL') or 'mysql+mysqlconnector://<DB_USERNAME>:<DB_PASSWORD>@<DB_ENDPOINT>:3306/<DB_SCHEMA>'
```

### 2. Open a new terminal and run the following code below to set up the database
```
flask db stamp head
flask db migrate
flask db upgrade
```

### 3. Lastly, run this line of code to boot up your flask application
```
flask run
```
