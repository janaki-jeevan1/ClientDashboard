# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.shortcuts import render, redirect, render_to_response
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib import messages
from .forms import *
from django.template.context_processors import csrf
from django.views.generic import View
from random import randint
import re
# from .commands.sms import send_sms
import urllib
from contextlib import closing
import json

# Create your views here.

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def sms_user(number, user):
    otp = random_with_N_digits(4)

def customer_register(request):

    if request.method == "GET":
        context = {}
        context.update(csrf(request))
        context['form'] = RegistrationForm()
        return render_to_response('register.html', context)

    if request.method == 'POST':
        context = {}
        form = RegistrationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_active = 1
            obj.email = form.cleaned_data["email"]
            obj.username = form.cleaned_data["mobile_phone"]
            obj.save()
            obj.portfolio.mobile_phone = form.cleaned_data["mobile_phone"]
            obj.portfolio.client = 0
            obj.save()
            context["user"] = obj.username
            return render(request, 'customer_dashboard.html', context)
        else:
            return render(request, 'register.html', {'form':form})

def client_register(request):

    if request.method == "GET":
        context = {}
        context.update(csrf(request))
        context['form'] = RegistrationForm()
        return render_to_response('register.html', context)

    if request.method == 'POST':
        context = {}
        form = RegistrationForm(request.POST)
        import ipdb; ipdb.set_trace()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_active = 1
            obj.email = form.cleaned_data["email"]
            obj.username = form.cleaned_data["mobile_phone"]
            obj.save()
            obj.portfolio.mobile_phone = form.cleaned_data["mobile_phone"]
            obj.portfolio.client = 1
            obj.save()
            context["user"] = obj.username
            return render(request, 'client_dashboard.html', context)
        else:
            print (form.errors)
            return render(request, 'register.html', {'form':form})

def auth_view(request):
    username = request.POST.get('username','')
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    if username and password:
        user = auth.authenticate(username=username, password=password)
        try:
            userobj = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Phone number does not exist, please register and try again.')
            return render(request, 'login.html')
    elif email and password:
        user = auth.authenticate(email=email, password=password)
        try:
            userobj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email does not exist, Please register and try again.')
            return render(request, 'login.html')
    elif username and email and password:
        user = auth.authenticate(username=username, password=password)
        try:
            userobj = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Phone number or email does not exist, please register and try again.')
            return render(request, 'login.html')
    else:
        user = None
    if user is not None and userobj.is_active is True:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        messages.error(request, 'Invalid Username or password')
        return render(request,'login.html')

def client_login(request):

    if request.method == 'GET':
        context = {}
        return render(request, 'login.html', context)

    if request.method == 'POST':
        context = {}
        return render(request, 'login.html', context)

class Dashboard(View):
    template_name = "client_dashboard.html"

    def get(self, request):
        context = {}
        context['user'] = request.user
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)

def dates_to_check(start_date,end_date):
    dates = []
    delta = end_date - start_date

    for i in range(delta.days+1):
        dates.append(start_date + datetime.timedelta(days=i))
    return dates

def Overview(request):

    if request.method == 'GET':
        context = {}
        id = request.GET.get('id')
        if id:
            today = date.today()
            week_ago = today - datetime.timedelta(days=6)
            dates = dates_to_check(week_ago, today)
            final_list = []
            for date_check in dates:
                if id == "1":
                    click_dict = {}
                    no_of_clicks = Parameters.objects.filter(user=request.user, date_time=date_check)
                    clicks = []
                    if no_of_clicks > 0:
                        for i in no_of_clicks:
                            clicks.append(int(i.clicks))
                        clicks_total = sum(clicks)
                    else:
                        clicks_total = 0
                    click_dict['clicks'] = clicks_total
                    click_dict['date'] = date_check.strftime("%Y-%m-%d")
                    final_list.append(click_dict)
                if id == "2":
                    feedback_dict = {}
                    no_of_feedbacks = FeedBackRating.objects.filter(user=request.user, date_time=date_check)
                    feedback_dict['feebacks'] = len(no_of_feedbacks)
                    feedback_dict['date'] = date_check.strftime("%Y-%m-%d")
                    final_list.append(feedback_dict)
                if id == "3":
                    design_dict = {}
                    invoice_dict = {}
                    proposals_dict = {}
                    no_of_invoices = InvoicesProposalsUploads.objects.filter(user=request.user,
                                                                             date_time=date_check).values('invoices')
                    no_of_proposals = InvoicesProposalsUploads.objects.filter(user=request.user,
                                                                             date_time=date_check).values('proposals')
                    no_of_designs = DeisgnUploads.objects.filter(user=request.user, date_time=date_check)
                    design_dict['designs'] = len(no_of_designs)
                    design_dict['date'] = date_check.strftime("%Y-%m-%d")
                    invoice_dict['invoices'] = len(no_of_invoices)
                    invoice_dict['date'] = date_check.strftime("%Y-%m-%d")
                    proposals_dict['proposals'] = len(no_of_proposals)
                    proposals_dict['date'] = date_check.strftime("%Y-%m-%d")
                    final_list.append(design_dict)
                    final_list.append(invoice_dict)
                    final_list.append(proposals_dict)
                if id == "4":
                    appointment_dict = {}
                    no_of_appointment = Appointment.objects.filter(user=request.user, date_time=date_check)
                    appointment_dict['appointments'] = len(no_of_appointment)
                    appointment_dict['date'] = date_check.strftime("%Y-%m-%d")
                    final_list.append(appointment_dict)
            final_dates = []
            for date_str in dates:
                final_dates.append(date_str.strftime("%Y-%m-%d"))
            context["dates"] = json.dumps(final_dates)
            context['json_list'] = json.dumps(final_list)
            context["id"] = str(id)
            return render(request, 'overview_line_chart.html', context)
        else:
            return render(request, 'overview.html', context)

class AppointmentScheduler(View):
    template_name = "appointment_scheduler.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)

class PortfolioView(View):
    template_name = "profileSeting.html"

    def get(self, request):
        form = PortfolioForm()
        user = request.user
        return render(request, self.template_name, {'form': form, 'user': user})

    def post(self, request, id=None):
        if id:
            instance = get_object_or_404(Portfolio, id=id)
            form = PortfolioForm(request.POST, request.FILES or None, instance=instance)
            if form.is_valid():
                form.save()
                form = PortfolioForm()
        else:
            form = PortfolioForm(request.POST, request.FILES or None)
            if form.is_valid():
                form.save()
                form = PortfolioForm()

        return render(request, self.template_name, {'form': form})

def load_sub_category(request):
    category_id = request.GET.get('category')
    sub_categories = sub_category.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'sub_categories.html', {'sub_categories': sub_categories})
