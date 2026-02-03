from modeltranslation.translator import TranslationOptions,register

from .models import Course, Category, Lesson


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('title',)