import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Pet, Product
from .forms import PetForm, ProductForm, CustomUserCreationForm
from django.db.models import Q 
from django.contrib.auth import authenticate, login, logout

# User views for registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_success')  # Redirect to a success page
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration_success.html') 

# Create your views here.
def home(request):
    return render(request, 'petstoreapp/home.html')

def about_us(request):
    return render(request, 'petstoreapp/about_us.html')

@login_required
def pets_list(request):
    pets = Pet.objects.all()
    return render(request, 'petstoreapp/pets_list.html', {'pets': pets})

@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)   
        if form.is_valid():
            form.save()
            return redirect('pets_list')
    else:
        form = PetForm()
    return render(request, 'petstoreapp/pet_create.html', {'form': form})

@login_required
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

@login_required
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

@login_required
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

@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, 'petstoreapp/pets_detail.html', {'pet': pet})

@login_required
def add_pet_to_cart(request, pk):
    if request.method == 'POST':
        pet = get_object_or_404(Pet, pk=pk)
        quantity = int(request.POST.get('quantity', 1))
        cart, created = Cart.objects.get_or_create(user=request.user)

        """try:
            # Attempt to create a new CartItem with the provided quantity
            cart_item, created = CartItem.objects.get_or_create(cart=cart, pet=pet, defaults={'quantity': quantity})
        except IntegrityError:
            # Handle case when the cart item already exists for the pet
            cart_item = CartItem.objects.get(cart=cart, pet=pet)
            cart_item.quantity += int(quantity)
            cart_item.save()"""
        
        # Check if the CartItem already exists for the pet in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, pet=pet, defaults={'quantity': quantity})

        # If the cart item already exists, update its quantity
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            # If the cart item is newly created, set its quantity
            cart_item.quantity = quantity
            cart_item.save()

        return redirect('cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart') 

@login_required
def proceed_to_pay(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_amount = sum(item.pet.price * item.quantity for item in cart_items)
    return render(request, 'petstoreapp/proceed_to_pay.html', {'total_amount': total_amount})

@login_required
def payment_confirmation(request):
    # Your logic for payment confirmation here
    # Get the current user's cart
    cart = Cart.objects.get(user=request.user)
    
    # Get all cart items for the current user
    cart_items = CartItem.objects.filter(cart=cart)
    order_amount = 0

    # Calculate the total amount to be paid
    total_amount = sum(item.pet.price * item.quantity for item in cart_items)
    print("total amount in payment_confirmation --------> ", total_amount)
    # Initialize Razorpay client with your API key and secret
    client = razorpay.Client(auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET))
    
    # Create Razorpay order
    # order_amount = int(total_amount * 100)  # Razorpay expects amount in paise
    order_amount = (order_amount + total_amount) * 100
    print("order_amount in payment_confirmation ------------ > ", order_amount)
    order_currency = 'INR'  # Change currency as per your requirement
    order_receipt = 'order_rcptid_11'  # Replace with your order receipt ID
    order = client.order.create({'amount': order_amount, 'currency': order_currency, 'receipt': order_receipt})
    
    # Pass Razorpay order details to the payment_confirmation template
    context = {'order_amount': order_amount, 'order': order, 'razorpay_key_id': settings.RAZORPAY_TEST_KEY_ID}
    
    # Render the payment confirmation template
    
    return render(request, 'petstoreapp/payment_confirmation.html', context)

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    return render(request, 'petstoreapp/cart.html', {'cart_items': cart_items})

@login_required
def search_results(request):
    search_query = request.GET.get('search', '')
    #pets = Pet.objects.filter(name__icontains=search_query)
    pets = Pet.objects.filter(Q(name__icontains=search_query) | Q(breed__icontains=search_query))
    return render(request, 'petstoreapp/search_results.html', {'pets': pets, 'search_query': search_query})

@login_required
def products_list(request):
    products = Product.objects.all()
    return render(request, 'petstoreapp/products_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)   
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm()
    return render(request, 'petstoreapp/product_create.html', {'form': form})

@login_required
def product_create_food(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)   
        if form.is_valid():
            product = form.save(commit=False)
            product.category = 'food'  # Set the category as needed
            product.save()
            return redirect('products_list')
    else:
        form = ProductForm(initial={'category': 'food'})
    return render(request, 'petstoreapp/product_create_food.html', {'form': form})

@login_required
def product_create_medicines(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)   
        if form.is_valid():
            product = form.save(commit=False)
            product.category = 'medicines'  # Set the category as needed
            product.save()
            return redirect('products_list')
    else:
        form = ProductForm(initial={'category': 'medicines'})
    return render(request, 'petstoreapp/product_create_medicines.html', {'form': form})

@login_required
def product_create_toys(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)   
        if form.is_valid():
            product = form.save(commit=False)
            product.category = 'toys'  # Set the category as needed
            product.save()
            return redirect('products_list')
    else:
        form = ProductForm(initial={'category': 'toys'})
    return render(request, 'petstoreapp/product_create_toys.html', {'form': form})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'petstoreapp/products_detail.html', {'product': product})

@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, 'petstoreapp/pets_detail.html', {'pet': pet})

@login_required
def search_product_results(request):
    search_query = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=search_query)
    #products = Product.objects.filter(Q(name__icontains=search_query))
    return render(request, 'petstoreapp/search_product_results.html', {'products': products, 'search_query': search_query})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the home page or a different URL after successful login
            return redirect('home')
        else:
            # Return an error message for invalid credentials
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        # Render the login page for GET requests
        return render(request, 'login.html')

def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to home page after logout