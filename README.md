gudlift-registration

    Why

    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

    Getting Started

    This project uses the following technologies:

        Python v3.x+

        Flask

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need.

        Virtual environment

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally.

    Installation

        After cloning, change into the directory and type virtualenv .. This will then set up a a virtual python environment within that directory.

        Next, type source bin/activate. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type deactivate

        Rather than hunting around for the packages you need, you can install in one step. Type pip install -r requirements.txt. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is pip freeze > requirements.txt

        Setting the Flask Environment: Before running the application, you need to tell Flask which file to use.

    export FLASK_APP=server.py

        You should now be ready to test the application. In the directory, type either flask run or python -m flask run. The app should respond with an address you should be able to go to using your browser.

    Current Setup

    The app is powered by JSON files. This is to get around having a DB until we actually need one. The main ones are:

        competitions.json - list of competitions

        clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

    Testing

    You are free to use whatever testing framework you like-the main thing is that you can show what tests you are using.

    We also like to show how well we're testing, so there's a module called
    coverage you should add to your project.
    Code Coverage

    To measure code coverage, you can use the coverage.py tool with pytest.

        Run the tests and collect data:

    coverage run -m pytest

        Generate a report:

            In the terminal: For a quick summary.

        coverage report

            As an HTML report: For a detailed, line-by-line view.

        coverage html

    Performance Testing

    To run load tests and measure the application's performance, we use Locust.

        Start Locust: Make sure your Flask application is running in another terminal.

    locust -f locustfile.py

        View the report: Open your browser and navigate to http://localhost:8089 to access the Locust web UI.