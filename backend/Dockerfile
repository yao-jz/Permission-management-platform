FROM python:3.8.3

ENV HOME=/opt/backend

WORKDIR $HOME

COPY . $HOME

CMD ["pip", "install", "-r", "./requirements.txt"]
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
