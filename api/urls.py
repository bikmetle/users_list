from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path("v1/", include(("api.v1.urls", "v1"), namespace="v1")),
    path('token/', ObtainAuthToken.as_view(), name='get_token'),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="swagger-ui",
    ),
]
