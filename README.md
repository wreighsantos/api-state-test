### Requirements
Python 3.5+

### Testing
`cd api-state-test && python3 -m unittest tests/state_manager_test.py`

### Quick Explanation
The _byTripId_ lookup is the source of truth for all trips; the _byStartDate_ lookup is then derived from it.
