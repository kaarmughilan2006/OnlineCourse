from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Course, Lesson, Question, Choice, Submission


def popular_course_list(request):
    """View to list all courses."""
    courses = Course.objects.all().order_by('-pub_date')
    return render(request, 'OnlineCourse/course_list.html', {'course_list': courses})


def course_details(request, course_id):
    """View to display details of a specific course and its lessons."""
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.all().order_by('order')
    return render(
        request,
        'OnlineCourse/course_details_bootstrap.html',
        {
            'course': course,
            'lessons': lessons,
        }
    )


def mock_exam_view(request, course_id):
    """View to display the mock exam form with questions and choices."""
    course = get_object_or_404(Course, pk=course_id)
    questions = Question.objects.filter(
        Q(course=course) | Q(lesson__course=course)
    ).distinct()
    return render(
        request,
        'OnlineCourse/mock_exam.html',
        {
            'course': course,
            'questions': questions,
        }
    )


def submit(request, course_id):
    """
    Accept the submitted exam form, retrieve selected answers,
    compare with correct answers in DB, calculate score,
    and save the submission.
    """
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        # Retrieve selected choice IDs from POST parameters
        selected_choice_ids = []
        for key, values in request.POST.lists():
            if key == 'choice' or key.startswith('choice_'):
                for val in values:
                    try:
                        selected_choice_ids.append(int(val))
                    except (ValueError, TypeError):
                        pass

        # Identify relevant questions for this course
        questions = Question.objects.filter(
            Q(course=course) | Q(lesson__course=course)
        ).distinct()

        # Calculate actual score based on question evaluation
        calculated_score = 0
        for question in questions:
            if question.is_get_score(selected_choice_ids):
                calculated_score += question.grade

        # Create and save the submission record
        submission = Submission.objects.create(
            course=course,
            score=calculated_score,
        )

        # Associate the user's selected choices with this submission
        if selected_choice_ids:
            selected_choices = Choice.objects.filter(id__in=selected_choice_ids)
            submission.choices.set(selected_choices)

        submission.save()

        # Redirect to the exam result view
        return redirect('OnlineCourse:show_exam_result', course_id=course.id, submission_id=submission.id)

    # If not a POST request, redirect back to the mock exam page
    return redirect('OnlineCourse:mock_exam', course_id=course.id)


def show_exam_result(request, course_id, submission_id):
    """
    Retrieve the submission, display score, exam results,
    and show 'Congratulations' if the attempt was successful.
    """
    course = get_object_or_404(Course, pk=course_id)
    
    try:
        submission = Submission.objects.get(pk=submission_id, course=course)
    except Submission.DoesNotExist:
        return render(
            request,
            'OnlineCourse/exam_result.html',
            {
                'course': course,
                'submission': None,
                'error_message': 'Submission record not found.',
            }
        )

    questions = Question.objects.filter(
        Q(course=course) | Q(lesson__course=course)
    ).distinct()
    
    total_possible_score = sum(q.grade for q in questions)
    actual_score = submission.score
    
    if total_possible_score > 0:
        percentage = round((actual_score / total_possible_score) * 100, 1)
    else:
        percentage = 100.0

    # Passing grade threshold is 70% or higher
    is_success = percentage >= 70.0

    # Build detailed result breakdown for each question
    selected_choice_ids = set(submission.choices.values_list('id', flat=True))
    question_results = []
    
    for question in questions:
        q_is_correct = question.is_get_score(selected_choice_ids)
        choices_data = []
        for choice in question.choices.all():
            is_selected = choice.id in selected_choice_ids
            choices_data.append({
                'id': choice.id,
                'text': choice.choice_text,
                'is_correct': choice.is_correct,
                'is_selected': is_selected,
            })
        question_results.append({
            'question': question,
            'is_correct': q_is_correct,
            'choices': choices_data,
        })

    context = {
        'course': course,
        'submission': submission,
        'actual_score': actual_score,
        'total_possible_score': total_possible_score,
        'percentage': percentage,
        'is_success': is_success,
        'question_results': question_results,
    }
    return render(request, 'OnlineCourse/exam_result.html', context)
