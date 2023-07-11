from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from .models import User, QRCode
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
import qrcode
import uuid
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import os
from .utils import create_shortened_url

# Create your views here.


def index(request):
    return render(request, 'pages/index.html')


def faq(request):
    return render(request, 'pages/faq.html')


def cookies(request):
    return render(request, 'pages/cookies.html')


def contract(request):
    return render(request, 'pages/contract.html')


def privacy(request):
    return render(request, 'pages/privacy.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['registerUsername']
        email = request.POST['registerEmail']
        password = request.POST['registerPassword']

        # Ensure password matches confirmation
        registerRepeatPassword = request.POST["registerRepeatPassword"]
        if password != registerRepeatPassword:
            return render(request, "pages/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "pages/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request, "pages/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["loginName"]
        password = request.POST["loginPassword"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "pages/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "pages/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def contact(request):
    return render(request, 'pages/contact.html')


def dashboard(request):

    if request.method == 'POST':
        url = request.POST['link']
        # insert here the qr url generator
        short_url = create_shortened_url()
        new_url = request.build_absolute_uri('/qr/') + short_url
        img = qrcode.make(new_url)
        temp_handle = NamedTemporaryFile(delete=False)
        img.save(temp_handle, 'png')

        qr = QRCode(user=request.user, link=url, short_url=short_url)
        with open(temp_handle.name, 'rb') as file_handle:
            qr.qr_code.save(f"{uuid.uuid4()}.png", File(file_handle))
        qr.save()

        os.unlink(temp_handle.name)

    qr_codes = QRCode.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'pages/dashboard.html', {'qrs': qr_codes})


def profile(request):

    if request.method == 'POST':

        user = User.objects.get(pk=request.user.id)

        username = user.username
        password = request.POST['password']
        new_password = request.POST['new_password']
        new_password2 = request.POST['new_password2']

        user = authenticate(request, username=username, password=password)

        if new_password != new_password2:
            messages.error(request, 'Passwords do not match')
            return HttpResponseRedirect(reverse("profile"))

        if new_password == '':
            messages.error(request, 'Password cannot be empty')
            return HttpResponseRedirect(reverse("profile"))

        if user is not None:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully')
            user = authenticate(request, username=username,
                                password=new_password)
            login(request, user)
            return HttpResponseRedirect(reverse("profile"))
        else:
            messages.error(request, 'Invalid password')
            return HttpResponseRedirect(reverse("profile"))

    else:
        return render(request, 'pages/profile.html')


def redirect_url_view(request, shortened_part):
    try:
        qr = QRCode.objects.get(short_url=shortened_part)
        qr.times_scanned = qr.times_scanned + 1
        qr.save()
        return HttpResponseRedirect(qr.link)
    except QRCode.DoesNotExist:
        raise Http404("QR Code does not exist")


def delete(request, qr_id):
    qr = QRCode.objects.get(pk=qr_id)
    qr.delete()
    return HttpResponseRedirect(reverse("dashboard"))
