from django.urls import path
from .views import *

urlpatterns = [
    path('', get_home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('verify/<int:user_pk>/<str:token>/', VerifyEmailView.as_view(), name='verify'),
    path('catalog/', get_catalog, name='catalog'),
    path('product/<int:product_id>/', get_product, name='product'),
    path('contact/', get_contact, name='contact'),
    path('user_ticket/<int:user_id>/', get_user_tickets, name='user_ticket'),
    path('create_product/', CreateProductView.as_view(), name='create_product')
]