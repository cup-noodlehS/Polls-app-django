from django.contrib import admin
from .models import Question, Choice, Set

class ChoiceInline(admin.TabularInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
        ("Set", {"fields": ["set"]})
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

class SetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["set_name"]}),  
    ]
    list_display = ["set_name"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Set, SetAdmin)
