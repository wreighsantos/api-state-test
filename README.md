### Requirements
Python 3.5+

### Testing
`cd api-state-test && python3 -m unittest tests/state_manager_test.py`

- [x] Tests Pass
```
python3 -m unittest tests/state_manager_test.py
........
----------------------------------------------------------------------
Ran 8 tests in 0.002s

OK
```

### Quick Explanation
The _byTripId_ lookup is the source of truth for all trips; the _byStartDate_ lookup is then derived from it.
