from django.urls import path
from .views import OficinaListView

app_name = 'oficina'

urlpatterns = [
    path(
        'lista/',
        OficinaListView.as_view(),
        name='lista'
    ),
]