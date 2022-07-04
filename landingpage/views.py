from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.
from .models import ContactMsg, Group, Links, Pupil, Course, Gallery, SocialName, Teacher, Location, SingCourse
from .forms import ContactForm, PupilForm, SignCourseForm, TeacherForm, GroupForm, LocationForm, CourseForm, GalleryForm, LinksForm, SocialForm


def AllView(request):
    context = {}
    context['teachers'] = Teacher.objects.all()
    context['gallery'] = Gallery.objects.all()
    context['location'] = Location.objects.all()
    context['courses'] = Course.objects.all()
    context['form'] = ContactForm()
    context['socials'] = Links.objects.all()
    context['sign_course_form'] = SignCourseForm()
    return render(request, 'landingpage/mainpage.html', context)

def msg_save(request):
    form = ContactForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has sent')
            return HttpResponseRedirect(reverse('landingpage:allview'))
        else:
            context = {'form': form}
            return render(request, 'landingpage/mainpage.html', context)


def sign_course_post(request):
    sign_course_form = SignCourseForm(request.POST)
    if request.method == "POST":
        if sign_course_form.is_valid():
            sign_course_form.save()
            messages.success(request, 'Your request has sent')
            return HttpResponseRedirect(reverse('landingpage:allview'))
    else:
        context = {'sign_course_form': sign_course_form}
        return render(request, 'landingpage/mainpage.html', context)



# user page ----------------------------------------------
class UserPageView(TemplateView):
    template_name = 'landingpage/user_page.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['teachers'] = Teacher.objects.filter(author=self.request.user.pk)
        context['gallery'] = Gallery.objects.filter(author=self.request.user.pk)
        context['location'] = Location.objects.filter(author=self.request.user.pk)
        context['courses'] = Course.objects.filter(author=self.request.user.pk)
        context['links'] = Links.objects.filter(name__author=self.request.user.pk)
        return context


def edit(request):
    return render(request, 'landingpage/landingpage_edit.html')


def user_edit(request, pk):
    return render(request, 'landingpage/landingpage_edit_user.html')


def JournalView(request):
    groups = Group.objects.all()
    students = Pupil.objects.all()
    teachers = Teacher.objects.all()
    show = ''
    ts = ''
    context = {}

    if request.method == "GET":
        group = request.GET.get('group')
        level = request.GET.get('level')
        teacher = request.GET.get('teacher')
        student = request.GET.get('student')
        paid = request.GET.get('paid')
        unpaid = request.GET.get('unpaid')
        if group:
            show = Group.objects.get(name=group)
            show = show.pupil_set.all()
        elif level:
            ts = Group.objects.filter(level=level)
        elif teacher:
            ts = Group.objects.filter(teacher__name=teacher)
        elif student:
            show = Pupil.objects.filter(name=student)
        elif paid:
            show = Pupil.objects.filter(paid=True)
        elif unpaid:
            show = Pupil.objects.filter(paid=False)
        context =  {'show': show, 'groups': groups, 'teachers': teachers, 'students': students, 'ts': ts}
        return render(request, 'landingpage/landingpage_journal.html', context)
    else:
        show = ''
    context = {'show': show, 'groups': groups, 'teachers': teachers, 'students': students, 'ts': ts}
    return render(request, 'landingpage/landingpage_journal.html', context)



# User journal -------------------------------------
def UserJournalView(request, pk):
    groups = Group.objects.filter(author=request.user.pk)
    students = Pupil.objects.filter(author=request.user.pk)
    teachers = Teacher.objects.filter(author=request.user.pk)
    show = ''
    ts = ''
    context = {}

    if request.method == "GET":
        group = request.GET.get('group')
        level = request.GET.get('level')
        teacher = request.GET.get('teacher')
        student = request.GET.get('student')
        paid = request.GET.get('paid')
        unpaid = request.GET.get('unpaid')
        if group:
            show = Group.objects.filter(author=request.user.pk).get(name=group)
            show = show.pupil_set.all()
        elif level:
            ts = Group.objects.filter(level=level).filter(author=request.user.pk)
        elif teacher:
            ts = Group.objects.filter(teacher__name=teacher, author=request.user.pk)
        elif student:
            show = Pupil.objects.filter(name=student).filter(author=request.user.pk)
        elif paid:
            show = Pupil.objects.filter(paid=True).filter(author=request.user.pk)
        elif unpaid:
            show = Pupil.objects.filter(paid=False).filter(author=request.user.pk)
        context =  {'show': show, 'groups': groups, 'teachers': teachers, 'students': students, 'ts': ts}
        return render(request, 'landingpage/landingpage_journal_user.html', context)
    else:
        show = ''
    context = {'show': show, 'groups': groups, 'teachers': teachers, 'students': students, 'ts': ts}
    return render(request, 'landingpage/landingpage_journal_user.html', context)


# Add Student ----------------------------------------------------
class StudenView(SuccessMessageMixin, CreateView):
    template_name = 'landingpage/landingpage_add.html'
    success_url = reverse_lazy('landingpage:add_student')
    form_class = PupilForm
    extra_context = {'add': 'student'}
    success_message = 'Student "%(name)s %(surname)s" has added'


    def get_initial(self):
        initial = CreateView.get_initial(self)
        initial['author'] = self.request.user.pk
        return initial

# Add Teacher ----------------------------------------------------
class TeacherView(SuccessMessageMixin, CreateView):
    template_name = 'landingpage/landingpage_add.html'
    success_url = reverse_lazy('landingpage:add_teacher')
    form_class = TeacherForm
    extra_context = {'add': 'teacher'}
    success_message = 'Teacher "%(name)s" has added'


    def get_initial(self):
        initial = CreateView.get_initial(self)
        initial['author'] = self.request.user.pk
        return initial


# Add Group ----------------------------------------------------
class GroupView(SuccessMessageMixin, CreateView):
    template_name = 'landingpage/landingpage_add.html'
    success_url = reverse_lazy('landingpage:add_group')
    form_class = GroupForm
    extra_context = {'add': 'group'}
    success_message = 'Group "%(name)s" has added'


    def get_initial(self):
        initial = CreateView.get_initial(self)
        initial['author'] = self.request.user.pk
        return initial

# Add Course ----------------------------------------------------
class CourseView(SuccessMessageMixin, CreateView):
    template_name = 'landingpage/landingpage_add.html'
    success_url = reverse_lazy('landingpage:add_course')
    form_class = CourseForm
    extra_context = {'add': 'course'}
    success_message = 'Course "%(name)s" has added'


    def get_initial(self):
        initial = CreateView.get_initial(self)
        initial['author'] = self.request.user.pk
        return initial

# Add Gallery ----------------------------------------------------
class GalleryView(SuccessMessageMixin, CreateView):
    template_name = 'landingpage/landingpage_add.html'
    success_url = reverse_lazy('landingpage:add_gallery')
    form_class = GalleryForm
    extra_context = {'add': 'gallery'}
    success_message = 'Image has added'


    def get_initial(self):
        initial = CreateView.get_initial(self)
        initial['author'] = self.request.user.pk
        return initial

# Add Location ----------------------------------------------------
class LocationView(SuccessMessageMixin, CreateView):
    template_name = 'landingpage/landingpage_add.html'
    success_url = reverse_lazy('landingpage:add_location')
    form_class = LocationForm
    extra_context = {'add': 'location'}
    success_message = 'Location has added'


    def get_initial(self):
        initial = CreateView.get_initial(self)
        initial['author'] = self.request.user.pk
        return initial

# Update Course --------------------------------------
class UpdateCourseView(SuccessMessageMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'landingpage/landingpage_update.html'
    extra_context = {'update': 'course'}
    success_message = 'Course "%(name)s" has updated'
    
    def get_success_url(self):
        success_url = reverse_lazy('landingpage:user_page', kwargs={'pk':self.request.user.pk})
        return success_url

# Update Teacher --------------------------------------
class UpdateTeacherView(SuccessMessageMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'landingpage/landingpage_update.html'
    extra_context = {'update': 'teacher'}
    success_message = 'Teacher "%(name)s" has updated'


    def get_success_url(self):
        success_url = reverse_lazy('landingpage:user_page', kwargs={'pk':self.request.user.pk})
        return success_url

# Update Location --------------------------------------
class UpdateLocationView(SuccessMessageMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'landingpage/landingpage_update.html'
    success_message = 'Location has updated'
    extra_context = {'update': 'location'}

    def get_success_url(self):
        success_url = reverse_lazy('landingpage:user_page', kwargs={'pk':self.request.user.pk})
        return success_url


# Update gallery --------------------------------------
class UpdateGalleryView(SuccessMessageMixin, UpdateView):
    model = Gallery
    form_class = GalleryForm
    template_name = 'landingpage/landingpage_update.html'
    extra_context = {'update': 'gallery'}
    success_message = 'Image has updated'


    def get_success_url(self):
        success_url = reverse_lazy('landingpage:user_page', kwargs={'pk':self.request.user.pk})
        return success_url


# Update Student --------------------------------------
class UpdatePupilView(SuccessMessageMixin, UpdateView):
    model = Pupil
    form_class = PupilForm
    template_name = 'landingpage/landingpage_journal_update.html'
    extra_context = {'update': 'student'}
    success_message = 'Student "%(name)s %(surname)s" has updated'

    def get_success_url(self):
        success_url = reverse_lazy('landingpage:user_journal', kwargs={'pk':self.request.user.pk})
        return success_url


# Update Group --------------------------------------
class UpdateGroupView(SuccessMessageMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'landingpage/landingpage_update.html'
    extra_context = {'update': 'group'} 
    success_message = 'Group "%(name)s" has updated'

    def get_success_url(self):
        success_url = reverse_lazy('landingpage:user_journal', kwargs={'pk':self.request.user.pk})
        return success_url     
    

# Delete Group --------------------------------------
class DelGroupView(DeleteView):
    model = Group
    template_name = 'landingpage/landingpage_delete_group.html'
    context_object_name = 'group'
    success_message = 'Group has deleted'

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        success_url = reverse_lazy('landingpage:user_journal', kwargs={'pk':self.request.user.pk})
        return success_url
    
    
# Delete Course --------------------------------------
class DelCourseView(DeleteView):
    model = Course
    template_name = 'landingpage/landingpage_delete_course.html'
    context_object_name = 'course'
    success_message = 'Course has deleted'


    def get_success_url(self):
        messages.success(self.request, self.success_message)
        success_url = reverse_lazy('landingpage:user_page', kwargs={'pk':self.request.user.pk})
        return success_url


# Delete Teacher --------------------------------------
class DelTeacherView(DeleteView):
    model = Teacher
    template_name = 'landingpage/landingpage_delete_teacher.html'
    context_object_name = 'teacher'
    success_message = 'Teacher has deleted'

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        success_url = reverse_lazy('landingpage:user_page', kwargs={'pk':self.request.user.pk})
        return success_url


# Delete Location --------------------------------------
class DelLocationView(DeleteView):
    model = Location
    template_name = 'landingpage/landingpage_delete_location.html'
    context_object_name = 'location'
    success_message = 'Location has deleted'

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        success_url = reverse_lazy('landingpage:user_page', kwargs={'pk':self.request.user.pk})
        return success_url


# Delete Gallery --------------------------------------
class DelGalleryView(DeleteView):
    model = Gallery
    template_name = 'landingpage/landingpage_delete_gallery.html'
    context_object_name = 'gallery'
    success_message = 'Image has deleted'

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        success_url = reverse_lazy('landingpage:user_page', kwargs={'pk':self.request.user.pk})
        return success_url


# Delete student -------------------------------------------------------------
class DelStudentView(DeleteView):
    model = Pupil
    template_name = 'landingpage/landingpage_delete_student.html'
    context_object_name = 'student'
    success_message = 'Student has deleted'


    def get_success_url(self):
        messages.success(self.request, self.success_message)
        success_url = reverse_lazy('landingpage:user_journal', kwargs={'pk':self.request.user.pk})
        return success_url
    

# Contact messages ---------------------------------------------------
class ContactMsgView(ListView):
    template_name = 'landingpage/landingpage_message.html'
    model = ContactMsg
    context_object_name = 'contact_msgs'


# Add social -------------------------------------------------------------
class AddSocialView(TemplateView):
    template_name = 'landingpage/landingpage_add_social.html'
    

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['social_form'] = SocialForm(initial={'author':self.request.user.pk})
        context['links_form'] = LinksForm()
        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        social_form = SocialForm(request.POST, initial={'author':self.request.user.pk})
        if social_form.is_valid():
            sf = social_form.save()
            links_form = LinksForm(request.POST, instance=sf)
            if links_form.is_valid():
                links_form.save()
                messages.success(request, 'Links of "%s" have added' % (sf.name))
                return HttpResponseRedirect(reverse('landingpage:add_social'))
        else:
            social_form = SocialForm(initial={'author':self.request.user.pk})
            links_form = LinksForm()
        context['social_form'] = social_form
        context['links_form'] = links_form
        return self.render_to_response(context)
    

# Update social -------------------------------------------------------------
def update_social(request, pk):
    social = SocialName.objects.get(pk=pk)
    form = SocialForm(instance=social)
    if request.method == 'POST':
        form = SocialForm(request.POST, instance=social)
        if form.is_valid():
            social = form.save()
            formset = LinksForm(request.POST, instance=social)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Links have updated')
                return HttpResponseRedirect(reverse('landingpage:user_page', kwargs={'pk': request.user.pk}))
    else:
        form = SocialForm(instance=social)
        formset = LinksForm(instance=social)
    context = {'form': form, 'formset': formset}
    return render(request, 'landingpage/landingpage_update.html', context)
    

# Delete social -------------------------------------------------------------
def del_social(request, pk):
    social = SocialName.objects.get(pk=pk)
    links = social.links_set.all()
    if request.method == 'POST':
        social.delete()
        messages.success(request, 'Links have deleted')
        return HttpResponseRedirect(reverse('landingpage:user_page', kwargs={'pk': request.user.pk}))
        
    else:
        context = {'social': social, 'links': links}
        return render(request, 'landingpage/landingpage_delete_social.html', context)



class SignMsgView(TemplateView):
    template_name = 'landingpage/sign_msg.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['msgs'] = SingCourse.objects.all()
        return context