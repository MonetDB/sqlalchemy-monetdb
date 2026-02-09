import pytest
from sqlalchemy.testing.suite import *

# Errors
@pytest.mark.skip(reason="The tests of this class use self-reference "
                  "foreign keys which are NOT supported by MonetDB")
class CTETest(CTETest):
    pass

class JSONTest:
    @pytest.mark.skip(reason="MonetDB normalizes json input "
                        "by removing whitespace. "
                        "This is unexpected in this test.")
    def test_round_trip_custom_json(self):
        pass

class DateTimeCoercedToDateTimeTest:
    @pytest.mark.skip(reason="Temporal types don't work yet")
    def test_literal(self):
        pass

class DateTimeHistoricTest:
    @pytest.mark.skip(reason="Temporal types don't work yet")
    def test_literal(self):
        pass

class DateTimeMicrosecondsTest:
    @pytest.mark.skip(reason="Temporal types don't work yet")
    def test_literal(self):
        pass

class DateTimeTZTest:
    @pytest.mark.skip(reason="Temporal types don't work yet")
    def test_literal(self):
        pass

class DateTimeTest:
    @pytest.mark.skip(reason="Temporal types don't work yet")
    def test_literal(self):
        pass

class TimeMicrosecondsTest:
    @pytest.mark.skip(reason="Temporal types don't work yet")
    def test_literal(self):
        pass

class TimeTZTest:
    @pytest.mark.skip(reason="Temporal types don't work yet")
    def test_literal(self):
        pass

class TimeTest:
    @pytest.mark.skip(reason="Temporal types don't work yet")
    def test_literal(self):
        pass

class TimestampMicrosecondsTest:
    @pytest.mark.skip(reason="Temporal types don't work yet")
    def test_literal(self):
        pass
