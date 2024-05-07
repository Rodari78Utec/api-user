FROM python:3-slim
WORKDIR /programas/api-users
RUN pip3 install flask
RUN pip3 install flask-mysql
RUN pip3 install Flask-RESTful
COPY . .
CMD [ "python3", "./app.py" ]
