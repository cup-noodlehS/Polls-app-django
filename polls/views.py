from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from asgiref.sync import sync_to_async

from .models import Question, Choice, Set

class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name="set_list"

    def get_queryset(self):
        return Set.objects.filter(pub_date__lte=timezone.now()).order_by("pub_date")

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
    
def new(request, choice_count, set_id):
    set_name = Set.objects.get(pk=set_id).set_name
    return render(request, "polls/new.html", {'choice_count_range': range(choice_count), 'choice_count':choice_count, 'choice_count_add':choice_count+1, 'choice_count_min':choice_count-1, 'set_id': set_id, 'set_name': set_name})

@sync_to_async
def save_question(question_text, choice_arr, set_id):
    s = Set.objects.get(pk=set_id)
    q = Question(question_text=question_text, pub_date=timezone.now(), set=s)
    q.save()
    s.question_set.add(q) 
    
    for choice_text in choice_arr:
        q.choice_set.create(choice_text=choice_text, votes=0)
    
    return q

async def addQuestion(request):
    if request.method == "POST":
        question_text = request.POST["question_text"]
        choice_count = int(request.POST["choice_count"])
        set_id = int(request.POST["set_id"])
        print("set id is: " + str(set_id))
        choice_arr = []
        for i in range(1, choice_count+1):
            choice_arr.append(request.POST[f"choice{i}"])

        q = await save_question(question_text, choice_arr, set_id)
        return HttpResponseRedirect(reverse("polls:index"))

@sync_to_async
def delete_question(id):
    q = Question.objects.get(pk=id)
    q.delete()


async def deleteQuestion(request):
    question_id = request.POST["id"]
    await delete_question(question_id)
    return HttpResponseRedirect(reverse("polls:index"))

@sync_to_async
def delete_set(set_id):
    s = Set.objects.get(pk=set_id)
    s.delete()

async def deleteSet(request, set_id):
    await delete_set(set_id)
    return HttpResponseRedirect(reverse("polls:index"))

@sync_to_async
def save_set(set_name):
    s = Set(set_name=set_name, pub_date=timezone.now())
    s.save()
    return s

async def addSet(request):
    set_name = request.POST["setname"]
    s = await save_set(set_name)
    return HttpResponseRedirect(reverse("polls:index"))
    # print("you are at addset")

