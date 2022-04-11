from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

app_name = "user"
"""
ModelViewSetはDefaultRouterでのみ設定可能
"""
router = DefaultRouter()
router.register("profile", views.ProfileViewSet)
router.register("post", views.PostViewSet)
router.register("comment", views.CommentViewSet)

"""
genericsから継承した汎用Viewはurlpatternsで振り分け
"""
urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("myprofile/", views.MyProfileViewSet.as_view(), name="myprofile"),
    path("", include(router.urls)),
]
