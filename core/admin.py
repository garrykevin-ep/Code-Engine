from django.contrib import admin
from .models import *
# Register your models here.


class TestCaseInline(admin.TabularInline):
	model = TestCase

class ProblemAdmin(admin.ModelAdmin):
 inlines = [
 	TestCaseInline,
 ]


admin.site.register(Test)
admin.site.register(Problem,ProblemAdmin)
#extra
admin.site.register(ProblemStatus)
admin.site.register(TestStatus)
admin.site.register(Submission)
