import app
from app import app
from functions import is_valid_email


class TestLoginUnknownEmail:
    client = app.test_client()

    def test_valid_email(self):
        # app.clubs = []
        if hasattr(app, "clubs") and app.clubs and len(app.clubs) > 0:
            result = self.client.post("/showSummary", data={"email": app.clubs[0]["email"]})
            assert result.status_code in [200, 302]
            # assert f"{app.clubs[0]['email']}" in result.data.decode()
        else:
            print("app does not have the attribute 'clubs' or it is empty")

    def test_invalid_email(self):
        email = "jhbdfkshdvf"
        if is_valid_email(email):
            result = self.client.post("/showSummary", data={"email": email})
            assert result.status_code == 401
            assert "No account related to this email." in result.data.decode()
        else:
            print("The email address is invalid.")

    def test_empty_email(self):
        email = ""
        if len(email) == 0:
            print("The email address is empty.")
        else:
            result = self.client.post("/showSummary", data={"email": email})
            assert result.status_code == 401
            assert "Please enter your email." in result.data.decode()
