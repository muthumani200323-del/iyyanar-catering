import os

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

PHOTO_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXT = {".mp4", ".webm", ".mov", ".m4v"}


class GalleryItem(models.Model):
    """A photo or video shown in the Gallery. Only admins can add or delete these."""

    PHOTO, VIDEO, LINK = "photo", "video", "link"
    KINDS = [(PHOTO, "Photo"), (VIDEO, "Video"), (LINK, "Video link")]

    kind = models.CharField(max_length=10, choices=KINDS, editable=False, default=PHOTO)
    file = models.FileField(upload_to="gallery/", blank=True)
    link = models.URLField("Video link (YouTube / Facebook / Instagram)", blank=True)
    caption = models.CharField(max_length=140, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created", "-id"]
        verbose_name = "Gallery photo / video"
        verbose_name_plural = "Gallery photos / videos"

    def __str__(self):
        return self.caption or (os.path.basename(self.file.name) if self.file else self.link)

    def clean(self):
        if not self.file and not self.link:
            raise ValidationError("Upload a photo or video, or paste a video link.")
        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext not in PHOTO_EXT | VIDEO_EXT:
                raise ValidationError("Use a JPG, PNG, WEBP, MP4, WEBM or MOV file.")

    def save(self, *args, **kwargs):
        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()
            self.kind = self.VIDEO if ext in VIDEO_EXT else self.PHOTO
        else:
            self.kind = self.LINK
        super().save(*args, **kwargs)


class Review(models.Model):
    """Customers send reviews from the website. They show publicly only after an admin approves."""

    name = models.CharField(max_length=80, blank=True)
    place = models.CharField("Town or village", max_length=80, blank=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(max_length=1500)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created", "-id"]

    def __str__(self):
        return f"{self.name or 'Customer'} - {self.rating} stars"


class Booking(models.Model):
    """Every booking request typed on the website is also saved here, so nothing is lost."""

    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=20)
    function = models.CharField(max_length=120, blank=True)
    date = models.DateField()
    guests = models.PositiveIntegerField()
    food = models.CharField(max_length=30, blank=True)
    delivery = models.CharField("Door delivery", max_length=10, blank=True)
    venue = models.CharField("Venue / address", max_length=250, blank=True)
    notes = models.TextField(blank=True)
    send_to = models.CharField("Sent to number", max_length=20, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created", "-id"]

    def __str__(self):
        return f"{self.name} - {self.function} - {self.date}"
