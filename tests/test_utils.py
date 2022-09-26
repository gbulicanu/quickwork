import pytest

from datetime import timedelta

from app.utils import strfdelta


@pytest.mark.parametrize(["tdelta", "fmt", "inputtype", "expected"], [
  (timedelta(seconds=3660), "{H}h {M}m", "timedelta", "1h 1m"),
  (timedelta(seconds=60), "{H}h {M}m", "timedelta", "1m"),
  (2*3660, "{H}h {M}m", "s", "2h 2m"),
  (2*3660, "{H}h {M}m", "seconds", "2h 2m"),
  (3, "{M}m {S}s", "m", "3m 0s"),
  (3, "{M}m {S}s", "minutes", "3m 0s"),
  (4, "{S}s", "h", "14400s"),
  (4, "{S}s", "hours", "14400s"),
  (2, "{H}h {M}m", "d", "48h"),
  (2, "{H}h {M}m", "days", "48h"),
  (2, "{H}h", "w", "336h"),
  (2, "{H}h", "weeks", "336h"),
])
def test_strfdelta(tdelta, fmt, inputtype, expected):
  assert strfdelta(tdelta, fmt=fmt, inputtype=inputtype) == expected
