from fastapi import FastAPI
import psycopg2
import os
import logging
from prometheus_client import Counter, generate_latest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI()

REQUEST_COUNT = Counter("api_requests_total", "Total API requests")

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@app.get("/status")
def status():
    REQUEST_COUNT.inc()
    return {"status": "OK"}

@app.get("/items")
def items():
    REQUEST_COUNT.inc()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items;")
    data = cur.fetchall()
    conn.close()
    return [{"id": i[0], "name": i[1]} for i in data]

@app.get("/metrics")
def metrics():
    return generate_latest()
