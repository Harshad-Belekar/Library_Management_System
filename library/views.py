from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import (
    Student,
    Book,
    Test,
    Question,
    Result,
    IssueReturn,
    Attendance
)


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(request, 'home.html')


# =========================================================
# STUDENT REGISTER
# =========================================================

def student_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, 'student_register.html', {
                'error': 'Passwords do not match!'
            })

        if Student.objects.filter(username=username).exists():
            return render(request, 'student_register.html', {
                'error': 'Username already exists!'
            })

        if Student.objects.filter(email=email).exists():
            return render(request, 'student_register.html', {
                'error': 'Email already exists!'
            })

        Student.objects.create(
            name=name,
            username=username,
            email=email,
            password=password
        )

        return redirect('student_login')

    return render(request, 'student_register.html')


# =========================================================
# STUDENT LOGIN
# =========================================================

def student_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        student = Student.objects.filter(
            username=username,
            password=password
        ).first()

        if student:
            return redirect(
                f'/student/dashboard/?username={student.username}'
            )

        return render(request, 'student_login.html', {
            'error': 'Invalid Username or Password!'
        })

    return render(request, 'student_login.html')


# =========================================================
# STUDENT DASHBOARD
# =========================================================

def student_dashboard(request):

    username = request.GET.get("username")

    student = Student.objects.filter(
        username=username
    ).first()

    books = Book.objects.filter(
        quantity__gt=0
    ).order_by('title')[:6]

    tests = Test.objects.all().order_by('-created_at')[:5]

    results = []

    attendance_count = 0
    attendance_total = 0
    attendance_percentage = 0

    if student:

        results = Result.objects.filter(
            student=student
        ).select_related('test').order_by('-created_at')[:5]

        attendance_total = Attendance.objects.filter(
            student=student
        ).count()

        attendance_count = Attendance.objects.filter(
            student=student,
            status="Present"
        ).count()

        if attendance_total > 0:
            attendance_percentage = (
                attendance_count / attendance_total
            ) * 100

    return render(
        request,
        'student_dashboard.html',
        {
            'student': student,
            'books': books,
            'tests': tests,
            'results': results,
            'attendance_count': attendance_count,
            'attendance_total': attendance_total,
            'attendance_percentage': attendance_percentage,
        }
    )


# =========================================================
# STUDENT BOOKS
# =========================================================

def student_books(request):

    username = request.GET.get("username")

    student = Student.objects.filter(
        username=username
    ).first()

    books = Book.objects.filter(
        quantity__gt=0
    ).order_by('title')

    return render(
        request,
        'student_books.html',
        {
            'student': student,
            'books': books
        }
    )


# =========================================================
# BOOK STUDY
# =========================================================

def book_study(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    username = request.GET.get("username")

    student = Student.objects.filter(
        username=username
    ).first()

    return render(
        request,
        'book_study.html',
        {
            'book': book,
            'student': student
        }
    )


# =========================================================
# STUDENT TESTS
# =========================================================

def student_tests(request):

    username = request.GET.get("username")

    student = Student.objects.filter(
        username=username
    ).first()

    tests = Test.objects.all().order_by('-created_at')

    return render(
        request,
        'student_tests.html',
        {
            'student': student,
            'tests': tests
        }
    )


# =========================================================
# TAKE TEST
# =========================================================

def take_test(request, test_id):

    username = request.GET.get("username")

    student = Student.objects.filter(
        username=username
    ).first()

    if not student:
        return redirect('student_login')

    test = get_object_or_404(Test, id=test_id)

    questions = Question.objects.filter(
        test=test
    )

    if request.method == "POST":

        score = 0

        for question in questions:

            answer = request.POST.get(
                f"question_{question.id}"
            )

            if answer == question.correct_answer:
                score += 1

        total = questions.count()

        percentage = 0

        if total > 0:
            percentage = (score / total) * 100

        result = Result.objects.create(
            student=student,
            test=test,
            score=score,
            total_questions=total,
            percentage=percentage
        )

        return redirect(
            f'/student/result/{result.id}/?username={username}'
        )

    return render(
        request,
        'take_test.html',
        {
            'student': student,
            'test': test,
            'questions': questions
        }
    )


# =========================================================
# STUDENT RESULT
# =========================================================

def student_result(request, result_id):

    username = request.GET.get("username")

    student = Student.objects.filter(
        username=username
    ).first()

    result = get_object_or_404(Result, id=result_id)

    return render(
        request,
        'student_result.html',
        {
            'student': student,
            'result': result
        }
    )


# =========================================================
# MY RESULTS
# =========================================================

def my_results(request):

    username = request.GET.get("username")

    student = Student.objects.filter(
        username=username
    ).first()

    results = []

    if student:
        results = Result.objects.filter(
            student=student
        ).select_related('test').order_by('-created_at')

    return render(
        request,
        'my_results.html',
        {
            'student': student,
            'results': results
        }
    )


# =========================================================
# RECOMMENDED BOOKS
# =========================================================

def recommended_books(request):

    username = request.GET.get("username")

    student = Student.objects.filter(
        username=username
    ).first()

    recommended = Book.objects.none()

    if student:

        latest_result = Result.objects.filter(
            student=student
        ).select_related(
            'test'
        ).order_by('-created_at').first()

        if latest_result:

            percentage = latest_result.percentage
            category = latest_result.test.category

            if percentage >= 60:

                recommended = Book.objects.filter(
                    category__iexact=category,
                    quantity__gt=0
                )

            elif percentage >= 40:

                recommended = Book.objects.filter(
                    quantity__gt=0
                ).order_by('title')[:5]

            else:

                recommended = Book.objects.filter(
                    quantity__gt=0
                ).order_by('title')[:3]

    return render(
        request,
        'recommended_books.html',
        {
            'student': student,
            'recommended': recommended
        }
    )


# =========================================================
# STUDENT MARK ATTENDANCE
# =========================================================

def mark_attendance(request):

    username = request.GET.get("username")

    student = Student.objects.filter(
        username=username
    ).first()

    if not student:
        return redirect('student_login')

    today = timezone.now().date()

    Attendance.objects.get_or_create(
        student=student,
        date=today,
        defaults={
            'status': 'Present'
        }
    )

    return redirect(
        f'/student/dashboard/?username={student.username}'
    )


# =========================================================
# STUDENT ATTENDANCE
# =========================================================

def student_attendance(request):

    username = request.GET.get("username")

    student = Student.objects.filter(
        username=username
    ).first()

    if not student:
        return redirect('student_login')

    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by('-date')

    total_days = attendance_records.count()

    present_days = attendance_records.filter(
        status="Present"
    ).count()

    attendance_percentage = 0

    if total_days > 0:
        attendance_percentage = (
            present_days / total_days
        ) * 100

    return render(
        request,
        'student_attendance.html',
        {
            'student': student,
            'attendance_records': attendance_records,
            'total_days': total_days,
            'present_days': present_days,
            'attendance_percentage': attendance_percentage,
        }
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        ).strip()

        if username == "admin" and password == "admin123":

            return redirect('admin_dashboard')

        return render(
            request,
            'admin_login.html',
            {
                'error': 'Invalid Username or Password!'
            }
        )

    return render(
        request,
        'admin_login.html'
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_dashboard(request):

    return render(
        request,
        'admin_dashboard.html'
    )


# =========================================================
# ADMIN ATTENDANCE
# =========================================================

def attendance(request):

    attendance_records = Attendance.objects.select_related(
        'student'
    ).order_by(
        '-date',
        '-check_in'
    )

    return render(
        request,
        'attendance.html',
        {
            'attendance_records': attendance_records
        }
    )


# =========================================================
# STUDENT ANALYTICS
# =========================================================

def student_analytics(request):

    students = Student.objects.all().order_by('name')

    analytics = []

    for student in students:

        results = Result.objects.filter(
            student=student
        )

        attendance_total = Attendance.objects.filter(
            student=student
        ).count()

        attendance_present = Attendance.objects.filter(
            student=student,
            status="Present"
        ).count()

        attendance_percentage = 0

        if attendance_total > 0:
            attendance_percentage = (
                attendance_present /
                attendance_total
            ) * 100

        average_percentage = 0

        if results.exists():

            total_percentage = sum(
                result.percentage
                for result in results
            )

            average_percentage = (
                total_percentage /
                results.count()
            )

        analytics.append({
            'student': student,
            'total_tests': results.count(),
            'average_percentage': round(
                average_percentage,
                2
            ),
            'attendance_percentage': round(
                attendance_percentage,
                2
            ),
        })

    return render(
        request,
        'student_analytics.html',
        {
            'analytics': analytics
        }
    )


# =========================================================
# MANAGE BOOKS
# =========================================================

def manage_books(request):

    books = Book.objects.all().order_by('-id')

    return render(
        request,
        'manage_books.html',
        {
            'books': books
        }
    )


# =========================================================
# ADD BOOK
# =========================================================

def add_book(request):

    if request.method == "POST":

        Book.objects.create(
            title=request.POST.get("title"),
            author=request.POST.get("author"),
            category=request.POST.get("category"),
            isbn=request.POST.get("isbn"),
            quantity=request.POST.get("quantity"),
            description=request.POST.get("description")
        )

        return redirect('manage_books')

    return render(
        request,
        'add_book.html'
    )


# =========================================================
# EDIT BOOK
# =========================================================

def edit_book(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )

    if request.method == "POST":

        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.category = request.POST.get("category")
        book.isbn = request.POST.get("isbn")
        book.quantity = request.POST.get("quantity")
        book.description = request.POST.get("description")

        book.save()

        return redirect('manage_books')

    return render(
        request,
        'edit_book.html',
        {
            'book': book
        }
    )


# =========================================================
# DELETE BOOK
# =========================================================

def delete_book(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )

    book.delete()

    return redirect('manage_books')


# =========================================================
# STUDENTS
# =========================================================

def students(request):

    students = Student.objects.all().order_by('-id')

    return render(
        request,
        'students.html',
        {
            'students': students
        }
    )


# =========================================================
# DELETE STUDENT
# =========================================================

def delete_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    student.delete()

    return redirect('students')


# =========================================================
# CREATE TEST
# =========================================================

def create_test(request):

    if request.method == "POST":

        Test.objects.create(
            title=request.POST.get("title"),
            category=request.POST.get("category"),
            description=request.POST.get("description"),
            total_questions=request.POST.get(
                "total_questions"
            )
        )

        return redirect('manage_tests')

    return render(
        request,
        'create_test.html'
    )


# =========================================================
# MANAGE TESTS
# =========================================================

def manage_tests(request):

    tests = Test.objects.all().order_by('-id')

    return render(
        request,
        'manage_tests.html',
        {
            'tests': tests
        }
    )


# =========================================================
# DELETE TEST
# =========================================================

def delete_test(request, id):

    test = get_object_or_404(
        Test,
        id=id
    )

    test.delete()

    return redirect('manage_tests')


# =========================================================
# ADD QUESTION
# =========================================================

def add_question(request, test_id):

    test = get_object_or_404(
        Test,
        id=test_id
    )

    if request.method == "POST":

        Question.objects.create(
            test=test,
            question=request.POST.get("question"),
            option1=request.POST.get("option1"),
            option2=request.POST.get("option2"),
            option3=request.POST.get("option3"),
            option4=request.POST.get("option4"),
            correct_answer=request.POST.get("correct_answer")
        )

        return redirect('manage_tests')

    return render(
        request,
        'add_question.html',
        {
            'test': test
        }
    )


# =========================================================
# TEST RESULTS
# =========================================================

def test_results(request):

    results = Result.objects.select_related(
        'student',
        'test'
    ).order_by('-created_at')

    return render(
        request,
        'test_results.html',
        {
            'results': results
        }
    )


# =========================================================
# ISSUE / RETURN
# =========================================================

def issue_return(request):

    records = IssueReturn.objects.select_related(
        'student',
        'book'
    ).order_by('-issue_date')

    students = Student.objects.all().order_by('name')

    books = Book.objects.filter(
        quantity__gt=0
    ).order_by('title')

    if request.method == "POST":

        student_id = request.POST.get("student")
        book_id = request.POST.get("book")

        student = get_object_or_404(
            Student,
            id=student_id
        )

        book = get_object_or_404(
            Book,
            id=book_id
        )

        IssueReturn.objects.create(
            student=student,
            book=book
        )

        if book.quantity > 0:

            book.quantity -= 1
            book.save()

        return redirect('issue_return')

    return render(
        request,
        'issue_return.html',
        {
            'records': records,
            'students': students,
            'books': books
        }
    )


# =========================================================
# RETURN BOOK
# =========================================================

def return_book(request, id):

    record = get_object_or_404(
        IssueReturn,
        id=id
    )

    if record.status == "Issued":

        record.status = "Returned"

        record.return_date = timezone.now().date()

        record.save()

        record.book.quantity += 1
        record.book.save()

    return redirect('issue_return')


# =========================================================
# REPORTS
# =========================================================

def reports(request):

    total_books = Book.objects.count()

    total_students = Student.objects.count()

    total_tests = Test.objects.count()

    total_results = Result.objects.count()

    issued_books = IssueReturn.objects.filter(
        status="Issued"
    ).count()

    returned_books = IssueReturn.objects.filter(
        status="Returned"
    ).count()

    recent_results = Result.objects.select_related(
        'student',
        'test'
    ).order_by('-created_at')[:5]

    recent_records = IssueReturn.objects.select_related(
        'student',
        'book'
    ).order_by('-issue_date')[:5]

    return render(
        request,
        'reports.html',
        {
            'total_books': total_books,
            'total_students': total_students,
            'total_tests': total_tests,
            'total_results': total_results,
            'issued_books': issued_books,
            'returned_books': returned_books,
            'recent_results': recent_results,
            'recent_records': recent_records
        }
    )