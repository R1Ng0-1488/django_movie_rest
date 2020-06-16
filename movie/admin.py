from django.contrib import admin
from django import forms

from .models import Category, Actor, Genre, Movies, MovieShots, RatingStar, Rating, Review

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MoviesAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())


    class Meta:
        model = Movies
        fields = '__all__'

    def clean_trailer(self):
        val = self.cleaned_data['trailer']
        if '=' in val:
            sp = val.split('=')
            val = 'https://www.youtube.com/embed/' + sp[-1]
            return val
        return val


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url' )
    list_display_links = ('name', 'id')


class ReviewsInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ('name', 'email')


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'tagline', 'draft')
    list_display_links = ('title', 'id')
    list_filter = ('category', 'genre', 'year')
    search_fields = ('title', 'description', 'category__name')
    inlines = [ReviewsInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    form = MoviesAdminForm
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'), )
            }),
        (None, {
            'fields': (('description', 'poster', 'trailer'), )
            }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'), )
            }),
        ('Actors', {
            'classes': ('collapse',),
            'fields': (('actors', 'genre', 'directors', 'category'), )
            }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'), )
            }),
        ('Options', {
            'fields': (('url', 'draft'), )
            }),
    )

    def get_image(self):
        pass

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f"{message_bit}")

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change', )

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change', )

    get_image.short_description = 'Постер'

@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'parent', 'movie')
    list_display_links = ('name', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star','ip', 'movie')


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value',)

admin.site.register(Category, CategoryAdmin)
