from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from asgiref.sync import sync_to_async

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name="latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-votes_num")[:15]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {"question": question, "error_message": "You didn't select a choice."})
    else:
        question.votes_num += 1
        selected_choice.votes += 1
        selected_choice.save()
        question.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
def new(request, choice_count):
    return render(request, "polls/new.html", {'choice_count_range': range(choice_count), 'choice_count':choice_count, 'choice_count_add':choice_count+1, 'choice_count_min':choice_count-1})

@sync_to_async
def save_question(question_text, choice_arr):
    q = Question(question_text=question_text, pub_date=timezone.now())
    q.save()
    for choice_text in choice_arr:
        q.choice_set.create(choice_text=choice_text, votes=0)

    return q

async def addQuestion(request):
    if request.method == "POST":
        question_text = request.POST["question_text"]
        choice_count = int(request.POST["choice_count"])
        choice_arr = []
        for i in range(1, choice_count+1):
            choice_arr.append(request.POST[f"choice{i}"])

        q = await save_question(question_text, choice_arr)
        return HttpResponseRedirect(reverse("polls:index"))

@sync_to_async
def delete_question(id):
    q = Question.objects.get(pk=id)
    q.delete()


async def deleteQuestion(request):
    question_id = request.POST["id"]
    await delete_question(question_id)
    return HttpResponseRedirect(reverse("polls:index"))

