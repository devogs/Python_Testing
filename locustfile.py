from locust import HttpUser, task, between
from datetime import datetime

class WebsiteUser(HttpUser):
    # Set the time to wait between tasks for each user
    wait_time = between(1, 5)

    def on_start(self):
        """on_start is called when a user starts a task set"""
        # This simulates a user logging in
        login_data = {
            "email": "john@simmons.com"
        }
        self.client.post("/showSummary", data=login_data)

    @task(3)
    def book_a_place(self):
        """Simulates booking a place"""
        # We need to retrieve a valid competition and club for the POST data
        # In a real test, you would fetch these dynamically from the app
        # For this example, we use a known working set
        book_data = {
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "1"
        }
        self.client.post("/purchasePlaces", data=book_data)

    @task(1)
    def view_points_board(self):
        """Simulates viewing the points board"""
        self.client.get("/pointsDisplay")

    @task
    def logout(self):
        """Simulates logging out"""
        self.client.get("/logout")
        self.stop() # This stops the user from executing further tasks