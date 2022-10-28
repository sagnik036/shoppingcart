from django.views import View


class FormatResponses(View):
    @staticmethod
    def error_response(validate_data_errors):
        response = [{error: validate_data_errors[error][0]} for error in validate_data_errors]
        return response
    