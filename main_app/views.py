from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch, Toy
from .forms import FeedingForm

 # Create your views here.
def about(request):
    return render(request, 'about.html')

class FinchList(ListView):
    model = Finch
    template_name = 'finches/index.html'
    context_object_name = 'finches'

class FinchCreate(CreateView):
    model = Finch
    fields = ['name', 'species', 'island']
    #success_url = '/finches/{finch_id}' # not sure if this works but get_absolute_url method takes care of it

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['species', 'island']

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches'

# def finches_index(request):
#     finches = Finch.objects.all()
#     return render(request, 'finches/index.html', { 'finches': finches })

def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    id_list = finch.toys.all().values_list('id')
    toys_finch_doesnt_have = Toy.objects.exclude(id__in=id_list)
    return render(request, 'finches/detail.html', { 'finch': finch, 'feeding_form': FeedingForm(), 'toys': toys_finch_doesnt_have })

def add_feeding(request, finch_id):
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it has the finch_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)

def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id=finch_id)

def unassoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('detail', finch_id=finch_id)