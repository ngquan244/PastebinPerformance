from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Paste, Analytics
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Paste
from django.utils.timezone import now
from django.shortcuts import render
from django.shortcuts import redirect


@api_view(['POST'])
def create_paste(request):
    content = request.data.get("content")
    expires_in = request.data.get("expiration_time", None)  # Nhận từ frontend
    print(f"Received expiration_time: {expires_in}")  # Debug

    time_map = {
        "12s": 0.2,
        "1m": 1,
        "10m": 10,
        "1h": 60,
        "1d": 1440,
        "1w": 10080
    }

    if expires_in == "never":
        expires_at = None
    elif expires_in in time_map:
        expires_at = timezone.now() + timezone.timedelta(minutes=time_map[expires_in])
    else:
        return Response({"error": "Invalid expiration time"}, status=400)

    paste = Paste.objects.create(content=content, expires_at=expires_at)
    Analytics.objects.create(paste=paste)

    print(f"Created paste: {paste.id}, Expires At: {paste.expires_at}")  # Debug

    return Response({"id": paste.id, "url": f"/view/{paste.id}/"})


@api_view(['GET'])
def get_paste(request, paste_id):
    paste = get_object_or_404(Paste, id=paste_id)

    if paste.has_expired():
        paste.delete()
        return Response({"error": "Paste has expired."}, status=404)

    analytics, created = Analytics.objects.get_or_create(paste=paste)
    analytics.views += 1
    analytics.save()

    return Response({"content": paste.content, "views": analytics.views})


@api_view(['DELETE'])
def delete_paste(request, paste_id):
    paste = get_object_or_404(Paste, id=paste_id)
    paste.delete()
    return Response({"message": "Paste deleted successfully."})


def create_paste_page(request):
    if request.method == "POST":
        title = request.POST.get("title", "Untitled")
        content = request.POST.get("content")
        expires_in = request.POST.get("expiration_time")

        # Ánh xạ expiration_time thành số phút
        time_map = {
            "12s": 0.2,
            "1m": 1,
            "10m": 10,
            "1h": 60,
            "1d": 1440,
            "1w": 10080,
            "never": None
        }

        # Xác định expires_at
        if expires_in in time_map:
            expires_at = timezone.now() + timezone.timedelta(minutes=time_map[expires_in]) if time_map[expires_in] else None
        else:
            expires_at = None  # Mặc định nếu không hợp lệ

        # Tạo Paste
        paste = Paste.objects.create(title=title, content=content, expires_at=expires_at)
        Analytics.objects.create(paste=paste)

        print(f"Created paste: {paste.id}, Expires At: {paste.expires_at}")  # Debug

        return redirect(f"/{paste.id}")  # Chuyển hướng đến paste vừa tạo

    return render(request, "create_paste.html")


def paste_detail_page(request, paste_id):
    paste = get_object_or_404(Paste, id=paste_id)

    # Kiểm tra nếu paste đã hết hạn
    if paste.expires_at and paste.expires_at < now():
        return render(request, "paste_expired.html")  # Trang thông báo hết hạn

    # Nếu còn hiệu lực, tăng lượt xem
    analytics, created = Analytics.objects.get_or_create(paste=paste)
    analytics.views += 1
    analytics.save()

    return render(request, "paste_detail.html", {
        "paste": paste,
        "views": analytics.views
    })


def paste_list(request):
    pastes = Paste.objects.all()
    data = []

    for paste in pastes:
        analytics = Analytics.objects.filter(paste=paste).first()
        views = analytics.views if analytics else 0
        expired = paste.expires_at and paste.expires_at < timezone.now()
        data.append({"paste": paste, "views": views, "expired": expired})

    return render(request, "paste_list.html", {"pastes": data})


@csrf_exempt
def delete_paste(request, paste_id):
    if request.method == "POST":
        paste = get_object_or_404(Paste, id=paste_id)
        paste.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


def delete_expired_pastes(request):
    if request.method == "POST":
        Paste.objects.filter(expires_at__lt=timezone.now()).delete()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)