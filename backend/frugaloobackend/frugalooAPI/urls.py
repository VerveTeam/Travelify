# urls.py
from django.urls import include, path
from rest_framework import routers
from .views import (
    GeneratePlan,
    FetchTripDetails,
    FetchPlan,
    UpdateUserTripProgress,
    FetchUserTripProgress,
    AddFinanceLog,
    GeminiSuggestions,
    UpdateTrip,
    GenerateMessageView,
    GetPhotosForLocations
)

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("generate-trip/", GeneratePlan.as_view(), name="generate-trip"),
    path("fetch-trip-details/", FetchTripDetails.as_view(), name="fetch-trip-details"),
    path("fetch-plan/", FetchPlan.as_view(), name="fetch-plan"),
    path("update-progress/", UpdateUserTripProgress.as_view(), name="update-progress"),
    path(
        "fetch-trip-progress/",
        FetchUserTripProgress.as_view(),
        name="fetch-trip-progress",
    ),
    path("gemini-suggestions/", GeminiSuggestions.as_view(), name="gemini-suggestions"),
    path("update-plan/", UpdateTrip.as_view(), name="update-plan"),
    path("add-finance-log/", AddFinanceLog.as_view(), name="add_finance_log"),
    path("generate-message/", GenerateMessageView.as_view(), name="generate-message"),
     path('get-photos-for-locations/', GetPhotosForLocations.as_view(), name='get_photos_for_locations'),
]
