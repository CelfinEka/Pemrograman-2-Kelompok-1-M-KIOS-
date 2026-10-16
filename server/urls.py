from django.urls import path
from kiosk_v28.views import home, state_api, health
urlpatterns=[path('',home,name='home'),path('app/',home,name='app'),path('api/state/',state_api,name='state_api'),path('health/',health,name='health')]
