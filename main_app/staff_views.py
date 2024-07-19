import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *
import random


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
        'page_title': 'Home',
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
def staff_edit_profile(request):
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

    return render(request, "staff_template/staff_edit_profile.html", context)


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
    prerequisGroupes = PrerequisGroupe.objects.filter(author=request.user)
    context = {
        'prerequisGroupes': prerequisGroupes,
        'page_title': 'Manage Groupe'
    }
    return render(request, "staff_template/manage_groupe.html", context)


def staff_add_groupe(request):
    levels = Course.objects.all()
    context = {  
        'levels' : levels
    }  
    if request.method == 'POST':  
        module = request.POST['module']
        niveau_id = request.POST['niveau'] 
        start_date = request.POST['start_date'] 
        end_date = request.POST['end_date'] 
        description = request.POST['description']
        try:
            niveau = Course.objects.get(id=niveau_id)
            prerequisGroupe = PrerequisGroupe() 


            prerequisGroupe.module = module
            prerequisGroupe.start_date = start_date
            prerequisGroupe.end_date = end_date
            prerequisGroupe.description = description
            prerequisGroupe.author = request.user
            prerequisGroupe.status = -1
            prerequisGroupe.niveau = niveau 
            prerequisGroupe.save()
            messages.success(request, "Successfully Added")
            print("Successfully Added")
            return JsonResponse({'success': 'Added successfully'})
            
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Une erreur est survenue'})  
    return render(request, 'staff_template/add_groupe_template.html', context)

def delete_prerequis_groupe(request, prerequisgroupe_id):
    prerequisgroupe = get_object_or_404(PrerequisGroupe, id=prerequisgroupe_id)
    try:
        prerequisgroupe.delete()
        messages.success(request, "deleted successfully!")
    except Exception:
        messages.error(
            request, "Sorry, try again")
    return redirect(reverse('staff_view_groupe'))


def manage_project(request): 
    projects = Projet.objects.filter(author=request.user)
    context = {
        'projects': projects,
        'page_title': 'Manage projects'
    }
    return render(request, "staff_template/manage_project.html", context)


def show_groupe_by_prerequisId(request, prerequisGroupe_id): 

    groupes = Groupe.objects.filter(prerequisGroupe = prerequisGroupe_id)
    context = {
        'groupes':groupes, 
    }
    print(prerequisGroupe_id)
    return render(request, "staff_template/manage_groupe_2.html",context)

def add_project(request): 
    context = { 
        'page_title': 'Add project'
    }
    if request.method == 'POST': 
        nom = request.POST['nom']
        description = request.POST['description']
        try:
            project = Projet()
            project.nom = nom
            project.description = description
            project.author = request.user
            project.save()
            print("Successfully Added")
            return JsonResponse({'success': 'Added successfully'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Une erreur est survenue'})  
    return render(request, 'staff_template/add_project_template.html', context)


def edit_project(request, project_id):
    project = get_object_or_404(Projet, id=project_id) 
    context = { 
        'project_id': project_id,
        'page_title': 'Edit project',
        'project' : project
    }
    if request.method == 'POST': 
        nom = request.POST['nom']
        description = request.POST['description']
        try:
            project.nom = nom
            project.description = description
            project.author = request.user
            project.save()
            print("Successfully Added")
            return JsonResponse({'success': 'Successfully'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Une erreur est survenue'})  
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


def assign_project(request): 
    groupes = list(Groupe.objects.filter(prerequisGroupe = 1))
    projets = list(Projet.objects.filter(id = 1))
    students = Students.objects.all()
    context = {
        'students': students,
        'page_title': 'Manage Groupe'
    }

    random.shuffle(projets)
    for i, groupe in enumerate(groupes):
        # Assigner le projet au groupe
        groupe.projet = projets[i]
        groupe.save()

    return render(request, "staff_template/manage_groupe.html", context)


def delivre_project(request, prerequisGroupe_id): 

    prerequisGroupe = get_object_or_404(PrerequisGroupe, id=prerequisGroupe_id) 
 
    if request.method == 'GET':   
        prerequisGroupe.status = 0 
        prerequisGroupe.save()
        return JsonResponse({'message': 'Saved'}) 
    
    return JsonResponse({'message': 'No modification'}) 


def assign_project_manytoone(request, prerequisGroupe_id): 
    groupes = Groupe.objects.filter(prerequisGroupe = prerequisGroupe_id) 
    projets = list(Projet.objects.all())
    
    # Vérification du nombre de projets par rapport au nombre de groupes
    if len(projets) > len(groupes):
        # Chaque groupe a son propre projet
        for groupe in groupes:
            projet_aleatoire = random.choice(list(projets))  # Sélectionner un projet aléatoire sans le retirer de la liste
            groupe.projet = projet_aleatoire
            groupe.save()
            projets.remove(projet_aleatoire)  # Retirer le projet attribué de la liste des projets disponibles
    else:
        # Plusieurs groupes peuvent partager le même projet
        for groupe in groupes:
            projet_aleatoire = random.choice(list(projets))  # Sélectionner un projet aléatoire sans le retirer de la liste
            groupe.projet = projet_aleatoire
            groupe.save()
    
    context = {
        'students': Students.objects.all(),
        'page_title': 'Manage Groupe',
        'groupes': groupes,
    } 
    
    try:
        print("Successfully Added")
        return render(request, "staff_template/manage_groupe_2.html", context)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Une erreur est survenue'})