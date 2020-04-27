from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from student.models import Quetions,Subject,topic,Analysis,Student,Imaged,Forum,Forum_reply,Kc_ana,Kc
from expert.models import Expert
from django.contrib.auth import authenticate, login, logout
import datetime


# Create your views here.

def login(request):
    print("skhbisvvbiubfvudbuyb")
    if request.method == 'POST':
        print("innnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        email=request.POST['email']
        print("email milaaaaaaaaaaaaa")
        password=request.POST['password']

        l=Expert.objects.filter(email=email,password=password)
        print(email,password,l,l[0])
        if len(l):
            request.session['email']=email #session started
            request.session['name']=l[0].name
            return HttpResponseRedirect(reverse('home1'))
        else:
            return HttpResponseRedirect(reverse('login')+'?login_failure=true')
    return render(request,'expert/signin.html')

def home1(request):
    return render(request,'expert/dash.html',{"sp":1})

def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('login'))

def add_user(request):
    if request.method == 'POST':
        username=request.POST.get('uname')
        password=request.POST.get('password')
        email=request.POST.get('email')
        institute=request.POST.get('institute')
        standard=request.POST.get('std')
        age=request.POST.get('age')
        u_id = Student.objects.all()
        user_id = []
        for i in u_id:
            user_id.append(i.id)
        print(user_id)
        uid = max(user_id)
        print(uid)
        
        sdata = Student(id = uid + 1,age=age,email=email,institute=institute,standard=standard,name=username,password=password,speed=1)
        sdata.save()
    return render(request,'expert/user.html',{"sp":1})

def add_subject(request):
    if request.method == 'POST':
        sub_name=request.POST.get('sname')
        subb = Subject.objects.all()
        sid = []
        for i in subb:
            sid.append(i.sub_id)
        print(sid)
        s_id = max(sid)
        print(s_id)
        subb = Subject(id = s_id +1,sub_id = s_id + 1,sub_name=sub_name,mots_id=1,confidence_s=1)
        subb.save()     
    return render(request,'expert/subject.html',{"sp":1})

def add_topic(request):
    # if request.method == 'GET':
    print("getttttttttttttt")
    sb = Subject.objects.all()
    print(sb,sb[0])
    sb_name = []
    sb_id = []
    for i in sb:
        print(i)
        sb_name.append(i.sub_name)
        sb_id.append(i.id)
    print(sb_name,sb_id)
    subject = zip(sb_name,sb_id)
    kct = Kc.objects.all()
    print(kct,kct[1])
    kc_name = []
    kc_id = []
    for i in kct:
        print(i)
        print(i.kc_name,i.kc_id)
        kc_name.append(i.kc_name)
        kc_id.append(i.kc_id)
    print(kc_id,kc_name)
    kcid = zip(kc_id,kc_name)
    kcid1 = kcid
    kcid2 = kcid
    if request.method == 'POST':
        top_name=request.POST['name']
        sub_name=request.POST['subject']
        kc1=request.POST['kc1']
        kc2=request.POST['kc2']
        kc3=request.POST['kc3']
        kc = ""
        if kc1 != "0":
            kc = kc + kc1
        elif kc2 != "0":
            kc = kc + kc2
        elif kc3 != "0":
            kc = kc + kc3
        print(kc)
        print(top_name,sub_name,kc,"posttt")
        tp = topic.objects.all()
        tid = []
        for i in tp:
            tid.append(i.top_id)
        print(tid)
        t_id = max(tid)
        print(t_id)
        top = topic(id = t_id +1,top_id = t_id + 1,top_name = top_name,level = 2,sub_id =int(sub_name),kcids = kc)
        top.save()
    return render(request,'expert/topic.html',{"sp":1,"s":subject,"kc":kcid,"kc22":kcid1,"kc33":kcid2})

def add_questions(request):
     print("gettttttttttttttMyyyyyyyyyy")
     sb = Subject.objects.all()
     print(sb,sb[0])
     sb_name = []
     sb_id = []
     for i in sb:
        print(i)
        sb_name.append(i.sub_name)
        sb_id.append(i.id)
     print(sb_name,sb_id)
     subject = zip(sb_name,sb_id)
     tp = topic.objects.all()
     print(tp,tp[0])
     tp_name = []
     tp_id = []
     for i in tp:
        print(i)
        print(i.top_name,i.top_id)
        tp_name.append(i.top_name)
        tp_id.append(i.top_id)
     print(tp_id,tp_name)
     tpp = zip(tp_id,tp_name)
     if request.method == 'POST':
        questions = request.POST.get('que')
        option1=request.POST.get('op1')
        option2=request.POST.get('op2')
        option3=request.POST.get('op3')
        option4=request.POST.get('op4')
        subject_id=request.POST.get('subject')
        topic_id=request.POST.get('topic')
        hint=request.POST.get('hint')
        ans=request.POST.get('ans')
        step1=request.POST.get('step1')
        step2=request.POST.get('step2')
        step3=request.POST.get('step3')
        solution=request.POST.get('solution')
        kcid=request.POST.get('kcid')
        print(kcid)
        que = Quetions(que_id = 1, question= questions,opt_1="dssfsf",opt_2="dssfsf",opt_3="dssfsf",opt_4="dssfsf",sub_id=1,top_id= 1,hint="sfsdfd",level=1,ans=1,solution="reggdf",
        avg_time=1,best_time=1,que_no=1,attempt=0,test_id=0,speed=1,kcid=kcid,step1=step1,step2=step2,step3=step3)
        que.save()
     return render(request,'expert/question.html')