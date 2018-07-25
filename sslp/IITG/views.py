from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse

from django.views import generic
from django.http import HttpResponse
from django.template import loader

# from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import UserForm, ProfessorForm, CourseForm, EducationForm, ExperienceForm, ProjectsForm, PublicationForm, RecognitionForm, StudentForm
from .models import Professor, Course, Education, Experience, Projects, Publication, Recognition, Dept, Student
# from django.contrib.auth.models import User

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def invalid(request):
    # all_depts = Dept.objects.all()
    # return render(request, 'login.html', {'all_depts': all_depts})
    return render(request, 'myIITapp/invalid.html')


def complete_profile(request):
    # all_depts = Dept.objects.all()
    # return render(request, 'login.html', {'all_depts': all_depts})
    return render(request, 'myIITapp/complete_profile.html')


def profile(request):
    # all_depts = Dept.objects.all()
    # return render(request, 'login.html', {'all_depts': all_depts})
    return render(request, 'IITG/profile.html')


class ProfUpdate(UpdateView):
    model = Professor
    fields = ['phone_no', 'room_no', 'visit_time', 'Department', 'designation', 'Research_Interests', 'Biography']


def prof_detail(request, professor_id):
    professor = Professor.objects.get(pk=professor_id)
    professor.course_set.all()
    professor.education_set.all()
    professor.experience_set.all()
    return render(request, "IITG/prof_detail.html", {'professor': professor})


def prof_detail_general(request, professor_id):
    professor = Professor.objects.get(pk=professor_id)
    professor.course_set.all()
    professor.education_set.all()
    professor.experience_set.all()
    return render(request, "IITG/prof_detail_general.html", {'professor': professor})


def prof_website(request, professor_id):
    professor = Professor.objects.get(pk=professor_id)
    return render(request, "IITG/professor_website.html", {'professor': professor})


def faculty(request):
    # context = RequestContext(request)
    if request.method == 'GET':
        # professor=ProfessorForm(request.GET)
        professors = Professor.objects.all()
    else:
        pass
    return render(request, 'IITG/faculty.html', {'professors': professors})


def faculty_page(request):
    if request.method == 'GET':
        depts = Dept.objects.all()
    else:
        pass
    return render(request, "IITG/faculty_page.html", {'depts': depts})


def dept_faculty(request, filter_by, dept_id):
    #    if not request.user.is_authenticated():
    #       return render(request, 'IITG/login.html')
    #    else:
    dept = Dept.objects.get(pk=dept_id)
    professor_ids = []
    # for dept in Dept.objects.filter(user=request.user):
    # for dept in Dept.objects.all():
    # for dept in Dept.objects.get(pk=dept_id):
    for professor in dept.professor_set.all():
        professor_ids.append(professor.pk)
    users_professors = Professor.objects.filter(pk__in=professor_ids)
    return render(request, 'IITG/dept_faculty.html', {
        'professor_list': users_professors,
        'filter_by': filter_by,
    }, dept_id)


def create_professor(request):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        form = ProfessorForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            professor = form.save(commit=False)
            professor.user = request.user
            professor.save()
            return render(request, 'IITG/prof_detail.html', {'professor': professor})
        context = {
            "form": form,
        }
        return render(request, 'IITG/create_professor.html', context)


def delete_professor(request, professor_id):
    professor = Professor.objects.get(pk=professor_id)
    professor.delete()
    professors = Professor.objects.filter(user=request.user)
    return render(request, 'IITG/index.html', {'professors': professors})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        professors = Professor.objects.filter(user=request.user)
        education = Education.objects.all()
        query = request.GET.get("q")
        if query:
            professors = professors.filter(
                Q(user__icontains=query) #|
                # Q(artist__icontains=query)
            ).distinct()
            return render(request, 'IITG/index.html', {
                'professors': professors,
                # 'course': course,
            })
        else:
            return render(request, 'IITG/index.html', {'professors': professors})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'IITG/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                professors = Professor.objects.filter(user=request.user)
                return render(request, 'IITG/index.html', {'professors': professors})
            else:
                return render(request, 'IITG/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'IITG/login.html', {'error_message': 'Invalid login'})
    return render(request, 'IITG/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                professors = Professor.objects.filter(user=request.user)
                return render(request, 'IITG/index.html', {'professors': professors})
    context = {
        "form": form,
    }
    return render(request, 'IITG/register.html', context)


def courses(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        try:
            course_ids = []
            for professor in Professor.objects.filter(user=request.user):
                for course in professor.course_set.all():
                    course_ids.append(course.pk)
            users_courses = Course.objects.filter(pk__in=course_ids)
        except Professor.DoesNotExist:
            users_courses = []
        return render(request, 'IITG/courses.html', {
            'course_list': users_courses,
            'filter_by': filter_by,
        })


def create_course(request, professor_id):
    form = CourseForm(request.POST or None, request.FILES or None)
    professor = get_object_or_404(Professor, pk=professor_id)
    if form.is_valid():
        professors_courses = professor.course_set.all()
        for s in professors_courses:
            if s.no == form.cleaned_data.get("no"):
                context = {
                    'professor': professor,
                    'form': form,
                    'error_message': 'You already added that course',
                }
                return render(request, 'IITG/create_course.html', context)
        course = form.save(commit=False)
        course.professor = professor
        course.save()
        return render(request, 'IITG/course_detail.html', {'professor': professor})
    context = {
        'professor': professor,
        'form': form,
    }
    return render(request, 'IITG/create_course.html', context)


def delete_course(request, professor_id, course_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    course = Course.objects.get(pk=course_id)
    course.delete()
    return render(request, 'IITG/course_detail.html', {'professor': professor})


def course_detail(request, professor_id):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        user = request.user
        professor = get_object_or_404(Professor, pk=professor_id)
        return render(request, 'IITG/course_detail.html', {'professor': professor, 'user': user})


def educations(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        try:
            education_ids = []
            for professor in Professor.objects.filter(user=request.user):
                for education in professor.education_set.all():
                    education_ids.append(education.pk)
            users_educations = Education.objects.filter(pk__in=education_ids)
        except Professor.DoesNotExist:
            users_educations = []
        return render(request, 'IITG/educations.html', {
            'education_list': users_educations,
            'filter_by': filter_by,
        })


def create_education(request, professor_id):
    form = EducationForm(request.POST or None, request.FILES or None)
    professor = get_object_or_404(Professor, pk=professor_id)
    if form.is_valid():
        professors_educations = professor.education_set.all()
        education = form.save(commit=False)
        education.professor = professor
        education.save()
        return render(request, 'IITG/education_detail.html', {'professor': professor})
    context = {
        'professor': professor,
        'form': form,
    }
    return render(request, 'IITG/create_education.html', context)


def delete_education(request, professor_id, education_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    education = Education.objects.get(pk=education_id)
    education.delete()
    return render(request, 'IITG/education_detail.html', {'professor': professor})


def education_detail(request, professor_id):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        user = request.user
        professor = get_object_or_404(Professor, pk=professor_id)
        return render(request, 'IITG/education_detail.html', {'professor': professor, 'user': user})


def experiences(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        try:
            experience_ids = []
            for professor in Professor.objects.filter(user=request.user):
                for experience in professor.project_set.all():
                    experience_ids.append(experience.pk)
            users_experiences = Experience.objects.filter(pk__in=experience_ids)
        except Professor.DoesNotExist:
            users_experiences = []
        return render(request, 'IITG/experiences.html', {
            'experience_list': users_experiences,
            'filter_by': filter_by,
        })


def create_experience(request, professor_id):
    form = ExperienceForm(request.POST or None, request.FILES or None)
    professor = get_object_or_404(Professor, pk=professor_id)
    if form.is_valid():
        professors_experiences = professor.experience_set.all()
        experience = form.save(commit=False)
        experience.professor = professor
        experience.save()
        return render(request, 'IITG/experience_detail.html', {'professor': professor})
    context = {
        'professor': professor,
        'form': form,
    }
    return render(request, 'IITG/create_experience.html', context)


def delete_experience(request, professor_id, experience_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    experience = Experience.objects.get(pk=experience_id)
    experience.delete()
    return render(request, 'IITG/experience_detail.html', {'professor': professor})


def experience_detail(request, professor_id):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        user = request.user
        professor = get_object_or_404(Professor, pk=professor_id)
        return render(request, 'IITG/experience_detail.html', {'professor': professor, 'user': user})


def projects(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        try:
            project_ids = []
            for professor in Professor.objects.filter(user=request.user):
                for project in professor.projects_set.all():
                    project_ids.append(project.pk)
            users_project = Projects.objects.filter(pk__in=project_ids)
        except Professor.DoesNotExist:
            users_project = []
        return render(request, 'IITG/publication.html', {
            'project_list': users_project,
            'filter_by': filter_by,
        })


def create_project(request, professor_id):
    form = ProjectsForm(request.POST or None, request.FILES or None)
    professor = get_object_or_404(Professor, pk=professor_id)
    if form.is_valid():
        professors_project = professor.projects_set.all()
        project = form.save(commit=False)
        project.professor = professor
        project.save()
        return render(request, 'IITG/project_detail.html', {'professor': professor})
    context = {
        'professor': professor,
        'form': form,
    }
    return render(request, 'IITG/create_project.html', context)


def delete_project(request, professor_id, project_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    project = Projects.objects.get(pk=project_id)
    project.delete()
    return render(request, 'IITG/project_detail.html', {'professor': professor})


def project_detail(request, professor_id):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        user = request.user
        professor = get_object_or_404(Professor, pk=professor_id)
        return render(request, 'IITG/project_detail.html', {'professor': professor, 'user': user})


def publications(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        try:
            publication_ids = []
            for professor in Professor.objects.filter(user=request.user):
                for publication in professor.publication_set.all():
                    publication_ids.append(publication.pk)
            users_publications = Publication.objects.filter(pk__in=publication_ids)
        except Professor.DoesNotExist:
            users_publications = []
        return render(request, 'IITG/publications.html', {
            'publication_list': users_publications,
            'filter_by': filter_by,
        })


def create_publication(request, professor_id):
    form = PublicationForm(request.POST or None, request.FILES or None)
    professor = get_object_or_404(Professor, pk=professor_id)
    if form.is_valid():
        professors_publications = professor.publication_set.all()
        publication = form.save(commit=False)
        publication.professor = professor
        publication.save()
        return render(request, 'IITG/publication_detail.html', {'professor': professor})
    context = {
        'professor': professor,
        'form': form,
    }
    return render(request, 'IITG/create_publication.html', context)


def delete_publication(request, professor_id, publication_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    publication = Publication.objects.get(pk=publication_id)
    publication.delete()
    return render(request, 'IITG/publication_detail.html', {'professor': professor})


def publication_detail(request, professor_id):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        user = request.user
        professor = get_object_or_404(Professor, pk=professor_id)
        return render(request, 'IITG/publication_detail.html', {'professor': professor, 'user': user})


def recognitions(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        try:
            recognition_ids = []
            for professor in Professor.objects.filter(user=request.user):
                for recognition in professor.recognition_set.all():
                    recognition_ids.append(recognition.pk)
            users_recognitions = Recognition.objects.filter(pk__in=recognition_ids)
        except Professor.DoesNotExist:
            users_recognitions = []
        return render(request, 'IITG/recognitions.html', {
            'recognition_list': users_recognitions,
            'filter_by': filter_by,
        })


def create_recognition(request, professor_id):
    form = RecognitionForm(request.POST or None, request.FILES or None)
    professor = get_object_or_404(Professor, pk=professor_id)
    if form.is_valid():
        professors_recognitions = professor.recognition_set.all()
        recognition = form.save(commit=False)
        recognition.professor = professor
        recognition.save()
        return render(request, 'IITG/recognition_detail.html', {'professor': professor})
    context = {
        'professor': professor,
        'form': form,
    }
    return render(request, 'IITG/create_recognition.html', context)


def delete_recognition(request, professor_id, recognition_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    recognition = Recognition.objects.get(pk=recognition_id)
    recognition.delete()
    return render(request, 'IITG/recognition_detail.html', {'professor': professor})


def recognition_detail(request, professor_id):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        user = request.user
        professor = get_object_or_404(Professor, pk=professor_id)
        return render(request, 'IITG/recognition_detail.html', {'professor': professor, 'user': user})


def students(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        try:
            student_ids = []
            for professor in Professor.objects.filter(user=request.user):
                for student in professor.student_set.all():
                    student_ids.append(student.pk)
            users_students = Student.objects.filter(pk__in=student_ids)
        except Professor.DoesNotExist:
            users_students = []
        return render(request, 'IITG/students.html', {
            'student_list': users_students,
            'filter_by': filter_by,
        })


def create_student(request, professor_id):
    form = StudentForm(request.POST or None, request.FILES or None)
    professor = get_object_or_404(Professor, pk=professor_id)
    if form.is_valid():
        professors_students = professor.student_set.all()
        student = form.save(commit=False)
        student.professor = professor
        student.save()
        return render(request, 'IITG/student_detail.html', {'professor': professor})
    context = {
        'professor': professor,
        'form': form,
    }
    return render(request, 'IITG/create_student.html', context)


def delete_student(request, professor_id, student_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    student = Student.objects.get(pk=student_id)
    student.delete()
    return render(request, 'IITG/student_detail.html', {'professor': professor})


def student_detail(request, professor_id):
    if not request.user.is_authenticated():
        return render(request, 'IITG/login.html')
    else:
        user = request.user
        professor = get_object_or_404(Professor, pk=professor_id)
        return render(request, 'IITG/student_detail.html', {'professor': professor, 'user': user})

