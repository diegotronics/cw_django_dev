from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from survey.models import Answer, LikeDislike, Question


class QuestionListView(ListView):
    model = Question
    template_name = "survey/question_list.html"

    def get_queryset(self):
        # get all questions
        queryset = super().get_queryset()
        # get ranking for each question
        queryset = sorted(queryset, key=lambda x: x.ranking(), reverse=True)
        return queryset


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ["title", "description"]
    redirect_url = ""

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ["title", "description"]
    template_name = "survey/question_form.html"

    def get_queryset(self):
        # Only the author of the question can edit it
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return self.request.GET.get("next", "/")


def answer_question(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not Authorized"}, status=401)

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


def like_dislike_question(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not Authorized"}, status=401)

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
