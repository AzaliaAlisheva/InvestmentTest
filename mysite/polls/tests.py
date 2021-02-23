import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_choices(self):
        question_with_choices = create_question(question_text="With choices.", days=0)
        question_with_choices.choice_set.create(choice_text='A choice.', votes=0)
        self.assertIs(question_with_choices.was_published_recently(), True)

    def test_was_published_recently_without_choices(self):
        question_without_choices = create_question(question_text="Without choices.", days=0)
        self.assertIs(question_without_choices.was_published_recently(), False)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_question_without_choices(self):
        create_question(question_text="Without choices.", days=0)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_questions_with_and_without_choices(self):
        question_with_choices = create_question(question_text="With choices.", days=0)
        question_with_choices.choice_set.create(choice_text='A choice.', votes=0)
        create_question(question_text="Without choices.", days=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: With choices.>']
        )

    def test_two_questions_with_choices(self):
        question_with_choices = create_question(question_text="With choices 1.", days=0)
        question_with_choices.choice_set.create(choice_text='A choice.', votes=0)
        question_with_choices = create_question(question_text="With choices 2.", days=0)
        question_with_choices.choice_set.create(choice_text='A choice.', votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: With choices 2.>', '<Question: With choices 1.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_question_with_choices(self):
        question_with_choices = create_question(question_text="With choices.", days=0)
        question_with_choices.choice_set.create(choice_text='A choice.', votes=0)
        url = reverse('polls:detail', args=(question_with_choices.id,))
        response = self.client.get(url)
        self.assertContains(response, question_with_choices.question_text)

    def test_question_without_choices(self):
        question_without_choices = create_question(question_text="Without choices.", days=0)
        url = reverse('polls:detail', args=(question_without_choices.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_question_with_choices(self):
        question_with_choices = create_question(question_text="With choices.", days=0)
        question_with_choices.choice_set.create(choice_text='A choice.', votes=0)
        url = reverse('polls:results', args=(question_with_choices.id,))
        response = self.client.get(url)
        self.assertContains(response, question_with_choices.question_text)

    def test_question_without_choices(self):
        question_without_choices = create_question(question_text="Without choices.", days=0)
        url = reverse('polls:results', args=(question_without_choices.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)