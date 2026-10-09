from django.urls import path

from . import views

app_name = "catering"

urlpatterns = [
    path("", views.index, name="index"),
    path("book/", views.book, name="book"),
    path("review/", views.review_submit, name="review_submit"),
    # Admin-only (staff login required)
    path("gallery/add/", views.gallery_add, name="gallery_add"),
    path("gallery/<int:pk>/delete/", views.gallery_delete, name="gallery_delete"),
    path("review/<int:pk>/approve/", views.review_approve, name="review_approve"),
    path("review/<int:pk>/delete/", views.review_delete, name="review_delete"),
]
