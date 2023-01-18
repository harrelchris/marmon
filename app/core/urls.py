from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("public.urls"), name="public"),
    path("account/", include("account.urls"), name="account"),
    path("dashboard/", include("dashboard.urls"), name="dashboard"),
    path("sso/", include("sso.urls"), name="sso"),
]
