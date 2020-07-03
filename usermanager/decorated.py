from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):

        req_data = args[0].request.data

        for key in req_data:
            if key == "avatar":
                continue
            elif not req_data[key]:

                message = "{key} unset value".format(key=key)

                return Response(
                    data={
                        "message": message
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return fn(*args, **kwargs)
    return decorated



# def validate_email(fn):
#     def decorated(*args, **kwargs):
#
#         req_data = args[0].request.data.get("email")
#
#
#
#         return fn(*args, **kwargs)
#     return decorated
