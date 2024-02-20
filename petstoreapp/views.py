from django.shortcuts import get_object_or_404, render, redirect
from .models import Pet
from .forms import PetForm, PetSearchForm
from django.views.generic import DetailView
from django.db.models import Q 

# Create your views here.
def home(request):
    return render(request, 'petstoreapp/home.html')

def pets_list(request):
    pets = Pet.objects.all()
    return render(request, 'petstoreapp/pets_list.html', {'pets': pets})

def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)   
        if form.is_valid():
            form.save()
            return redirect('pets_list')
    else:
        form = PetForm()
    return render(request, 'petstoreapp/pet_create.html', {'form': form})

def pet_create_dog(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)   
        if form.is_valid():
            pet = form.save(commit=False)
            pet.category = 'dog'  # Set the category as needed
            print("Pet dog :::: ", pet.category)
            pet.save()
            return redirect('pets_list')
    else:
        form = PetForm(initial={'category': 'dog'})
    return render(request, 'petstoreapp/pet_create_dog.html', {'form': form})

def pet_create_cat(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)   
        if form.is_valid():
            pet = form.save(commit=False)
            pet.category = 'cat'  # Set the category as needed
            pet.save()
            return redirect('pets_list')
    else:
        form = PetForm(initial={'category': 'cat'})
    return render(request, 'petstoreapp/pet_create_cat.html', {'form': form})

def pet_create_bird(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)   
        if form.is_valid():
            pet = form.save(commit=False)
            pet.category = 'bird'  # Set the category as needed
            pet.save()
            return redirect('pets_list')
    else:
        form = PetForm(initial={'category': 'bird'})
    return render(request, 'petstoreapp/pet_create_bird.html', {'form': form})

class PetDetailView(DetailView):
    model = Pet
    template_name = 'petstoreapp/pets_detail.html'
    context_object_name = 'pet'

def search_results(request):
    search_query = request.GET.get('search', '')
    #pets = Pet.objects.filter(name__icontains=search_query)
    pets = Pet.objects.filter(Q(name__icontains=search_query) | Q(breed__icontains=search_query))
    return render(request, 'petstoreapp/search_results.html', {'pets': pets, 'search_query': search_query})