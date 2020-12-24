class Lands(object):
    get_lands = "/api/v1.1/land-holders/lands"
    create_land = "/api/v1.1/land-holders/lands"
    delete_land = "/api/v1.1/land-holders/lands/delete"


class Analyzes(object):
    analyze = "/api/v1.1/analyzes/by-field/"


class AgroJob(object):
    agro_job_endpoint = "/api/v1.1/catalog/agrojob/list"


class CultureList(object):
    culture_list_endpoint = "/api/v1.1/catalog/culture/list"


class FieldReports(object):
    field_report_endpoint = "/api/v1.1/field-reports"


class AddFileToReport(object):
    add_file_endpoint = "/api/v1.1/field-reports/media?json="

class Counterparties (object):
    add_counterpaties_endpoint = "/api/v1.1/counterparties"
    del_counterpaties_endpoint = "/api/v1.1/counterparties/delete"