from rest_framework import status
from rest_framework.response import Response


class StandardizedDestroyMixin:
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        status_code = status.HTTP_200_OK 
        message = "Success" if 200 <= status_code < 300 else "Error"

        return Response({
            "rc": status_code,
            "message": message,
            "data": None
        }, status=status_code)
        