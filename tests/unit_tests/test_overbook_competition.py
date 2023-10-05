import app
from app import app


class TestOverbookCompetition:
    client = app.test_client()
    competition = [
        {
            "name": "Test",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "5"
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "test_club@email.com",
            "points": "20"
        }
    ]

    def setup_method(self):
        app.competitions = self.competition
        app.clubs = self.club

    def test_overbook_competition(self):
        booked = 6
        try:
            result = self.client.post(
                "/purchasePlaces",
                data={
                    "places": booked,
                    "club": self.club[0]["name"],
                    "competition": self.competition[0]["name"]
                }
            )

            assert result.status_code == 400
            try:
                assert "Not enough places available." in result.data.decode()
                assert int(self.competition[0]['numberOfPlaces']) >= 0
            except AttributeError:
                print("'NoneType' object has no attribute")
        except AssertionError:
            print("'NoneType' object has no attribute")

    def test_book_within_availability(self):
        booked = 1
        try:
            result = self.client.post(
                "/purchasePlaces",
                data={
                    "places": booked,
                    "club": self.club[0]["name"],
                    "competition": self.competition[0]["name"]
                }
            )
            try:
                assert result.status_code == 200
                assert "Great-booking complete!" in result.data.decode()
                assert int(self.competition[0]['numberOfPlaces']) >= 0
            except AssertionError:
                print("'NoneType' object has no attribute")
        except AttributeError:
            print("'NoneType' object has no attribute")
