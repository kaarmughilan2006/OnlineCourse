from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from OnlineCourse.models import Course, Lesson, Instructor, Learner, Question, Choice

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds sample courses, lessons, questions, and choices idempotently.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting seed process...'))

        # 1. Create or get superuser for admin access
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('adminpassword123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created superuser "admin" with password "adminpassword123"'))
        else:
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.set_password('adminpassword123')
            admin_user.save()
            self.stdout.write(self.style.NOTICE('Superuser "admin" already exists (password reset to adminpassword123).'))

        # 2. Create Instructor
        instructor_user, _ = User.objects.get_or_create(
            username='dr_johnson',
            defaults={'first_name': 'Alex', 'last_name': 'Johnson', 'email': 'alex@example.com'}
        )
        instructor, _ = Instructor.objects.get_or_create(
            user=instructor_user,
            defaults={'full_time': True, 'total_learners': 1500}
        )

        # 3. Create Learner
        learner_user, _ = User.objects.get_or_create(
            username='student_sam',
            defaults={'first_name': 'Sam', 'last_name': 'Taylor', 'email': 'sam@example.com'}
        )
        Learner.objects.get_or_create(
            user=learner_user,
            defaults={'occupation': Learner.STUDENT, 'social_link': 'https://github.com/student_sam'}
        )

        # 4. Create Main Course
        course, _ = Course.objects.get_or_create(
            name='Cloud Application Development with Django',
            defaults={
                'description': 'Master backend web development using Python and Django. Learn models, the ORM, admin site customization, interactive templates with Bootstrap, and exam evaluation workflows.',
                'pub_date': now().date(),
                'total_enrollment': 1240,
            }
        )
        course.instructors.add(instructor)

        # 5. Create Lessons
        lessons_data = [
            (1, 'Django Architecture & MVT Pattern', 'Understand Django\'s Model-View-Template architecture, request-response cycle, and core project settings.'),
            (2, 'Models, Migrations & Database ORM', 'Define robust relational models, create migrations, execute migrations, and perform complex queries using Django ORM.'),
            (3, 'Django Admin Customization & Inlines', 'Leverage Django\'s automatic administration panel, configure StackedInline and TabularInline classes, and register custom ModelAdmin options.'),
            (4, 'Views, URL Routing & Dynamic Templates', 'Create function-based views, configure application and project level urls.py, and render dynamic context data with Bootstrap styling.'),
            (5, 'Form Processing & Interactive Assessments', 'Process HTTP POST requests, validate CSRF tokens, evaluate user submissions against database answers, and calculate scores dynamically.'),
        ]

        created_lessons = {}
        for order, title, content in lessons_data:
            lesson, _ = Lesson.objects.get_or_create(
                course=course,
                title=title,
                defaults={'order': order, 'content': content}
            )
            created_lessons[order] = lesson

        # 6. Create Questions and Choices
        questions_data = [
            {
                'text': 'Which design pattern is primarily used by Django to structure web applications?',
                'lesson_order': 1,
                'grade': 1,
                'choices': [
                    ('Model-View-Template (MVT)', True),
                    ('Model-View-Controller (MVC) with strict external routing', False),
                    ('Single-Page Reactive State Architecture', False),
                    ('Three-Tier Monolithic Client-Server Engine', False),
                ]
            },
            {
                'text': 'Which Django model admin class is used to edit related child objects on the parent admin page in a stacked layout?',
                'lesson_order': 3,
                'grade': 1,
                'choices': [
                    ('admin.StackedInline', True),
                    ('admin.TabularView', False),
                    ('admin.HorizontalInline', False),
                    ('admin.InlineController', False),
                ]
            },
            {
                'text': 'In Django templates, which tag is used to iterate over a list of items?',
                'lesson_order': 4,
                'grade': 1,
                'choices': [
                    ('{% for item in items %}', True),
                    ('{{ for item in items }}', False),
                    ('{% loop items as item %}', False),
                    ('{# foreach item in items #}', False),
                ]
            },
            {
                'text': 'Which Django management command executes database migrations against the configured database?',
                'lesson_order': 2,
                'grade': 1,
                'choices': [
                    ('python manage.py migrate', True),
                    ('python manage.py makemigrations', False),
                    ('python manage.py dbsync', False),
                    ('python manage.py commit', False),
                ]
            },
            {
                'text': 'Which HTTP request method is standard for securely submitting mock exam answers in Django?',
                'lesson_order': 5,
                'grade': 1,
                'choices': [
                    ('POST', True),
                    ('GET', False),
                    ('PUT', False),
                    ('HEAD', False),
                ]
            },
        ]

        for q_data in questions_data:
            lesson = created_lessons[q_data['lesson_order']]
            question, _ = Question.objects.get_or_create(
                course=course,
                question_text=q_data['text'],
                defaults={
                    'lesson': lesson,
                    'grade': q_data['grade']
                }
            )
            # Ensure choices exist
            for choice_text, is_correct in q_data['choices']:
                Choice.objects.get_or_create(
                    question=question,
                    choice_text=choice_text,
                    defaults={'is_correct': is_correct}
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with Course, Lessons, Questions, Choices, and Users!'))
