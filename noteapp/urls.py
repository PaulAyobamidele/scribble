from django.urls import path
from . import views
from .views import NoteList, NoteDetail, NoteCreate, NoteUpdate,NoteDelete, RegisterPage
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    # path('register', views.register_request, name='register'),
    path('home/', NoteList.as_view(), name='notes'),
    path('note/detail/<int:pk>/', NoteDetail.as_view(), name='note'),
    path('note/create', NoteCreate.as_view(), name='note-create'),
    path('note/update/<int:pk>/', NoteUpdate.as_view(), name='note-update'),
    path('note/delete/<int:pk>/', NoteDelete.as_view(), name = 'note-delete'),
]

