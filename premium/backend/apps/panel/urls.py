from django.urls import path

from . import views

# Slash'siz yo'llar (Next.js rewrite trailing slash'ni olib tashlaydi)
urlpatterns = [
    path("csrf", views.csrf),
    path("login", views.login_view),
    path("logout", views.logout_view),
    path("me", views.me),
    path("password", views.change_password),
    path("dashboard", views.dashboard),
    path("schema/<slug:key>", views.schema),
    path("r/<slug:key>", views.collection),
    path("r/<slug:key>/reorder", views.reorder),
    path("r/<slug:key>/export", views.export),
    path("r/<slug:key>/<int:pk>", views.item),
    path("r/<slug:key>/<int:pk>/toggle", views.toggle),
    path("r/<slug:key>/<int:pk>/c/<slug:rel>", views.child_create),
    path("r/<slug:key>/<int:pk>/c/<slug:rel>/reorder", views.child_reorder),
    path("r/<slug:key>/<int:pk>/c/<slug:rel>/<int:cid>", views.child_item),
]
