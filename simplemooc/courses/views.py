from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.defaultfilters import slugify
from datetime import datetime

from .models import Course, Enrollment, Announcement, Lesson, Material
from .forms import ContactCourse, CommentForm,AnnouncementForm,CourseForm,LessonForm,MaterialForm
from .decorators import enrollment_required

def index(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    context = {
        'courses': courses
    }
    
    return render(request, template_name, context)

def create(request):
    courses = Course.objects.all()
    form = CourseForm(request.POST or None,request.FILES or None)

    if request.method == "POST":

        context = {"form":form,
                    "courses":courses}  
        if form.is_valid():
            create = form.save(commit=False)
            create.slug = slugify(create.name)
            create.start_date = datetime.today().strftime('%Y/%m/%d')
            create.save()
            messages.success(request, 'Curso cadastrado com sucesso')
                    
        return render(request,'courses/create.html',context)
    return render(request,'courses/create.html',{"courses":courses,"form":form})

def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST': 
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
    context['form'] = form
    context['course'] = course
    template_name = 'courses/details.html'
    return render(request, template_name, context)

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if created:
        # enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')

    return redirect('accounts:dashboard')

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course
    )
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }
    return render(request, template, context)

@login_required
@enrollment_required
def announcements(request, slug):
    template = 'courses/announcements.html'
    course = request.course
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
        
    return render(request, template, context)     

@login_required
@enrollment_required
def forum(request, slug): 
    course = request.course     
    form = AnnouncementForm(request.POST or None)
    #query_dict = request.POST.copy()
    print(request.POST)

    context = {
        'course': course,
        'announcements': course.announcements.all(),
        'form':form
    }
    if form.is_valid():
        forum_duvidas = form.save(commit=False)
        forum_duvidas.save()
        messages.success(request, 'Seu Anuncio foi criado com sucesso')
        return redirect('accounts:dashboard')


    return render(request,'courses/create_announcements.html',context)


@login_required
@enrollment_required
def create_aula(request,slug):
    course = request.course
    aula = LessonForm(request.POST or None)
    context = {
        'course': course,
        'aula' : course.announcements.all(),
        'form' : aula
    }
    if aula.is_valid():
        aula.save(commit=False)
        aula.save()
        messages.success(request,'Sua aula foi criada com sucesso')
    return render(request,'courses/create_aula.html',context)

@login_required
@enrollment_required
def create_material(request,slug):
    course = request.course
    material = MaterialForm(request.POST or None, request.FILES or None)
    context = {
        'course': course,
        'material' : course.announcements.all(),
        'form' : material
    }
    print(material.errors)
    if material.is_valid():
        material.save(commit=False)
        material.save()
        messages.success(request,'Seu material foi criada com sucesso')
    return render(request,'courses/create_material.html',context)


@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    print(request.POST)
    form = CommentForm(request.POST or None)
    print(request.POST)
    print(form.errors)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = Announcement.objects.get(pk=announcement.id)
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso')
    template = 'courses/show_announcement.html'
    context = {
        'course': course,
        'announcement': announcement,
        'form': form,
    }
    return render(request, template, context)

@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    template = 'courses/lessons.html'
    lessons = course.release_lessons()
    if request.user.is_staff:
        lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, template, context)

@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    print(lesson)
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta aula não está disponível')
        return redirect('courses:lessons', slug=course.slug)
    template = 'courses/lesson.html'
    context = {
        'course': course,
        'lesson': lesson
    }
    return render(request, template, context)

@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    url_video = "videos/" + str(material.file)[18:]
    print(url_video)
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Este material não está disponível')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)
    template = 'courses/material.html'
    context = {
        'course': course,
        'lesson': lesson,
        'material': material,
        'url' : url_video
    }
    return render(request, template, context)
