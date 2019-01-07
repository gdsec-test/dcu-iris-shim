class MockMailer(object):
    def report_successfully_parsed(self, reporter_email):
        pass

    def report_failed_to_parse(self, reporter_email):
        pass


class MockIrisSoap(object):
    note_successfully_parsed = None
    note_failed_to_parse = None
    note_csam_failed_to_parse = None
    note_csam_failed_to_submit_to_api = None

    def get_customer_notes(self, report_id):
        pass

    def get_report_info_by_id(self, report_id):
        pass

    def notate_report_and_close(self, report_id, note):
        pass

    def notate_report(self, report_id, note):
        pass


class MockAbuseAPI(object):
    def create_ticket(self, type, source, report_id, reporter_email, modify_date):
        pass
