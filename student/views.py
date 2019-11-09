from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from student.models import Quetions,Subject,topic,Analysis

def home(request):
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
        log = Analysis(id = l,user_id=1,sub_id = sub_name,topic_id=top_name,attempt = 0,hint = 0)
        log.save()
        return HttpResponseRedirect(reverse('test', args=(l,q_id,)))


    return render(request,'student/start_test.html',{"sub":sub,"top":top})

def test(request,ana_id,que_id):
    ele=Quetions.objects.all().filter(que_id=que_id)
    # print(ele)
    ana = Analysis.objects.all().filter(id=ana_id)
    print(id)
    x = 0
    sub_id = ana[0].sub_id
    top_id = ana[0].topic_id
    user_id = ana[0].user_id
    print(ana,ana_id,sub_id,top_id)
    
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
        m = 0
        msg = ""
        ah = ana[0].hint
        att = ana[0].attempt
        print("printttttt",ah)
    # print(q,h,o1,o2,o3,o4,c,qi)
    z = zip(q,h,o1,o2,o3,o4,qi,ai)
    if att < 3:
        if request.method == 'POST':
            opt = request.POST.get('opt', '')
            hint = request.POST.get('hint', '0')
            a = ana[0].attempt
            a = a + 1
            log = Analysis(id = ana_id,user_id=1,sub_id = sub_id,topic_id=top_id,attempt = a,hint = ah)
            log.save()
            h = int(hint)
            print("hintttttttt",h,a)
            if h == 0 and ah == 1:
                h = ah
                print("printttttttttt::::",h)
            # if h == 0 and ah == 0:
            #     log4 = Analysis(id = ana_id,hint = 1,attempt = a)
            #     log4.save()
            elif h == 1 and ah == 0:
                log1 = Analysis(id = ana_id,user_id=1,sub_id = sub_id,topic_id=top_id,hint = 1,attempt = a)
                log1.save()
            elif h == 1 and ah == 2:
                log2 = Analysis(id = ana_id,user_id=1,sub_id = sub_id,topic_id=top_id,hint = 3,attempt = a)
                log2.save()
            if h == 0 and a == 2:
                h = 2
                log3 = Analysis(id = ana_id,user_id=1,sub_id = sub_id,topic_id=top_id,hint = 2,attempt = a)
                log3.save()
            if h == 0 and a == 3:
                h = 2
            print("hinttttttt: ",h)
            print("attemptttt: ",a)
            print(type(opt))
            print(opt,"fhj",hint)
            print("hvjhvcj zvjv")
            anss = Quetions.objects.all().filter(que_id=que_id)
            # print(anss)
            ans = anss[0].ans
            # print(ans)
            k = 0
            if ans == int(opt):
                que_id = que_id + 1
                a_id = ana_id + 1
                log6 = Analysis(id = ana_id,user_id=1,sub_id = sub_id,topic_id=top_id,que_id = (que_id - 1),attempt = a,hint = h,correct = 1)
                log6.save()
                log7 = Analysis(id = a_id,user_id=1,sub_id = sub_id,topic_id=top_id,attempt = 0,hint = 0)
                log7.save()
                return HttpResponseRedirect(reverse('test', args=(a_id,que_id,)))
            else:
                if h == 0 and a == 1:
                    k=1
                    msg = "hint!"
                elif h == 1 and a ==1:
                    k =7
                    msg = "Don't hurry. Try once more."
                elif h == 2 and a ==2:
                    k = 2
                    msg = "Warning: Pl check hint and last attempt"
                elif h == 1 and a == 2:
                    k = 3
                    msg = "Learn site"
                elif h == 2 and a == 3:
                    k = 6
                    x = 1
                    msg = "You havn't checked the hint. This is disappointing."
                elif h == 3 and a == 3:
                    k = 4
                    x = 1
                    msg = "learn site and solution"
                elif h == 1 and a == 3:
                    k = 5
                    x = 1
                    msg = "Solution"
                m = 1
                return render(request,'student/test.html',{"z":z,"m":m,"msg":msg,"k":k,"x":x})
    else:
        if request.method == 'POST':
            x = 1
            ah = ana[0].hint
            att = ana[0].attempt
            que_id = que_id + 1
            a_id = ana_id + 1
            log6 = Analysis(id = ana_id,user_id=1,sub_id = sub_id,topic_id=top_id,que_id = (que_id - 1),attempt = att, hint = ah,correct = 0)
            log6.save()
            log8 = Analysis(id = a_id,user_id=1,sub_id = sub_id,topic_id=top_id,attempt = 0,hint = 0)
            log8.save()
            return HttpResponseRedirect(reverse('test', args=(a_id,que_id,)))
    return render(request,'student/test.html',{"z":z,"m":m,"msg":msg,"x":x})

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