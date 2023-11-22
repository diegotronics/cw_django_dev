from django.contrib.auth import get_user_model
from django.test import TestCase

from survey.models import Answer, LikeDislike, Question


class QuestionModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.question = Question.objects.create(
            title="Test question",
            author=self.user,
            description="Test description",
        )

    def test_user_value_with_no_answer(self):
        self.assertEqual(self.question.user_value(self.user), 0)

    def test_user_value_with_answer(self):
        Answer.objects.create(question=self.question, author=self.user, value=4)
        self.assertEqual(self.question.user_value(self.user), 4)

    def test_user_likes(self):
        LikeDislike.objects.create(question=self.question, author=self.user, value=1)
        self.assertTrue(self.question.user_likes(self.user))

    def test_user_dislikes(self):
        LikeDislike.objects.create(question=self.question, author=self.user, value=-1)
        self.assertTrue(self.question.user_dislikes(self.user))

    def test_ranking(self):
        Answer.objects.create(
            question=self.question, author=self.user, value=4
        )  # 10 pts
        LikeDislike.objects.create(
            question=self.question, author=self.user, value=1
        )  # 5 pts
        # 10 pts extra por ser la pregunta del día
        self.assertEqual(self.question.ranking(), 25)

    def test_get_absolute_url(self):
        self.assertEqual(self.question.get_absolute_url(), "/question/edit/1")
