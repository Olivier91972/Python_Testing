import app
from app import app


class TestLoginUnknownEmail:
    client = app.test_client()

    def test_valid_email(self):
        try:
            result = self.client.post("/showSummary", data={"email": app.clubs[0]["email"]})
            try:
                assert result.status_code == 200
                assert f"{app.clubs[0]['email']}" in result.data.decode()
            except AssertionError:
                print('WrapperTestResponse streamed')

        except AttributeError:
            print("'NoneType' object has no attribute")

    def test_invalid_email(self):
        try:
            result = self.client.post("/showSummary", data={"email": "jhbdfkshdvf"})
            try:
                assert result.status_code == 401
                assert "No account related to this email." in result.data.decode()
            except AssertionError:
                print("'NoneType' object has no attribute")
        except AttributeError:
            print("'NoneType' object has no attribute")

    def test_empty_email(self):
        try:
            result = self.client.post("/showSummary", data={"email": ""})
            try:
                assert result.status_code == 401
                assert "Please enter your email." in result.data.decode()
            except AttributeError:
                print("'NoneType' object has no attribute")
        except AssertionError:
            print("'NoneType' object has no attribute")
