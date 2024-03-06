<h1 align="center" style="font-weight: bold;">HelpInvestor API 💸 💻</h1>

<p align="center">
 <a href="#technologies">Technologies</a> • 
<a href="#architecture">Architecture</a> •
 <a href="#started">Getting Started</a> • 
 <a href="#future">Features, suggestions and the future</a> 
</p>

<p align="center">
    <b>Add your asset from Brazilian stock exchange<br> set a buy and sell price.
When the price targets<br> we going to send you a notification</b>
</p>

<h2 id="technologies">💻 Technologies</h2>

- Django
- Django Rest Framework
- AWS Lambda
- AWS EC2
- AWS RDS
- AWS SNS
- PostgresSQL
- pytest

<h2 id="architecture">🏠 Architecture</h2>

<p>This api was built using clean architecture, TDD methodology, SOLID and clean code.</p>

```
- helpinvestor/
  - api/
    - *exposes the application to the internet*
  - configs/
    - *configs for project*
  - core/
    - *contains the business logic*
  - db/
    - *our database models*
  - services/
    - *connects with third party system*
```
<h2 id="started">⏲️ Getting started</h2>

The app are running with `Python 3.10.12`

- Clone the project
- Create a virtualenv

```bash
python3 -m venv venv
```
- Activate
  
```bash
source venv/bin/activate
```

- Install libraries and dependencies

```bash
pip install -r requirements.txt
```

<h3>Config .env variables</h2>

Use the `.env.example` as reference to create your configuration file `.env` with your Credentials

```yaml
DATABASE_ENGINE='django.db.backends.sqlite3'
DATABASE_NAME="./db.sqlite3"
DATABASE_USER=""
DATABASE_PASSWORD=""
DATABASE_HOST="127.0.0.1"
DATABASE_PORT="5432"

DEBUG=1

SECRET_KEY='django-insecure-c=3jl88ulheb!jv6w_)1l(6b7nge527vza4^)hofolc43f1+wh'

ASSETS_API_KEY = '123123123' # get your key here: https://www.alphavantage.co/
```

<h3>Starting</h3>

```bash
python manage.py runserver
```

<h2 id="future">🚀 Features, suggestions and the future</h2>
<p>This api is alive, it will be update with new features, and suggestions:</p>

| desc.           | status |
|-----------------|--------|
| Create Investor | Done   |
| Create Asset    | Done   |
| Task for quotes | Done   |
| Push notifications | To-do |
| Phone Validator | To-do  |
| Update Investor | To-do  |
| Update Asset | To-do  |
| Test coverage 100% | To-do  |
| CI/CD for deploy | To-do  |


Do you want register a new feature or a bug? open a `pull-request` or contact me at [gvianadev.com](https://gvianadev.com)
