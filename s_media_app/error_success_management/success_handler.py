from rest_framework.response import Response


def success_response(detail, code):
    response = {
        "message": "success",
        "code": code,
        "detail": detail,
        "status": True
    }
    return Response(response)
