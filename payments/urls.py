from django.urls import path

from . import views
from .views import CreateCheckoutSession#, WebHook

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSession.as_view()),
    # path('webhook-test/', WebHook.as_view()),
]
