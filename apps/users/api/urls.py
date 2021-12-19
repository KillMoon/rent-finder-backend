from rest_framework.routers import DefaultRouter

from . import views

# register URL like
# router.register(r"users", UsersAPIView)
router = DefaultRouter()
router.register(r"", views.UsersViewSet, basename="user")
urlpatterns = router.urls
