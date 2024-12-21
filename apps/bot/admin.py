from django.contrib import admin

from apps.bot.models import * # noqa
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "category")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "rating", "is_active")

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "start_date", "end_date")

@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "book_name", "date")

