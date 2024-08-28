<h1 align="center" style="font-weight: bold;">HelpInvestor API 💸 💻</h1>

<p align="center">
 <a href="#technologies">Technologies</a> • 
<a href="#architecture">Architecture</a> •
 <a href="#routes">Routes</a> •
 <a href="#started">Getting Started</a> • 
 <a href="#future">Features, suggestions and the future</a> •
 <a href="#warnings">Warnings</a>
</p>

<p align="center">
    <b>Add your asset from Brazilian stock exchange<br> set a buy and sell price.
When the price targets<br> we going to send you a notification</b>
</p>

<p align="center">
  <img src="https://github.com/guirlviana/helpinvestor/assets/65058505/b05b0253-ba69-4f44-a677-3f5049489573" alt="Screenshot" />
</p>

<p align="center">
 For get a live demo, check the <a href="#routes">Routes</a> and consider the <a href="#warnings">Warnings</a>
</p>


<h2 id="technologies">💻 Technologies</h2>

- Python
- Django
- Django Rest Framework
- AWS Lambda
- AWS EventBridge
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
    - task_send_quote_prices_sms
     - *python code scheduled for periodic execution on Lambda*
```

<h2 id="routes">🛣️ Routes</h2>

URL: http://34.196.116.240

<h3>POST /investor/</h3>

**REQUEST**
```json
{
    "name": "John",
    "last_name": "Cena",
    "email": "johncena@gmail.com",
    "phone": "+5511999999999",
    "password": "123456"
}
```
<h3>POST /api-token-auth/</h3>

**REQUEST**
```json
{
    "username": "johncena@gmail.com",   
    "password": "123456"
}
```

**RESPONSE**
```json
{
  "token": "OwoMRHsaQwyAgVoc3OXmL1JhMVUYXGGBbCTK0GBgiYitwQwjf0gVoBmkbuyy0pSi"
}
```

<p>🚨 All of the endpoints below need to pass the token in headers, in the format:</p>

```
Key: Authorization
Value: Token OwoMRHsaQwyAgVoc3OXmL1JhMVUYXGGBbCTK0GBgiYitwQwjf0gVoBmkbuyy0pSi
```

<h3>POST /create-asset/</h3>

**REQUEST**
```json
{"symbol": "ITSA4", "buy_price": 11.86, "sale_price": 12.06}
```

<h3>PUT /edit-asset/[id: int]/</h3>

Will change only the fields passed

**REQUEST**
```json
{"buy_price": 11.81, "sale_price": 12.01}
```

<h3>GET /get-assets/</h3>

**RESPONSE**
```json
{
    "response": [
        {
            "id": 1,
            "symbol": "ITSA4",
            "buy_price": "11.86",
            "sale_price": "12.06"
        }
    ]
}
```

<h3>DELETE /delete-asset[id: int]/</h3>

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

You can run using Docker as well

Change the ENV's in `Dockerfile` using `.env.example` as reference, after run

```
docker build -t helpinvestor .
```
```
docker run -d -p 8000:8000 helpinvestor
```

<h3>Starting</h3>

```bash
python manage.py runserver
```

<h2 id="future">🚀 Features, suggestions and the future</h2>
<p>This api is alive, it will be update with new features, and suggestions:</p>

| desc.           | status |
|-----------------|--------|
| Create Investor | ✔️   |
| Create Asset    | ✔️   |
| Async Task for quotes | ✔️   |
| SMS notifications | ✔️ |
| Phone Validator | ✔️  |
| Tests | ✔️  |
| Dockerization | ✔️  |
| CI/CD for unit tests | ✔️  |


Do you want register a new feature or a bug? open a `pull-request` or contact me at [gvianadev.com](https://gvianadev.com)

<h2 id="warnings">⚠️ Warnings</h2>

Our API will have a break because the API we used to obtain the asset quote will now be paid.

If you want to sponsor the project, contact me!

<p>If you want to deploy and customize it, feel free to change the values</p>
