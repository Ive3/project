from django.contrib import admin
from django.utils.safestring import mark_safe
# Register your models here.
from .models import Pupil, Teacher, Group, Gallery, SocialName, Links, Location, Course, ContactMsg, CourseImage, SingCourse


class LinksInline(admin.TabularInline):
    model = Links

class SocialAdmin(admin.ModelAdmin):
    inlines = (LinksInline,)
    list_per_page = 6
    search_fields = ('name', 'author__username')


class CourseImageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 6
    search_fields = ('name',)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_per_page = 6
    search_fields = ('name', 'price', 'author__username')



class GalleryAdmin(admin.ModelAdmin):
    list_display = ('get_image', )
    fields = (('image', 'get_image'), 'description', 'author')
    readonly_fields = ('get_image',)
    list_per_page = 6
    search_fields = ('description', 'author__username')


    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=80px>')
    
    get_image.short_description = 'current image'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'lesson_time', 'days_of_week', 'teacher', 'creaded_at', 'exists')
    list_editable = ('exists', 'level')
    list_filter = ('level', 'teacher', 'exists') 
    list_per_page = 6
    search_fields = ('name', 'teacher', 'level', 'lesson_time', 'author__username')



class PupilAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone', 'group', 'paid')
    list_editable = ('group', 'paid')
    list_filter = ('paid',) 
    list_per_page = 6
    search_fields = ('name', 'surname', 'phone', 'group', 'author__username')



class TeacherAdmin(admin.ModelAdmin):
    fields = ('name', 'image', 'get_image', 'expirience', 'strong_side', 'achievement', 'author')
    list_display = ('name', 'get_image')
    readonly_fields = ('get_image',)
    list_per_page = 6
    search_fields = ('name', 'author__username')



    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=80px>')

    get_image.short_description = 'Current image'


class LocationAdmin(admin.ModelAdmin):
    list_display = ('subway', 'get_image', )
    fields = (('image', 'get_image'), 'street', 'address', 'subway', 'author__username')
    readonly_fields = ('get_image',)
    list_per_page = 6
    search_fields = ('street', 'address', 'subwat', 'author__username')


    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=80px>')
    
    get_image.short_description = 'current image'

class ContactMsgAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'sent')
    list_per_page = 6
    search_fields = ('name', 'phone', 'author__username')


    
admin.site.register(Pupil, PupilAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(SocialName, SocialAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(ContactMsg, ContactMsgAdmin)
admin.site.register(CourseImage, CourseImageAdmin)
admin.site.register(SingCourse)