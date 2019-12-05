# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import date
from .validations import validate_file_extension

import datetime, os

from django.core.files.storage import FileSystemStorage

# Create your models here.

PREFIX_CHOICES = (
    ('MR', 'MR'),
    ('MRS', 'MRS'),
    ('MS', 'MS'),
    ('MX', 'MX')
)

RATING_CHOICES = [(i,i) for i in range(1,6)]

EXPERIENCE_CHOICES = [(str(i),str(i)) for i in range(51)]

BUDGET_CHOICES = [(str(i),str(i)) for i in range(101)]

QUALIFICATION_CHOICES = (
    ('UG', 'UNDER GRADUATE'),
    ('G', 'GRADUATE'),
    ('PG', 'POST GRADUATE'),
    ('PhD', 'PhD'),
)

GENDER_CHOICES = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
)

def change_file_path(instance, filename):
    ''' This function generates a random string of length 16 which will be a combination of (4 digits + 4
    characters(lowercase) + 4 digits + 4 characters(uppercase)) seperated 4 characters by hyphen(-) '''

    import random
    import string

    # random_str length will be 16 which will be combination of (4 digits + 4 characters + 4 digits + 4 characters)

    filetype = filename.split(".")[-1].lower()
    filename = filename + "." + filetype
    path = "IungoClientDashboard/uploads/" + str(datetime.datetime.now().year) + "/" + str(
        datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day) + "/"
    os_path = os.path.join(path, filename)
    return os_path

def content_file_name(instance, filename):
    ''' This function generates a random string of length 16 which will be a combination of (4 digits + 4
    characters(lowercase) + 4 digits + 4 characters(uppercase)) seperated 4 characters by hyphen(-) '''

    import random
    import string

    # random_str length will be 16 which will be combination of (4 digits + 4 characters + 4 digits + 4 characters)

    filetype = filename.split(".")[-1].lower()
    filename = filename
    path = "uploads/" + str(instance.user)
    os_path = os.path.join(path, filename)
    return os_path

class ConfirmationCode(models.Model):

    user = models.ForeignKey(User, default=True, on_delete=models.CASCADE)
    confirmation_code = models.CharField(verbose_name="Confirmation Code", max_length=100, blank=False, null=False,
                                         unique=True)

    def __unicode__(self):
        return u'{0}'.format(
            self.confirmation_code)

class Category(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50)

    def __unicode__(self):
        return self.name

class sub_category(models.Model):
    name = models.CharField(verbose_name="Name", max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

class child_sub_category(models.Model):
    name = models.CharField(verbose_name="Name", max_length=30)
    sub_category = models.ForeignKey(sub_category, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'{0}'.format(self.name)

class Design(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design_type = models.ForeignKey(child_sub_category, on_delete=models.CASCADE)
    design_name = models.CharField(verbose_name="Design project Name", max_length=30)
    design_images = models.FileField(upload_to=content_file_name, blank=True, null=True, verbose_name="Design Images")

    def __unicode__(self):
        return u'{0}'.format(self.design_name)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_type = models.ForeignKey(child_sub_category, on_delete=models.CASCADE)
    project_name = models.CharField(verbose_name="Project Name", max_length=30)
    project_images = models.FileField(upload_to=content_file_name, blank=True, null=True, verbose_name="Project Images")

    def __unicode__(self):
        return u'{0}'.format(self.project_name)


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.CharField(verbose_name="Experience", max_length=10, choices=EXPERIENCE_CHOICES, blank=False,
                                  null=False)
    qualification = models.CharField(verbose_name="Qualification", max_length=20, choices=QUALIFICATION_CHOICES,
                                     blank=False, null=False)
    budget = models.CharField(verbose_name="Budget", max_length=20, choices=BUDGET_CHOICES)
    prefix = models.CharField(verbose_name="Prefix", max_length=3, choices=PREFIX_CHOICES)
    gender = models.CharField(verbose_name="Gender", max_length=10, choices=GENDER_CHOICES)
    mobile_phone = models.CharField(verbose_name="Mobile phone", max_length=10, unique=True, blank=False, null=True)
    secondary_phone = models.CharField(verbose_name="Secondary phone", max_length=10, unique=True, blank=False,
                                       null=True)
    tel_phone = models.CharField(verbose_name="Tele phone", max_length=10, unique=True, blank=False,
                                       null=True)
    date_of_birth = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    about_me = models.CharField(verbose_name="About me ", blank=True, max_length=250)
    profile_pic = models.ImageField(upload_to=content_file_name, blank=True, null=True, verbose_name="Profile Picture")
    location = models.CharField(verbose_name="location", max_length=30)
    client = models.BooleanField(verbose_name="Client", default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(sub_category, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'{0}'.format(self.user)

@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    if created:
        category = Category.objects.get(id=1)
        subcategory = sub_category.objects.get(id=1)
        Portfolio.objects.create(user=instance, category=category, sub_category=subcategory)

@receiver(post_save, sender=User)
def save_client_profile(sender, instance, **kwargs):
    instance.portfolio.save()


class WalkinCustomer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=30)
    email = models.EmailField(verbose_name="email", max_length=70, blank=True)
    mobile_phone = models.CharField(verbose_name="Mobile phone", max_length=10, unique=True, blank=False, null=True)
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Appointment(models.Model):
    user = models.ForeignKey(User, related_name="client_appointment", on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name="customer_appointment", on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Status', default=False)
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.user)

class DeisgnUploads(models.Model):
    user = models.ForeignKey(User, related_name="client_designs", on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name="customer_designs", on_delete=models.CASCADE)
    design_type = models.ForeignKey(child_sub_category, on_delete=models.CASCADE)
    design_name = models.CharField(verbose_name="Design project Name", max_length=30)
    design_images = models.FileField(upload_to=content_file_name)
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.user)

class InvoicesProposalsUploads(models.Model):
    user = models.ForeignKey(User, related_name="client_invoice_and_proposals", on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name="customer_invoice_and_proposals", on_delete=models.CASCADE)
    invoices = models.FileField(upload_to=change_file_path, validators=[validate_file_extension], verbose_name="Invoices")
    proposals = models.FileField(upload_to=change_file_path, validators=[validate_file_extension], verbose_name="Proposals")
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.user)

class AppointmentScheduler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slots_booked = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'{0}'.format(self.user)

class FeedBackRating(models.Model):
    user = models.ForeignKey(User, related_name="client_feedback", on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name="Customer_feedback", on_delete=models.CASCADE)
    feedback = models.CharField(verbose_name="Feedback", max_length=250)
    rating = models.CharField(verbose_name="rating", max_length=5, choices=RATING_CHOICES)
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.user)

class Parameters(models.Model):
    user = models.ForeignKey(User, related_name="client", on_delete=models.CASCADE)
    clicks = models.CharField(verbose_name="clicks", max_length=10)
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.user)

