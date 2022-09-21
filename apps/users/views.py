from django.db.models.query_utils import Q
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import ExtUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  
from .models import ExtUser


class ExtUserView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk=None, format=None):  
        criterion1=Q(is_active__exact=True)
        criterion2=Q(pk__exact=pk)

        try:
          if pk is not None:
            user = ExtUser.objects.get(id=pk)
            if user:
              serializer = ExtUserSerializer(user, many=False)
              return Response({'result': serializer.data}, status=status.HTTP_200_OK)
            else:
              return Response({'result': "User does not exists."}, status=status.HTTP_204_NO_CONTENT)
            
          users = ExtUser.objects.filter(criterion1 & criterion2)
          serializer = ExtUserSerializer(users, many=True)      
          return Response({'result': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'result': 'Bad request occurred: {}'.format(e), 'status_code':400}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
      
        user = ExtUser.objects.get(id=pk)        
        serializer = ExtUserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': serializer.data}, status=status.HTTP_200_OK)
        else:
            emessage = serializer.errors
            return Response({'result': emessage}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            user = ExtUser.objects.get(id=pk)
            if user:
                user.is_active = False
                user.save()
                return Response({'result':'Success!','status':200},status=status.HTTP_200_OK)
            else:
                return Response({'result':'User not found!','status':204},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'result': 'Bad request occurred: {}'.format(e), 'status_code':400}, status=status.HTTP_400_BAD_REQUEST)



# Register API
class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({
      "user": ExtUserSerializer(user, context=self.get_serializer_context()).data,
      "token": user.tokens()
    })

# Login API
class LoginAPI(generics.GenericAPIView):
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    _, token = user.tokens()
    return Response({
      "user": ExtUserSerializer(user, context=self.get_serializer_context()).data,
      "token": user.tokens()
    })

# Get User API
class UserAPI(generics.RetrieveAPIView):
  permission_classes = [
    permissions.IsAuthenticated,
  ]
  serializer_class = ExtUserSerializer

  def get_object(self):
    return self.request.user

