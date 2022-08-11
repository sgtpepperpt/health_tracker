from django.urls import path

from . import views
from .views import SingleReadingDelete, IndividualFormView, MultipleReadingsAdd, SingleReadingUpdate

app_name = 'htracker'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('reading/', MultipleReadingsAdd.as_view(), name='multi-reading-add'),
    path('reading/<str:field>/<int:pk>/', SingleReadingUpdate.as_view(), name='single-reading-update'),
    path('reading/<str:field>/<int:pk>/delete/', SingleReadingDelete.as_view(), name='single-reading-delete'),

    path('individual/', IndividualFormView.as_view(), name='individual-edit'),
]
