FROM python:3.8.1
ADD main.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]
