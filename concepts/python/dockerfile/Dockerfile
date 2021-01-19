FROM python:3

WORKDIR /home/kaizhang/f/helloworld/concepts/python

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./TESTG.py" ]