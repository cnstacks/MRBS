from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import auth
from .models import *
import datetime


def login(request):
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        user = auth.authenticate(username=user, password=pwd)
        if user:
            auth.login(request, user)  # request.user
            return redirect("/index/")
    return render(request, "login.html")


def index(request):
    date = datetime.datetime.now().date()
    book_date = request.GET.get("book_date", date)
    time_choices = Book.time_choices
    room_list = Room.objects.all()
    book_list = Book.objects.filter(date=book_date)

    htmls = ""
    for room in room_list:
        htmls += "<tr><td>{}({})</td>".format(room.caption, room.num)
        for time_choice in time_choices:
            flag = False
            for book in book_list:
                if book.room.pk == room.pk and book.time_id == time_choice[0]:
                    flag = True
                    break  # 意味着这个单元格已经被预定;
            if flag:
                if request.user.pk == book.user.pk:
                    htmls += "<td class = 'active item' room_id={} time_id={} >{}</td>".format(room.pk, time_choice[0],
                                                                                          book.user)
                else:
                    htmls += "<td class = 'another_active item' room_id={} time_id={} >{}</td>".format(room.pk,
                                                                                                  time_choice[0],
                                                                                                  book.user)
            else:
                htmls += "<td room_id={} time_id={} class = 'item'></td>".format(room.pk, time_choice[0],
                                                                   )
        htmls += "</tr>"

    print(htmls)
    return render(request, "index.html", locals())
