from django.urls import path

from .views import ArtifactDetailView, ArtifactListView, HomeView, YearOverviewView

app_name = "portfolio"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("<slug:year_slug>/", YearOverviewView.as_view(), name="year_overview"),
    path("<slug:year_slug>/<slug:category>/", ArtifactListView.as_view(), name="artifact_list"),
    path(
        "<slug:year_slug>/<slug:category>/<slug:slug>/",
        ArtifactDetailView.as_view(),
        name="artifact_detail",
    ),
]