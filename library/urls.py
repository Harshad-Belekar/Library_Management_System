from django.urls import path
from . import views


urlpatterns = [

    # HOME
    path(
        '',
        views.home,
        name='home'
    ),


    # =====================================================
    # STUDENT
    # =====================================================

    path(
        'student/register/',
        views.student_register,
        name='student_register'
    ),

    path(
        'student/login/',
        views.student_login,
        name='student_login'
    ),

    path(
        'student/dashboard/',
        views.student_dashboard,
        name='student_dashboard'
    ),

    path(
        'student/books/',
        views.student_books,
        name='student_books'
    ),

    path(
        'student/book/<int:book_id>/',
        views.book_study,
        name='book_study'
    ),


    # =====================================================
    # TEST
    # =====================================================

    path(
        'student/tests/',
        views.student_tests,
        name='student_tests'
    ),

    path(
        'student/take-test/<int:test_id>/',
        views.take_test,
        name='take_test'
    ),

    path(
        'student/result/<int:result_id>/',
        views.student_result,
        name='student_result'
    ),

    path(
        'student/results/',
        views.my_results,
        name='my_results'
    ),

    path(
        'student/recommendations/',
        views.recommended_books,
        name='recommended_books'
    ),


    # =====================================================
    # STUDENT ATTENDANCE
    # =====================================================

    path(
        'student/mark-attendance/',
        views.mark_attendance,
        name='mark_attendance'
    ),

    path(
        'student/attendance/',
        views.student_attendance,
        name='student_attendance'
    ),


    # =====================================================
    # ADMIN
    # =====================================================

    path(
        'admin-login/',
        views.admin_login,
        name='admin_login'
    ),

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'student-analytics/',
        views.student_analytics,
        name='student_analytics'
    ),

    path(
        'attendance/',
        views.attendance,
        name='attendance'
    ),


    # =====================================================
    # BOOK MANAGEMENT
    # =====================================================

    path(
        'manage-books/',
        views.manage_books,
        name='manage_books'
    ),

    path(
        'add-book/',
        views.add_book,
        name='add_book'
    ),

    path(
        'edit-book/<int:id>/',
        views.edit_book,
        name='edit_book'
    ),

    path(
        'delete-book/<int:id>/',
        views.delete_book,
        name='delete_book'
    ),


    # =====================================================
    # STUDENT MANAGEMENT
    # =====================================================

    path(
        'students/',
        views.students,
        name='students'
    ),

    path(
        'delete-student/<int:id>/',
        views.delete_student,
        name='delete_student'
    ),


    # =====================================================
    # TEST MANAGEMENT
    # =====================================================

    path(
        'create-test/',
        views.create_test,
        name='create_test'
    ),

    path(
        'manage-tests/',
        views.manage_tests,
        name='manage_tests'
    ),

    path(
        'delete-test/<int:id>/',
        views.delete_test,
        name='delete_test'
    ),

    path(
        'add-question/<int:test_id>/',
        views.add_question,
        name='add_question'
    ),


    # =====================================================
    # RESULTS
    # =====================================================

    path(
        'test-results/',
        views.test_results,
        name='test_results'
    ),


    # =====================================================
    # ISSUE / RETURN
    # =====================================================

    path(
        'issue-return/',
        views.issue_return,
        name='issue_return'
    ),

    path(
        'return-book/<int:id>/',
        views.return_book,
        name='return_book'
    ),


    # =====================================================
    # REPORTS
    # =====================================================

    path(
        'reports/',
        views.reports,
        name='reports'
    ),
]