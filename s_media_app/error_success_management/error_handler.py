from rest_framework.response import Response

error_message = {
    400: {
        'message': "BAD_REQUEST",
    },
    401: {
        'message': "UNAUTHORISED",
    },
    404: {
        'message': "NOT FOUND",
    },
    208: {
        'message': "ALREADY REPORTED",
    },
}


def error_response(detail, error_code):
    response = {
        "code": error_code,
        "message": error_message[error_code]['message'],
        "detail": detail,
        "status": False
    }
    return Response(response)
