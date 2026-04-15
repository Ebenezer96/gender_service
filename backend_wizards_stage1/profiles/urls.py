from django.urls import path
from .views import ProfileListCreateView, ProfileDetailView

urlpatterns = [
    path("api/profiles", ProfileListCreateView.as_view(), name="profile-list-create"),
    path("api/profiles/<uuid:profile_id>", ProfileDetailView.as_view(), name="profile-detail"),
]