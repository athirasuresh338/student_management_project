from django.shortcuts import render,redirect,get_object_or_404
from .forms import StudentForm
from .models import Student
from django.contrib import messages
from django.core.paginator import Paginator
from .serializers import StudentSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


#STUDENT LIST
def student_list(request):
    students = Student.objects.all()

    # Filter parameters
    number = request.GET.get('number')
    name = request.GET.get('name')
    field = request.GET.get('field')
    min_cgpa = request.GET.get('min_cgpa')
    year = request.GET.get('year')

    # Normalization
    number = number.strip() if number and number.strip() else None
    name = name.strip() if name and name.strip() else None
    field = field if field else None
    min_cgpa = min_cgpa.strip() if min_cgpa and min_cgpa.strip() else None
    year = year.strip() if year and year.strip() else None

    # Sorting parameters
    sort_field = request.GET.get('sort_field')
    direction = request.GET.get('direction')

    if direction not in ['', '-']:
        direction = ''

    # Filtering
    if number and number.isdigit():
        students = students.filter(student_number=number)

    if name:
        parts = name.split()
        if len(parts) == 1:
            students = students.filter(first_name__icontains=parts[0])
        elif len(parts) >= 2:
            students = students.filter(
                first_name__icontains=parts[0],
                last_name__icontains=parts[1]
            )
    if field:
        students = students.filter(field_of_study=field)
    if min_cgpa:
        try:
            students = students.filter(cgpa__gte=float(min_cgpa))
        except ValueError:
            pass
    if year and year.isdigit():
        students = students.filter(enrollment_date__year=int(year))

    # Sorting
    allowed_fields = ['cgpa', 'student_number', 'enrollment_date']
    if sort_field in allowed_fields:
        students = students.order_by(f"{direction}{sort_field}")

    # Pagination
    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_list.html', {
        'page_obj': page_obj,
        'number': number or '',
        'name': name or '',
        'field': field or '',
        'min_cgpa': min_cgpa or '',
        'year': year or '',
        'sort_field': sort_field or '',
        'direction': direction or ''
    })


#VIEW SINGLE STUDENT
def view_student(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'view_student.html', {'student': student})


#ADD NEW STUDENT
def add_student(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login required to add student.")
        return redirect('login')
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('student_list')   
    else:
        form = StudentForm()    
    return render(request,'add_student.html',{'form':form})


#UPDATE STUDENT
def update_student(request,id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login required to update student.")
        return redirect('login')

    student = get_object_or_404(Student,id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request,'update_student.html',{'form':form})


#DELETE STUDENT
def delete_student(request,id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login required to delete student.")
        return redirect('login')

    student = get_object_or_404(Student,id=id)
    student.delete()
    return redirect('student_list')


#API FILTER CONFIGURATION
class StudentFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name')
    min_cgpa = filters.NumberFilter(field_name='cgpa', lookup_expr='gte')
    year = filters.NumberFilter(field_name='enrollment_date', lookup_expr='year')
    class Meta:
        model = Student
        fields = ['student_number', 'field_of_study']
    def filter_name(self, queryset, name, value):
        parts = value.split()
        if len(parts) == 1:
            return queryset.filter(first_name__icontains=parts[0])
        elif len(parts) >= 2:
            return queryset.filter(
                first_name__icontains=parts[0],
                last_name__icontains=parts[1]
            )
        return queryset

#STUDENT API (VIEWSET)
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = StudentFilter
    ordering_fields = ['student_number','cgpa','enrollment_date']