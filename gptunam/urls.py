from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('recovery', views.recovery, name="recovery"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.user_logout, name="logout"),
    path('edit_account', views.edit_account, name="edit_account"),
    path('subjects', views.subjects, name="subjects"),
    path('subjects/delete/<int:materia_id>/', views.delete_subject, name='delete_subject'),
    path('subjects/<int:materia_id>/topics', views.topics, name="topics"),
    path('subjects/<int:materia_id>/topics/delete/<int:tema_id>/', views.delete_topic, name='delete_topic'),
    path('subjects/<int:materia_id>/topics/<int:tema_id>/subtopics', views.subtopics, name="subtopics"),
    path('subjects/<int:materia_id>/topics/<int:tema_id>/subtopics/delete/<int:subtema_id>', views.delete_subtopic, name='delete_subtopic'),
    path('subjects/<int:materia_id>/topics/<int:tema_id>/subtopics/edit/<int:subtema_id>', views.edit_subtopic, name='edit_subtopic'),
    path('subjects/<int:materia_id>/topics/<int:tema_id>/subtopics/new', views.new_subtopic, name='new_subtopic'),
    path('student/subjects', views.subjectstudent, name="subjectstudent"),
    path('users', views.users, name="users"),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('subject/<int:materia_id>/list', views.subjectopic, name='subjectopic'),
    path('subject/<int:materia_id>/topic/<int:tema_id>/subtopic/list', views.usersubtopics, name='usersubtopics'),
    path('subject/<int:materia_id>/topic/<int:tema_id>/subtopic/<int:subtema_id>', views.practice, name='practice'),
    path('subject/<int:materia_id>/topic/<int:tema_id>/subtopic/<int:subtema_id>/video', views.video, name='video'),
]