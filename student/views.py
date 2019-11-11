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
            for j in topics:
                talid.append(j.top_id)
                talnm.append(j.top_name)
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
                que = Analysis.objects.all().filter(sub_id = i,topic_id=j,test_id = 0)
                print(que)
                q = []
                for k in que:
                    if k.que_id != None:
                        q.append(k.que_id)
                mxa = max(q)
                print("heeeeeeeerrrrrrreeeeeeeeeeee",mxa,i)
                ques = Quetions.objects.all().filter(sub_id = i,top_id=j,test_id = 0)
                q1 = []
                for k1 in ques:
                    q1.append(k1.que_id)
                mx = max(q1)
                mn = min(q1)
                print("heeeeeeeerrrrrrreeeeeeeeeeee",mx,mn)
                p = mxa - mn + 1
                cp = mx - mn +1
                print("heeeeeeeerrrrrrreeeeeeeeeeee",p,cp)
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
    # print(sid,sname)
    sub = zip(sid,sname)
    topics = topic.objects.all()
    tid = []
    tname = []
    for i in topics:
        tid.append(i.top_id)
        tname.append(i.top_name)
    # print(tid,tname)
    top = zip(tid,tname)
    # subjj = Subject.objects.get(id = 2)
    # subjj.sub_name = "MATHEMATICS-dumdum"
    # subjj.save()

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
        qu_id = Analysis.objects.all().filter(user_id=1,sub_id = sub_name,topic_id=top_name,que_id = q_id)
        c = qu_id[0].correct
        w = qu_id[0].wasted
        ana_id = qu_id[0].id
        print(c,w,ana_id)
        ques = Quetions.objects.all().filter(que_id=q_id)

        if ques[0].que_no == 15:
            if c == 1 or w == 1:
                print("shhjsddddddddddddddssssss")
                return HttpResponseRedirect(reverse('test', args=(1111111111,(q_id),)))
        if c == 1 or w == 1:
            log = Analysis(id = l,user_id=1,sub_id = sub_name,topic_id=top_name,attempt = 0,hint = 0,correct = 0,wasted = 0, que_id = (q_id + 1),test_id = 0)
            log.save()
            return HttpResponseRedirect(reverse('test', args=(l,(q_id+1),)))
        else:
            return HttpResponseRedirect(reverse('test', args=(ana_id,q_id,)))


    return render(request,'student/start_test.html',{"sub":sub,"top":top})

def test(request,ana_id,que_id):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    ele=Quetions.objects.all().filter(que_id=que_id)
    sidd = ele[0].sub_id
    qn = ele[0].que_no
    if ana_id != 0 and ana_id != 1111111111:
        ana = Analysis.objects.all().filter(id=ana_id)
        print(qn,"at firstttttttttttttttttttttttttttttttttttttttttttt")
        # print(ele)
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
        qno = []
        for i in ele:
            qi.append(i.que_id)
            qno.append(i.que_no)
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
            lt = ana[0].last_time
        sol = ele[0].solution
        # print(q,h,o1,o2,o3,o4,c,qi)
        z = zip(q,h,o1,o2,o3,o4,qi,ai,qno)
        if att < 3:
            if request.method == 'POST':
                opt = request.POST.get('opt', '-2')
                if int(opt) != -2:
                    hint = request.POST.get('hint', '0')
                    time = request.POST.get('time', '0')
                    t = int(time)
                    if att == 0:
                        log22 = Analysis.objects.get(id = ana_id)
                        log22.last_time = t
                        log22.save()
                    else:
                        log23 = Analysis.objects.get(id = ana_id)
                        t = t + lt
                        log23.last_time = t
                        log23.save()
                    print(lt,t)
                    print("timeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",time)
                    a = ana[0].attempt
                    a = a + 1
                    log = Analysis.objects.get(id = ana_id)
                    log.attempt = a
                    log.hint = ah
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
                        log1 = Analysis.objects.get(id = ana_id)
                        log1.hint = 1
                        log1.save()
                    elif h == 1 and ah == 2:
                        log2 = Analysis.objects.get(id = ana_id)
                        log2.hint = 3
                        log2.save()
                    if h == 0 and a == 2:
                        h = 2
                        log3 = Analysis.objects.get(id = ana_id)
                        log3.hint = 2
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
                        log33 = Quetions.objects.get(id = que_id)
                        bt = ele[0].best_time
                        avt = ele[0].avg_time
                        avtt = ele[0].attempt
                        if bt == 0 or bt == None:
                            log33.best_time = t
                        elif bt > t:
                            log33.best_time = t
                        if avt == 0 or avt == None:
                            log33.avg_time = t
                            log33.attempt = 1
                        else:
                            avgt = avt * avtt
                            avggt = avgt + t
                            attem = avtt + 1
                            aver_t = int(avggt/attem)
                            log33.avg_time = aver_t
                            log33.attempt = attem
                        log33.save()
                        que_id = que_id + 1
                        a_id = ana_id + 1
                        log6 = Analysis.objects.get(id = ana_id)
                        log6.hint = h
                        log6.correct = 1
                        log6.save()
                        if qn < 15:
                            log7 = Analysis(id = a_id,que_id=que_id,user_id=1,sub_id = sub_id,topic_id=top_id,attempt = 0,hint = 0,correct = 0,wasted = 0,test_id = 0)
                            log7.save()
                        else:
                            a_id = 0
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
                        if a == 3:
                            t1 = ana[0].last_time
                            log331 = Quetions.objects.get(id = que_id)
                            bt1 = ele[0].best_time
                            avt1 = ele[0].avg_time
                            avtt1 = ele[0].attempt
                            if bt1 == 0 or bt1 == None:
                                log331.best_time = t1
                            elif bt1 > t1:
                                log331.best_time = t1
                            if avt1 == 0 or avt1 == None:
                                log331.avg_time = t1
                                log331.attempt = 1
                            else:
                                avgt1 = avt1 * avtt1
                                avggt1 = avgt1 + t1
                                attem1 = avtt1 + 1
                                aver_t1 = int(avggt1/attem1)
                                log331.avg_time = aver_t1
                                log331.attempt = attem1
                            log331.save()
                            log9 = Analysis.objects.get(id = ana_id)
                            log9.wasted = 1
                            log9.save()
                        m = 1
                        return render(request,'student/test.html',{"z":z,"m":m,"msg":msg,"k":k,"x":x,"so":sol})
                else:
                    k=11
                    m = 1
                    return render(request,'student/test.html',{"z":z,"m":m,"msg":msg,"k":k,"x":x,"so":sol})
        else:
            if request.method == 'POST':
                x = 1
                ah = ana[0].hint
                att = ana[0].attempt
                que_id = que_id + 1
                a_id = ana_id + 1
                log6 = Analysis.objects.get(id = ana_id,)
                log6.wasted = 1
                log6.save()
                if qn < 15:
                    log8 = Analysis(id = a_id,que_id=que_id,user_id=1,sub_id = sub_id,topic_id=top_id,attempt = 0,hint = 0,correct = 0,wasted = 0,test_id = 0)
                    log8.save()
                else:
                    a_id = 0
                return HttpResponseRedirect(reverse('test', args=(a_id,que_id,)))
    elif ana_id == 0:
        k = 0
        print("hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        return render(request,'student/test.html',{"k":k,"sid":sidd})
    elif ana_id == 1111111111:
        k = -1
        print("hereeeeeeeeeeeeeeeeeeeeeeeeee","-11111111111111")
        return render(request,'student/test.html',{"k":k,"sid":sidd})
    print(qn,"at lastttttttttttttttttttttttttttttttttttttttttt")
    return render(request,'student/test.html',{"z":z,"m":m,"msg":msg,"x":x,"so":sol})

def start_test2(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    subject = Subject.objects.all()
    sid = []
    sname = []
    for i in subject:
        sid.append(i.sub_id)
        sname.append(i.sub_name)
    # print(sid,sname)
    sub = zip(sid,sname)
    topics = topic.objects.all()
    tid = []
    tname = []
    for i in topics:
        tid.append(i.top_id)
        tname.append(i.top_name)
    # print(tid,tname)
    top = zip(tid,tname)
    # subjj = Subject.objects.get(id = 2)
    # subjj.sub_name = "MATHEMATICS-dumdum"
    # subjj.save()

    if request.method == 'POST':
        sub_id = request.POST.get('subject', '')
        top_id = request.POST.get('topic', '')
        # print(sub_name,top_name)
        # ana = Analysis.objects.all()
        # l = len(ana)
        # print(l)
        # l = l+1
        # que = Analysis.objects.all().filter(user_id=1,sub_id = sub_name,topic_id=top_name).values("que_id")
        # print(que)
        # q = []
        # for i in que:
        #     if i["que_id"] != None:
        #         q.append(i["que_id"])
        # print(q,max(q))
        # q_id = max(q)
        # qu_id = Analysis.objects.all().filter(user_id=1,sub_id = sub_name,topic_id=top_name,que_id = q_id)
        # c = qu_id[0].correct
        # w = qu_id[0].wasted
        # ana_id = qu_id[0].id
        # print(c,w,ana_id)
        # if c == 1 or w == 1:
        #     log = Analysis(id = l,user_id=1,sub_id = sub_name,topic_id=top_name,attempt = 0,hint = 0,correct = 0,wasted = 0, que_id = (q_id + 1))
        #     log.save()
        #     return HttpResponseRedirect(reverse('test', args=(l,(q_id+1),)))
        # else:
        return HttpResponseRedirect(reverse('test2', args=(sub_id,top_id)))


    return render(request,'student/start_test2.html',{"sub":sub,"top":top})

def test2(request,sub_id,top_id):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    ele=Quetions.objects.all().filter(sub_id=sub_id,top_id=top_id,test_id=1).order_by('que_id')
    # print(ele)
    print(ele[0].que_id)
    # ana = Analysis.objects.all().filter(id=ana_id)
    # print(id)
    x = 0
    # sub_id = ana[0].sub_id
    # top_id = ana[0].topic_id
    # user_id = ana[0].user_id
    # print(ana,ana_id,sub_id,top_id)
    
    q = []
    # h = []
    o1 = []
    o2 = []
    o3 = []
    o4 = []
    c = 0
    qi = []
    ans = []
    # ai = []
    for i in ele:
        qi.append(i.que_id)
        q.append(i.question)
        # h.append(i.hint)
        o1.append(i.opt_1)
        o2.append(i.opt_2)
        o3.append(i.opt_3)
        o4.append(i.opt_4)
        ans.append(i.ans)
        # ai.append(ana_id)
        c = c + 1
        m = 0
        msg = ""
        # ah = ana[0].hint
        # att = ana[0].attempt
        # print("printttttt",ah)
    # print(q,h,o1,o2,o3,o4,c,qi)
    z = zip(q,o1,o2,o3,o4,qi)
    if request.method == 'POST':
        c = 0
        correct,wasted,left=0,0,0
        # print(request.POST.get('opt3'))
        for i in qi:
            if request.POST.get('opt'+str(i)) is None:
                left+=1
            elif request.POST.get('opt'+str(i))==str(ans[c]):
                correct+=1
            else:
                wasted+=1
            c+=1
        time = request.POST.get('time','0')
        print(correct,wasted,left,time)
        log = Analysis(user_id=1,sub_id = sub_id,topic_id=top_id,last_time=int(time),attempt = (correct+wasted),hint = len(qi),correct = correct,wasted = wasted,test_id = 1)
        log.save()
        return HttpResponseRedirect(reverse('start_test2'))



    # if att < 3:
    #     if request.method == 'POST':
    #         opt = request.POST.get('opt', '')
    #         hint = request.POST.get('hint', '0')
    #         time = request.POST.get('time', '0')
    #         print("timeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",time)
    #         a = ana[0].attempt
    #         a = a + 1
    #         log = Analysis.objects.get(id = ana_id)
    #         log.attempt = a
    #         log.hint = ah
    #         log.save()
    #         h = int(hint)
    #         print("hintttttttt",h,a)
    #         if h == 0 and ah == 1:
    #             h = ah
    #             print("printttttttttt::::",h)
    #         # if h == 0 and ah == 0:
    #         #     log4 = Analysis(id = ana_id,hint = 1,attempt = a)
    #         #     log4.save()
    #         elif h == 1 and ah == 0:
    #             log1 = Analysis.objects.get(id = ana_id)
    #             log1.hint = 1
    #             log1.save()
    #         elif h == 1 and ah == 2:
    #             log2 = Analysis.objects.get(id = ana_id)
    #             log2.hint = 3
    #             log2.save()
    #         if h == 0 and a == 2:
    #             h = 2
    #             log3 = Analysis.objects.get(id = ana_id)
    #             log3.hint = 2
    #             log3.save()
    #         if h == 0 and a == 3:
    #             h = 2
    #         print("hinttttttt: ",h)
    #         print("attemptttt: ",a)
    #         print(type(opt))
    #         print(opt,"fhj",hint)
    #         print("hvjhvcj zvjv")
    #         anss = Quetions.objects.all().filter(que_id=que_id)
    #         # print(anss)
    #         ans = anss[0].ans
    #         # print(ans)
    #         k = 0
    #         if ans == int(opt):
    #             que_id = que_id + 1
    #             a_id = ana_id + 1
    #             log6 = Analysis.objects.get(id = ana_id)
    #             log6.hint = h
    #             log6.correct = 1
    #             log6.save()
    #             log7 = Analysis(id = a_id,que_id=que_id,user_id=1,sub_id = sub_id,topic_id=top_id,attempt = 0,hint = 0,correct = 0,wasted = 0)
    #             log7.save()
    #             return HttpResponseRedirect(reverse('test', args=(a_id,que_id,)))
    #         else:
    #             if h == 0 and a == 1:
    #                 k=1
    #                 msg = "hint!"
    #             elif h == 1 and a ==1:
    #                 k =7
    #                 msg = "Don't hurry. Try once more."
    #             elif h == 2 and a ==2:
    #                 k = 2
    #                 msg = "Warning: Pl check hint and last attempt"
    #             elif h == 1 and a == 2:
    #                 k = 3
    #                 msg = "Learn site"
    #             elif h == 2 and a == 3:
    #                 k = 6
    #                 x = 1
    #                 msg = "You havn't checked the hint. This is disappointing."
    #             elif h == 3 and a == 3:
    #                 k = 4
    #                 x = 1
    #                 msg = "learn site and solution"
    #             elif h == 1 and a == 3:
    #                 k = 5
    #                 x = 1
    #                 msg = "Solution"
    #             if a == 3:
    #                 log9 = Analysis.objects.get(id = ana_id)
    #                 log9.wasted = 1
    #                 log9.save()
    #             m = 1
    #             return render(request,'student/test.html',{"z":z,"m":m,"msg":msg,"k":k,"x":x})
    # else:
    #     if request.method == 'POST':
    #         x = 1
    #         ah = ana[0].hint
    #         att = ana[0].attempt
    #         que_id = que_id + 1
    #         a_id = ana_id + 1
    #         log6 = Analysis.objects.get(id = ana_id,)
    #         log6.wasted = 1
    #         log6.save()
    #         log8 = Analysis(id = a_id,que_id=que_id,user_id=1,sub_id = sub_id,topic_id=top_id,attempt = 0,hint = 0,correct = 0,wasted = 0)
    #         log8.save()
    #         return HttpResponseRedirect(reverse('test', args=(a_id,que_id,)))
    return render(request,'student/test2.html',{"z":z,'sid':sub_id,'tid':top_id,"m":m,"msg":msg,"x":x})

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
        que = Analysis.objects.all().filter(sub_id = sub_id,topic_id=j,test_id = 0).values("que_id")
        print(que)
        q = []
        for i in que:
            if i["que_id"] != None:
                q.append(i["que_id"])
        print(q,max(q))
        mx.append(max(q))
    print(mx,"hereeeeeeeeeeeeeeeeeeeeeeee")
    lstt = []
    corr = []
    for j in tid:
        que2 = Analysis.objects.all().filter(sub_id = sub_id,topic_id=j,test_id = 0)
        lst = 0
        cor = 0
        for h in que2:
            lst = lst + h.last_time
            cor = cor + h.correct
        corr.append(cor)
        lstt.append(lst)
    print("lasttttttttttt timeeeeeeeee",lstt)
    mxx = []
    for i in mx:
        que1 = Analysis.objects.all().filter(que_id = i,test_id = 0)
        c1 = que1[0].correct
        w1 = que1[0].wasted
        if c1 == 1 or w1 == 1:
            mxx.append(i)
        else:
            mxx.append(i - 1)
    qn = []
    for i in mxx:
        if mxx != 0:
            ques1 = Quetions.objects.all().filter(que_id = i,test_id = 0)
            qn.append(ques1[0].que_no)
        else:
            qn.append(0)
    print(mxx,qn,"hereeeeeeeeeeeeeeeeeeeeeeee")
    quet = []
    avtt = []
    for i in range(len(tid)):
        ques = Quetions.objects.all().filter(sub_id = sub_id,top_id=tid[i],test_id = 0)
        qte = []
        avt = 0
        cor = 0
        for j in ques:
            x1 = j.que_no
            if x1 <= qn[i]:
                qt = []
                qt.append(j.que_no)
                qt.append(j.question)
                k = j.ans
                if k == 1:
                    qt.append(j.opt_1)
                elif k == 2:
                    qt.append(j.opt_2)
                elif k == 3:
                    qt.append(j.opt_3)
                else:
                    qt.append(j.opt_4)
                qt.append(j.avg_time)
                avt = avt + j.avg_time
                qt.append(j.solution)
                qte.append(qt)
        avtt.append(avt)
        quet.append(qte)
    # print(quet)
    sub = Subject.objects.all().filter(sub_id = sub_id).values("sub_name")
    sub_nm = sub[0]["sub_name"]
    print(sub_nm)
    act = []
    for k in range(len(corr)):
        act.append(((corr[k])/qn[k])*100)
    print("fvdbdgbsddgdffddddddddddddddddddd",qn,corr,act)
    tt = zip(tid,tname,quet,lstt,avtt,act)
    # was = []
    # for jj in range(qn):
    #     was.append = qn[i] - corr[i]
    

    return render(request,'student/analyse.html',{"sub_nm":sub_nm,"tt":tt,"tid":tid})

def ajax_load_action(request):
    # print("AJax")
    subid=request.GET.get('subid')
    t=topic.objects.filter(sub_id=subid)
    # print(t)
    return render(request, 'student/topic_ajax.html', {'t': t})