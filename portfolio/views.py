from __future__ import annotations

from dataclasses import dataclass

from django.db.models import Count
from django.http import Http404
from django.views.generic import DetailView, ListView, TemplateView

from .models import Artifact, SchoolYear


@dataclass(frozen=True)
class CategoryLink:
    key: str
    label: str


def category_links() -> list[CategoryLink]:
    return [CategoryLink(key=k, label=v) for k, v in Artifact.Category.choices]


class HomeView(TemplateView):
    template_name = "portfolio/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["years"] = SchoolYear.objects.all()
        ctx["categories"] = category_links()
        return ctx


class YearOverviewView(TemplateView):
    template_name = "portfolio/year_overview.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        year = SchoolYear.objects.get(slug=self.kwargs["year_slug"])

        counts = (
            Artifact.objects.filter(school_year=year)
            .values("category")
            .annotate(total=Count("id"))
        )
        count_map = {c["category"]: c["total"] for c in counts}

        ctx["year"] = year
        ctx["categories"] = [
            {"key": c.key, "label": c.label, "count": count_map.get(c.key, 0)}
            for c in category_links()
        ]
        return ctx


class ArtifactListView(ListView):
    model = Artifact
    template_name = "portfolio/artifact_list.html"
    context_object_name = "artifacts"
    paginate_by = 24

    def get_queryset(self):
        year = SchoolYear.objects.get(slug=self.kwargs["year_slug"])
        category = self.kwargs["category"]

        valid_categories = {k for k, _ in Artifact.Category.choices}
        if category not in valid_categories:
            raise Http404("Unknown category")

        return (
            Artifact.objects.filter(school_year=year, category=category)
            .select_related("school_year")
            .prefetch_related("artifact_standards__standard__category")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        year = SchoolYear.objects.get(slug=self.kwargs["year_slug"])
        category = self.kwargs["category"]
        ctx["year"] = year
        ctx["category"] = category
        ctx["category_label"] = dict(Artifact.Category.choices).get(category, category)
        return ctx


class ArtifactDetailView(DetailView):
    model = Artifact
    template_name = "portfolio/artifact_detail.html"
    context_object_name = "artifact"

    def get_queryset(self):
        return (
            Artifact.objects.select_related("school_year")
            .prefetch_related(
                "artifact_standards__standard__category",
                "images",
                "videos",
            )
        )

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        return queryset.get(
            school_year__slug=self.kwargs["year_slug"],
            category=self.kwargs["category"],
            slug=self.kwargs["slug"],
        )
