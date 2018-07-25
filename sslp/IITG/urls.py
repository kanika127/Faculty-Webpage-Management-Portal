from django.conf.urls import url
from . import views

app_name = 'IITG'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^faculty/$', views.faculty, name='faculty'),
    url(r'^facultypage/$', views.faculty_page, name='faculty_page'),
    url(r'^dept_faculty/(?P<filter_by>[a-zA_Z]+)/(?P<dept_id>[0-9]+)$', views.dept_faculty, name='dept_faculty'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<professor_id>[0-9]+)/$', views.prof_detail, name='prof_detail'),
    url(r'^(?P<professor_id>[0-9]+)/details$', views.prof_detail_general, name='prof_detail_general'),
    url(r'^faculty/(?P<professor_id>[0-9]+)/$', views.prof_website, name='professor_website'),
    url(r'^(?P<professor_id>[0-9]+)/courses$', views.course_detail, name='course_detail'),
    url(r'^courses/(?P<filter_by>[a-zA_Z]+)/$', views.courses, name='courses'),
    url(r'^(?P<professor_id>[0-9]+)/create_course/$', views.create_course, name='create_course'),
    url(r'^(?P<professor_id>[0-9]+)/delete_course/(?P<course_id>[0-9]+)/$', views.delete_course, name='delete_course'),
    url(r'^(?P<professor_id>[0-9]+)/education$', views.education_detail, name='education_detail'),
    url(r'^educations/(?P<filter_by>[a-zA_Z]+)/$', views.educations, name='education'),
    url(r'^(?P<professor_id>[0-9]+)/create_education/$', views.create_education, name='create_education'),
    url(r'^(?P<professor_id>[0-9]+)/delete_education/(?P<education_id>[0-9]+)/$', views.delete_education, name='delete_education'),
    url(r'^(?P<professor_id>[0-9]+)/experiences$', views.experience_detail, name='experience_detail'),
    url(r'^experiences/(?P<filter_by>[a-zA_Z]+)/$', views.experiences, name='experiences'),
    url(r'^(?P<professor_id>[0-9]+)/create_experience/$', views.create_experience, name='create_experience'),
    url(r'^(?P<professor_id>[0-9]+)/delete_experience/(?P<experience_id>[0-9]+)/$', views.delete_experience, name='delete_experience'),
    url(r'^(?P<professor_id>[0-9]+)/projects$', views.project_detail, name='project_detail'),
    url(r'^projects/(?P<filter_by>[a-zA_Z]+)/$', views.projects, name='projects'),
    url(r'^(?P<professor_id>[0-9]+)/create_project/$', views.create_project, name='create_project'),
    url(r'^(?P<professor_id>[0-9]+)/delete_project/(?P<project_id>[0-9]+)/$', views.delete_project, name='delete_project'),
    url(r'^(?P<professor_id>[0-9]+)/publications$', views.publication_detail, name='publication_detail'),
    url(r'^publications/(?P<filter_by>[a-zA_Z]+)/$', views.publications, name='publications'),
    url(r'^(?P<professor_id>[0-9]+)/create_publication/$', views.create_publication, name='create_publication'),
    url(r'^(?P<professor_id>[0-9]+)/delete_publication/(?P<publication_id>[0-9]+)/$', views.delete_publication, name='delete_publication'),
    url(r'^(?P<professor_id>[0-9]+)/recognitions$', views.recognition_detail, name='recognition_detail'),
    url(r'^recognitions/(?P<filter_by>[a-zA_Z]+)/$', views.recognitions, name='recognitions'),
    url(r'^(?P<professor_id>[0-9]+)/create_recognition/$', views.create_recognition, name='create_recognition'),
    url(r'^(?P<professor_id>[0-9]+)/delete_recognition/(?P<recognition_id>[0-9]+)/$', views.delete_recognition, name='delete_recognition'),
    url(r'^(?P<professor_id>[0-9]+)/students$', views.student_detail, name='student_detail'),
    url(r'^students/(?P<filter_by>[a-zA_Z]+)/$', views.students, name='students'),
    url(r'^(?P<professor_id>[0-9]+)/create_student/$', views.create_student, name='create_student'),
    url(r'^(?P<professor_id>[0-9]+)/delete_student/(?P<student_id>[0-9]+)/$', views.delete_student, name='delete_student'),
    url(r'^create_professor/$', views.create_professor, name='create_professor'),
    url(r'^(?P<professor_id>[0-9]+)/delete_professor/$', views.delete_professor, name='delete_professor'),
    url(r'prof/update/(?P<pk>[0-9]+)/$', views.ProfUpdate.as_view(), name='prof_update'),                     #
]
