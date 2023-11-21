from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from survey.models import Answer, Question


class QuestionListView(ListView):
    model = Question


class QuestionCreateView(CreateView):
    model = Question
    fields = ["title", "description"]
    redirect_url = ""

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ["title", "description"]
    template_name = "survey/question_form.html"


@login_required
def answer_question(request):
    # avoid non POST requests
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    # Get the question
    try:
        question_pk = request.POST.get("question_pk")
        print(request.POST)
        question = Question.objects.get(pk=question_pk)
    except Question.DoesNotExist:
        # if question does not exists, return an error
        return JsonResponse({"ok": False}, status=400)

    # create or update to garantize only one answer per user
    obj, created = Answer.objects.update_or_create(
        question=question, author=request.user
    )
    obj.value = request.POST.get("value")
    obj.save()
    return JsonResponse({"ok": True})


def like_dislike_question(request):
    question_pk = request.POST.get("question_pk")
    if not request.POST.get("question_pk"):
        return JsonResponse({"ok": False})
    question = Question.objects.filter(pk=question_pk)[0]
    # TODO: Dar Like
    return JsonResponse({"ok": True})
