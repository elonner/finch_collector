from typing import Any
import uuid
import boto3
import os
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch, Toy, Photo
from .forms import FeedingForm


 # Create your views here.
def about(request):
    return render(request, 'about.html')

class FinchList(ListView):
    template_name = 'finches/index.html'
    context_object_name = 'finches'

    def get_queryset(self):
        return Finch.objects.filter(user=self.request.user)

class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = ['name', 'species', 'island']
    #success_url = '/finches/{finch_id}' # not sure if this works but get_absolute_url method takes care of it

    # override the form_valid method to assign the logged in user, self.request.user
    def form_valid(self, form):
        form.instance.user = self.request.user # form.instance is the finch
        return super().form_valid(form)

class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ['species', 'island']

class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = '/finches'

# def finches_index(request):
#     finches = Finch.objects.all()
#     return render(request, 'finches/index.html', { 'finches': finches })

@login_required
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    id_list = finch.toys.all().values_list('id')
    toys_finch_doesnt_have = Toy.objects.exclude(id__in=id_list)
    return render(request, 'finches/detail.html', { 'finch': finch, 'feeding_form': FeedingForm(), 'toys': toys_finch_doesnt_have })

@login_required
def add_feeding(request, finch_id):
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it has the finch_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)

@login_required
def add_photo(request, finch_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, finch_id=finch_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', finch_id=finch_id)

class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = '__all__'

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy 
    success_url = '/toys'

@login_required
def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id=finch_id)

@login_required
def unassoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('detail', finch_id=finch_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)