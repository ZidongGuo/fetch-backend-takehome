# Fetch Backend Takehome Exercise (Receipt-processor)

Build a webservice that fulfils the documented API. You can find the specific requirements under Receipt-Processor-Instruction.md.
The backend service for receipt processor was built with Flask and python. You can find the detailed code in app.py. The backend service is tested with unit_tests.py and you can find some tested JSON queries under /examples. 

## Local Setup and Testing- Without Docker
1. Clone the repository: 

```bash
    git clone https://github.com/ZidongGuo/fetch-backend-takehome.git
```

2. CD to the corresponding file directory:

```bash
    cd fetch-backend-takehome
```

3. Make sure to have pip and python 3.9 or newer version installed. Install the required libraries with the command:

```bash
    pip install -r requirements.txt
```

4. Launch the server at http://127.0.0.1:5000/ by running app.py under the directory or by running command:

```bash
    python app.py
```

5. Unit tests are provided in unit_tests.py and you can run the test cases with:
```bash
    python unit_tests.py
```

6. You can utilize Postman for mocking GET/POST JSON query to http://127.0.0.1:5000/receipts/process and http://127.0.0.1:5000/receipts/{id}/points where id is the response value. 
![Screenshot](POSTquery.png)
<br />
![Screenshot](GETquery.png)


## Local Setup and Testing- With Docker
1. Clone the repository: 

```bash
    git clone https://github.com/ZidongGuo/fetch-backend-takehome.git
```
2. CD to the corresponding file directory:

```bash
    cd fetch-backend-takehome
```
3. Open Docker Destop.

4. Generate Docker Container with the command:
```bash
    docker build -t flask-app .
```

5. Run the container and map container port to host machine (in this case, port 5000) with:
```bash
    docker run -p 5000:5000 flask-app
```

6. Test GET and POST request with curl command