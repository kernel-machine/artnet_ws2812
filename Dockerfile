FROM python:3.11

RUN apt update -y && apt install -y python3-venv
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN python3 -m venv env
RUN ./env/bin/pip3 install -r requirements.txt

EXPOSE 6454
# Run your app
COPY . /app
CMD [ "./env/bin/python3", "main.py" ]
