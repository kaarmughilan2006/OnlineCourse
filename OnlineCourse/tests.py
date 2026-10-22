from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from OnlineCourse.models import Course, Lesson, Question, Choice, Submission
from OnlineCourse import views

User = get_user_model()


class OnlineCourseModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            description='Test course description'
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            order=1,
            content='Lesson content'
        )
        self.question = Question.objects.create(
            course=self.course,
            lesson=self.lesson,
            question_text='What is 2+2?',
            grade=2
        )
        self.choice_correct = Choice.objects.create(
            question=self.question,
            choice_text='4',
            is_correct=True
        )
        self.choice_wrong = Choice.objects.create(
            question=self.question,
            choice_text='5',
            is_correct=False
        )

    def test_question_is_get_score_correct(self):
        """Selecting all correct answers and no wrong answers should score."""
        self.assertTrue(self.question.is_get_score([self.choice_correct.id]))

    def test_question_is_get_score_incorrect(self):
        """Selecting a wrong answer should not score."""
        self.assertFalse(self.question.is_get_score([self.choice_wrong.id]))

    def test_question_is_get_score_mixed(self):
        """Selecting both correct and wrong answers should not score."""
        self.assertFalse(self.question.is_get_score([self.choice_correct.id, self.choice_wrong.id]))

    def test_question_is_get_score_empty(self):
        """Selecting no answers should not score."""
        self.assertFalse(self.question.is_get_score([]))

    def test_submission_creation_and_choices(self):
        """Submission should save score and associate selected choices."""
        sub = Submission.objects.create(course=self.course, score=2)
        sub.choices.add(self.choice_correct)
        self.assertEqual(sub.score, 2)
        self.assertIn(self.choice_correct, sub.choices.all())


class OnlineCourseViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            name='Django Basics',
            description='Learn Django'
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Intro Lesson',
            order=1,
            content='Introduction to Django framework.'
        )
        self.question1 = Question.objects.create(
            course=self.course,
            lesson=self.lesson,
            question_text='Question 1',
            grade=1
        )
        self.q1_c1 = Choice.objects.create(
            question=self.question1,
            choice_text='Correct 1',
            is_correct=True
        )
        self.q1_c2 = Choice.objects.create(
            question=self.question1,
            choice_text='Wrong 1',
            is_correct=False
        )

    def test_course_details_view(self):
        """Test course details page renders course_details_bootstrap.html with course & lessons."""
        response = self.client.get(reverse('OnlineCourse:course_details', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'OnlineCourse/course_details_bootstrap.html')
        self.assertContains(response, 'Django Basics')
        self.assertContains(response, 'Intro Lesson')

    def test_mock_exam_view(self):
        """Test mock exam page loads questions."""
        response = self.client.get(reverse('OnlineCourse:mock_exam', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'OnlineCourse/mock_exam.html')
        self.assertContains(response, 'Question 1')
        self.assertContains(response, 'Correct 1')

    def test_successful_exam_submission_and_result(self):
        """Submitting correct answers should calculate score and display Congratulations."""
        post_data = {
            f'choice_{self.question1.id}': [self.q1_c1.id]
        }
        submit_url = reverse('OnlineCourse:submit', args=[self.course.id])
        response = self.client.post(submit_url, post_data)
        
        # Verify redirect to result view
        self.assertEqual(response.status_code, 302)
        submission = Submission.objects.latest('id')
        self.assertEqual(submission.score, 1)

        # Follow redirect or directly get result page
        result_url = reverse('OnlineCourse:show_exam_result', args=[self.course.id, submission.id])
        result_response = self.client.get(result_url)
        self.assertEqual(result_response.status_code, 200)
        self.assertTemplateUsed(result_response, 'OnlineCourse/exam_result.html')
        # Rubric requirement: Exact word Congratulations
        self.assertContains(result_response, 'Congratulations')
        self.assertContains(result_response, '1 / 1')

    def test_unsuccessful_exam_submission_and_result(self):
        """Submitting wrong answers should not show Congratulations."""
        post_data = {
            f'choice_{self.question1.id}': [self.q1_c2.id]
        }
        submit_url = reverse('OnlineCourse:submit', args=[self.course.id])
        response = self.client.post(submit_url, post_data)
        self.assertEqual(response.status_code, 302)
        
        submission = Submission.objects.latest('id')
        self.assertEqual(submission.score, 0)

        result_url = reverse('OnlineCourse:show_exam_result', args=[self.course.id, submission.id])
        result_response = self.client.get(result_url)
        self.assertEqual(result_response.status_code, 200)
        self.assertNotContains(result_response, 'Congratulations')
        self.assertContains(result_response, '0 / 1')

    def test_missing_submission_handled_gracefully(self):
        """Accessing a non-existent submission id should render gracefully without 500."""
        result_url = reverse('OnlineCourse:show_exam_result', args=[self.course.id, 9999])
        response = self.client.get(result_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Submission record not found.')


class OnlineCourseURLTests(TestCase):
    def test_submit_url_resolves(self):
        """Verify URL pattern for submit resolves to views.submit."""
        resolver = resolve('/course/1/submit/')
        self.assertEqual(resolver.func, views.submit)

    def test_show_exam_result_url_resolves(self):
        """Verify URL pattern for show_exam_result resolves to views.show_exam_result."""
        resolver = resolve('/course/1/submission/1/result/')
        self.assertEqual(resolver.func, views.show_exam_result)
