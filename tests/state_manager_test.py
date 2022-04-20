import unittest
from src.state_manager import StateManager

class StateManagerTest(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()

    def test_empty_state_is_initialized(self):
        """Test that the initial empty state is propery initialized."""
        current_state = {}
        trip = self._generate_trip_object(1, start_time="2022-01-01T00:00:00+0000")
        api_response = self._generate_api_response(trip)

        updated_state = self.state_manager.update_state(current_state, api_response)

        self.assertDictEqual(
            updated_state,
            {
                "byTripId": {trip["trip_id"]: trip},
                "byStartDate": {"2022-01-01": [trip]},
            }
        )

    def test_append_trip(self):
        """Test that new trip is appended to the existing state."""
        trip = self._generate_trip_object(1, start_time="2022-01-01T00:00:00+0000")
        current_state = {
            "byTripId": {trip["trip_id"]: trip},
            "byStartDate": {"2022-01-01": [trip]}
        }
        new_trip = self._generate_trip_object(2, start_time="2022-01-01T00:01:00+0000")
        api_response = self._generate_api_response(new_trip)

        updated_state = self.state_manager.update_state(current_state, api_response)

        self.assertDictEqual(
            updated_state,
            {
                "byTripId": {trip["trip_id"]: trip, new_trip["trip_id"]: new_trip},
                "byStartDate": {"2022-01-01": [trip, new_trip]}
            }
        )

    def test_append_trip_with_diff_date(self):
        """Test that new trip with a different date from the existing trip is appended properly to the existing state."""
        trip = self._generate_trip_object(1, start_time="2022-01-01T00:00:00+0000")
        current_state = {
            "byTripId": {trip["trip_id"]: trip},
            "byStartDate": {"2022-01-01": [trip]}
        }
        new_trip = self._generate_trip_object(2, start_time="2022-01-02T00:01:00+0000")
        api_response = self._generate_api_response(new_trip)

        updated_state = self.state_manager.update_state(current_state, api_response)

        self.assertDictEqual(
            updated_state,
            {
                "byTripId": {trip["trip_id"]: trip, new_trip["trip_id"]: new_trip},
                "byStartDate": {
                    "2022-01-01": [trip],
                    "2022-01-02": [new_trip]
                }
            }
        )

    def test_update_trip(self):
        """Test that existing trip in the existing state is properly updated."""
        trip = self._generate_trip_object(1, end_time=None)
        current_state = {
            "byTripId": {trip["trip_id"]: trip},
            "byStartDate": {"1970-01-01": [trip]}
        }
        updated_trip = self._generate_trip_object(1, end_time="1970-01-01T00:20:15+0000")
        api_response = self._generate_api_response(updated_trip)

        updated_state = self.state_manager.update_state(current_state, api_response)

        self.assertDictEqual(
            updated_state,
            {
                "byTripId": {trip["trip_id"]: updated_trip},
                "byStartDate": {"1970-01-01": [updated_trip]}
            }
        )

    def test_update_trip_retain_other_trips(self):
        """Test that updating a trip does not affect other trips."""
        trip = self._generate_trip_object(1, end_time=None)
        trip_2 = self._generate_trip_object(2)
        current_state = {
            "byTripId": {trip["trip_id"]: trip, trip_2["trip_id"]: trip_2},
            "byStartDate": {"1970-01-01": [trip, trip_2]}
        }
        updated_trip = self._generate_trip_object(1, end_time="1970-01-01T00:20:15+0000")
        api_response = self._generate_api_response(updated_trip)

        updated_state = self.state_manager.update_state(current_state, api_response)

        self.assertDictEqual(
            updated_state,
            {
                "byTripId": {trip["trip_id"]: updated_trip, trip_2["trip_id"]: trip_2},
                "byStartDate": { "1970-01-01": [updated_trip, trip_2]}
            }
        )

    def test_api_return_empty_trip_list(self):
        """Test when vehicle API responds with empty trip list."""
        trip = self._generate_trip_object(1)
        current_state = {
            "byTripId": {trip["trip_id"]: trip},
            "byStartDate": {"1970-01-01": [trip]}
        }
        api_response = self._generate_api_response()

        updated_state = self.state_manager.update_state(current_state, api_response)

        self.assertDictEqual(
            updated_state,
            {
                "byTripId": {trip["trip_id"]: trip},
                "byStartDate": {"1970-01-01": [trip]}
            }
        )

    def test_api_return_duplicate_trips(self):
        """Test when vehicle API responds with duplicate trips."""
        current_state = {}
        trip = self._generate_trip_object(1)
        trip_2 = self._generate_trip_object(1, duration=2000)
        api_response = self._generate_api_response(trip, trip_2)

        updated_state = self.state_manager.update_state(current_state, api_response)

        self.assertDictEqual(
            updated_state,
            {
                "byTripId": {trip["trip_id"]: trip_2},
                "byStartDate": {"1970-01-01": [trip_2]}
            }
        )

    def test_current_state_is_none(self):
        """Test when the given current state is None."""
        current_state = None
        api_response = self._generate_api_response()

        updated_state = self.state_manager.update_state(current_state, api_response)

        self.assertDictEqual(updated_state, {"byTripId": {}, "byStartDate": {}})

    def _generate_trip_object(
        self,
        id,
        duration=1000,
        distance=10,
        start_time="1970-01-01T00:00:00+0000",
        end_time="1970-01-01T00:01:00+0000"
    ):
        return {
            "trip_id": id,
            "duration": duration,
            "distance": distance,
            "start_time": start_time,
            "end_time": end_time
        }

    def _generate_api_response(self, *trips):
        return {
            "vehicle_no": 1,
            "trips": list(trips)
        }
