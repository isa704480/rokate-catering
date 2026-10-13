from django.urls import path

from . import api

# Slash'siz yo'llar: Next.js trailing slash'ni olib tashlaydi
urlpatterns = [
    path("site", api.site),
    path("home", api.home),
    path("services/<slug:slug>", api.service_detail),
    path("packages", api.packages),
    path("menu", api.menu),
    path("portfolio/<slug:slug>", api.portfolio_detail),
    path("partners", api.partners),
    path("legal/<slug:slug>", api.legal),
    path("sitemap", api.sitemap),
    path("inquiries", api.create_inquiry),
    path("partner-requests", api.create_partner_request),
]
