import sys
from django.db import models
from django.utils.timezone import now
from django.conf import settings


# <HINT> Create Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


# <HINT> Create Learner model
class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username},{self.occupation}"


# <HINT> Create Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=150, default='online course')
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True, default=now)
    instructors = models.ManyToManyField(Instructor, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment', blank=True)
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"


# <HINT> Create Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    content = models.TextField(blank=True, default="")

    def __str__(self):
        return self.title


# <HINT> Create Enrollment model
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

    def __str__(self):
        return f"Enrollment {self.id}: {self.user.username} in {self.course.name}"


# <HINT> Create Question model
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='questions')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name='questions')
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

    @property
    def choice_set(self):
        """Provide compatibility for choice_set access."""
        return self.choices

    def is_get_score(self, selected_ids):
        """
        Check if selected choices for this question are all the correct choices,
        and no incorrect choice is selected.
        """
        all_correct_count = self.choices.filter(is_correct=True).count()
        selected_correct_count = self.choices.filter(is_correct=True, id__in=selected_ids).count()
        selected_incorrect_count = self.choices.filter(is_correct=False, id__in=selected_ids).count()

        if all_correct_count > 0 and all_correct_count == selected_correct_count and selected_incorrect_count == 0:
            return True
        return False


# <HINT> Create Choice model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


# <HINT> Create Submission model
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    choices = models.ManyToManyField(Choice, related_name='submissions')
    score = models.IntegerField(default=0)
    time_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        course_name = self.course.name if self.course else "Course"
        return f"Submission {self.id} for {course_name} (Score: {self.score})"

    @property
    def choice_set(self):
        """Provide compatibility for submission.choice_set access."""
        return self.choices
