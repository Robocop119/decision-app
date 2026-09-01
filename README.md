# Decision App

#### Video Demo: 

Decision App is a simple web application for comparing different alternatives using weighted criteria.

I created this project as my final project for CS50x. The goal of the application is to help a user make a decision when several options need to be compared using different factors.

For example, a user could create a decision called "Which laptop should I buy?", add several laptops as alternatives, and then add criteria such as price, GPU, RAM, processor, and refresh rate.

## Features

The application allows users to:

- Create decisions.
- Add alternatives to a decision.
- Add criteria and assign a weight to each criterion.
- Give each alternative a score from 0 to 10 for each criterion.
- Calculate a weighted score for every alternative.
- Display a ranking from the highest-scoring alternative to the lowest.
- Update an existing score.
- Store decisions and their data in a SQLite database.

The weights of all criteria must add up to `1.0` before the application displays a ranking.

## How the ranking works

Each criterion has a weight that represents how important it is.

For every alternative, the application multiplies the score of each criterion by its corresponding weight and adds the results together.

For example, if an alternative has:

- Price score: 8, weight: 0.6
- Performance score: 5, weight: 0.4

its final score is:

`8 × 0.6 + 5 × 0.4 = 6.8`

The alternatives are then ordered from the highest final score to the lowest.

The score calculation is separated from the Flask routes in `engine/decision_engine.py`. This keeps the decision logic independent from the web interface and makes the code easier to understand.

## Technologies

The project uses:

- Python
- Flask
- SQLite
- HTML
- CSS

## Project structure

`app.py` contains the Flask application and the routes used to create and display decisions, alternatives, criteria, scores, and results.

`engine/decision_engine.py` contains the function used to calculate the weighted score of an alternative.

`schema.sql` defines the SQLite database tables for decisions, alternatives, criteria, and scores.

`init_db.py` creates the SQLite database using the SQL statements in `schema.sql`.

`templates/index.html` contains the home page and displays the list of existing decisions.

`templates/create.html` contains the form used to create a new decision.

`templates/decision.html` displays a decision and allows the user to add alternatives, criteria, and scores. It also displays the final ranking.

`static/style.css` contains the CSS used to style the application.

`requirements.txt` contains the Python dependencies required to run the project.

## Database design

The application uses a SQLite database.

A decision can contain multiple alternatives and multiple criteria.

Each alternative belongs to one decision, and each criterion also belongs to one decision.

The `scores` table connects alternatives and criteria. Each score represents the value given to one alternative for one specific criterion.

The database also prevents duplicate scores for the same alternative and criterion combination.

## Installation

Clone the repository and open the project folder.

Create a Python virtual environment:

bash python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate.bat

Install the dependencies:

python -m pip install -r requirements.txt

Create the SQLite database:

python init_db.py

Start the application:

python app.py

Then open the following address in a web browser: http://127.0.0.1:5000
Usage

From the home page, create a new decision.

Open the decision and add the alternatives that you want to compare.

Then add criteria and assign a weight to each one. The total weight of all criteria must equal 1.0.

For every alternative and criterion, enter a score between 0 and 10.

Once the criterion weights equal 1.0, the results section displays the alternatives ordered by their weighted score.

If a score is entered again for the same alternative and criterion, the application updates the previous score instead of creating a duplicate.

The application includes basic validation to prevent invalid or empty values from causing errors.

Design choices

I decided to use Flask because it provides a simple way to connect Python code with HTML pages without requiring a more complex frontend framework.

SQLite was chosen because it is lightweight, simple to use, and sufficient for a project of this size.

Scores use a scale from 0 to 10 because it provides a simple and consistent way to compare alternatives across different criteria.

Criterion weights must add up to 1.0. This makes each weight represent a proportion of the final score and keeps the weighted calculation easy to understand.

I also separated the score calculation into engine/decision_engine.py instead of placing all the logic directly inside the Flask routes. This keeps the calculation logic separate from the web-related code.

Limitations

The application is intentionally simple.

It does not include user accounts, automatic collection of external data, advanced decision-making algorithms, or external APIs.

All alternatives, criteria, weights, and scores are entered manually by the user.

The current version uses a simple weighted scoring method. It is designed as a small final project that demonstrates the concepts learned during CS50x rather than as a production-ready application.