FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y wireguard-tools
RUN pip install flask
COPY main.py .
CMD ["python", "main.py"]
