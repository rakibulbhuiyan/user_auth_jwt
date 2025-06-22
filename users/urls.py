from django.urls import path
from .views import SignupAPIView,LoginView,UserView,AlluserView,LogoutView


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
app_name = 'users'

urlpatterns = [
    
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='Login'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    
    path('user/', UserView.as_view(), name='userView'),
    path('alluser/', AlluserView.as_view(), name='userView'),

# JWT

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
