from django.contrib import admin

from survey.models import Answer, Question


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ("author", "value", "comment")
    verbose_name = "Answer"
    verbose_name_plural = "Answers"


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
