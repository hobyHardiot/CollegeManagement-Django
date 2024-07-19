import json
import math
from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage 
from django.forms import ValidationError
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, get_object_or_404
import pdfkit
from django.template.loader import render_to_string
from django.http import FileResponse


def student_home(request): 
    student = get_object_or_404(Student, admin=request.user)
    total_subject = Subject.objects.filter(course=student.course).count()
    total_attendance = AttendanceReport.objects.filter(student=student).count()
    total_present = AttendanceReport.objects.filter(student=student, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present/total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(course=student.course)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, student=student).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, student=student).count()
        subject_name.append(subject.name)
        data_present.append(present_count)
        data_absent.append(absent_count)
    context = { 
        'total_attendance': total_attendance,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_subject': total_subject,
        'subjects': subjects,
        'data_present': data_present,
        'data_absent': data_absent,
        'data_name': subject_name,
        'page_title': 'Student Homepage',
        'student':student

    }
    return render(request, 'student_template/home_content.html', context)

 

def student_feedback(request):
    form = FeedbackStudentForm(request.POST or None)
    student = get_object_or_404(Student, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackStudent.objects.filter(student=student),
        'page_title': 'Student Feedback',
        'student':student

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.student = student
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('student_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "student_template/student_feedback.html", context)


def student_view_profile(request):
    student = get_object_or_404(Student, admin=request.user)
    form = StudentEditForm(request.POST or None, request.FILES or None,
                           instance=student)
    context = {'form': form,
               'page_title': 'View/Edit Profile',
               'student':student
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = student.admin
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
                student.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('student_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "student_template/student_view_profile.html", context)

def student_edit_profile(request):
    student = get_object_or_404(Student, admin=request.user)
    form = StudentEditForm(request.POST or None, request.FILES or None,
                           instance=student)
    context = {'form': form,
               'page_title': 'View/Edit Profile',
               'student':student
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = student.admin
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
                student.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('student_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "student_template/student_edit_profile.html", context)


@csrf_exempt
def student_fcmtoken(request):
    token = request.POST.get('token')
    student_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        student_user.fcm_token = token
        student_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")

  

####

def view_students(request): 
    student = get_object_or_404(Student, admin=request.user)
    students = Students.objects.filter(niveau=student.course)
    context = {
        'students': students,
        'page_title': 'View students',
        'student':student
    }
    return render(request, "student_template/view_students.html", context)



def manage_groupe(request): 
    student = get_object_or_404(Student, admin=request.user)  

    prerequis_id = 1
    if request.method == 'POST':
        prerequis_id = int(request.POST.get('prerequisGroupe'))
        print(prerequis_id)
        etudiants_sans_groupe = Students.objects.filter(niveau=student.course).exclude(groupeetudiant__prerequisGroupe=prerequis_id)
        etudiants_sans_groupe_list = list(etudiants_sans_groupe.values()) 
        return JsonResponse({'etudiants_sans_groupe': etudiants_sans_groupe_list})
        

    prerequisGroupes = PrerequisGroupe.objects.filter(niveau=student.course)
    students = Students.objects.filter(niveau=student.course)   
    etudiants_sans_groupe = Students.objects.filter(niveau=student.course).exclude(groupeetudiant__prerequisGroupe=prerequis_id)
   
        
    context = {
        'students': students,
        'page_title': 'Manage Groupe',
        'student':student,  
        'etudiants_sans_groupe': etudiants_sans_groupe, 
        'prerequisGroupes': prerequisGroupes,

    }
    return render(request, "student_template/manage_groupe.html", context)

def show_groupe_by_prerequisId(request, prerequisGroupe_id):
    student = get_object_or_404(Student, admin=request.user) 

    prerequisGroupes = PrerequisGroupe.objects.filter(id=prerequisGroupe_id)

    etudiants_sans_groupe = Students.objects.filter(niveau=student.course).exclude(groupeetudiant__prerequisGroupe=prerequisGroupe_id)

    groupes = Groupe.objects.filter(niveau = student.course, prerequisGroupe = prerequisGroupe_id)
    context = {
        'groupes':groupes,
        'etudiants_sans_groupe': etudiants_sans_groupe, 
        'prerequisGroupes': prerequisGroupes.first(),
    }
    print(prerequisGroupes)
    return render(request, "student_template/manage_groupe_2.html",context)

def manage_groupe_form(request, prerequisGroupe_id):
    student = get_object_or_404(Student, admin=request.user) 

    etudiants_sans_groupe = Students.objects.filter(niveau=student.course).exclude(groupeetudiant__prerequisGroupe=prerequisGroupe_id)
    etudiants_sans_groupe_list = list(etudiants_sans_groupe.values()) 
    
    context = { 
        'etudiants_sans_groupe': etudiants_sans_groupe_list, 
    }
    if request.method == 'POST':  
        numero = request.POST['numero']
        niveau = student.course
        prerequisGroupe_id = int(prerequisGroupe_id)
        etudiants = request.POST.getlist('etudiants')
        try:   
            prerequisGroupe_instance = get_object_or_404(PrerequisGroupe, id=prerequisGroupe_id)

            groupe = Groupe(numero=numero, niveau=niveau, prerequisGroupe=prerequisGroupe_instance)
            groupe.save()
 
            for etudiant_id in etudiants:
                etudiant = get_object_or_404(Students, numMattr=etudiant_id)
                try:
                    groupe_etudiant = GroupeEtudiant(groupe=groupe, etudiant=etudiant, prerequisGroupe=prerequisGroupe_instance)
                    groupe_etudiant.save()
                    print(etudiant)    
                except Exception as e: 
                    print("erreur" + e) 
                
            return JsonResponse(context)
        except Exception as e:
            print("Could Not Add" + str(e)) 
            return JsonResponse({'error': 'Une erreur est survenue'}, status=500)
    else: 
        return JsonResponse(context)

def getGroupeByPrerequisId(request, prerequisGroupe_id):
    student = get_object_or_404(Student, admin=request.user) 

    etudiants_sans_groupe = Students.objects.filter(niveau=student.course).exclude(groupeetudiant__prerequisGroupe=prerequisGroupe_id)

    groupes = Groupe.objects.filter(niveau = student.course, prerequisGroupe = prerequisGroupe_id)
    
    etudiants_sans_groupe_list = list(etudiants_sans_groupe.values())
    groupes_list = list(groupes.values())
    
    context = {
        'groupes': groupes_list,
        'etudiants_sans_groupe': etudiants_sans_groupe_list, 
    }
    return JsonResponse(context)

def add_groupe(request):
    connected_student = get_object_or_404(Student, admin=request.user)  
    form = GroupeForm(request.POST or None)
    if request.method == 'POST': 
        if form.is_valid():
            try: 
                groupe = Groupe()
                groupe.numero = form.cleaned_data.get('numero')
                groupe.niveau = connected_student.course
                groupe.save()

                etudiants_ids = form.cleaned_data.get('etudiants')
                groupe.etudiants.set(etudiants_ids) 

                messages.success(request, "Successfully Added")
                return redirect('manage_groupe')
             
            except Exception as e:
                print("Could Not Add" + str(e))
    else:
        form = GroupeForm()
    return render(request, 'student_template/add_groupe_template.html', {'form': form})

 
def edit_groupe(request, groupe_id):
    groupe = get_object_or_404(Groupe, id=groupe_id)
    form = GroupeForm(request.POST or None, instance=groupe)
    context = {
        'form': form,
        'groupe_id': groupe_id,
        'page_title': 'Edit groupe'
    }
    if request.method == 'POST':
        if form.is_valid(): 

            try:  
                groupe.numero = form.cleaned_data.get('numero') 
                groupe.save()


                etudiants_ids = form.cleaned_data.get('etudiants')
                groupe.etudiants.set(etudiants_ids) 

                messages.success(request, "Successfully Updated")
                return redirect(reverse('manage_groupe'))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "student_template/edit_groupe_template.html", context)

def delivre_groupe(request, prerequisGroupe_id): 
    student = get_object_or_404(Student, admin=request.user)  

    prerequisGroupe = get_object_or_404(PrerequisGroupe, id=prerequisGroupe_id) 
 
    if request.method == 'GET':   
        prerequisGroupe.status = 1 
        prerequisGroupe.save()
        return JsonResponse({'message': 'Saved'}) 
    
    return JsonResponse({'message': 'No modification'}) 



def share_groupe(request, prerequisGroupe_id, generate_pdf=False):
    student = get_object_or_404(Student, admin=request.user) 

    prerequisGroupes = PrerequisGroupe.objects.filter(id=prerequisGroupe_id)

    etudiants_sans_groupe = Students.objects.filter(niveau=student.course).exclude(groupeetudiant__prerequisGroupe=prerequisGroupe_id)

    groupes = Groupe.objects.filter(niveau = student.course, prerequisGroupe = prerequisGroupe_id)
    
    # Generate PDF if requested
    if generate_pdf:
        html_content = render_to_string("student_template/PDF.html", {'groupes': groupes, 'etudiants_sans_groupe': etudiants_sans_groupe, 'prerequisGroupes': prerequisGroupes.first()})
        pdfkit.from_string(html_content, 'out.pdf')
        return FileResponse(open('out.pdf', 'rb'), content_type='application/pdf')

    context = {
        'groupes':groupes,
        'etudiants_sans_groupe': etudiants_sans_groupe, 
        'prerequisGroupes': prerequisGroupes.first(),
    }
    return render(request, "student_template/PDF.html",context)