from __future__ import annotations

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class SchoolYear(models.Model):
    name = models.CharField(max_length=32, unique=True)  # e.g. "2025-2026"
    slug = models.SlugField(max_length=48, unique=True, blank=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    class Meta:
        ordering = ["-start_year", "-end_year"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class StandardCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)  # e.g. "CSTA", "ISTE"

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Standard(models.Model):
    category = models.ForeignKey(
        StandardCategory,
        on_delete=models.PROTECT,
        related_name="standards",
    )
    code = models.CharField(max_length=64)  # e.g. "2-AP-11"
    description = models.TextField(blank=True)  # optional global description

    class Meta:
        ordering = ["category__name", "code"]
        constraints = [
            models.UniqueConstraint(
                fields=["category", "code"],
                name="uniq_standard_code_per_category",
            )
        ]

    def __str__(self) -> str:
        return f"{self.category.name} · {self.code}"


class Artifact(models.Model):
    class Category(models.TextChoices):
        ACTIVITIES = "activities", "Activities"
        CODING = "coding-activities", "Coding Activities"
        PRESENTATIONS = "presentations", "Presentations"
        PROJECTS = "projects", "Projects"

    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name="artifacts")
    category = models.CharField(max_length=32, choices=Category.choices)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    description = models.TextField(blank=True)

    standards = models.ManyToManyField(
        Standard,
        through="ArtifactStandard",
        related_name="artifacts",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["school_year", "category", "slug"],
                name="uniq_artifact_slug_per_year_category",
            )
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.school_year} · {self.get_category_display()})"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse(
            "portfolio:artifact_detail",
            kwargs={
                "year_slug": self.school_year.slug,
                "category": self.category,
                "slug": self.slug,
            },
        )


class ArtifactStandard(models.Model):
    """
    Selected standard for an artifact + per-artifact note/description.
    """
    artifact = models.ForeignKey(
        Artifact,
        on_delete=models.CASCADE,
        related_name="artifact_standards",
    )
    standard = models.ForeignKey(
        Standard,
        on_delete=models.PROTECT,
        related_name="artifact_standards",
    )
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["standard__category__name", "standard__code"]
        constraints = [
            models.UniqueConstraint(
                fields=["artifact", "standard"],
                name="uniq_standard_per_artifact",
            )
        ]

    def __str__(self) -> str:
        return f"{self.artifact.title} · {self.standard}"


class ArtifactImage(models.Model):
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="artifact_images/%Y/%m/")
    caption = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"Image for {self.artifact.title}"


class ArtifactVideo(models.Model):
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)  # embed URL recommended
    file = models.FileField(upload_to="artifact_videos/%Y/%m/", blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.title or f"Video for {self.artifact.title}"

