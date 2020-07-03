from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        name = args[0].request.data.get('name')

        # test = args[0].request.data

        # for key in test:
        #     print("in loop")
        #     print(key, " = ", test[key])

        if not name:
            return Response(
                data={
                    "message": "Group must has name!"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated
