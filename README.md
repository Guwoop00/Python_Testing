# Güdlft

Reservation platform for competition spots for the company Güdlft.

L'objectif du projet est de corriger les erreurs et bugs présents dans le projet 
[Python_Testing](https://github.com/OpenClassrooms-Student-Center/Python_Testing), 


## Project Initialization

### Windows :
Navigate to the desired folder.

###### • Clone the project

```
git clone https://github.com/Guwoop00/Python_Testing.git
```

###### • Activate the virtual environment

```
python -m venv env 
env\Scripts\activate
```

###### • Install the required packages

```
pip install -r requirements.txt
```

### MacOS et Linux :
Navigate to the desired folder.

###### • Clone the project
```
git clone https://github.com/Guwoop00/Python_Testing.git
```

###### • Activate the virtual environment
```
python3 -m venv env 
source env/bin/activate
```

###### • Install the required packages
```
pip install -r requirements.txt
```


## Usage

1. Run Flask server

```
$env:FLASK_APP = "server.py"
flask run
```

2. To access the site, go to the default address: : [http://127.0.0.1:5000/](http://127.0.0.1:5000/)


### Tests unitaires / tests d'intégration

Unit and integration tests are executed using [Pytest](https://docs.pytest.org/en/6.2.x/index.html) (version 6.2.5).

To perform all unit and integration tests, enter the command:
```
pytest tests
```

### Test de performances

It is possible to perform a performance test using the Locust module [Locust](https://locust.io) (version 2.7.2).
To start the test server, enter the command:

```
locust -f tests/perf_tests/locustfile.py --host http://127.0.0.1:5000 --run-time 3m
```

Go to the address [http://localhost:8089](http://localhost:8089)
