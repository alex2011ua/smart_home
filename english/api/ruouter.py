from django.urls import path

from english.api import views

urlpatterns = [
    path("words/", views.WordListCreateView.as_view(), name="wordRUD"),
    path("word/<int:pk>/", views.WordRUD.as_view(), name="wordRUD"),
]
