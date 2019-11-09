from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from student.models import Quetions,Subject,topic,Analysis,Student
from django.contrib.auth import authenticate, login, logout

def login(request):
    return render(request,'student/signin.html')

def login_action(request):
    email=request.POST['email']
    password=request.POST['password']

    l=Student.objects.filter(email=email,password=password)

    if len(l):
        request.session['email']=email #session started
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('login')+'?login_failure=true')

def register(request):
    return render(request,'student/signup.html')

def register_action(request):
    registered = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        standard = request.POST.get('standard')
        institute = request.POST.get('institute')
        password = request.POST.get('password')
        if not len(Student.objects.filter(email=email)): 
            if all(values is not None for values in [name,email,password,age,standard]):
                log = Student(name=name,email=email,age=age,standard=standard,institute=institute,password=password)
                log.save()
            registered = True 
            print("registered!")      
            return render(request,'student/signin.html',{"registered":registered,})
        else:
            return render(request,'student/signup.html',{"registered":registered,})

def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('login'))

def home(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    else:
        subject = Subject.objects.all()
        sid = []
        sname = []
        for i in subject:
            sid.append(i.sub_id)
            sname.append(i.sub_name)
        print(sid,sname)
        # sub = zip(sid,sname)
        tid = []
        tname = []
        for i in sid:
            topics = topic.objects.all().filter(sub_id = i)
            talid = []
            talnm = []
            for i in topics:
                talid.append(i.top_id)
                talnm.append(i.top_name)
            tid.append(talid)
            tname.append(talnm)
        print(tid,tname)
        acc = []
        c = []

        for i in sid:
            act = []
            ct=[]
            co=0
            for j in tid[i-1]:
                que = Analysis.objects.all().filter(sub_id = i,topic_id=j)
                print(que)
                q = []
                for k in que:
                    if k.que_id != None:
                        q.append(k.que_id)
                mxa = max(q)
                ques = Quetions.objects.all().filter(sub_id = i,top_id=j)
                q1 = []
                for k1 in ques:
                    q1.append(k1.que_id)
                mx = max(q1)
                mn = min(q1)
                p = mxa - mn + 1
                cp = mx - mn +1
                
                act.append(int((p/cp)*100))
                ct.append(co)
                co=co+1
            acc.append(act)
            c.append(ct)
        print(acc,c)
        final = []
        for i in range(len(acc)):
            s = []
            for j in range(len(acc[i])):
                s1 = []
                s1.append(tname[i][j])
                s1.append(acc[i][j])
                s.append(s1)
            final.append(s)
        print(final)
        z = zip(sid,sname,tid,final)
        print(z)


        return render(request,'student/dash.html',{"z":z})

def start_test(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
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
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    # ana = Analysis.objects.all().filter(id = ana_id)
    # print(ana)
    # sub_id = ana[0].sub_id
    # top_id = ana[0].topic_id
    # print(ana,ana_id,sub_id,top_id)
    ele=Quetions.objects.all().filter(que_id=que_id)
    # print(ele)
    q = []
    h = []
    o1 = []
    o2 = []
    o3 = []
    o4 = []
    c = 0
    qi = []
    ai = []
    for i in ele:
        qi.append(i.que_id)
        q.append(i.question)
        h.append(i.hint)
        o1.append(i.opt_1)
        o2.append(i.opt_2)
        o3.append(i.opt_3)
        o4.append(i.opt_4)
        ai.append(ana_id)
        c = c + 1
    # print(q,h,o1,o2,o3,o4,c,qi)
    z = zip(q,h,o1,o2,o3,o4,qi,ai)
    if request.method == 'POST':
        opt = request.POST.get('opt', '')
        print(type(opt))
        anss = Quetions.objects.all().filter(que_id=que_id)
        print(anss)
        ans = anss[0].ans
        print(ans)
        if ans == int(opt):
            que_id = que_id + 1
            return HttpResponseRedirect(reverse('test', args=(ana_id,que_id,)))


        return HttpResponseRedirect(reverse('test', args=(ana_id,que_id,)))
    return render(request,'student/test.html',{"z":z})

def analyse(request,sub_id):
    topics = topic.objects.all().filter(sub_id=sub_id).distinct()
    print(topics)
    tid = []
    tname = []
    for i in topics:
        tid.append(i.top_id)
        tname.append(i.top_name)
    print(tid,tname)
    mx = []
    for j in tid:
        que = Analysis.objects.all().filter(sub_id = sub_id,topic_id=j).values("que_id")
        print(que)
        q = []
        for i in que:
            if i["que_id"] != None:
                q.append(i["que_id"])
        print(q,max(q))
        mx.append(max(q))
    print(mx)
    quet = []
    for i in range(len(tid)):
        ques = Quetions.objects.all().filter(sub_id = sub_id,top_id=tid[i])
        # time = Analysis.objects.all().filter(sub_id = sub_id,topic_id=tid[i])
        qte = []
        for j in ques:
            qt = []
            qt.append(j.que_id)
            qt.append(j.question)
            qt.append(j.ans)
            qte.append(qt)
        quet.append(qte)
    print(quet)
    sub = Subject.objects.all().filter(sub_id = sub_id).values("sub_name")
    sub_nm = sub[0]["sub_name"]
    print(sub_nm)
    tt = zip(tid,tname,quet)

    
    return render(request,'student/analyse.html',{"sub_nm":sub_nm,"tt":tt})