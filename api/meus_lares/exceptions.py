from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        if 'place' in exc.detail:
            for error in exc.detail['place']:
                if error.code == 'does_not_exist':
                    exc.detail['place'] = ['O local especificado não foi encontrado.']
                    break

    return response