from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import DataSerializer


@api_view(http_method_names=['POST'])
@permission_classes((AllowAny, ),)
def data_view(request):
    serializer = DataSerializer(data=request.data)
    if serializer.is_valid():
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.validated_data)
    else:
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
