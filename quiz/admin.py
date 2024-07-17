# quiz/admin.py
from django.contrib import admin
from .models import Question, Choice, Result

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['text']}),
    ]
    inlines = [ChoiceInline]

class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_groups_display')
    search_fields = ['user__username']

    def get_groups_display(self, obj):
        return ", ".join(obj.get_groups())
    get_groups_display.short_description = 'Groups'

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Result, ResultAdmin)
