# Programming Task
# Ironically, I've written the solution in Python :joy-tears:

import datetime

class StateManager:
    api_date_fmt = "%Y-%m-%dT%H:%M:%S%z"
    date_key_fmt = "%Y-%m-%d"

    def update_state(self, state, api_response):
        state = state if state else {}
        current_trips = self._extract_trips_from_state(state)

        incoming_trips = {
            trip["trip_id"]: {**trip}
            for trip in api_response["trips"]
        }
        updated_trips = {**current_trips, **incoming_trips}
        updated_trips_by_start_date = {}

        for trip in updated_trips.values():
            trip_start_date = self._simplify_date_string(trip["start_time"])
            updated_trips_by_start_date.setdefault(trip_start_date, []).append(trip)

        return {
            "byTripId": updated_trips,
            "byStartDate": updated_trips_by_start_date,
        }

    def _extract_trips_from_state(self, state):
        return state["byTripId"] if "byTripId" in state else {}

    def _simplify_date_string(self, date_string):
        return datetime.datetime.strptime(date_string, self.api_date_fmt).strftime(self.date_key_fmt)
