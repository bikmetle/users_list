from django.urls import include, path
from rest_framework.routers import SimpleRouter
from api.v1.users.views import UserViewSet

router = SimpleRouter(trailing_slash=False)

router.register("users", UserViewSet, basename="users")

urlpatterns = router.urls