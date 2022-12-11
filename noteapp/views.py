from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from . forms import NewUserForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Note

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
# Create your views here.
def home(request):
    return render (request, 'index.html')
    
class NoteList(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)
        context['count'] = context['notes'].filter(complete=False).count()
        return context

class NoteDetail(LoginRequiredMixin, DetailView):
    model = Note
    context_object_name = 'note'
    template_name = 'noteapp/note_detail.html'

class NoteCreate(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title','content', 'complete']
    template_name = 'noteapp/note_form.html'
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NoteCreate, self).form_valid(form)

class NoteUpdate(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ['title', 'content', 'complete']
    success_url = reverse_lazy('notes')

class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    context_object_name  = 'note'
    template_name = 'noteapp/note_delete.html'
    success_url = reverse_lazy('notes')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('notes')

class RegisterPage(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    fields = '__all__'

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
        messages(request, f'{user}You have successfully created an account, start creating your note')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterPage, self).get(*args, **kwargs)
