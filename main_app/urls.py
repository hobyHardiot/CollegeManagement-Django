"""django-sneat-gestion-projet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from main_app.EditResultView import EditResultView

from . import hod_views, staff_views, student_views, views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("staff/add", hod_views.add_staff, name='add_staff'),



    path("students/manage", hod_views.manage_students, name='manage_students'), 
    path("students/add", hod_views.add_students, name='add_students'),
    path("students/edit/<int:students_id>", hod_views.edit_students, name='edit_students'),
    path("students/delete/<int:students_id>", hod_views.delete_students, name='delete_students'),




 


    path("course/add", hod_views.add_course, name='add_course'),
    path("send_student_notification/", hod_views.send_student_notification,
         name='send_student_notification'),
    path("send_staff_notification/", hod_views.send_staff_notification,
         name='send_staff_notification'),
    path("add_session/", hod_views.add_session, name='add_session'),
    path("admin_notify_student", hod_views.admin_notify_student,
         name='admin_notify_student'),
    path("admin_notify_staff", hod_views.admin_notify_staff,
         name='admin_notify_staff'),
    path("admin_view_profile", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("admin_edit_profile", hod_views.admin_edit_profile,
         name='admin_edit_profile'),

    path("check_email_availability", hod_views.check_email_availability,
         name="check_email_availability"),
    path("session/manage/", hod_views.manage_session, name='manage_session'),
    path("session/edit/<int:session_id>",
         hod_views.edit_session, name='edit_session'),
    path("student/view/feedback/", hod_views.student_feedback_message,
         name="student_feedback_message",),
    path("staff/view/feedback/", hod_views.staff_feedback_message,
         name="staff_feedback_message",),
    path("student/view/leave/", hod_views.view_student_leave,
         name="view_student_leave",),
    path("staff/view/leave/", hod_views.view_staff_leave, name="view_staff_leave",),
    path("attendance/view/", hod_views.admin_view_attendance,
         name="admin_view_attendance",),
    path("attendance/fetch/", hod_views.get_admin_attendance,
         name='get_admin_attendance'),
    path("student/add/", hod_views.add_student, name='add_student'),
    path("subject/add/", hod_views.add_subject, name='add_subject'),
    path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
    path("student/manage/", hod_views.manage_student, name='manage_student'),
    path("course/manage/", hod_views.manage_course, name='manage_course'),
    path("subject/manage/", hod_views.manage_subject, name='manage_subject'),
    path("staff/edit/<int:staff_id>", hod_views.edit_staff, name='edit_staff'),
    path("staff/delete/<int:staff_id>",
         hod_views.delete_staff, name='delete_staff'),

    path("course/delete/<int:course_id>",
         hod_views.delete_course, name='delete_course'),

    path("subject/delete/<int:subject_id>",
         hod_views.delete_subject, name='delete_subject'),

    path("session/delete/<int:session_id>",
         hod_views.delete_session, name='delete_session'),

    path("student/delete/<int:student_id>",
         hod_views.delete_student, name='delete_student'),
    path("student/edit/<int:student_id>",
         hod_views.edit_student, name='edit_student'),
    path("course/edit/<int:course_id>",
         hod_views.edit_course, name='edit_course'),
    path("subject/edit/<int:subject_id>",
         hod_views.edit_subject, name='edit_subject'),


    # Staff
    path("staff/home/", staff_views.staff_home, name='staff_home'), 
    path("staff/feedback/", staff_views.staff_feedback, name='staff_feedback'),
    path("staff/view/profile/", staff_views.staff_view_profile, name='staff_view_profile'),    
    path("staff/edit/profile/", staff_views.staff_edit_profile, name='staff_edit_profile'),    

    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'), 
    path("staff/groupe/view", staff_views.staff_view_groupe, name='staff_view_groupe'),  
    path("staff/groupe/add", staff_views.staff_add_groupe, name='staff_add_groupe'),
    path("staff/groupe/delete/<int:prerequisgroupe_id>", staff_views.delete_prerequis_groupe, name='delete_prerequis_groupe'),

    path("staff/groupe/manage_2/<int:prerequisGroupe_id>", staff_views.show_groupe_by_prerequisId, name='show_groupe_by_prerequisId'), 

    path("staff/project/manage", staff_views.manage_project, name='manage_project'), 
    path("staff/project/add", staff_views.add_project, name='add_project'),
    path("staff/project/edit/<int:project_id>", staff_views.edit_project, name='edit_project'),
    path("staff/project/delete/<int:project_id>", staff_views.delete_project, name='delete_project'),

    path("staff/groupe/assign", staff_views.assign_project, name='assign_project'),
    path("staff/groupe/delivre/<int:prerequisGroupe_id>", staff_views.delivre_project, name='delivre_project'),
    path("staff/groupe/assign2/<int:prerequisGroupe_id>", staff_views.assign_project_manytoone, name='assign_project_manytoone'),

    # Student
    path("student/home/", student_views.student_home, name='student_home'),  
    path("student/feedback/", student_views.student_feedback,
         name='student_feedback'),
    path("student/view/profile/", student_views.student_view_profile,
         name='student_view_profile'),
    path("student/edit/profile/", student_views.student_edit_profile,
         name='student_edit_profile'),
    path("student/fcmtoken/", student_views.student_fcmtoken,
         name='student_fcmtoken'),  

    path("student/lists/", student_views.view_students, name='view_students'),

    path("groupe/manage", student_views.manage_groupe, name='manage_groupe'), 
    path("groupe/manage_2/<int:prerequisGroupe_id>", student_views.show_groupe_by_prerequisId, name='show_groupe_by_prerequisId'), 
    path("groupe/manage_3/<int:prerequisGroupe_id>", student_views.manage_groupe_form, name='manage_groupe_form'), 
    path("groupe/manage_4/<int:prerequisGroupe_id>", student_views.getGroupeByPrerequisId, name='getGroupeByPrerequisId'), 
    path("groupe/add", student_views.add_groupe, name='add_groupe'),
    path("groupe/edit/<int:groupe_id>", student_views.edit_groupe, name='edit_groupe'),
    path("groupe/delivre/<int:prerequisGroupe_id>", student_views.delivre_groupe, name='delivre_groupe'),

    path("groupe/share/<int:prerequisGroupe_id>", student_views.share_groupe,  {'generate_pdf': True}, name='share_groupe'), 
]
