# Final Submission Checklist - Coursera / IBM OnlineCourse Project

**Student GitHub Username**: `kaarmughilan2006`  
**Repository Name**: `OnlineCourse`  
**Repository URL**: [https://github.com/kaarmughilan2006/OnlineCourse](https://github.com/kaarmughilan2006/OnlineCourse)  
**Branch**: `main`  
**Overall Status**: **PASS** (All 7 assignment questions fully automated, tested, screenshot-verified, and published to GitHub).

---

## 📋 Deliverable URLs & Verification

### Question 1: models.py
* **Type**: URL (3 Points)
* **Exact Rubric Requirement**: "Task 1: Submit the public GitHub URL of the models.py file, which includes the Question, Choice, and Submission models."
* **Public GitHub URL**:  
  `https://github.com/kaarmughilan2006/OnlineCourse/blob/main/OnlineCourse/models.py`
* **Local File Path**: `OnlineCourse/models.py`
* **Verification Status**: **PASS (HTTP 200 Verified)**
* **Details**: Contains `Question`, `Choice`, and `Submission` models alongside supporting `Course`, `Lesson`, `Instructor`, `Learner`, and `Enrollment` models. Implements `is_get_score(selected_ids)` evaluation method and relational foreign keys.

---

### Question 2: admin.py
* **Type**: URL (3 Points)
* **Exact Rubric Requirement**: "Task 2: Submit the public GitHub URL of the admin.py file, which includes seven imported classes, along with the implementations of QuestionInline, ChoiceInline, QuestionAdmin, and LessonAdmin."
* **Public GitHub URL**:  
  `https://github.com/kaarmughilan2006/OnlineCourse/blob/main/OnlineCourse/admin.py`
* **Local File Path**: `OnlineCourse/admin.py`
* **Verification Status**: **PASS (HTTP 200 Verified)**
* **Details**: Contains exactly the seven imported model classes (`Course, Lesson, Question, Choice, Instructor, Learner, Submission`) and implements `QuestionInline`, `ChoiceInline`, `QuestionAdmin`, and `LessonAdmin` with appropriate inlines and model registrations.

---

### Question 3: Django Admin Site Screenshot
* **Type**: Upload (1 Point)
* **Exact Rubric Requirement**: "Task 3: Submit a screenshot of the admin site with the image name 03-admin-site that displays the “Authentication and Authorization” section and the “OnlineCourse” section."
* **Image Name**: `03-admin-site.png`
* **File Path**: `submissions/03-admin-site.png`
* **Verification Status**: **PASS (Visual Inspection Verified)**
* **Details**: Genuine browser screenshot of the live authenticated Django Admin site. Visibly displays:
  1. `AUTHENTICATION AND AUTHORIZATION` (Groups, Users)
  2. `ONLINECOURSE` (Choices, Courses, Instructors, Learners, Lessons, Questions, Submissions)
  3. Logged-in admin user status (`WELCOME, ADMIN.`)

---

### Question 4: course_details_bootstrap.html
* **Type**: URL (2 Points)
* **Exact Rubric Requirement**: "Task 4: Submit the public GitHub URL of the course_details_bootstrap.html file, which includes the course detail template to display the course name and all related lessons using Django template tags and Bootstrap styling?"
* **Public GitHub URL**:  
  `https://github.com/kaarmughilan2006/OnlineCourse/blob/main/OnlineCourse/templates/OnlineCourse/course_details_bootstrap.html`
* **Local File Path**: `OnlineCourse/templates/OnlineCourse/course_details_bootstrap.html`
* **Verification Status**: **PASS (HTTP 200 Verified)**
* **Details**: Built with Bootstrap 5. Displays dynamic course name `{{ course.name }}`, description, instructor highlights, sequential lesson modules via collapsible accordion, and an empty-state alert if no lessons exist.

---

### Question 5: views.py
* **Type**: URL (2 Points)
* **Exact Rubric Requirement**: "Task 5: Submit the public GitHub URL of the views.py file, which includes the submit and show_exam_result functions."
* **Public GitHub URL**:  
  `https://github.com/kaarmughilan2006/OnlineCourse/blob/main/OnlineCourse/views.py`
* **Local File Path**: `OnlineCourse/views.py`
* **Verification Status**: **PASS (HTTP 200 Verified)**
* **Details**: Contains exact functions `submit` and `show_exam_result`. `submit` handles POST answers, calculates scores via database-backed questions, persists `Submission` records, and redirects to result page. `show_exam_result` retrieves the submission, calculates percentages, and passes result context.

---

### Question 6: urls.py
* **Type**: URL (2 Points)
* **Exact Rubric Requirement**: "Task 6: Submit the public GitHub URL of the urls.py file, which includes the paths for submit and show_exam_result."
* **Public GitHub URL**:  
  `https://github.com/kaarmughilan2006/OnlineCourse/blob/main/OnlineCourse/urls.py`
* **Local File Path**: `OnlineCourse/urls.py`
* **Verification Status**: **PASS (HTTP 200 Verified)**
* **Details**: Application-level `urls.py` with `app_name = 'OnlineCourse'`. Maps routes for `views.submit` (`name='submit'`) and `views.show_exam_result` (`name='show_exam_result'`). Tested with Django URL reverse and resolve.

---

### Question 7: Successful Mock Exam Result Screenshot
* **Type**: Upload (2 Points)
* **Exact Rubric Requirement**: "Task 7: Submit a screenshot showing the result of the mock exam with the image name 07-final showing a successful attempt, including the ‘Congratulations’ message, score, and exam results."
* **Image Name**: `07-final.png`
* **File Path**: `submissions/07-final.png`
* **Verification Status**: **PASS (Visual Inspection Verified)**
* **Details**: Genuine browser screenshot from the running application showing:
  1. Exact word `Congratulations!` banner with trophy icon.
  2. Actual calculated score: `5 / 5` (`Percentage: 100.0%`).
  3. Detailed question-by-question evaluation results with correct answer indicators.

---

## 🛠️ Verification Execution Results

* **Django System Checks**: `python manage.py check` -> 0 errors / 0 warnings (**PASS**).
* **Automated Unit Tests**: `python manage.py test` -> 12 tests passed in 0.032s (**PASS**).
* **Database Migrations**: Applied cleanly to SQLite database (**PASS**).
* **Sample Data Seeding**: `seed_course_data` executed idempotently (**PASS**).
* **Public Access**: All 5 GitHub URLs return HTTP status 200 and are publicly viewable without authentication (**PASS**).
