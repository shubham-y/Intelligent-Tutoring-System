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
        email=request.POST['email']
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
    st = Student.objects.all()
    std = len(st)
    subb = Subject.objects.all()
    subj = len(subb)
    topi = topic.objects.all()
    top = len(topi)
    kcss = Kc.objects.all()
    kcc = len(kcss)
    return render(request,'expert/dash.html',{"sp":1,"stu":std,"sub":subj,"top":top,"kcs":kcc})

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
    kcid1 = zip(kc_id,kc_name)
    kcid2 = zip(kc_id,kc_name)
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
     print("svsf")
     tpp = zip(tp_id,tp_name)
     kcs = Kc.objects.all()
     kc_name = []
     kc_id = []
     for i in kcs:
        print(i)
        print(i.kc_name,i.kc_id)
        kc_name.append(i.kc_name)
        kc_id.append(i.kc_id)
     print(kc_id,kc_name)
     kcs = zip(kc_id,kc_name)
     kcs2 = zip(kc_id,kc_name)
     kcs3 = zip(kc_id,kc_name)
     if request.method == 'POST':
        questions = request.POST.get('ques')
        option1=request.POST.get('op1')
        option2=request.POST.get('op2')
        option3=request.POST.get('op3')
        option4=request.POST.get('op4')
        sb_name=request.POST.get('subject')
        tp_name=request.POST.get('topic')
        hint=request.POST.get('hint')
        ans=request.POST.get('ans')
        kcid=request.POST.get('numkc')
        kc1=request.POST['kcc1']
        kc2=request.POST['kcc2']
        kc3=request.POST['kcc3']
        print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
        kcidd=""
        if int(kcid) == 1:
            print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
            step1=request.POST.get('step1','-1')
            print(step1)
            step2= -1
            step3= -1
            kcidd= kc1
            print(kcidd) 
        elif int(kcid) == 2:
            step1=request.POST.get('step1')
            print(step1)
            step2= request.POST.get('step2')
            print(step2)
            step3= -1
            kcidd=kc1+ ","+ kc2
            print(kcidd)
        else:
            step1=request.POST.get('step1','-1')
            step2= request.POST.get('step2','-1')
            step3= request.POST.get('step3','-1')
            kcidd=kc1 + ","+kc2+ ","+kc3
        solution=request.POST.get('solution')
        
        print(questions,option1,option2,option3,option4,sb_name,tp_name,hint,ans,solution,kcid,step1,step2,step3)
        qq = Quetions.objects.all()
        qid = []

        for i in qq:
            qid.append(i.que_id)
        
        q_id = max(qid)
        
        que = Quetions(id=q_id+1,que_id =q_id+1, question= questions,opt_1=option1,opt_2=option2,opt_3=option3,opt_4=option4,sub_id=int(sb_name),top_id=int(tp_name),hint=hint,level=1,ans=ans,
        solution=solution,avg_time=1,best_time=1,que_no=1,attempt=0,test_id=0,speed=1,kcid=kcidd,step1=int(step1),step2=int(step2),step3=int(step3))
        que.save()
     return render(request,'expert/question.html',{"sp":1,"subb":subject,"topp":tpp,"kcs":kcs,"kcs2":kcs2,"kcs3":kcs3})