FROM python:3.8

WORKDIR /app

COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

RUN chmod +x ./entrypoint.sh
ENTRYPOINT [ "/app/entrypoint.sh" ]