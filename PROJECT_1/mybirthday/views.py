from django.shortcuts import render
import datetime
now = datetime.datetime.now()

# Create your views here.
def index(request):
    return render(request, "mybirthday/index.html", {
        "mybirthday": now.month == 8 and now.day == 14
    })