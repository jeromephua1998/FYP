from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dogs/', views.dog_list, name='dog_list'),

    path('cats/', views.cat_list, name='cat_list'),

    path('registration/', views.register, name='registration'),

    path('home/', views.home, name='home'),

    path('login/', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),

    path('dogregister/', views.dogregister, name='dogregister'),

    path('catregister/', views.catregister, name='catregister'),

    path('pet/<int:id>/', views.petdesc, name='petdesc'),

    path('pet2/<int:id>/', views.catdesc, name='catdesc'),

    path('createevents/', views.createevents, name='createevents'),
    
    path('viewevents/', views.view_events, name='view_events'),

    path('events/<int:eventid>/', views.eventsview, name='eventsview'),

    path('events/<int:eventid>/edit/', views.editevent, name='edit_event'),

    path('events/<int:eventid>/delete/', views.deleteevents, name='delete_event'),

    path('pets/<int:pet_id>/createmeeting/', views.createmeeting, name='createmeeting'),

    path('viewmeetings/', views.viewmeeting, name='viewmeeting'),

    path('editprofile/', views.editprofile, name='editprofile'),

    path('donation/', views.donation, name='donation'),

    path('faq/', views.faqview, name='faq'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

