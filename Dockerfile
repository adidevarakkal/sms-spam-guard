FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run the tests, then the full evaluation; the container fails if any test fails
CMD ["sh", "-c", "python -m pytest -q && python -m src.evaluate"]
