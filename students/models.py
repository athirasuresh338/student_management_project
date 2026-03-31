from django.db import models

class Student(models.Model):

    FIELD_OF_STUDY_CHOICES = [
        ('ENG', 'Engineering'),
        ('COM', 'Commerce'),
        ('ART', 'Arts'),
        ('BUS', 'Business'),
        ('MED', 'Medical'),
        ('LAW', 'Law'),
    ]

    student_number = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    field_of_study = models.CharField(max_length=10, choices=FIELD_OF_STUDY_CHOICES)
    enrollment_date = models.DateField()
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.student_number}"
