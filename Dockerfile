FROM python:3.10.12

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV DATABASE_ENGINE='django.db.backends.sqlite3'
ENV DATABASE_NAME="./db.sqlite3"
ENV DATABASE_USER=""
ENV DATABASE_PASSWORD=""
ENV DATABASE_HOST="127.0.0.1"
ENV DATABASE_PORT="5432"

ENV DEBUG=1

ENV SECRET_KEY='django-insecure-c=3jl88ulheb!jv6w_)1l(6b7nge527vza4^)hofolc43f1+wh'

# get your key here: https://www.alphavantage.co/
ENV ASSETS_API_KEY='' 

ENV ADMIN_USERNAME='support@helpinvestor.com'
ENV ADMIN_PASSWORD='123456'

CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
