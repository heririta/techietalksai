# FastAPI SSE Server
FROM python:3.11-slim

WORKDIR /app
COPY sse_server.py /app/
RUN pip install fastapi uvicorn aiohttp websockets

CMD ["python", "sse_server.py"]
