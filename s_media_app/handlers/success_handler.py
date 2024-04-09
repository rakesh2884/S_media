from rest_framework.response import Response
def success_response(message,code):
    response = {
        "message": message,
        "code": code,
        "detail": message,
        "status": True
    }
    return Response(response)