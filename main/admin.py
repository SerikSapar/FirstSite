from django.contrib import admin

from main.models import *


# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    pass


class ChoiceAdmin(admin.ModelAdmin):
    pass


class ShiAdmin(admin.ModelAdmin):
    pass


admin.site.register(Choice, ChoiceAdmin)

admin.site.register(Course, CourseAdmin)

admin.site.register(Shi, ShiAdmin)
