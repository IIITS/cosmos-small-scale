from django.contrib import admin
from btp.models import *

admin.site.register(Application)
admin.site.register(Batch)
admin.site.register(BTPProject)
admin.site.register(BTPStudent)
admin.site.register(Faculty)
admin.site.register(Semester)
admin.site.register(BTPWeek)
admin.site.register(BTPEvalPanel)
admin.site.register(BTPEvalSet)
admin.site.register(BTPProjectGroup)
admin.site.register(BTPSetWeek)
admin.site.register(BTPSubmission)
admin.site.register(Resources)
admin.site.register(BTPMarks)
admin.site.site_header = 'Cosmos Administrator'

