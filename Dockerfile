FROM python:3.8.1
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD main.py .
ENTRYPOINT ["python", "main.py"]
