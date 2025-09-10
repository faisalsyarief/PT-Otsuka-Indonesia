from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        wrapped = {
            "rc": 500,
            "message": response.data.get('detail', 'Terjadi kesalahan'),
            "data": None
        }
        return Response(wrapped, status=response.status_code)

    return response
