from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Question(models.Model):
    created = models.DateField("Creada", auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        related_name="questions",
        verbose_name="Pregunta",
        on_delete=models.CASCADE,
    )
    title = models.CharField("Título", max_length=200)
    description = models.TextField("Descripción")

    # TODO: Quisieramos tener un ranking de la pregunta, con likes y dislikes dados por los usuarios.
    def user_value(self):
        media = 0
        answers = self.answers.all()
        if answers:
            media = sum([answer.value for answer in answers]) / len(answers)
        # return integer from 0 to 5
        return int(round(media))

    def user_likes(self):
        return self.likes_dislikes.filter(value=1).count()

    def user_dislikes(self):
        return self.likes_dislikes.filter(value=-1).count()

    def get_absolute_url(self):
        return reverse("survey:question-edit", args=[self.pk])


class Answer(models.Model):
    ANSWERS_VALUES = (
        (0, "Sin Responder"),
        (1, "Muy Bajo"),
        (2, "Bajo"),
        (3, "Regular"),
        (4, "Alto"),
        (5, "Muy Alto"),
    )

    question = models.ForeignKey(
        Question,
        related_name="answers",
        verbose_name="Pregunta",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        get_user_model(),
        related_name="answers",
        verbose_name="Autor",
        on_delete=models.CASCADE,
    )
    value = models.PositiveIntegerField("Respuesta", default=0)
    comment = models.TextField("Comentario", default="", blank=True)


class LikeDislike(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        related_name="likes_dislikes",
        verbose_name="LikeDislike",
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        related_name="likes_dislikes",
        verbose_name="LikeDislike",
        on_delete=models.CASCADE,
    )
    LIKE_DISLIKE_VALUES = ((1, "Like"), (-1, "Dislike"))
    value = models.SmallIntegerField(
        "Like/Dislike", choices=LIKE_DISLIKE_VALUES, default=1
    )

    class Meta:
        # an user can only give one like or dislike to a question
        unique_together = ("author", "question")
