from v2.iris_shim.models import Report, Reporter


class TestReport:
    def __init__(self):
        self.report = Report(None, None, None, None)

    def test_validate_valid(self):
        assert False

    def test_validate_invalid(self):
        assert False

    def test_parse(self):
        assert False

    def test_parse_fail(self):
        assert False


class TestReporter:
    def __init__(self):
        self.reporter = Reporter(None)

    def test_add_incident(self):
        assert False

    def test_successfully_parsed(self):
        assert False
