from django.test import TestCase
import datetime

from django.utils import timezone

from .models import Question
from django.urls import reverse

# Create your tests here.
def create_question(question_text, days):
    """
    createa  question with question_text, and published the give num of days offest to now 
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        if no questions, then display proper message 
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")

        self.assertQuerySetEqual(response.context["latest_question_list"], [])


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for future questions 
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is older than 1 day 
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True from publication within the day 
        """
        time = timezone.now() - datetime.timedelta(hours=20, minutes=40, seconds=20)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)