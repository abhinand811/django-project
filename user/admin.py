from django.contrib import admin

from user.models import Student, Teacher, Question, Comment, Department, Hod, Management, Account

admin.site.register(Account)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Department)
admin.site.register(Hod)
admin.site.register(Management)
