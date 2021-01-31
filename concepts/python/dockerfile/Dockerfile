FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY config.toml /root/.streamlit/config.toml
EXPOSE 8051/tcp
ENTRYPOINT [ "/usr/local/bin/streamlit", "run", "streamlit_helloworld2.py" ]