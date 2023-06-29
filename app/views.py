import hashlib
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import CustomUser
from django.contrib.auth.hashers import make_password

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        first_name = request.POST['name']
        last_name = request.POST['lastname']
        email = request.POST['email']
        nc = request.POST['nc']
        role = request.POST['role']
        password = request.POST['password']

        print("contraseña " + password)
        # Encriptar la contraseña con PBKDF2
        hashed_password = make_password(password)
        print("encriptada " + hashed_password)
        
        try:
            usuario = CustomUser.objects.create_user(
                email=email, 
                password=hashed_password, 
                first_name=first_name, 
                last_name=last_name, 
                nc=nc, 
                role=role, 
                username=email
            )
            usuario.save()
            
            messages.add_message(request, 70, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect(login)
        except Exception as e:
            messages.add_message(request, 90, 'Ha ocurrido un error durante el registro. Intente nuevamente.')
            return redirect(signup)
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        # Verificar las credenciales del usuario
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.add_message(request, 90, 'Credenciales inválidas, intente de nuevo.')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def recovery(request):
    if request.method == 'POST':
        nc = request.POST.get('nc')
        username = request.POST.get('email')
        new_password = request.POST.get('password')

        # Obtener el usuario de la base de datos
        try:
            user = CustomUser.objects.get(nc=nc, username=username)
        except CustomUser.DoesNotExist:
            messages.add_message(request, 90, 'No se encontró ningún usuario con el número de cuenta y correo proporcionados.')
            return redirect('recovery')
        
        # Encriptar la nueva contraseña con el mismo algoritmo PBKDF2
        hashed_password = make_password(new_password)
        
        # Actualizar la contraseña en la base de datos
        user.password = hashed_password
        user.save()
        
        messages.add_message(request, 70, 'Contraseña restablecida exitosamente. Ahora puedes iniciar sesión.')
        return redirect('login')
    else:
        return render(request, 'recovery.html')

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    short_name = user.get_short_name()
    context = {
        'user': user,
        'short_name': short_name,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')
