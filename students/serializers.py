from rest_framework import serializers
from .models import Student
from datetime import date

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


    def validate_student_number(self,value):
        if value < 10000 or value > 99999:
            raise serializers.ValidationError("Student number must be exactly 5 digits")
        return value


    def validate_first_name(self,value):
        value = value.strip().title()
        if len(value) < 3:
            raise serializers.ValidationError('Name must contain atleast 3 characters')
        if not value.isalpha():
            raise serializers.ValidationError('First name should contain only letters')
        return value


    def validate_last_name(self,value):
        value = value.strip().title()
        if not value:
            raise serializers.ValidationError("Last name cannot be empty")
        for char in value:
            if not (char.isalpha() or char == ' ' or char == '.'):
                raise serializers.ValidationError('Last name can contain only letters, spaces, and dots')
        return value


    def validate_email(self,value):
        value = value.strip().lower()
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError('Only Gmail addresses are allowed')
        return value
    

    def validate_enrollment_date(self,value):
        if value > date.today():
            raise serializers.ValidationError("Enrollment date cannot be in the future")
        if value.year < 2000:
            raise serializers.ValidationError("Invalid enrollment year")
        return value
    

    def validate_cgpa(self,value):
        if value < 0 or value > 10:
            raise serializers.ValidationError('CGPA must be between 0 and 10')
        return value
    