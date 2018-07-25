from django import forms
from django.contrib.auth.models import User
from .models import Professor, Course, Education, Experience, Projects, Publication, Recognition, Student

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class ProfessorForm(forms.ModelForm):

    class Meta:
        model = Professor
#        fields = ['course', 'album_title', 'genre', 'album_logo']
        fields = ['Department', 'designation', 'pro_pic', 'phone_no', 'room_no', 'visit_time', 'Research_Interests', 'Biography']


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'Dept', 'no', 'prof']
        # fields = ['name', 'Dept', 'no', 'credits', 'start_year', 'end_year', 'prof']


class EducationForm(forms.ModelForm):

    class Meta:
        model = Education
        fields = ['degree', 'field', 'University', 'Year', 'prof']


class ExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        fields = ['Detail', 'Institution', 'start_Year', 'end_Year', 'Professor']


class ProjectsForm(forms.ModelForm):

    class Meta:
        model = Projects
        fields = ['Title', 'Detail', 'start_Year', 'end_Year', 'Professor']


class PublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = ['Name', 'Detail', 'Date', 'Professor']


class RecognitionForm(forms.ModelForm):

    class Meta:
        model = Recognition
        fields = ['Name', 'Detail', 'Professor']


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['Name', 'degree', 'Detail', 'Professor']
