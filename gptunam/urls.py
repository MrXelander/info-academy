from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('recovery', views.recovery, name="recovery"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('welcome', views.initialtest, name="initialtest"),
    path('editinitialtest', views.editinitialtest, name="editinitialtest"),
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
    path('<uuid:codigo>', views.subjectopic, name='subjectopic'),
    path('<uuid:codigo>/add', views.inscripcion, name='inscripcion'),
    path('<uuid:codigo>/rm', views.baja, name='baja'),
    path('<uuid:codigo>/<int:tema_id>/add', views.addsubtopic, name='addsubtopic'),
    path('<uuid:codigo>/<int:tema_id>/add/material', views.addMaterial, name='addmaterial'),
    path('<uuid:codigo>/<int:tema_id>/add/video', views.addVideo, name='addvideo'),
    path('subject/<int:materia_id>/topic/<int:tema_id>/subtopic/list', views.usersubtopics, name='usersubtopics'),
    path('<uuid:codigo>/<int:tema_id>/v/<int:subtema_id>', views.video, name='video'),
    path('<uuid:codigo>/<int:tema_id>/d/<int:subtema_id>', views.document, name='document'),
    path('<uuid:codigo>/<int:tema_id>/d/<int:subtema_id>/<int:doc_id>', views.openpdf, name='openpdf'),
    path('<uuid:codigo>/<int:tema_id>/e/<int:subtema_id>', views.evaluationq, name='evaluationq'),
    path('chatbot_endpoint/<int:tokens>/', views.chatbot_endpoint, name='chatbot_endpoint'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)