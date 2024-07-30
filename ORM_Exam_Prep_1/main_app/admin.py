from django.contrib import admin
from .models import Director, Actor, Movie


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'nationality')
    list_filter = ('years_of_experience',)
    search_fields = ('full_name', 'nationality')
    search_help_text = "Search by full name or nationality."


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'nationality')
    list_filter = ('is_awarded',)
    search_fields = ('full_name',)
    search_help_text = "Search by full name."
    readonly_fields = ('last_updated',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'storyline', 'rating', 'director')
    list_filter = ('is_awarded', 'is_classic', 'genre')
    search_fields = ('title', 'director__full_name')
    search_help_text = "Search by movie title or director's full name."
    readonly_fields = ('last_updated',)
