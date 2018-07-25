from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User
# from datetime import datetime


"""class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mail = models.EmailField(max_length=150)
    password = models.CharField(max_length=50, default='IITG')  #
    Pro_pic = models.ImageField(upload_to="", default='/pro_pic.png')

#    @property
    def __str__(self):
        return self.first_name + ' ' + self.last_name
"""


class Dept(models.Model):
    Dept_name = models.CharField(max_length=100)
    Dept_detail = models.TextField

    def __str__(self):
        return self.Dept_name


class Desgn(models.Model):
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.position


class Professor(models.Model):
    user = models.ForeignKey(User, default=1)
    pro_pic = models.ImageField(upload_to="", default='/pro_pic.png')
    Department = models.ForeignKey(Dept, on_delete=models.CASCADE)
    designation = models.ForeignKey(Desgn, on_delete=models.CASCADE)
    phone_no = models.IntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)])
    room_no = models.CharField(max_length=10)
    visit_time = models.TimeField()
    Research_Interests = models.TextField(max_length=1000, default='')
    Biography = models.TextField(default='')

    def get_absolute_url(self):                                                 ###
        return reverse('IITG:prof_detail', kwargs={'pk': self.pk})          ###

    def clean_fields(self, exclude=None):
        if self.phone_no < 1000000000:
            raise ValidationError({'phone_no': [" must be a 10-digit number"]})
        if 9999999999 < self.phone_no:
            raise ValidationError({'phone_no': [" must be a 10-digit number"]})

    def __str__(self):
        return self.user.__str__()


class Course(models.Model):
    prof = models.ForeignKey(Professor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    Dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    no = models.CharField(max_length=8)
    # credits = models.IntegerField
    # start_year = models.IntegerField
    # end_year = models.IntegerField

#    def get_absolute_url(self):
#        return reverse('IITG:prof_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.no


class Education(models.Model):
    prof = models.ForeignKey(Professor, on_delete=models.CASCADE)
    degree = models.CharField(max_length=8)
    field = models.CharField(max_length=100)
    University = models.CharField(max_length=100)
    Year = models.CharField(max_length=6)

#    def get_absolute_url(self):
#        return reverse('IITG:prof_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.degree


class Experience(models.Model):

    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    # Title = models.CharField(max_length=150)
    Detail = models.TextField()
    Institution = models.CharField(max_length=100)
    start_Year = models.CharField(max_length=10)
    end_Year = models.CharField(max_length=10)

#    def get_absolute_url(self):
#        return reverse('IITG:prof_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.start_Year


class Recognition(models.Model):
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Detail = models.TextField()
    Year = models.IntegerField

#    def get_absolute_url(self):
#        return reverse('project:prof_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.Name


class Publication(models.Model):
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    Name = models.CharField(max_length=150)
    Detail = models.TextField()
    Date = models.DateField()

#    def get_absolute_url(self):
#        return reverse('IITG:prof_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.Name


class Projects(models.Model):
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Detail = models.TextField()
    start_Year = models.CharField(max_length=10)
    end_Year = models.CharField(max_length=10)
    # start_year = models.DateField()
    # end_year = models.DateField()

#    def get_absolute_url(self):
#        return reverse('IITG:prof_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.Title


class Student(models.Model):
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    degree = models.CharField(max_length=8)
    Detail = models.TextField()

#    def get_absolute_url(self):
#        return reverse('IITG:prof_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.Name
