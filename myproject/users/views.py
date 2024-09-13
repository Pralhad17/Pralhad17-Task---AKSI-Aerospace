from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from .permissions import IsSuperadmin, IsAdmin, IsSuperuser, IsUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'login': reverse('login', request=request, format=format),
        'register': reverse('register', request=request, format=format),
        'superadmin_dashboard': reverse('superadmin_dashboard', request=request, format=format),
        'admin_dashboard': reverse('admin_dashboard', request=request, format=format),
        'token_refresh': reverse('token_refresh', request=request, format=format),
    })

User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can register new users
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        creator = self.request.user

        # Superadmin can create users with any role
        if creator.role == 'Superadmin':
            role = self.request.data.get('role', 'User')  # Default to User role if not provided
            if role not in ['Admin', 'Superuser', 'Superadmin', 'User']:
                raise PermissionDenied("Invalid role specified.")
            serializer.save(created_by=creator, role=role)

        # Admin can only create Superusers or Users
        elif creator.role == 'Admin':
            role = self.request.data.get('role', 'User')  # Default to User role if not provided
            if role not in ['Superuser', 'User']:
                raise PermissionDenied("Admins can only create Superusers and Users.")
            serializer.save(created_by=creator, role=role)

        # Prevent Superusers and Users from creating other users
        else:
            raise PermissionDenied("You do not have permission to create users.")
        
class LoginView(generics.GenericAPIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# class SuperadminDashboardView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated, IsSuperadmin]
#     queryset = User.objects.all()  # Superadmin can see all users
#     serializer_class = UserSerializer

# class AdminDashboardView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated, IsAdmin]
    
#     def get_queryset(self):
#         # Admin can only see users they created
#         return User.objects.filter(created_by=self.request.user)
#     serializer_class = UserSerializer



class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Superadmin Dashboard View (already implemented)
class SuperadminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Superadmin can see all Admins, Superusers, and Users
        admin_users = CustomUser.objects.filter(role='Admin')
        superusers = CustomUser.objects.filter(role='Superuser')
        regular_users = CustomUser.objects.filter(role='User')

        return Response({
            'admins': [admin.username for admin in admin_users],
            'superusers': [superuser.username for superuser in superusers],
            'users': [user.username for user in regular_users]
        })


# Admin Dashboard View (already implemented)
class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Ensure the logged-in user is an Admin
        if request.user.role != 'Admin':
            return Response({'detail': 'You do not have permission to access this page.'}, status=status.HTTP_403_FORBIDDEN)

        # Admins can only view Superusers and Users they created
        created_superusers = CustomUser.objects.filter(role='Superuser', created_by=request.user)
        created_users = CustomUser.objects.filter(role='User', created_by=request.user)

        return Response({
            'superusers': [superuser.username for superuser in created_superusers],
            'users': [user.username for user in created_users]
        })


# Superuser Dashboard View
class SuperuserDashboardView(APIView):
    permission_classes = [IsSuperuser]

    def get(self, request, *args, **kwargs):
        # Superusers can manage departments but cannot view or manage other users
        return Response({
            'message': 'Welcome, Superuser. You can manage certain company departments.'
        })


# User Dashboard View
class UserDashboardView(APIView):
    permission_classes = [IsUser]

    def get(self, request, *args, **kwargs):
        # Users can access the platform but cannot see other users or departments
        return Response({
            'message': 'Welcome, User. You have basic access to the platform.'
        })
