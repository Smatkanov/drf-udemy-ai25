from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import (UserProfile,Category,Course,Lesson,Assignment,ExamQuestion,Variants,ExamAnswer,Submission,Certificate,Question,Exam,
                     Review,Cart,CartItem,Favorite,Message)

@admin.register(Course,Category,Lesson)
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(UserProfile)
admin.site.register(Assignment)
admin.site.register(ExamQuestion)
admin.site.register(Variants)
admin.site.register(ExamAnswer)
admin.site.register(Submission)
admin.site.register(Question)
admin.site.register(Exam)
admin.site.register(Certificate)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
admin.site.register(Message)