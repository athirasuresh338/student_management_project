from django import forms
from .models import Student
from datetime import date


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_number','first_name','last_name','email','field_of_study','enrollment_date','cgpa']


    #Student number validation
    def clean_student_number(self):
        student_number = self.cleaned_data.get('student_number')

        if student_number < 10000 or student_number > 99999:
            raise forms.ValidationError("Student number must be exactly 5 digits")

        return student_number



    # First name validation
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        first_name = first_name.strip().title()

        if len(first_name) < 3:
            raise forms.ValidationError('Name must contain atleast 3 characters')

        if not first_name.isalpha():
            raise forms.ValidationError('First name should contain only letters')

        return first_name



    # Last name validation
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        last_name = last_name.strip().title()

        if not last_name:
            raise forms.ValidationError("Last name cannot be empty")

        for char in last_name:
            if not (char.isalpha() or char == ' ' or char == '.'):
                raise forms.ValidationError('Last name can contain only letters, spaces, and dots')

        return last_name



    # Form-level validation
    def clean(self):
        cleaned_data = super().clean()
        first = cleaned_data.get('first_name')
        last = cleaned_data.get('last_name')

        if first and last and first == last:
            raise forms.ValidationError("First name and last name cannot be same")

        return cleaned_data


    #Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.strip().lower()

        if not email.endswith('@gmail.com'):
            raise forms.ValidationError('Only Gmail addresses are allowed')
        
        return email
    


    #Enrollment date validation
    def clean_enrollment_date(self):
        enrollment_date = self.cleaned_data.get('enrollment_date')

        if enrollment_date > date.today():
            raise forms.ValidationError("Enrollment date cannot be in the future")

        if enrollment_date.year < 2000:
            raise forms.ValidationError("Invalid enrollment year")

        return enrollment_date
    


    #CGPA validation
    def clean_cgpa(self):
        cgpa = self.cleaned_data.get('cgpa')

        if cgpa < 0 or cgpa > 10:
            raise forms.ValidationError('CGPA must be between 0 and 10')
        
        return cgpa