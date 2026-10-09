from django.contrib import admin

from .models import Booking, GalleryItem, Review

admin.site.site_header = "Sri Iyyanar Catering - Admin"
admin.site.site_title = "Sri Iyyanar Catering"
admin.site.index_title = "Manage the website"


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "kind", "created")
    list_filter = ("kind",)
    fields = ("file", "link", "caption")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "place", "rating", "approved", "created")
    list_filter = ("approved", "rating")
    list_editable = ("approved",)
    search_fields = ("name", "place", "text")
    actions = ["approve_selected"]

    @admin.action(description="Approve selected reviews (show on website)")
    def approve_selected(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "function", "date", "guests", "food", "created")
    list_filter = ("date", "food", "delivery")
    search_fields = ("name", "phone", "function", "venue")
    date_hierarchy = "date"
