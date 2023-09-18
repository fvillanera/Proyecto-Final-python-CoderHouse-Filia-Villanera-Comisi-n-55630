from django.shortcuts import render, redirect
from .models import Clase, Instructor, Alumno, Fechaproxima, Avatar
from .forms import CursoForm, Profesorform, Estudianteform, Fechasform, RegistroUsuariosForm, UEditForm, AvatarFormulario
from django.http import HttpResponse
from django.urls import reverse_lazy


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth       import authenticate, login


from django.contrib.auth.decorators import login_required



# Create your views here.

#----------------------------------->Main pages

def home (request):
    return render(request, "aplicacion/home.html")

def acerca (request):
    return render(request, "aplicacion/acerca.html")

@login_required
def cursos (request):
    contexto = {"clases": Clase.objects.all(), 'titulo': 'Clases disponibles'}
    return render(request, "aplicacion/cursos.html", contexto)

@login_required
def profesores (request):
    contexto = {"profesores": Instructor.objects.all(), 'titulo': 'instructores disponibles al'}
    return render(request, "aplicacion/profesores.html", contexto)

@login_required
def estudiantes (request):
    contexto = {"estudiantes": Alumno.objects.all(), 'titulo': 'alumnos'}
    return render(request, "aplicacion/estudiantes.html", contexto)

@login_required
def fechaproxima (request):
    contexto = {"fechasproximas": Fechaproxima.objects.all(), 'titulo': 'Hoy es: '}
    return render(request, "aplicacion/fechaproxima_list.html", contexto)



#-----------------------------------> Forms
@login_required
def cursoform(request):
    if request.method == "POST":
        curso = Clase(nombre=request.POST['nombre'],
                      comision=request.POST['comision'])
        curso.save()
        return HttpResponse("Nueva asignatura/curso agregada con exito!")
    
    return render(request, "aplicacion/cursoform.html")

@login_required
def cursoform2(request):
    if request.method == "POST":
        miform= CursoForm(request.POST)
        if miform.is_valid():
            name_curso= miform.cleaned_data.get('nombre')
            name_comision= miform.cleaned_data.get('comision')
            name_duracion= miform.cleaned_data.get('duracion')
            curso= Clase(nombre = name_curso,
                         comision= name_comision,
                         duracion= name_duracion)
            curso.save()
            return render(request, "aplicacion/base.html")
    else:
        miform= CursoForm()
    return render (request, "aplicacion/cursoform2.html", {"form": miform})


@login_required
def searchcomision(request):
    return render (request, "aplicacion/searchcomision.html")

@login_required
def search2(request):
    if request.GET['buscar']:
        patron= request.GET['buscar']
        cursos= Clase.objects.filter(nombre__icontains=patron)
        contexto= {"clases": cursos}
        return render(request, "aplicacion/cursos.html", contexto)
    
    return HttpResponse ("Vuelva a intentarlo, ingreso invalido, asegurate de llenar todos los campos")

@login_required
def profesorform(request):
    if request.method == "POST":
        miform= Profesorform (request.POST)
        if miform.is_valid():
            name_nombre= miform.cleaned_data.get('nombre')
            name_apellido= miform.cleaned_data.get('apellido')
            name_email= miform.cleaned_data.get('email')
            name_profesion= miform.cleaned_data.get('profesion')
            profesor= Instructor(nombre = name_nombre,
                         apellido= name_apellido,
                         email= name_email,
                         profesion= name_profesion)
            profesor.save()
            return render(request, "aplicacion/base.html")
    else:
        miform= Profesorform()
    return render (request, "aplicacion/profesorform.html", {"form": miform})

@login_required
def searchprofesor(request):
    return render (request, "aplicacion/searchprofesor.html")

@login_required
def searchprofesor2(request):
    if request.GET['buscar']:
        patron= request.GET['buscar']
        profesores= Instructor.objects.filter(nombre__icontains= patron)
        contexto= {"profesores": profesores}
        return render(request, "aplicacion/profesores.html", contexto)
    
    return HttpResponse ("Vuelva a intentarlo, ingreso invalido, asegurate de llenar todos los campos")


@login_required
def estudiantesform(request):
    if request.method == "POST":
        miform=  Estudianteform(request.POST)
        if miform.is_valid():
            name_nombre= miform.cleaned_data.get('nombre')
            name_apellido= miform.cleaned_data.get('apellido')
            name_email= miform.cleaned_data.get('email')
            name_edad= miform.cleaned_data.get('edad')
            
            estudiante= Alumno(nombre = name_nombre,
                         apellido= name_apellido,
                         email= name_email,
                         hobbie= name_edad,
            )
            estudiante.save()
            return render(request, "aplicacion/base.html")
    else:
        miform= Estudianteform()
    return render (request, "aplicacion/estudianteform.html", {"form": miform})

@login_required
def searchestudiante(request):
    return render (request, "aplicacion/searchestudiante.html")

@login_required
def searchestudiante2(request):
    if request.GET['buscar']:
        patron= request.GET['buscar']
        estudiantes= Alumno.objects.filter(nombre__icontains= patron)
        contexto= {"estudiantes": estudiantes}
        return render(request, "aplicacion/estudiantes.html", contexto)
    
    return HttpResponse ("Vuelva a intentarlo, ingreso invalido, asegurate de llenar todos los campos")

#-----------------------------------------------------> CRUD


        #----------------------------------------> model profesores

@login_required
def updprofesor (request, id_profe ):
    profesor= Instructor.objects.get (id = id_profe)
    if request.method == "POST" :
        miForm = Profesorform(request.POST)
        if miForm.is_valid():
            profesor.nombre = miForm.cleaned_data.get('nombre')
            profesor.apellido = miForm.cleaned_data.get('apellido')
            profesor.email = miForm.cleaned_data.get('email')
            profesor.profesion = miForm.cleaned_data.get('profesion')
            profesor.save()
            return redirect(reverse_lazy('profesores'))
    else:
        miForm = Profesorform (initial = {

            'nombre' : profesor.nombre,
            'apellido' : profesor.apellido,
            'email' : profesor.email,
            'profesion' : profesor.profesion,

        })

    return render (request, "aplicacion/profesorform.html", {'form' : miForm})

@login_required
def delProfesor (request, id_profe):
    profesor = Instructor.objects.get(id=id_profe)
    profesor.delete()
    return redirect(reverse_lazy('profesores'))


@login_required
def buildprofesor(request):    
    if request.method == "POST":
        miForm = Profesorform(request.POST)
        if miForm.is_valid():
            p_nombre = miForm.cleaned_data.get('nombre')
            p_apellido = miForm.cleaned_data.get('apellido')
            p_email = miForm.cleaned_data.get('email')
            p_profesion = miForm.cleaned_data.get('profesion')
            profesor = Instructor(nombre=p_nombre, 
                              apellido=p_apellido,
                             email=p_email,
                             profesion=p_profesion,
                             )
            profesor.save()
            return redirect(reverse_lazy('profesores'))
    else:
        miForm = Profesorform()

    return render(request, "aplicacion/profesorform.html", {"form":miForm})

        #----------------------------------------------> model cursos

@login_required
def updcurso (request, id_curso ):
    curso = Clase.objects.get (id = id_curso)
    if request.method == "POST" :
        miForm = CursoForm(request.POST)
        if miForm.is_valid():
            curso.nombre = miForm.cleaned_data.get('nombre')
            curso.comision = miForm.cleaned_data.get('comision')
            curso.duracion = miForm.cleaned_data.get('duracion')
            curso.save()
            return redirect(reverse_lazy('cursos'))
    else:
        miForm = CursoForm (initial = {

            'nombre' : curso.nombre,
            'comision' : curso.comision,
            'duracion' : curso.duracion
            

        })

    return render (request, "aplicacion/cursoform2.html", {'form' : miForm})


@login_required
def delcurso (request, id_curso):
    curso = Clase.objects.get(id=id_curso)
    curso.delete()
    return redirect(reverse_lazy('cursos'))


@login_required
def buildcurso(request):    
    if request.method == "POST":
        miForm = CursoForm(request.POST)
        if miForm.is_valid():
            c_nombre = miForm.cleaned_data.get('nombre')
            c_comision = miForm.cleaned_data.get('comision')
            c_duracion = miForm.cleaned_data.get('duracion')
            
            curso = Clase(nombre=c_nombre, 
                              comision=c_comision,
                              duracion=c_duracion,
                             
                             )
            curso.save()
            return redirect(reverse_lazy('cursos'))
    else:
        miForm = CursoForm()

    return render(request, "aplicacion/cursoform2.html", {"form":miForm})


        #------------------------------------------------> model Estudiante 

@login_required
def updestudiante (request, id_estudiante ):
    estudiante = Alumno.objects.get (id = id_estudiante)
    if request.method == "POST" :
        miForm = Estudianteform(request.POST)
        if miForm.is_valid():
            estudiante.nombre = miForm.cleaned_data.get('nombre')
            estudiante.apellido = miForm.cleaned_data.get('apellido')
            estudiante.email = miForm.cleaned_data.get('email')
            estudiante.edad = miForm.cleaned_data.get('edad')
            estudiante.save()
            return redirect(reverse_lazy('estudiantes'))
    else:
        miForm = Estudianteform (initial = {

            'nombre' : estudiante.nombre,
            'apellido' : estudiante.apellido,
            'email' : estudiante.email,
            'edad' : estudiante.edad,
            

        })

    return render (request, "aplicacion/estudianteform.html", {'form' : miForm})


@login_required
def delestudiante (request, id_estudiante):
    estudiante = Alumno.objects.get(id=id_estudiante)
    estudiante.delete()
    return redirect(reverse_lazy('estudiantes'))


@login_required
def buildestudiante(request):    
    if request.method == "POST":
        miForm = Estudianteform(request.POST)
        if miForm.is_valid():
            e_nombre = miForm.cleaned_data.get('nombre')
            e_apellido = miForm.cleaned_data.get('apellido')
            e_email = miForm.cleaned_data.get('email')
            e_edad = miForm.cleaned_data.get('edad')
            
            estudiante = Alumno(nombre=e_nombre, 
                              apellido=e_apellido,
                              email=e_email,
                              edad=e_edad,
                             
                             )
            estudiante.save()
            return redirect(reverse_lazy('estudiantes'))
    else:
        miForm = Estudianteform()

    return render(request, "aplicacion/estudianteform.html", {"form":miForm})

        #----------------------------------------------> model proximas fechas

@login_required
def updfechaproxima (request, id_fechaproxima ):
    proximafecha = Fechaproxima.objects.get (id = id_fechaproxima)
    if request.method == "POST" :
        miForm = Fechasform(request.POST)
        if miForm.is_valid():
            proximafecha.nombre = miForm.cleaned_data.get('nombre')
            proximafecha.fechaProxima = miForm.cleaned_data.get('fechaProxima')
            proximafecha.duracion = miForm.cleaned_data.get('duracion')
            
            proximafecha.save()
            return redirect(reverse_lazy('fechas_proximas'))
    else:
        miForm = Fechasform (initial = {

            'nombre' : proximafecha.nombre,
            'fechaProxima' : proximafecha.fechaProxima,
            'duracion' : proximafecha.duracion,
            
            

        })

    return render (request, "aplicacion/fechaproximaform.html", {'form' : miForm})


@login_required
def delfechaproxima (request, id_fechaproxima):
    fecha = Fechaproxima.objects.get(id=id_fechaproxima)
    fecha.delete()
    return redirect(reverse_lazy('fechas_proximas'))


@login_required
def buildfechaproxima(request):    
    if request.method == "POST":
        miForm = Fechasform(request.POST)
        if miForm.is_valid():
            f_nombre = miForm.cleaned_data.get('nombre')
            f_fechaproxima = miForm.cleaned_data.get('fechaProxima')
            f_duracion = miForm.cleaned_data.get('duracion')
            
            fechaproxima = Fechaproxima (nombre = f_nombre, 
                              fechaProxima = f_fechaproxima,
                              duracion = f_duracion,
                             
                             )
            fechaproxima.save()
            return redirect(reverse_lazy('fechas_proximas'))
    else:
        miForm = Fechasform()

    return render(request, "aplicacion/fechaproximaform.html", {"form":miForm})


#---------------------------------------------------> Login / logout / registracion

def loginrequest(request):
     if request.method == "POST":
        miForm = AuthenticationForm(request, data=request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get('username')
            password = miForm.cleaned_data.get('password')
            user = authenticate(username=usuario, password=password)
            if user is not None:
                login(request, user)

                try:
                    avatar = Avatar.objects.get(user=request.user.id).imagen.url
                except:
                    avatar = "/media/avatares/default.jpg"
                finally:
                    request.session["avatar"] = avatar

                return render(request, "aplicacion/base.html", {'mensaje': f'Acceso exitoso, bienvenido {usuario}'})
            else:
                return render(request, "aplicacion/login.html", {'form': miForm, 'mensaje': f'Datos invalidos, intente nuevamente'})
        else:
            return render(request, "aplicacion/login.html", {'form': miForm, 'mensaje': f'Datos invalidos, intente nuevamente'})

     miForm =   AuthenticationForm()      

     return render(request, "aplicacion/login.html", {"form":miForm})  


def registrou(request):
    if request.method == "POST":
        miForm = RegistroUsuariosForm(request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get('username')
            miForm.save()
            return render(request, "aplicacion/base.html")
    else:
        miForm =   RegistroUsuariosForm()      
    return render(request, "aplicacion/registro.html", {"form":miForm}) 

@login_required
def editPerfil(request):
    usuario = request.user
    if request.method == "POST":
        form = UEditForm(request.POST)
        if form.is_valid():
            usuario.email = form.cleaned_data.get('email')
            usuario.password1 = form.cleaned_data.get('password1')
            usuario.password2 = form.cleaned_data.get('password2')
            usuario.first_name = form.cleaned_data.get('first_name')
            usuario.last_name = form.cleaned_data.get('last_name')
            usuario.save()
            return render(request,"aplicacion/base.html")
        else:
            return render(request,"aplicacion/editPerfil.html", {'form': form, 'usuario': usuario.username})
    else:
        form = UEditForm(instance=usuario)
    return render(request, "aplicacion/editPerfil.html", {'form': form, 'usuario': usuario.username})


@login_required
def aggAvatar(request):
    if request.method == "POST":
        form = AvatarFormulario(request.POST, request.FILES)
        if form.is_valid():
            u = User.objects.get(username=request.user)

            
            avatarViejo = Avatar.objects.filter(user=u)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()

            
            avatar = Avatar(user=u, imagen=form.cleaned_data['imagen'])
            avatar.save()

            
            imagen = Avatar.objects.get(user=request.user.id).imagen.url
            request.session["avatar"] = imagen
            return render(request,"aplicacion/base.html")
    else:
        form = AvatarFormulario()
    return render(request, "aplicacion/aggAvatar.html", {'form': form })