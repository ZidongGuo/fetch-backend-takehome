FROM python:3.9

WORKDIR /fetch-backend-takehome

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run the unit tests
RUN python -m unittest unit_tests.py

EXPOSE 5000

CMD ["python", "app.py"]