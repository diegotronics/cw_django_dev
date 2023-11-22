import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from survey.models import Answer, LikeDislike, Question


class Command(BaseCommand):
    """
    This command creates dummy data for the survey app
    """

    def handle(self, *args, **options):
        # Create 10 users
        for i in range(10):
            try:
                user = User.objects.create_user(
                    username=f"dummy{i}",
                    password="1234",
                )
                user.save()
            except:
                pass
        print("100 Users created")

        # Create 100 questions with random author and diffents dates
        for i in range(100):
            try:
                question = Question(
                    title=f"Question {i}",
                    description=f"Description {i}",
                    author=random.choice(User.objects.all()),
                )
                question.save()
            except:
                pass
        print("100 Questions created")

        # Create 1000 answers
        for i in range(1000):
            try:
                answer, created = Answer.objects.update_or_create(
                    author=random.choice(User.objects.all()),
                    question=random.choice(Question.objects.all()),
                )
                answer.value = random.randint(0, 5)
                answer.save()
            except:
                pass
        print("1000 Answers created")

        # Create 1000 likes
        for i in range(1000):
            try:
                like, created = LikeDislike.objects.update_or_create(
                    question=random.choice(Question.objects.all()),
                    author=random.choice(User.objects.all()),
                )
                like.value = random.choice([-1, 1])
                like.save()
            except:
                pass
        print("1000 LikesDislikes created")

        # make some questions older
        days = 100
        for question in Question.objects.all()[:90]:
            question.created -= timedelta(days=days)
            days -= 1
            question.save()

        print("Done!")
