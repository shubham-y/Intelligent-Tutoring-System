from django.contrib import admin
from student.models import Quetions,Subject,topic,Analysis,Student,Imaged,Forum,Forum_reply,Kc_ana
# Register your models here.
admin.site.register(Subject)
admin.site.register(topic)
admin.site.register(Analysis)
admin.site.register(Student)
admin.site.register(Imaged)

admin.site.register(Quetions)
admin.site.register(Forum)
admin.site.register(Forum_reply)
admin.site.register(Kc_ana)








# for model in models:
#     admin.site.register(model)