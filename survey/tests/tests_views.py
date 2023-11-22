from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from survey.models import Answer, LikeDislike, Question


class TestQuestionListView(TestCase):
    """
    Test QuestionListView
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse("survey:question-list")
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.question1 = Question.objects.create(
            title="Test question 1",
            author=self.user,
            description="Test description 1",
        )
        self.question2 = Question.objects.create(
            title="Test question 2",
            author=self.user,
            description="Test description 2",
        )
        self.question3 = Question.objects.create(
            created="2020-01-01",
            title="Test question 3",
            author=self.user,
            description="Test description 3",
        )
        self.answer1 = Answer.objects.create(
            question=self.question1, author=self.user, value=4
        )
        self.answer2 = Answer.objects.create(
            question=self.question2, author=self.user, value=3
        )
        self.like1 = LikeDislike.objects.create(
            question=self.question1, author=self.user, value=1
        )

    def test_view_url_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "survey/question_list.html")

    def test_view_orders_questions_correctly(self):
        response = self.client.get(self.url)
        questions = list(response.context["object_list"])
        self.assertEqual(questions, [self.question1, self.question2, self.question3])


class AnswerQuestionViewTestCase(TestCase):
    """
    Test answer_question
    """

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.question = Question.objects.create(
            title="Question 1", author=self.user, description="Description 1"
        )
        self.url = reverse("survey:question-answer")

    def test_answer_question_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            self.url, {"question_pk": self.question.pk, "value": "3"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Answer.objects.filter(question=self.question, author=self.user).exists()
        )

    def test_answer_question_unauthenticated_user(self):
        response = self.client.post(
            self.url, {"question_pk": self.question.pk, "value": "1"}
        )

        self.assertEqual(response.status_code, 401)

    def test_answer_question_invalid_question(self):
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(self.url, {"question_pk": 9999, "value": "2"})

        self.assertEqual(response.status_code, 400)

    def test_answer_question_invalid_value(self):
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            self.url, {"question_pk": self.question.pk, "value": "9999"}
        )

        self.assertEqual(response.status_code, 400)


class LikeDislikeQuestionViewTestCase(TestCase):
    """
    Test like_dislike_question
    """

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.question = Question.objects.create(
            title="Question 1", author=self.user, description="Description 1"
        )
        self.url = reverse("survey:question-like")

    def test_like_question_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            self.url, {"question_pk": self.question.pk, "value": "1"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            LikeDislike.objects.filter(
                question=self.question, author=self.user
            ).exists()
        )

    def test_dislike_question_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            self.url, {"question_pk": self.question.pk, "value": "-1"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            LikeDislike.objects.filter(
                question=self.question, author=self.user
            ).exists()
        )

    def test_like_question_unauthenticated_user(self):
        response = self.client.post(
            self.url, {"question_pk": self.question.pk, "value": "1"}
        )

        self.assertEqual(response.status_code, 401)

    def test_like_question_invalid_question(self):
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(self.url, {"question_pk": 9999, "value": "1"})

        self.assertEqual(response.status_code, 400)

    def test_like_question_invalid_value(self):
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            self.url, {"question_pk": self.question.pk, "value": "9999"}
        )

        self.assertEqual(response.status_code, 400)
