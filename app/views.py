import django
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from .models import CustomUser, GoldCost, Category, Product, BailTicket
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin 
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, ProductForm

class SignUpView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')
    success_message = "Аккаунт создан успешно!"

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}/')
        subject = 'Verify your email'
        message = f'Hello {user.username}, please click the link below to verify your email:\n\n{verify_url}'
        send_mail(subject, message, 'sender@example.com', [user.email])

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object  
        user.is_active = False
        user.save()
        self.send_verification_email(self.object)
        return response
    
class VerifyEmailView(View):
    def get(self, request, user_pk, token):
        user = CustomUser.objects.get(pk=user_pk)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has been verified')
            return redirect('home')
        else:
            messages.error(request, 'Invalid verification link')
            return redirect('home')
        
class Login(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')
    success_message = 'You are logged in successfully'

class Logout(LogoutView):
    next_page = reverse_lazy('home')


class HomeView(ListView):
    template_name = 'home.html'

def get_home(request):
    products = Product.objects.all()[:5]
    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            weight = int(request.POST.get('product_weight'))
            proba = request.POST.get('product_proba')
        except:
            weight = 0
            proba = '333'
        
        gold_cost = GoldCost.objects.get(product_proba=int(proba))
        result = weight * gold_cost.product_cost
        
        context = {
            'categories': categories,
            'products': products,
            'result': result
        }
        return render(request, 'home.html', context)    
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'home.html', context)

def get_catalog(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'catalog.html', context)

def get_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': product})

def get_contact(request):
    return render(request, 'contact.html')

@login_required
def get_user_tickets(request, user_id):
    # Check if the logged-in user is the owner of the tickets
    if request.user.id != user_id:
        return HttpResponseForbidden("You do not have permission to view these tickets.")
    
    # Get all tickets associated with the user_id
    tickets = BailTicket.objects.filter(user__id=user_id)
    
    # Check if there are no tickets for the user
    if not tickets.exists():
        return HttpResponse("No tickets found for this user.", status=404)
    
    # Render the template with the list of tickets
    return render(request, 'user_tickets.html', {'tickets': tickets})

class CreateProductView(CreateView):
    model = Product
    form = ProductForm
    login_url = reverse_lazy('home')
    template_name = 'product_create.html'
    success_url = reverse_lazy('home')