from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("new/<int:choice_count>", views.new, name="new"),
    path("delete-question/", views.deleteQuestion, name="deletequestion"),
    path("add/", views.addQuestion, name="addquestion"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]