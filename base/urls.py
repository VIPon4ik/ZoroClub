from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('announcment/<str:pk>', views.announcment, name='announcment'),
    path('create-announcment/', views.createAnnouncment, name='create-announcment'),
    path('update-announcment/<str:pk>', views.updateAnnouncment, name='update-announcment'),
    path('delete-announcment/<str:pk>', views.deleteAnnouncment, name='delete-announcment'),

    path('registration/', views.registerPage, name='registration'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('profile/<str:pk>',views.profilePage, name='profile'),
    path('edit-profile/', views.editProfile, name='edit-profile'),

    path('favorites',views.favoritesPage, name='favorites'),
    path('favorites/<str:pk>',views.favoritesAdd, name='add-favorites'),
    path('delete-favorites/<str:pk>',views.favoritesDelete, name='delete-favorites'),

    path('chat/', views.chatPanel, name='chat-panel'),
    path('create-chat/<str:user_id>', views.createChat, name='create-chat'),
    path('chat/<str:pk>', views.chatPage, name='chat-page'),
]
