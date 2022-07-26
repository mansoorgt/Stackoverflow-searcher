
from .import views 

from django.urls import path

urlpatterns = [
    
    path('getquestions',views.getQuestions,name='getquestions'),
    path('',views.renderIndex,name='searchpage')
]
