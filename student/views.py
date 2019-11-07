from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from student.models import Quetions

def home(request):
    return render(request,'student/index2.html')

def test(request):
    ele=Quetions.objects.all()
    print(ele)
    q = []
    h = []
    o1 = []
    o2 = []
    o3 = []
    o4 = []
    c = 0
    qi = []
    for i in ele:
        qi.append(i.que_id)
        q.append(i.question)
        h.append(i.hint)
        o1.append(i.opt_1)
        o2.append(i.opt_2)
        o3.append(i.opt_3)
        o4.append(i.opt_4)
        c = c + 1
    print(q,h,o1,o2,o3,o4,c,qi)
    z = zip(q,h,o1,o2,o3,o4,qi)
    return render(request,'student/test.html',{"z":z})

# "q":q,"h":h."o1":o1,"o2":o2,"o3":o3,"o4":o4