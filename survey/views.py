from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from survey.models import Answer, LikeDislike, Question


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
    # Avoid non POST requests
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


@login_required
def like_dislike_question(request):
    # Avoid non POST requests
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

    # verify value is valid
    value = int(request.POST.get("value"))
    if value not in [-1, 1]:
        return JsonResponse({"ok": False}, status=400)

    # create or update to garantize only one answer per user
    obj, created = LikeDislike.objects.update_or_create(
        question=question, author=request.user
    )
    obj.value = value
    obj.save()

    return JsonResponse({"ok": True})
