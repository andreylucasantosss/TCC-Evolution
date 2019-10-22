from django import forms
from django.core.mail import send_mail
from django.conf import settings

from simplemooc.core.mail import send_mail_template

from .models import Comment,Announcement,Course,Lesson,Material


class ContactCourse(forms.Form):

    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(
        label='Mensagem/Dúvida', widget=forms.Textarea
    )

    def send_mail(self, course):
        subject = '[%s] Contato' % course
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
        }
        template_name = 'courses/contact_email.html'
        send_mail_template(
            subject, template_name, context, [settings.CONTACT_EMAIL]
        )
class AnnouncementForm(forms.ModelForm):


    #course = forms.ChoiceField(choices=[('0', '--Selecione--')]+    [(course.id, course.name) for course in Course.objects.all()])
    #title = forms.CharField(label='Titulo',max_length=100)
    #content = forms.CharField(label='Conteudo',max_length=100)

    class Meta:
        model = Announcement
        fields=['course','title','content']
        #widgets = {'course':forms.Select}
    # Envio antigo, sem o uso de template
    # def send_mail(self, course):
    #     subject = '[%s] Contato' % course
    #     message = 'Nome: %(name)s;E-mail: %(email)s;%(message)s'
    #     context = {
    #         'name': self.cleaned_data['name'],
    #         'email': self.cleaned_data['email'],
    #         'message': self.cleaned_data['message'],
    #     }
    #     message = message % context
    #     send_mail(
    #         subject, message, settings.DEFAULT_FROM_EMAIL,
    #         [settings.CONTACT_EMAIL]
    #     )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']

class CourseForm(forms.ModelForm):


    slug = forms.HiddenInput()

    class Meta:
        model = Course
        fields = ['name','description','about','image']

class LessonForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = ['name','description','course']

class MaterialForm(forms.ModelForm):
    
    #url_video = forms.HiddenInput()

    class Meta:
        model = Material
        fields = ['name','file','lesson']
