# OnlineCourse - Django Application Development with SQL and Databases

A full-stack Django online learning and interactive exam assessment platform built from scratch, designed to meet the exact requirements of the Coursera / IBM Django Application Development assignment.

---

## 📋 Features

- **Core Models (`models.py`)**:
  - `Course` and `Lesson`: Course catalog and sequential syllabus modules.
  - `Instructor` and `Learner`: Profiles linked to Django's authentication system.
  - `Question`: Exam questions with point weights (`grade`) and answer verification (`is_get_score`).
  - `Choice`: Answer choices with `is_correct` boolean flags.
  - `Submission`: Records student submissions, score calculations, and selected choices.
- **Admin Portal (`admin.py`)**:
  - Seven imported model classes.
  - Inlines: `QuestionInline`, `ChoiceInline`, and `LessonInline` for streamlined editing.
  - Model admins: `QuestionAdmin` and `LessonAdmin` configured with search and display filters.
- **Responsive Bootstrap UI (`course_details_bootstrap.html`)**:
  - Dynamic course title, description, and instructor highlights.
  - Bootstrap 5 collapsible accordion for course lessons.
  - Empty-state alerts when no lessons are present.
- **Exam Assessment Engine (`views.py` & `urls.py`)**:
  - `submit`: Processes HTTP POST submissions, validates answers, calculates scores, and records student attempts.
  - `show_exam_result`: Displays final score, percentage, detailed question/choice review, and the **"Congratulations!"** badge for passing attempts.
- **Comprehensive Automated Tests (`tests.py`)**:
  - 12 automated unit and integration tests covering models, scoring logic, views, templates, and URL resolution.

---

## 📁 Repository Structure

```text
OnlineCourseProject/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── project_config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── OnlineCourse/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_course_data.py
│   └── templates/
│       └── OnlineCourse/
│           ├── base.html
│           ├── course_list.html
│           ├── course_details_bootstrap.html
│           ├── mock_exam.html
│           └── exam_result.html
└── submissions/
    ├── 03-admin-site.png
    └── 07-final.png
```

---

## 🚀 Quickstart & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/kaarmughilan2006/OnlineCourse.git
cd OnlineCourse
```

### 2. Set up Python Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Seed Database & Create Admin
Run the idempotent seeding command to populate sample courses, lessons, questions, and superuser:
```bash
python manage.py seed_course_data
```
* **Admin Username**: `admin`
* **Admin Password**: `adminpassword123`

### 5. Run Tests
```bash
python manage.py test
```

### 6. Start Development Server
```bash
python manage.py runserver
```
Visit:
- Home / Course Catalog: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Course Details: [http://127.0.0.1:8000/course/1/](http://127.0.0.1:8000/course/1/)
- Mock Exam: [http://127.0.0.1:8000/course/1/mock_exam/](http://127.0.0.1:8000/course/1/mock_exam/)
- Django Admin Site: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🎯 Deliverables Summary

| Task | Deliverable | Path |
|------|-------------|------|
| **Task 1** | Model definitions (`Question`, `Choice`, `Submission`) | `OnlineCourse/models.py` |
| **Task 2** | Admin configurations & inlines | `OnlineCourse/admin.py` |
| **Task 3** | Admin site screenshot | `submissions/03-admin-site.png` |
| **Task 4** | Bootstrap course details template | `OnlineCourse/templates/OnlineCourse/course_details_bootstrap.html` |
| **Task 5** | Views (`submit`, `show_exam_result`) | `OnlineCourse/views.py` |
| **Task 6** | URL patterns (`submit`, `show_exam_result`) | `OnlineCourse/urls.py` |
| **Task 7** | Mock exam result screenshot | `submissions/07-final.png` |
