# Gudlift Registration

## Why
This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is to keep things as light as possible, and use feedback from the users to iterate.

---

## Getting Started

This project uses the following technologies:
- **Python v3.x+**
- **Flask**

Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need.

---

## Virtual Environment

Using a virtual environment ensures you'll be able to install the correct packages without interfering with Python on your machine. Before you begin, please ensure you have this installed globally.

---

## Installation

1. Clone the repository and change into the directory.

2. Set up a virtual environment:
   ```bash
   virtualenv .
   ```

3. Activate the environment:
   ```bash
   source bin/activate
   ```
   You should see that your command prompt has changed to the name of the folder. This means that you can install packages here without affecting files outside.  
   To deactivate:
   ```bash
   deactivate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. If you install a package, make sure others know by updating the `requirements.txt` file:
   ```bash
   pip freeze > requirements.txt
   ```

---

## Setting the Flask Environment

Before running the application, tell Flask which file to use:
```bash
export FLASK_APP=server.py
```

Now you are ready to test the application. In the directory, type either:
```bash
flask run
```
or
```bash
python -m flask run
```

The app should respond with an address that you can open in your browser.

---

## Current Setup

The app is powered by **JSON files**. This avoids using a database until we actually need one. The main files are:
- `competitions.json` – list of competitions
- `clubs.json` – list of clubs with relevant information

You can check `clubs.json` to see what email addresses the app will accept for login.

---

## Testing

You are free to use whatever testing framework you like—the main thing is to demonstrate what tests you are using.

We also encourage showing **how well the app is tested**, so you should add the `coverage` module to your project.

---

## Code Coverage

To measure code coverage, use **coverage.py** with **pytest**.

Run the tests and collect data:
```bash
coverage run -m pytest
```

Generate a report:
- Quick summary:
  ```bash
  coverage report
  ```
- Detailed, line-by-line HTML report:
  ```bash
  coverage html
  ```

---

## Performance Testing

We use **Locust** to run load tests and measure the application's performance.

1. Make sure your Flask application is running in another terminal.
2. Start Locust:
   ```bash
   locust -f locustfile.py
   ```
3. Open your browser and go to [http://localhost:8089](http://localhost:8089) to access the Locust web UI.
