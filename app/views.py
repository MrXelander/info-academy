import openai
import random
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from app.models import CustomUser, Materia, Tema, Subtema, SubtemaDoc, CuestionarioInicial, Evaluacion, Pregunta
from django.contrib.auth.hashers import make_password
from gptunam import settings
from pytube import Search, extract
from django.http import HttpResponse

version="beta(231008)"

def index(request):
    if request.user.is_authenticated:
        return redirect('initialtest')

    return render(request, 'index.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('initialtest')

    if request.method == 'POST':
        # Obtener los datos del formulario
        first_name = request.POST['name']
        last_name = request.POST['lastname']
        email = request.POST['email']
        nc = request.POST['nc']
        role = request.POST['role']
        password = request.POST['password']
        try:
            usuario = CustomUser.objects.create_user(
                email=email, 
                password=password, 
                first_name=first_name, 
                last_name=last_name, 
                nc=nc, 
                role=role, 
                username=email
            )
            usuario.set_password(password)
            usuario.save()
            
            messages.add_message(request, 70, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect(login)
        except Exception as e:
            messages.add_message(request, 90, 'Ha ocurrido un error durante el registro. Intente nuevamente.')
            return redirect(signup)
    return render(request, 'signup.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('initialtest')

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

def es_administrador(user):
    return user.is_authenticated and user.role == 'Administrador'

def es_profesor(user):
    return user.is_authenticated and user.role != 'Estudiante'

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    if not user.initial_test:
        return redirect('initialtest')

    short_name = user.get_short_name()
    colores_disponibles = ['uno', 'dos', 'tres', 'cuatro', 'cinco']
    if user.role == 'Administrador' or user.role == 'Profesor':
        materias = Materia.objects.all()
    else:
        materias = user.materias_inscritas.all()
    context = {
        'user': user,
        'short_name': short_name,
        'materias': materias,
        'colores': colores_disponibles,
        'version': version,
    }
    if request.method == 'POST' and es_profesor(user):
        nombre = request.POST['nombre_materia']
        profesor = user

        if nombre:
            try:
                materia = Materia.objects.create(nombre=nombre, profesor=profesor)
                messages.add_message(request, 70, 'Materia creada exitosamente.')
                return redirect('dashboard')
            except Exception as e:
                messages.add_message(request, 90, 'Error al crear materia')
                return redirect('dashboard')
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def initialtest(request):
    user = request.user
    if user.initial_test:
        return redirect('dashboard')
    
    if request.method == 'POST':
        nivel_experiencia = request.POST.get('nivel_experiencia', '')
        estilo_aprendizaje = request.POST.get('estilo_aprendizaje', '')
        contenido_preferido = request.POST.get('contenido_preferido', '')
        horarios_estudio = request.POST.get('horarios_estudio', '')
        duracion_sesiones = request.POST.get('duracion_sesiones', '')
        formato_evaluacion = request.POST.get('formato_evaluacion', '')
        recibir_recomendaciones = request.POST.get('recibir_recomendaciones', False)
        try:
            cuestionario = CuestionarioInicial.objects.create(
                user=user,
                nivel_experiencia=nivel_experiencia,
                estilo_aprendizaje=estilo_aprendizaje,
                contenido_preferido=contenido_preferido,
                horarios_estudio=horarios_estudio,
                duracion_sesiones=duracion_sesiones,
                formato_evaluacion=formato_evaluacion,
                recibir_recomendaciones=recibir_recomendaciones
            )
            cuestionario.save()
            user.initial_test = True
            user.save()
            messages.add_message(request, 70, 'Cuestionario guardado correctamente')
            return redirect('dashboard')
        except Exception as e:
            messages.add_message(request, 90, 'Error al guardar cuestionario')
            return redirect('initialtest')
    return render(request, 'initialtest.html')

@login_required(login_url='login')
def editinitialtest(request):
    user = request.user
    if not user.initial_test:
        return redirect('initialtest')
    cuestionario = CuestionarioInicial.objects.get(user=user)
    print(cuestionario.estilo_aprendizaje)
    print(cuestionario.estilo_aprendizaje == 'Visual')
    context = {
        'user': user,
        'cuestionario': cuestionario,
    }
    if request.method == 'POST':
        nivel_experiencia = request.POST.get('nivel_experiencia', '')
        estilo_aprendizaje = request.POST.get('estilo_aprendizaje', '')
        contenido_preferido = request.POST.get('contenido_preferido', '')
        horarios_estudio = request.POST.get('horarios_estudio', '')
        duracion_sesiones = request.POST.get('duracion_sesiones', '')
        formato_evaluacion = request.POST.get('formato_evaluacion', '')
        recibir_recomendaciones = request.POST.get('recibir_recomendaciones', False)

        cuestionario.nivel_experiencia=nivel_experiencia
        cuestionario.estilo_aprendizaje=estilo_aprendizaje
        cuestionario.contenido_preferido=contenido_preferido
        cuestionario.horarios_estudio=horarios_estudio
        cuestionario.duracion_sesiones=duracion_sesiones
        cuestionario.formato_evaluacion=formato_evaluacion
        cuestionario.recibir_recomendaciones=recibir_recomendaciones
        try:
            cuestionario.save()
            messages.add_message(request, 70, 'Datos actualizados correctamente')
            return redirect('dashboard')
        except Exception as e:
            print(e)
            messages.add_message(request, 90, 'Error al actualizar datos')
            return redirect('dashboard')
    return render(request, 'editinitialtest.html', context)

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def edit_account(request):
    user = request.user
    context = {
        'user': user,
    }
    if request.method == 'POST':
        # Obtener los datos del formulario
        first_name = request.POST['name']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        
        user.email=email
        user.first_name=first_name
        user.last_name=last_name
        user.username=email
        # Encriptar la contraseña con PBKDF2
        if password:
            hashed_password = make_password(password)
            user.password=hashed_password
        
        try:
            user.save()
            
            messages.add_message(request, 70, 'Datos actualizados correctamente')
            return redirect('dashboard')
        except Exception as e:
            messages.add_message(request, 90, 'Error al actualizar datos')
            return redirect('dashboard')
    return render(request, 'editaccount.html', context)

@login_required(login_url='login')
def subjects(request):
    if not es_profesor:
        return HttpResponseForbidden()
    user = request.user
    short_name = user.get_short_name()
    if user.role == 'Administrador':
        materias = Materia.objects.all()
    elif user.role == 'Profesor':
        materias = Materia.objects.filter(profesor=user)
    context = {
        'user': user,
        'short_name': short_name,
        'materias': materias,
    }
    if request.method == 'POST':
        nombre = request.POST['nombre_materia']
        profesor = user

        if nombre:
            try:
                materia = Materia.objects.create(nombre=nombre, profesor=profesor)
                messages.add_message(request, 70, 'Materia creada exitosamente.')
                return redirect('subjects')
            except Exception as e:
                messages.add_message(request, 90, 'Error al crear materia')
                return redirect('subjects')
    return render(request, 'subjects.html', context)

@user_passes_test(es_profesor, login_url='login')
def delete_subject(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    try:
        materia.delete()
        messages.add_message(request, 70, 'Materia eliminada exitosamente.')
    except Exception as e:
        messages.add_message(request, 90, 'Error al eliminar materia')
    return redirect('dashboard')

@login_required(login_url='login')
def topics(request, materia_id):
    if not es_profesor:
        return HttpResponseForbidden()
    user = request.user
    short_name = user.get_short_name()
    materia = get_object_or_404(Materia, id=materia_id)
    temas = Tema.objects.filter(materia=materia)
    alumnos = materia.alumnos.all()
    context = {
        'user': user,
        'short_name': short_name,
        'materia': materia,
        'temas': temas,
        'alumnos': alumnos,
    }
    if request.method == 'POST':
        nombre = request.POST['nombre_tema']

        if nombre:
            try:
                tema = Tema.objects.create(nombre=nombre, materia=materia)
                messages.add_message(request, 70, 'Tema creado exitosamente.')
                return redirect('topics', materia_id=materia.id)
            except Exception as e:
                print(e)
                messages.add_message(request, 90, 'Error al crear tema')
                return redirect('topics', materia_id=materia.id)
    return render(request, 'topics.html', context)

@user_passes_test(es_profesor, login_url='login')
def delete_topic(request, materia_id, tema_id):
    materia = get_object_or_404(Materia, id=materia_id)
    tema = get_object_or_404(Tema, id=tema_id)
    try:
        tema.delete()
        messages.add_message(request, 70, 'Tema eliminado exitosamente.')
    except Exception as e:
        messages.add_message(request, 90, 'Error al eliminar tema')
    return redirect('subjectopic', codigo=materia.codigo)

@login_required(login_url='login')
def subtopics(request, materia_id, tema_id):
    if not es_profesor:
        return HttpResponseForbidden()
    user = request.user
    short_name = user.get_short_name()
    materia = get_object_or_404(Materia, id=materia_id)
    tema = get_object_or_404(Tema, id=tema_id)
    subtemas = Subtema.objects.filter(tema=tema)
    context = {
        'user': user,
        'short_name': short_name,
        'materia': materia,
        'tema': tema,
        'subtemas': subtemas,
    }
    return render(request, 'subtopics.html', context)

@user_passes_test(es_profesor, login_url='login')
def new_subtopic(request, materia_id, tema_id):
    materia = get_object_or_404(Materia, id=materia_id)
    tema = get_object_or_404(Tema, id=tema_id)
    context = {
        'materia': materia,
        'tema': tema,
    }
    if request.method == 'POST':
        nombre = request.POST['nombre_subtema']
        tipo = request.POST['tipo']
        descripcion = request.POST['descripcion']

        if nombre and tipo:
            try:
                subtema = Subtema.objects.create(nombre=nombre, tema=tema, tipo=tipo, descripcion=descripcion)
                messages.add_message(request, 70, 'Subtema creado exitosamente.')
                return redirect('subtopics', materia_id=materia_id, tema_id=tema.id)
            except Exception as e:
                messages.add_message(request, 90, 'Error al crear subtema')
                return redirect('subtopics', materia_id=materia_id, tema_id=tema.id)
    return render(request, 'newsubtopic.html', context)

@user_passes_test(es_profesor, login_url='login')
def addsubtopic(request, codigo, tema_id):
    materia = get_object_or_404(Materia, codigo=codigo)
    tema = get_object_or_404(Tema, id=tema_id)
    context = {
        'materia': materia,
        'tema': tema,
    }
    if request.method == 'POST':
        nombre = request.POST['nombre_subtema']
        tipo = request.POST['tipo']
        descripcion = request.POST['descripcion']

        if nombre and tipo:
            try:
                subtema = Subtema.objects.create(nombre=nombre, tema=tema, tipo=tipo, descripcion=descripcion)
                if tipo == "Material didáctico":
                    uploaded_file = request.FILES.get('file')
                    if uploaded_file:
                        try:
                            subtema_doc = SubtemaDoc(subtema=subtema, file=uploaded_file)
                            subtema_doc.save()
                            messages.add_message(request, 70, 'Actividad creada exitosamente.')
                            return redirect('subjectopic', codigo=codigo)
                        except Exception as E:
                            messages.add_message(request, 90, 'Error al guardar el archivo')
                            return redirect('subjectopic', codigo=codigo)
                if tipo == "Evaluación":
                    tipo_evaluacion = request.POST['tipo_evaluacion']
                    try:
                        evaluacion = Evaluacion(subtema=subtema,tipo=tipo_evaluacion)
                        evaluacion.save()
                    except Exception as E:
                        messages.add_message(request, 90, 'Error al crear evaluacion')
                        return redirect('subjectopic', codigo=codigo)
                    
                    preguntas = request.POST.getlist('preg[]')
                    respuestas_correctas = request.POST.getlist('correcta[]')
                    opciones_a = request.POST.getlist('opc_a[]')
                    opciones_b = request.POST.getlist('opc_b[]')
                    opciones_c = request.POST.getlist('opc_c[]')

                    if len(preguntas) == len(respuestas_correctas) == len(opciones_a) == len(opciones_b) == len(opciones_c):
                        try:
                            for i in range(len(preguntas)):
                                pregunta = Pregunta.objects.create(
                                    evaluacion=evaluacion,
                                    preg=preguntas[i],
                                    correcta=respuestas_correctas[i],
                                    opc_a=opciones_a[i],
                                    opc_b=opciones_b[i],
                                    opc_c=opciones_c[i]
                                )
                                pregunta.save()

                            messages.add_message(request, 70, 'Actividad y preguntas creadas exitosamente.')
                            return redirect('subjectopic', codigo=codigo)
                        except Exception as e:
                            messages.add_message(request, 90, 'Error al crear actividad o preguntas')
                            return redirect('subjectopic', codigo=codigo)
                    else:
                        messages.add_message(request, 90, 'La cantidad de preguntas y respuestas no coincide')
                        return redirect('subjectopic', codigo=codigo)
            except Exception as e:
                messages.add_message(request, 90, 'Error al crear actividad')
                return redirect('subjectopic', codigo=codigo)
    return render(request, 'addsubtopic.html', context)

@user_passes_test(es_profesor, login_url='login')
def edit_subtopic(request, tema_id, subtema_id):
    tema = get_object_or_404(Tema, id=tema_id)
    subtema = get_object_or_404(Subtema, id=subtema_id)
    if request.method == 'POST':
        nombre = request.POST['nombre_subtema']
        tipo = request.POST['tipo']
        descripcion = request.POST['descripcion']

        subtema.nombre = nombre
        subtema.tipo = tipo
        descripcion = descripcion

        try:
            subtema.save()
            messages.add_message(request, 70, 'Subtema editado correctamente.')
            return redirect('subtopics', tema_id=tema.id)
        except Exception as e:
            print(e)
            messages.add_message(request, 90, 'Error al editar subtema')
            return redirect('subtopics', tema_id=tema.id)
    return render(request, 'subtopicnew.html')

@user_passes_test(es_profesor, login_url='login')
def delete_subtopic(request, tema_id, subtema_id):
    subtema = get_object_or_404(Subtema, id=subtema_id)
    try:
        subtema.delete()
        messages.add_message(request, 70, 'Subtema eliminado exitosamente.')
    except Exception as e:
        messages.add_message(request, 90, 'Error al eliminar subtema')
    return redirect('subtopics', tema_id=tema_id)

@login_required(login_url='login')
def subjectstudent(request):
    user = request.user
    short_name = user.get_short_name()
    materia = user.materias_inscritas.first()
    materias = user.materias_inscritas.all()
    context = {
        'user': user,
        'short_name': short_name,
        'materia': materia,
        'materias': materias,
    }
    if request.method == 'POST':
        codigo_materia = request.POST['codigo_materia']

        # Obtener la materia específica utilizando el código
        try:
            materia = Materia.objects.get(codigo=codigo_materia)
        except Materia.DoesNotExist:
            messages.add_message(request, 90, 'La materia especificada no existe')
            return redirect('subjectstudent')

        # Verificar si el alumno ya está inscrito en la materia
        if materia.alumnos.filter(id=user.id).exists():
            messages.add_message(request, 90, 'Ya estás inscrito en esta materia')
            return redirect('subjectstudent')

        # Inscribir al alumno en la materia
        materia.alumnos.add(user)
        materia.save()
        messages.add_message(request, 70, 'Inscripción exitosa')
        return redirect('subjectstudent')
    return render(request, 'subjectstudent.html', context)

@user_passes_test(es_administrador, login_url='login')
def users(request):
    users = CustomUser.objects.all()
    user = request.user
    short_name = user.get_short_name()
    context = {
        'user': user,
        'short_name': short_name,
        'users': users
    }
    return render(request, 'users.html', context)

@user_passes_test(es_administrador, login_url='login')
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        # Obtener los datos del formulario
        first_name = request.POST['name']
        last_name = request.POST['lastname']
        email = request.POST['email']
        nc = request.POST['nc']
        password = request.POST['password']
        nuevo_rol = request.POST['role']
        
        user.role = nuevo_rol
        user.email=email
        user.first_name=first_name
        user.last_name=last_name
        user.nc=nc
        user.username=email
        if password:
            hashed_password = make_password(password)
            user.password=hashed_password
        try:
            user.save()
            
            messages.add_message(request, 70, 'Datos actualizados correctamente')
            return redirect('dashboard')
        except Exception as e:
            messages.add_message(request, 90, 'Error al actualizar datos')
            return redirect('dashboard')
    return render(request, 'edituser.html', {'user': user})

@login_required(login_url='login')
def subjectopic(request, codigo):
    materia = get_object_or_404(Materia, codigo=codigo)
    temas = Tema.objects.filter(materia=materia)
    user = request.user
    short_name = user.get_short_name()
    colores_disponibles = ['uno', 'dos', 'tres', 'cuatro', 'cinco']
    is_registered = materia.alumnos.filter(id=user.id).exists()
    permiso = es_profesor(user) or (user.role=='Estudiante' and is_registered)
    context = {
        'materia': materia,
        'temas': temas,
        'short_name': short_name,
        'colores': colores_disponibles,
        'user': user,
        'is_registered': is_registered,
        'permiso': permiso,
        'version': version,
    }
    if request.method == 'POST':
        nombre = request.POST['nombre_tema']

        if nombre:
            try:
                tema = Tema.objects.create(nombre=nombre, materia=materia)
                messages.add_message(request, 70, 'Tema creado exitosamente.')
                return redirect('subjectopic', codigo=codigo)
            except Exception as e:
                print(e)
                messages.add_message(request, 90, 'Error al crear tema')
                return redirect('subjectopic', codigo=codigo)
    return render(request, 'subjectopic.html', context)

@login_required(login_url='login')
def inscripcion(request, codigo):
    user = request.user
    materia = get_object_or_404(Materia, codigo=codigo)

    if request.user.role != 'Estudiante':
        messages.error(request, "Solo los estudiantes pueden registrarse en esta materia.")
        return redirect('subjectopic', codigo=codigo)

    if materia.alumnos.filter(id=user.id).exists():
            messages.add_message(request, 90, 'Ya estás inscrito en esta materia')
            return redirect('dashboard')

    # Inscribir al alumno en la materia
    materia.alumnos.add(user)
    materia.save()
    messages.add_message(request, 70, 'Inscripción exitosa')
    return redirect('dashboard')

def baja(request, codigo):
    user = request.user
    materia = get_object_or_404(Materia, codigo=codigo)

    if request.user.role != 'Estudiante':
        messages.error(request, "Solo los estudiantes pueden registrarse en esta materia.")
        return redirect('dashboard')
    
    if materia.alumnos.filter(id=request.user.id).exists():
        materia.alumnos.remove(request.user)
        messages.add_message(request, 70, "Te has dado de baja de la materia con éxito.")
    return redirect('dashboard')

@login_required(login_url='login')
def usersubtopics(request, materia_id, tema_id):
    materia = get_object_or_404(Materia, id=materia_id)
    tema = get_object_or_404(Tema, id=tema_id)
    subtemas = Subtema.objects.filter(tema=tema)
    user = request.user
    short_name = user.get_short_name()
    context = {
        'materia': materia,
        'tema': tema,
        'short_name': short_name,
        'subtemas': subtemas,
    }
    return render(request, 'usersubtopics.html', context)

openai.api_key = settings.OPENAI_API_KEY

def practice(request, materia_id, tema_id, subtema_id):
    user = request.user
    short_name = user.get_short_name()
    materia = get_object_or_404(Materia, id=materia_id)
    tema = get_object_or_404(Tema, id=tema_id)
    subtema = get_object_or_404(Subtema, id=subtema_id)
    entrada = "Hazme una práctica de la materia " + materia.nombre + ", del tema " + tema.nombre + ", específicamente del subtema " + subtema.nombre + ", este es de tipo " + subtema.tipo + " (práctico, teórico o mixto). El usuario también proporcionó algunos detalles que pueden ser de ayuda (no siepre los proporciona): " + subtema.descripcion + ". La práctica debe incluir los siguientes pasos: Introducción, Ejemplos, Pasos de la práctica con instalacion de librerias (en caso de ser de tipo Práctico se necesita codigo de ser necesario y en caso de ser teorico, agrega mucha más información aqui, como definiciones), y conclusión.  No olvides al final poner las fuentes o referencias, recuerda poner lo necesario porque solo limito a un maximo de 1024 tokens"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=entrada,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5
        )
        response_content = response.choices[0].text
        response_content_html = response_content.replace('\n', '<br>')
    except openai.error.RateLimitError as e:
        response_content = "Error de límite de uso. Por favor, inténtalo más tarde."
        response_content_html = response_content
    context = {
        'materia': materia,
        'tema': tema,
        'short_name': short_name,
        'subtema': subtema,
        'response_content': response_content,
        'response_content_html': response_content_html,
    }
    print(response_content)
    return render(request, 'practice.html', context)

def buscar_video(query):
    s = Search(query)
    if len(s.results) > 0:
        video = random.choice(s.results)
        video_id = extract.video_id(video.watch_url)
        video_url_embed = f"https://www.youtube.com/embed/{video_id}"
        return video_url_embed
    else:
        return None

def video(request, codigo, tema_id, subtema_id):
    user = request.user
    short_name = user.get_short_name()
    materia = get_object_or_404(Materia, codigo=codigo)
    tema = get_object_or_404(Tema, id=tema_id)
    subtema = get_object_or_404(Subtema, id=subtema_id)
    video_url = buscar_video(subtema.nombre + " " + tema.nombre)

    context = {
        'materia': materia,
        'tema': tema,
        'short_name': short_name,
        'subtema': subtema,
        'video_url': video_url,
    }
    return render(request, 'video.html', context)

@login_required(login_url='login')
def document(request, codigo, tema_id, subtema_id):
    user = request.user
    short_name = user.get_short_name()
    materia = get_object_or_404(Materia, codigo=codigo)
    tema = get_object_or_404(Tema, id=tema_id)
    subtema = get_object_or_404(Subtema, id=subtema_id)
    subtema_doc = subtema.subtemadoc_set.first()
    print(subtema_doc.id)
    context = {
        'materia': materia,
        'tema': tema,
        'short_name': short_name,
        'subtema': subtema,
        'subtema_doc': subtema_doc,
    }
    return render(request, 'document.html', context)

@login_required(login_url='login')
def openpdf(request, codigo, tema_id, subtema_id, doc_id):
    # Obtener el objeto SubtemaDoc asociado al subtema
    subtema_doc = get_object_or_404(SubtemaDoc, id=doc_id)

    # Obtener el nombre del archivo PDF y la ruta al archivo
    pdf_filename = subtema_doc.name
    pdf_file_path = subtema_doc.file.path

    # Abrir y leer el archivo PDF
    with open(pdf_file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{pdf_filename}"'
        
        # Configurar el encabezado X-Frame-Options para permitir la incrustación en iframes
        response['X-Frame-Options'] = 'SAMEORIGIN'

        return response
    
@login_required(login_url='login')
def evaluationq(request, codigo, tema_id, subtema_id):
    user = request.user
    short_name = user.get_short_name()
    materia = get_object_or_404(Materia, codigo=codigo)
    tema = get_object_or_404(Tema, id=tema_id)
    subtema = get_object_or_404(Subtema, id=subtema_id)
    evaluacion = Evaluacion.objects.filter(subtema=subtema).first()
    preguntas = Pregunta.objects.filter(evaluacion=evaluacion)
    context = {
        'materia': materia,
        'tema': tema,
        'short_name': short_name,
        'subtema': subtema,
        'evaluacion': evaluacion,
        'preguntas': preguntas,
    }
    return render(request, 'evaluationq.html', context)