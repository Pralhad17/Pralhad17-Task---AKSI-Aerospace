from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import SuperadminDashboardView, AdminDashboardView, RegisterUserView, LoginView, SuperuserDashboardView, UserDashboardView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('dashboard/superadmin/', SuperadminDashboardView.as_view(), name='superadmin_dashboard'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/superuser/', SuperuserDashboardView.as_view(), name='superuser_dashboard'),
    path('dashboard/user/', UserDashboardView.as_view(), name='user_dashboard'),

    # Jwt token endpoints
    path('token/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
