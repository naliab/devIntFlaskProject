FROM python:latest

EXPOSE 5000

COPY . .

RUN pip install --upgrade pip
RUN pip install --default-timeout=100 -r requirements.txt
CMD ["bash", "start.sh"]