from django.contrib import admin

from .models import (
    Artifact,
    ArtifactImage,
    ArtifactStandard,
    ArtifactVideo,
    SchoolYear,
    Standard,
    StandardCategory,
)


class ArtifactStandardInline(admin.TabularInline):
    model = ArtifactStandard
    extra = 1
    autocomplete_fields = ("standard",)
    fields = ("standard", "note")


class ArtifactImageInline(admin.TabularInline):
    model = ArtifactImage
    extra = 1


class ArtifactVideoInline(admin.TabularInline):
    model = ArtifactVideo
    extra = 1


@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    list_display = ("title", "school_year", "category", "updated_at")
    list_filter = ("school_year", "category")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ArtifactStandardInline, ArtifactImageInline, ArtifactVideoInline]


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ("name", "start_year", "end_year")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(StandardCategory)
class StandardCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ("code", "category")
    list_filter = ("category",)
    search_fields = ("code", "description", "category__name")
    ordering = ("category__name", "code")
    autocomplete_fields = ("category",)
