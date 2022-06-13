from django.urls import path
from . import views

app_name='electronickxz'
urlpatterns=[
    path('', views.IndexClientView.as_view(), name="index_view"),
    path('login', views.LoginView.as_view(), name="login_view"),
    path('register', views.RegistrationView.as_view(), name="register_view"),
    path('editor/products', views.EditorProductsView.as_view(), name="editorProduct_view"),
    path('editor/products/register', views.EditorProductsRegistrationView.as_view(), name="productRegister_view"),
    path('editor/users', views.EditorUsersView.as_view(), name="editorUser_view"),
    path('checkout', views.CheckoutView.as_view(), name="checkout_view"),
    path('payment', views.PaymentView.as_view(), name="payment_view"),
]