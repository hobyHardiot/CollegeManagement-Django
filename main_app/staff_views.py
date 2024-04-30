import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def staff_home(request):
    staff = get_object_or_404(Staff, admin=request.user)
    total_students = Student.objects.filter(course=staff.course).count()
    total_leave = LeaveReportStaff.objects.filter(staff=staff).count()
    subjects = Subject.objects.filter(staff=staff)
    total_subject = subjects.count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name)
        attendance_list.append(attendance_count)
    context = {
        'page_title': 'Staff Panel - ' + str(staff.admin.last_name) + ' (' + str(staff.course) + ')',
        'total_students': total_students,
        'total_attendance': total_attendance,
        'total_leave': total_leave,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list
    }
    return render(request, 'staff_template/home_content.html', context)
   
 
 

def staff_feedback(request):
    form = FeedbackStaffForm(request.POST or None)
    staff = get_object_or_404(Staff, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackStaff.objects.filter(staff=staff),
        'page_title': 'Add Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.staff = staff
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('staff_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "staff_template/staff_feedback.html", context)


def staff_view_profile(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = StaffEditForm(request.POST or None, request.FILES or None,instance=staff)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = staff.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                staff.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('staff_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "staff_template/staff_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "staff_template/staff_view_profile.html", context)

    return render(request, "staff_template/staff_view_profile.html", context)


@csrf_exempt
def staff_fcmtoken(request):
    token = request.POST.get('token')
    try:
        staff_user = get_object_or_404(CustomUser, id=request.user.id)
        staff_user.fcm_token = token
        staff_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")
 

def staff_view_groupe(request): 
    prerequisGroupes = PrerequisGroupe.objects.all()
    context = {
        'prerequisGroupes': prerequisGroupes,
        'page_title': 'Manage Groupe'
    }
    return render(request, "staff_template/manage_groupe.html", context)


def staff_add_groupe(request):
    if request.method == 'POST':
        form = PrerequisGroupeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Successfully Added")
                return redirect('staff_view_groupe')
             
            except Exception as e:
                messages.error(request, "Could Not Add" + str(e))
    else:
        form = PrerequisGroupeForm()
    return render(request, 'staff_template/add_groupe_template.html', {'form': form})



def manage_project(request): 
    projects = Projet.objects.all()
    context = {
        'projects': projects,
        'page_title': 'Manage projects'
    }
    return render(request, "staff_template/manage_project.html", context)


def add_project(request):
    form = ProjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add project'
    }
    if request.method == 'POST':
        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            description = form.cleaned_data.get('description')
            try:
                project = Projet()
                project.nom = nom
                project.description = description
                project.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('manage_project'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'staff_template/add_project_template.html', context)


def edit_project(request, project_id):
    project = get_object_or_404(Projet, id=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    context = {
        'form': form,
        'project_id': project_id,
        'page_title': 'Edit project'
    }
    if request.method == 'POST':
        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            description = form.cleaned_data.get('description') 
            try: 
                project.nom = nom
                project.description = description 
                project.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('manage_project'))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "staff_template/edit_project_template.html", context)
    

def delete_project(request, project_id):
    project = get_object_or_404(Projet, id=project_id)
    try:
        project.delete()
        messages.success(request, "Project deleted successfully!")
    except Exception:
        messages.error(
            request, "Sorry, try again")
    return redirect(reverse('manage_project'))

