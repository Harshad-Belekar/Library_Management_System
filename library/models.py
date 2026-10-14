from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    isbn = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Test(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    total_questions = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.test.title}"

class IssueReturn(models.Model):
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        default="Issued"
        
    )

    def __str__(self):
        return f"{self.student.username} - {self.book.title}" 


class Attendance(models.Model):
    
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    check_in = models.TimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        default="Present"
    )

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.username} - {self.date}"       