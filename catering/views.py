import json
import os
from datetime import date

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import PHOTO_EXT, VIDEO_EXT, Booking, GalleryItem, Review

MAX_PHOTO_MB = 10
MAX_VIDEO_MB = 50


def index(request):
    """The one-page website."""
    reviews = Review.objects.filter(approved=True)
    avg = reviews.aggregate(a=Avg("rating"))["a"]
    context = {
        "items": GalleryItem.objects.all(),
        "reviews": reviews,
        "review_count": reviews.count(),
        "review_avg": round(avg, 1) if avg else None,
        # Only logged-in admins (staff) see pending reviews and the add / delete buttons.
        "pending": Review.objects.filter(approved=False) if request.user.is_staff else [],
    }
    return render(request, "index.html", context)


@require_POST
def book(request):
    """The booking form calls this in the background to save the booking in the database."""
    try:
        data = json.loads(request.body.decode("utf-8"))
        Booking.objects.create(
            name=str(data.get("name", ""))[:80].strip(),
            phone=str(data.get("phone", ""))[:20].strip(),
            function=str(data.get("function", ""))[:120].strip(),
            date=date.fromisoformat(str(data.get("date", ""))),
            guests=max(1, int(data.get("guests", 1))),
            food=str(data.get("food", ""))[:30],
            delivery=str(data.get("delivery", ""))[:10],
            venue=str(data.get("venue", ""))[:250],
            notes=str(data.get("notes", ""))[:2000],
            send_to=str(data.get("send_to", ""))[:20],
        )
    except (ValueError, TypeError, KeyError):
        return JsonResponse({"ok": False}, status=400)
    return JsonResponse({"ok": True})


@require_POST
def review_submit(request):
    """Customers can send a review. It is saved as 'not approved' until an admin approves it."""
    text = request.POST.get("text", "").strip()
    try:
        rating = int(request.POST.get("rating", "0"))
    except ValueError:
        rating = 0
    if not (1 <= rating <= 5) or not text:
        messages.error(request, "Please choose a star rating and write a few words.")
        return redirect("/#reviews")
    Review.objects.create(
        name=request.POST.get("name", "").strip()[:80],
        place=request.POST.get("place", "").strip()[:80],
        rating=rating,
        text=text[:1500],
    )
    messages.success(request, "Thank you! Your review will appear here after the owner approves it.")
    return redirect("/#reviews")


# ---------------- admin-only actions ----------------

@staff_member_required
@require_POST
def gallery_add(request):
    files = request.FILES.getlist("files")
    link = request.POST.get("link", "").strip()
    caption = request.POST.get("caption", "").strip()[:140]
    if not files and not link:
        messages.error(request, "Choose a photo or video, or paste a video link.")
        return redirect("/#gallery")
    added = 0
    for f in files:
        ext = os.path.splitext(f.name)[1].lower()
        if ext in PHOTO_EXT:
            limit = MAX_PHOTO_MB
        elif ext in VIDEO_EXT:
            limit = MAX_VIDEO_MB
        else:
            messages.error(request, f"{f.name}: use JPG, PNG, WEBP, MP4, WEBM or MOV.")
            continue
        if f.size > limit * 1024 * 1024:
            messages.error(request, f"{f.name} is bigger than {limit} MB.")
            continue
        GalleryItem.objects.create(file=f, caption=caption)
        added += 1
    if link:
        if link.startswith("https://"):
            GalleryItem.objects.create(link=link, caption=caption)
            added += 1
        else:
            messages.error(request, "The link must start with https://")
    if added:
        messages.success(request, f"Added {added} item(s) to the gallery.")
    return redirect("/#gallery")


@staff_member_required
@require_POST
def gallery_delete(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    if item.file:
        item.file.delete(save=False)  # also removes the file from the media folder
    item.delete()
    messages.success(request, "Deleted from the gallery.")
    return redirect("/#gallery")


@staff_member_required
@require_POST
def review_approve(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.approved = True
    review.save(update_fields=["approved"])
    messages.success(request, "Review approved. It is now visible on the website.")
    return redirect("/#reviews")


@staff_member_required
@require_POST
def review_delete(request, pk):
    get_object_or_404(Review, pk=pk).delete()
    messages.success(request, "Review deleted.")
    return redirect("/#reviews")
