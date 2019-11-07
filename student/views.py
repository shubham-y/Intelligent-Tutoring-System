from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from student.models import Quetions,Subject,topic,Analysis

def home(request):
    return render(request,'student/index2.html')

def start_test(request):
    subject = Subject.objects.all()
    sid = []
    sname = []
    for i in subject:
        sid.append(i.sub_id)
        sname.append(i.sub_name)
    print(sid,sname)
    sub = zip(sid,sname)
    topics = topic.objects.all()
    tid = []
    tname = []
    for i in topics:
        tid.append(i.top_id)
        tname.append(i.top_name)
    print(tid,tname)
    top = zip(tid,tname)

    if request.method == 'POST':
        sub_name = request.POST.get('subject', '')
        top_name = request.POST.get('topic', '')
        print(sub_name,top_name)
        ana = Analysis.objects.all()
        l = len(ana)
        print(l)
        l = l+1
        que = Analysis.objects.all().filter(user_id=1,sub_id = sub_name,topic_id=top_name).values("que_id")
        print(que)
        q = []
        for i in que:
            if i["que_id"] != None:
                q.append(i["que_id"])
        print(q,max(q))
        q_id = max(q)
        log = Analysis(id = l,user_id=1,sub_id = sub_name,topic_id=top_name)
        log.save()
        return HttpResponseRedirect(reverse('test', args=(l,q_id,)))


    return render(request,'student/start_test.html',{"sub":sub,"top":top})

def test(request,ana_id,que_id):
    # ana = Analysis.objects.all().filter(id = ana_id)
    # print(ana)
    # sub_id = ana[0].sub_id
    # top_id = ana[0].topic_id
    # print(ana,ana_id,sub_id,top_id)
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