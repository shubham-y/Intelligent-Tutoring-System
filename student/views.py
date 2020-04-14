from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from student.models import Quetions,Subject,topic,Analysis,Student,Imaged,Forum,Forum_reply,Kc_ana
from django.contrib.auth import authenticate, login, logout
import datetime
import pytesseract
 
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.remote.webdriver import WebDriver

# driver = webdriver.Chrome()
# driver.get('file:///C:/Users/RU/Desktop/its-launch.html')
# executor_url = driver.command_executor._url
# sessions_id = driver.session_id
# print(executor_url,sessions_id)

# def attach_to_session(executor_url, sessions_id):
#     original_execute = WebDriver.execute
#     def new_command_execute(self, command, params=None):
#         if command == "newSession":
#             # Mock the response
#             return {'success': 0, 'value': None, 'sessionId': sessions_id}
#         else:
#             return original_execute(self, command, params)
#     # Patch the function before creating the driver object
#     WebDriver.execute = new_command_execute
#     driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
#     driver.session_id = sessions_id
#     # Replace the patched function with original function
#     WebDriver.execute = original_execute
#     return driver

# curd = attach_to_session(executor_url, sessions_id)
# print(curd.current_url)
# nmnm = "kkhkjh"

# def sele(request):
#     print("inside sele")
#     curd.get('http://127.0.0.1:8000/home/') 
#     searchbox = curd.find_element_by_xpath('//*[@id="gsc-i-id1"]')
#     searchbox.send_keys('Set theory')
#     print("below sele url")
#     return render(request,'student/dash.html')

def getpred(kcidd):
    pred = 0.0
    slip = 0.07
    guess = 0.13
    transit = 0.3
    prev = float(kcidd[0])
    prev_groundtruth = str(kcidd[1]) 
    # print('prev: ')
    # print(prev)
    # print('prev_groundtruth: ')
    # print(prev_groundtruth)
    transitProb = 0.0
    if prev_groundtruth=='1':
        transitProb = (prev*(1 - slip))/(prev*(1-slip) + (1-prev)*guess)
    else:
        transitProb = (prev * slip) / (prev * slip + (1 - prev) * (1 - guess))
    # print('prev_groundtruth: ')
    # print(prev_groundtruth)
    # print('transitProb: ')
    # print(transitProb)
    prob = float(transitProb + (1 - transitProb) * transit)
    # print('prob: ')
    # print(prob)
    pred = float(prob * (1 - slip) + (1 - prob) * guess)
    return pred

def calthres(corr,prev_pred,pred_list):
    av = 0
    jj = 0
    # c = input()
    kcidd = [prev_pred,corr]
    print("Kcidd: ",kcidd)
    pred = getpred(kcidd)
    # pred_list.append(pred)
    if corr == 1:
        print("111111111111111111111111")
        if len(pred_list) == 1:
            avg = pred_list[0]
        elif len(pred_list) == 2:
            avg = 0.5*pred_list[0] + 0.5*pred_list[1]
        elif len(pred_list) == 3:
            avg = (1/3)*pred_list[0] + (1.1/3)*pred_list[1] + (0.9/3)*pred_list[2]
        elif len(pred_list) == 4:
            avg = (1.1/4)*pred_list[0] + (1/4)*pred_list[1] + (1/4)*pred_list[2] + (0.9/4)*pred_list[3]
        elif len(pred_list) == 5:
            avg = (1.1/5)*pred_list[0] + (1/5)*pred_list[1] + (1/5)*pred_list[2] + (1/5)*pred_list[3] + (0.9/5)*pred_list[4]
        elif len(pred_list) == 6:
            avg = (0.5/6)*pred_list[0] + (0.75/6)*pred_list[1] + (1.15/6)*pred_list[2] + (1.25/6)*pred_list[3] + (1.25/6)*pred_list[4] + (1.1/6)*pred_list[5]
        elif len(pred_list) == 7:
            avg = (0.55/7)*pred_list[0] + (0.7/7)*pred_list[1] + (0.8/7)*pred_list[2] + (1.2/7)*pred_list[3] + (1.3/7)*pred_list[4] + (1.3/7)*pred_list[5] + (1.15/7)*pred_list[6]
        else:
            lenn = len(pred_list)
            avg = (0.4/8)*pred_list[lenn - 8] + (0.5/8)*pred_list[lenn - 7] + (0.7/8)*pred_list[lenn - 6] + (1.15/8)*pred_list[lenn - 5] + (1.35/8)*pred_list[lenn - 4] + (1.35/8)*pred_list[lenn - 3] + (1.35/8)*pred_list[lenn - 2] + (1.2/8)*pred_list[lenn - 1]
        # avg = (avg) + pred
    else:
        print("000000000000000000000000000000000")
        if len(pred_list) == 1:
            avg = pred_list[0]
        elif len(pred_list) == 2:
            avg = 0.5*pred_list[0] + 0.5*pred_list[1]
        elif len(pred_list) == 3:
            avg = (0.95/3)*pred_list[0] + (1.05/3)*pred_list[1] + (1.1/3)*pred_list[2]
        elif len(pred_list) == 4:
            avg = (0.9/4)*pred_list[0] + (1/4)*pred_list[1] + (1/4)*pred_list[2] + (1.1/4)*pred_list[3]
        elif len(pred_list) == 5:
            avg = (0.75/5)*pred_list[0] + (0.9/5)*pred_list[1] + (1/5)*pred_list[2] + (1.05/5)*pred_list[3] + (1.3/5)*pred_list[4]
        elif len(pred_list) == 6:
            avg = (0.5/6)*pred_list[0] + (0.75/6)*pred_list[1] + (1.05/6)*pred_list[2] + (1.15/6)*pred_list[3] + (1.2/6)*pred_list[4] + (1.35/6)*pred_list[5]
        elif len(pred_list) == 7:
            avg = (0.55/7)*pred_list[0] + (0.75/7)*pred_list[1] + (0.85/7)*pred_list[2] + (1.05/7)*pred_list[3] + (1.2/7)*pred_list[4] + (1.25/7)*pred_list[5] + (1.35/7)*pred_list[6]
        else:
            lenn = len(pred_list)
            avg = (0.4/8)*pred_list[lenn - 8] + (0.5/8)*pred_list[lenn - 7] + (0.8/8)*pred_list[lenn - 6] + (1.2/8)*pred_list[lenn - 5] + (1.25/8)*pred_list[lenn - 4] + (1.325/8)*pred_list[lenn - 3] + (1.325/8)*pred_list[lenn - 2] + (1.2/8)*pred_list[lenn - 1]
        # avg = (avg) + pred
    kcidd[0] = pred
    
    print("pred: ",pred)
    av = avg
    # print(av)
    # print(pred_list)
    if av > 0.75 and len(pred_list) >= 4:
        jj = 1
    kcidd[1] = jj
    print(av)
    return kcidd

perm = [1,1,0,1,0,0,1,0,1]
pred_list = [0.6]
kcdi = [0.6,1]
# pred_list = [0.676]
# kcdi = [0.676,1]
ct = 1
for i in perm:
    ct = ct + 1
    pr_pr = kcdi[0]
    kcdi = calthres(i,pr_pr,pred_list)
    pred_list.append(kcdi[0])
    if kcdi[1] == 1:
        print("Pass",ct,perm)
        break

def login(request):
    return render(request,'student/signin.html')

def login_action(request):
    email=request.POST['email']
    password=request.POST['password']

    l=Student.objects.filter(email=email,password=password)

    if len(l):
        request.session['email']=email #session started
        request.session['name']=l[0].name
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
                u_id = Student.objects.all().filter(email=email)
                uid = u_id[0].id
                anaa = Analysis.objects.all()
                anaa_id = []
                for i in anaa:
                    anaa_id.append(i.id)
                mxq = max(anaa_id)
                print(anaa_id)
                print(mxq)
                topics = topic.objects.all()
                for i in topics:
                    mxq = mxq + 50
                    if i.top_id == 1:
                        ti = 1
                    elif i.top_id == 2:
                        ti = 31
                    elif i.top_id == 3:
                        ti = 46
                    elif i.top_id == 4:
                        ti = 16
                    log12 = Analysis(id = mxq,user_id= uid,sub_id = i.sub_id,topic_id= i.top_id,time = 0, last_time = 0,best_time = 0,attempt = 0,hint = 0,correct = 0,wasted = 0, que_id = ti,test_id = 0)
                    log12.save()
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
        print(request.session['email'])
        uid = Student.objects.all().filter(email = request.session['email'])
        print(uid[0].email,uid[0].id)
        u_id = uid[0].id
        spd = uid[0].speed
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
                print("hehehehehehe",talid,talnm)
            tid.append(talid)
            tname.append(talnm)
            print(tid,tname)
        print(tid,tname)
        acc = []
        c = []
        message = []
        st = []

        for i in sid:
            act = []
            ms1=[]
            ct=[]
            stt = []
            co=0
            for j in tid[i-1]:
                crr = wtt = 0
                que = Analysis.objects.all().filter(user_id = u_id ,sub_id = i,topic_id=j,test_id = 0)
                print(u_id,i,j)
                print(que)
                q = []
                for k in que:
                    if k.que_id != None:
                        q.append(k.que_id)
                    if k.correct == 1:
                        crr = crr +1
                    elif k.wasted == 1:
                        wtt = wtt + 1
                if (crr + wtt) == 0:
                    wtt = 1
                sttr = (crr / (crr + wtt))*100
                stt.append(int(sttr))
                print("sttsttsttsttsttstt",stt,sttr,q)
                print("quesssssssssss",q)
                mxa = max(q)
                qud = Analysis.objects.all().filter(user_id = u_id ,que_id = mxa,test_id = 0)
                print(qud[0].correct,qud[0].wasted)
                cr = qud[0].correct
                wt = qud[0].wasted
                if cr == 0 and wt == 0:
                    mxa = mxa - 1
                print("heeeeeeeerrrrrrreeeeeeeeeeee",mxa,i,j)
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
                kk = int((p/cp)*100)
                print(kk)
                act.append(kk)
                if kk < 34:
                    mss = "Beginner" 
                    ms1.append(mss)
                elif kk > 34 and kk <67:
                    mss = "Intermediate"
                    ms1.append(mss) 
                elif kk > 67:
                    mss = "Advanced"
                    ms1.append(mss)
                ct.append(co)
                co=co+1
            acc.append(act)
            message.append(ms1)
            c.append(ct)
            st.append(stt)
        print(st)
        print("jdhgvjvgvhdchschgvghdvhg",acc,c,message)
        final = []
        for i in range(len(acc)):
            s = []
            for j in range(len(acc[i])):
                s1 = []
                s1.append(tname[i][j])
                s1.append(acc[i][j])
                s1.append(message[i][j])
                s.append(s1)
            final.append(s)
        print("finallllllllll",final)
        z = zip(sid,sname,tid,final)
        print(z)
        strong = []
        weak = []
        print(tname)
        for y in sid:
            strong1 = []
            weak1 = []
            for k in range(0,len(tname[y-1])):
                if st[y-1][k] >=80:
                    strong1.append(tname[y-1][k])
                elif st[y-1][k] <=34:
                    weak1.append(tname[y-1][k])
                    print(weak1)
            strong.append(strong1)
            weak.append(weak1)
        print(strong,weak)
        sz = zip(sname,strong)
        wz = zip(sname,weak)
        adpt = 0
        for i in st:
            print(i)
            for j in i:
                adpt = adpt + j
        
        adpt = int(adpt/4)
        print(adpt)
        if adpt >= 75:
            mot = 1
        elif adpt >=50:
            mot = 2
        else:
            mot = 3
        im = Imaged.objects.all().filter(sub_id = 0 ,top_id = 0,mot_id = mot)
        path = []
        for i in im:
            path.append(i.location)
        print(path)

        return render(request,'student/dash.html',{"z":z,"sz":sz,"wz":wz,"sp":spd,"path":path,'username':request.session['name'],'useremail':request.session['email']})

def start_test(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    print(request.session['email'])
    uid = Student.objects.all().filter(email = request.session['email'])
    print(uid[0].email,uid[0].id)
    u_id = uid[0].id
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
        que = Analysis.objects.all().filter(user_id=u_id,sub_id = sub_name,topic_id=top_name).values("que_id")
        print(que)
        q = []
        for i in que:
            if i["que_id"] != None:
                q.append(i["que_id"])
        print(q,max(q))
        q_id = max(q)
        qu_id = Analysis.objects.all().filter(user_id=u_id,sub_id = sub_name,topic_id=top_name,que_id = q_id)
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
            log = Analysis(user_id=u_id,sub_id = sub_name,topic_id=top_name,time = 0, last_time = 0,best_time = 0,attempt = 0,hint = 0,correct = 0,wasted = 0, que_id = (q_id + 1),test_id = 0)
            log.save()
            print("shhjsddddddddddddddssssss niiiiii")
            lol = Analysis.objects.all().filter(user_id=u_id,sub_id = sub_name,topic_id=top_name,que_id = q_id + 1)
            l = lol[0].id
            print(l)
            return HttpResponseRedirect(reverse('test', args=(l,(q_id+1),)))
        else:
            return HttpResponseRedirect(reverse('test', args=(ana_id,q_id,)))


    return render(request,'student/start_test.html',{"sub":sub,"top":top,'username':request.session['name'],'useremail':request.session['email']})

def test(request,ana_id,que_id):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    print(request.session['email'])
    uid = Student.objects.all().filter(email = request.session['email'])
    print(uid[0].email,uid[0].id)
    u_id = uid[0].id
    aaaaid = ana_id
    ana = Analysis.objects.all().filter(id=ana_id)
    print(ana,ana_id)
    subid = ana[0].sub_id
    topid = ana[0].topic_id
    userid = ana[0].user_id
    ele=Quetions.objects.all().filter(que_id=que_id)
    sidd = ele[0].sub_id
    qn = ele[0].que_no
    qn_kc = ele[0].kcid
    kc_qne = qn_kc.split(",")
    kc_qn = []
    for i in kc_qne:
        kc_qn.append(int(i))
    print(kc_qn)
    kc_stat = Kc_ana.objects.all().filter(stu_id = u_id)
    kc_list = []
    status = 1
    kc_stat_list = []
    for i in kc_stat:
        kc_list.append(i.kc_id)
        kc_stat_list.append(i.status)
        if i.status == 0:
            status = 0
    print("jdjdjdjdjdjdjdjdjdjdjd",kc_list,status,kc_stat_list,kc_qn)
    if status == 1:
        aaaaid = ana_id
        ana_id = 0
    else:
        status1 = 1
        for i in kc_qn:
            j = kc_list.index(i)
            if kc_stat_list[j] == 0:
                status1 = 0
    
        if status1 == 1:
            logkc1 = Analysis(id = ana_id + 1,user_id=userid,sub_id = subid,topic_id=topid,time = 0, last_time = 0,best_time = 0,attempt = 0,hint = 0,correct = 0,wasted = 0, que_id = (que_id + 1),test_id = 0,status =1)
            logkc1.save()
            return HttpResponseRedirect(reverse('test', args=(ana_id + 1,que_id + 1,)))
    if request.method == 'GET':
        stepv1 = "-1"
        stepv2 = "-1"
        stepv3 = "-1"
        # atttr = 0
    if request.method == 'POST':
        
        hhin = int(request.POST.get('hint', '0'))
        opt = request.POST.get('opt', '-2')
        if len(kc_qn) == 3:
            step1 = request.POST.get('step1', '-22')
            stepv1 = step1
            step2 = request.POST.get('step2', '-22')
            stepv2 = step2
            step3 = request.POST.get('step3', '-22')
            stepv3 = step3
        elif len(kc_qn) == 2:
            if kc_qn.count(1) > 0 and kc_qn.count(2) > 0:
                step1 = request.POST.get('step1', '-22')
                stepv1 = step1
                step2 = request.POST.get('step2', '-22')
                stepv2 = step2
                stepv3 = "-1"
                step3 = "-22"
            elif kc_qn.count(1) > 0 and kc_qn.count(3) > 0:
                step1 = request.POST.get('step1', '-22')
                stepv1 = step1
                stepv3 = "-1"
                step3 = request.POST.get('step2', '-22')
                stepv2 = step3
                step2 = "-22"
            elif kc_qn.count(2) > 0 and kc_qn.count(3) > 0:
                stepv3 = "-1"
                step2 = request.POST.get('step1', '-22')
                stepv1 = step2
                step3 = request.POST.get('step2', '-22')
                stepv2 = step3
                step1 = "-22"
        elif len(kc_qn) == 1:
            if kc_qn.count(1) > 0:
                step1 = request.POST.get('step1', '-22')
                stepv1 = step1
                stepv2 = "-1"
                stepv3 = "-1"
                step2 = "-22"
                step3 = "-22"
            elif kc_qn.count(2) > 0:
                stepv2 = "-1"
                step2 = request.POST.get('step1', '-22')
                stepv1 = step2
                stepv3 = "-1"
                step1 = "-22"
                step3 = "-22"
            elif kc_qn.count(3) > 0:
                stepv2 = "-1"
                stepv3 = "-1"
                step3 = request.POST.get('step1', '-22')
                stepv1 = step3
                step1 = "-22"
                step2 = "-22"
        if int(opt) != -2:
            answer = Quetions.objects.all().filter(que_id=que_id)
            step1_a = answer[0].step1
            step2_a = answer[0].step2
            step3_a = answer[0].step3
            wr = []
            for ii in kc_qn:
                zzz = 0
                kc_data = Kc_ana.objects.all().filter(stu_id = u_id,kc_id = ii)
                # kc_datac = Kc_ana.objects.all().filter(stu_id = user_id,que_id = que_id,kc_id = 1)
                print(kc_data)
                pr_list = kc_data[0].p_list
                pre_list = []
                print(len(pr_list),"LLLLLLLLLLLLLLLLLLLLLL")
                if len(pr_list) == 0:
                    zzz = 1
                else:
                    for i in pr_list.split(","):
                        pre_list.append(float(i))
                print(pre_list)
                kcid_id = kc_data[0].id
                if ii == 1:
                    if float(step1_a) == float(step1) or float(step1_a) == float(step2) or float(step1_a) == float(step3):
                        co_pr = 1
                    else:
                        co_pr = 0
                    wr.append(co_pr)
                elif ii == 2:
                    if float(step2_a) == float(step1) or float(step2_a) == float(step2) or float(step2_a) == float(step3):
                        co_pr = 1
                    else:
                        co_pr = 0
                    wr.append(co_pr)
                elif ii == 3:
                    if float(step3_a) == float(step1) or float(step3_a) == float(step2) or float(step3_a) == float(step3):
                        co_pr = 1
                    else:
                        co_pr = 0
                    wr.append(co_pr)
                if zzz == 1:
                    if co_pr == 1:
                        pr_list = "0.8"
                    else:
                        pr_list = "0.676"
                    logkc2 = Kc_ana(id = kcid_id,stu_id = u_id,kc_id = ii,status = 0,p_list = pr_list)
                    logkc2.save()
                else:
                    pr_pr = pre_list[-1]
                    kcid = calthres(co_pr,pr_pr,pre_list)
                    print("jjjjjjjjjjjjjjjjjjjj",kcid,pr_list)
                    pr_list = pr_list + "," + str(kcid[0])
                    print("jjjjjjjjjjjjjjjjjjjj",pr_list)
                    jj=0
                    if kcid[1] == 1:
                        # Pass = 1
                        jj = 1
                        print("PAssssssssssss")
                        logkc11 = Kc_ana(id = kcid_id,stu_id = u_id,kc_id = ii,status = 1,p_list = pr_list)
                        logkc11.save()
                        opt = -2
                        status1 = 1
                        kc_stat1 = Kc_ana.objects.all().filter(stu_id = u_id)
                        kc_stat_list1 = []
                        for i in kc_stat1:
                            kc_stat_list1.append(i.status)
                        print("Kcccccccccccstattttttttttlistttttttt",kc_stat_list1)
                        for i in kc_qn:
                            j = kc_list.index(i)
                            if kc_stat_list1[j] == 0:
                                status1 = 0
                        if status1 == 1:
                            logkc22 = Analysis(id = ana_id + 1,user_id=u_id,sub_id = subid,topic_id=topid,time = 0, last_time = 0,best_time = 0,attempt = 0,hint = 0,correct = 0,wasted = 0, que_id = (que_id + 1),test_id = 0,status =1)
                            logkc22.save()
                            return HttpResponseRedirect(reverse('test', args=(ana_id + 1,que_id + 1,)))
                    else:
                        logkc2 = Kc_ana(id = kcid_id,stu_id = u_id,kc_id = ii,status = 0,p_list = pr_list)
                        logkc2.save()
                    print("kciddddddddddddd",kcid[0])
        
        print(ana_id)
        log6kc = Analysis.objects.get(id = aaaaid)
        log6kc.hint = hhin
        if wr.count(0)>0:
            log6kc.wasted = 1
        else:
            log6kc.correct = 1
        log6kc.save()
        logkc222 = Analysis(id = aaaaid + 1,user_id=u_id,sub_id = subid,topic_id=topid,time = 0, last_time = 0,best_time = 0,attempt = 0,hint = 0,correct = 0,wasted = 0, que_id = (que_id + 1),test_id = 0,status =1)
        logkc222.save()
        ana_id = -111

    # ana = Analysis.objects.all().filter(id=ana_id)
    print(qn,"at firstttttttttttttttttttttttttttttttttttttttttttt")
    # print(ele)
    print(id)
    x = 0
    sub_id = ana[0].sub_id
    top_id = ana[0].topic_id
    user_id = ana[0].user_id
    print(ana,ana_id,sub_id,top_id)
    # zzz = 0
    # kc_data = Kc_ana.objects.all().filter(stu_id = user_id,kc_id = 1)
    # # kc_datac = Kc_ana.objects.all().filter(stu_id = user_id,que_id = que_id,kc_id = 1)
    # pr_list = kc_data[0].p_list
    
    # pre_list = []
    # print(len(pr_list),"LLLLLLLLLLLLLLLLLLLLLL")
    # if len(pr_list) == 0:
    #     zzz = 1
    # else:
    #     for i in pr_list.split(","):
    #         pre_list.append(float(i))
    # print(pre_list)
    # kcid_id = kc_data[0].id
    # kcid_idc = kc_datac[0].id
    # kc_data1 = Kc_ana.objects.all().filter(stu_id = user_id,que_id = que_id + 1,kc_id = 1)
    # if len(kc_data1) == 0:
    #     logkc = Kc_ana(stu_id = user_id,que_id = que_id + 1,kc_id = 1,status = 0,p_list ="0")
    #     logkc.save()
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
    if ana_id != 0 and ana_id != 1111111111 and ana_id != -111:
        if att < 1:
            if request.method == 'POST':
                opt = request.POST.get('opt', '-2')
                if len(kc_qn) == 3:
                    step1 = request.POST.get('step1', '-22')
                    stepv1 = step1
                    step2 = request.POST.get('step2', '-22')
                    stepv2 = step2
                    step3 = request.POST.get('step3', '-22')
                    stepv3 = step3
                elif len(kc_qn) == 2:
                    if kc_qn.count(1) > 0 and kc_qn.count(2) > 0:
                        step1 = request.POST.get('step1', '-22')
                        stepv1 = step1
                        step2 = request.POST.get('step2', '-22')
                        stepv2 = step2
                        stepv3 = "-1"
                        step3 = "-22"
                    elif kc_qn.count(1) > 0 and kc_qn.count(3) > 0:
                        step1 = request.POST.get('step1', '-22')
                        stepv1 = step1
                        stepv3 = "-1"
                        step3 = request.POST.get('step2', '-22')
                        stepv2 = step3
                        step2 = "-22"
                    elif kc_qn.count(2) > 0 and kc_qn.count(3) > 0:
                        stepv3 = "-1"
                        step2 = request.POST.get('step1', '-22')
                        stepv1 = step2
                        step3 = request.POST.get('step2', '-22')
                        stepv2 = step3
                        step1 = "-22"
                elif len(kc_qn) == 1:
                    if kc_qn.count(1) > 0:
                        step1 = request.POST.get('step1', '-22')
                        stepv1 = step1
                        stepv2 = "-1"
                        stepv3 = "-1"
                        step2 = "-22"
                        step3 = "-22"
                    elif kc_qn.count(2) > 0:
                        stepv2 = "-1"
                        step2 = request.POST.get('step1', '-22')
                        stepv1 = step2
                        stepv3 = "-1"
                        step1 = "-22"
                        step3 = "-22"
                    elif kc_qn.count(3) > 0:
                        stepv2 = "-1"
                        stepv3 = "-1"
                        step3 = request.POST.get('step1', '-22')
                        stepv1 = step3
                        step1 = "-22"
                        step2 = "-22"
                if int(opt) != -2:
                    answer = Quetions.objects.all().filter(que_id=que_id)
                    step1_a = answer[0].step1
                    step2_a = answer[0].step2
                    step3_a = answer[0].step3
                    for ii in kc_qn:
                        zzz = 0
                        kc_data = Kc_ana.objects.all().filter(stu_id = user_id,kc_id = ii)
                        # kc_datac = Kc_ana.objects.all().filter(stu_id = user_id,que_id = que_id,kc_id = 1)
                        pr_list = kc_data[0].p_list
                        pre_list = []
                        print(len(pr_list),"LLLLLLLLLLLLLLLLLLLLLL")
                        if len(pr_list) == 0:
                            zzz = 1
                        else:
                            for i in pr_list.split(","):
                                pre_list.append(float(i))
                        print(pre_list)
                        kcid_id = kc_data[0].id
                        if ii == 1:
                            if float(step1_a) == float(step1) or float(step1_a) == float(step2) or float(step1_a) == float(step3):
                                co_pr = 1
                            else:
                                co_pr = 0
                        elif ii == 2:
                            if float(step2_a) == float(step1) or float(step2_a) == float(step2) or float(step2_a) == float(step3):
                                co_pr = 1
                            else:
                                co_pr = 0
                        elif ii == 3:
                            if float(step3_a) == float(step1) or float(step3_a) == float(step2) or float(step3_a) == float(step3):
                                co_pr = 1
                            else:
                                co_pr = 0
                        if zzz == 1:
                            if co_pr == 1:
                                pr_list = "0.8"
                            else:
                                pr_list = "0.676"
                            logkc2 = Kc_ana(id = kcid_id,stu_id = user_id,kc_id = ii,status = 0,p_list = pr_list)
                            logkc2.save()
                        else:
                            pr_pr = pre_list[-1]
                            kcid = calthres(co_pr,pr_pr,pre_list)
                            print("jjjjjjjjjjjjjjjjjjjj",kcid,pr_list)
                            pr_list = pr_list + "," + str(kcid[0])
                            print("jjjjjjjjjjjjjjjjjjjj",pr_list)
                            jj=0
                            if kcid[1] == 1:
                                # Pass = 1
                                jj = 1
                                print("PAssssssssssss")
                                logkc11 = Kc_ana(id = kcid_id,stu_id = user_id,kc_id = ii,status = 1,p_list = pr_list)
                                logkc11.save()
                                opt = -2
                                status1 = 1
                                kc_stat1 = Kc_ana.objects.all().filter(stu_id = u_id)
                                kc_stat_list1 = []
                                for i in kc_stat1:
                                    kc_stat_list1.append(i.status)
                                print("Kcccccccccccstattttttttttlistttttttt",kc_stat_list1)
                                for i in kc_qn:
                                    j = kc_list.index(i)
                                    if kc_stat_list1[j] == 0:
                                        status1 = 0
                                if status1 == 1:
                                    logkc22 = Analysis(id = ana_id + 1,user_id=userid,sub_id = subid,topic_id=topid,time = 0, last_time = 0,best_time = 0,attempt = 0,hint = 0,correct = 0,wasted = 0, que_id = (que_id + 1),test_id = 0,status =1)
                                    logkc22.save()
                                    return HttpResponseRedirect(reverse('test', args=(ana_id + 1,que_id + 1,)))
                            else:
                                logkc2 = Kc_ana(id = kcid_id,stu_id = user_id,kc_id = ii,status = 0,p_list = pr_list)
                                logkc2.save()
                            print("kciddddddddddddd",kcid[0])
                    
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
                            log7 = Analysis(id = a_id,que_id=que_id,user_id=u_id,sub_id = sub_id,topic_id=top_id,time = 0, last_time = 0,best_time = 0,attempt = 0,hint = 0,correct = 0,wasted = 0,test_id = 0)
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
                        return render(request,'student/test.html',{"z":z,"m":m,"msg":msg,"k":k,"x":x,"nkc":len(kc_qn),"rkc":range(1,(len(kc_qn) + 1)),"step1":stepv1,"step2":stepv2,"step3":stepv3,"so":sol,'username':request.session['name'],'useremail':request.session['email']})
                else:
                    if jj == 1:
                        k=111
                        m = 1
                        return render(request,'student/test.html',{"z":z,"m":m,"msg":msg,"k":k,"x":x,"nkc":len(kc_qn),"rkc":range(1,(len(kc_qn) + 1)),"step1":stepv1,"step2":stepv2,"step3":stepv3,'username':request.session['name'],'useremail':request.session['email'],"sid":sidd})
                    else:
                        k=11
                        m = 1
                        return render(request,'student/test.html',{"z":z,"m":m,"msg":msg,"k":k,"x":x,"nkc":len(kc_qn),"rkc":range(1,(len(kc_qn) + 1)),"step1":stepv1,"step2":stepv2,"step3":stepv3,'username':request.session['name'],'useremail':request.session['email']})

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
                    log8 = Analysis(id = a_id,que_id=que_id,user_id=u_id,sub_id = sub_id,topic_id=top_id,time = 0, last_time = 0,best_time = 0,attempt = 0,hint = 0,correct = 0,wasted = 0,test_id = 0)
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
    elif ana_id == -111:
        wrr = []
        for i in range(len(wr)):
            if i == 0:
                if wr[i] == 0:
                    wrr.append(i+1)
            elif i == 1:
                if wr[i] == 0:
                    wrr.append(i+1)
            elif i == 2:
                if wr[i] == 0:
                    wrr.append(i+1)
            elif i == 3:
                if wr[i] == 0:
                    wrr.append(i+1)
        corrr = 1
        if wr.count(0) > 0:
            corrr = 0
        print("hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","-11111111111111")
        if hhin == 1:
            k=1115
        else:
            k=1116
        m = 1
        print(m,k,hhin,wr,wrr)
        return render(request,'student/test.html',{"k":k,"aid":aaaaid + 1,"qid":que_id + 1,"m":m,"corr":corrr,"lwr":len(wrr),"wrong":wrr,"sid":sidd,"so":sol,'username':request.session['name'],'useremail':request.session['email']})
    print(qn,"at lastttttttttttttttttttttttttttttttttttttttttt")

    return render(request,'student/test.html',{"z":z,"m":m,"msg":msg,"x":x,"nkc":len(kc_qn),"rkc":range(1,(len(kc_qn) + 1)),"step1":stepv1,"step2":stepv2,"step3":stepv3,'username':request.session['name'],'useremail':request.session['email']})


def start_test2(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    print(request.session['email'])
    uid = Student.objects.all().filter(email = request.session['email'])
    print(uid[0].email,uid[0].id)
    u_id = uid[0].id
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


    return render(request,'student/start_test2.html',{"sub":sub,"top":top,'username':request.session['name'],'useremail':request.session['email']})

def test2(request,sub_id,top_id):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    print(request.session['email'])
    uid = Student.objects.all().filter(email = request.session['email'])
    print(uid[0].email,uid[0].id)
    u_id = uid[0].id
    if len(Analysis.objects.all().filter(user_id = u_id,sub_id=sub_id,topic_id=top_id,test_id=1)) >0:
        return render(request,'student/test2.html',{'sid':sub_id,'tid':top_id,'test_done':1})
    ele=Quetions.objects.all().filter(sub_id=sub_id,top_id=top_id,test_id=1).order_by('que_id')
    # print(ele)
    # print(ele[0].que_id)
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
        log = Analysis(user_id=u_id,sub_id = sub_id,topic_id=top_id,time = 0,best_time = 0,last_time=int(time),attempt = (correct+wasted),hint = len(qi),correct = correct,wasted = wasted,test_id = 1)
        log.save()
        return HttpResponseRedirect(reverse('start_test2'))

    return render(request,'student/test2.html',{"z":z,'sid':sub_id,'tid':top_id,"m":m,"msg":msg,"x":x,'username':request.session['name'],'useremail':request.session['email']})

def analyse(request,sub_id):
    print(request.session['email'])
    uid = Student.objects.all().filter(email = request.session['email'])
    print(uid[0].email,uid[0].id)
    u_id = uid[0].id
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
        que = Analysis.objects.all().filter(user_id = u_id,sub_id = sub_id,topic_id=j,test_id = 0)
        print(que)
        q = []
        for i in que:
            c11 = i.correct
            w11 = i.wasted
            if i.que_id != None:
                if c11 == 1 or w11 == 1:
                    q.append(i.que_id)
                else:
                    if i.que_id == 1 or i.que_id == 16 or i.que_id == 31 or i.que_id == 46:
                        q.append(i.que_id)
        print(q,max(q))
        mx.append(max(q))
    print(mx,"hereeeeeeeeeeeeeeeeeeeeeeee")
    lstt = []
    corr = []
    for j in tid:
        que2 = Analysis.objects.all().filter(user_id = u_id,sub_id = sub_id,topic_id=j,test_id = 0)
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
        que1 = Analysis.objects.all().filter(user_id = u_id,que_id = i,test_id = 0)
        c1 = que1[0].correct
        w1 = que1[0].wasted
        if c1 == 1 or w1 == 1:
            mxx.append(i)
        else:
            if i == 1 or i == 16 or i == 31 or i == 46:
                starting = 1
                msg = "just started"
            mxx.append(0)
    qn = []
    print(mxx,"fafafafafafaf")
    for i in mxx:
        if i != 0:
            if i == 0:
                i =1
            print("ghgh")
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
        if qn[k] == 0:
            act.append(0)
        else:
            act.append(((corr[k])/qn[k])*100)
    print("fvdbdgbsddgdffddddddddddddddddddd",qn,corr,act)
    tt = zip(tid,tname,quet,lstt,avtt,act)
    # was = []
    # for jj in range(qn):
    #     was.append = qn[i] - corr[i]
    

    return render(request,'student/analyse.html',{"sub_nm":sub_nm,"tt":tt,"tid":tid,'username':request.session['name'],'useremail':request.session['email']})

def ajax_load_action(request):
    # print("AJax")
    subid=request.GET.get('subid')
    t=topic.objects.filter(sub_id=subid)
    # print(t)
    return render(request, 'student/topic_ajax.html', {'t': t})

def forum(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    email = request.session['email']
    forum = Forum.objects.order_by('-id')
    # print(forum)
    id=[]
    title = []
    username = []
    date = []
    for forum in forum:
        id.append(forum.id)
        title.append(forum.title)
        username.append(forum.username)
        date.append(forum.date.split(',')[0])
        # l.append((title,username,date))
    # print(l)
    z=zip(id,title,username,date)
    # print(z)



    return render(request, 'student/forum.html',{'z':z})

def forum_add(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        email = request.session['email']
        name = request.session['name']
        uid = Student.objects.all().filter(email = request.session['email'])[0].id
        date = datetime.datetime.now().strftime("%d-%m-%Y,%H:%M:%S")
        # print(title,desc,email,uid)
        # print(datetime.date.today())

        log = Forum(title = title, desc = desc, email = email, username = name, date = date)
        log.save()

        # print("done")
        return HttpResponseRedirect(reverse('forum'))



    return render(request, 'student/forum_add.html')

def forum_topic(request,forum_id):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    forum = Forum.objects.all().get(id = forum_id)
    # print(type(forum.desc))
    z = []
    z.extend([forum_id,forum.title,forum.desc,forum.username,forum.date.split(',')[0]])

    #Display Replies
    replies = Forum_reply.objects.all().filter(forum_id=forum_id).order_by('-id')
    desc,username,date,time = ([] for i in range(4))

    for reply in replies:
        # id.append(r.id)
        desc.append(reply.desc)
        username.append(reply.username)
        date_time=reply.date.split(',')
        date.append(date_time[0])
        time.append(date_time[1])
        # date.append(reply.date.split(',')[0])
    r=zip(desc,username,date,time)

    return render(request, 'student/forum_topic.html',{'z':z,'r':r})

def forum_reply(request,forum_id):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        desc = request.POST.get('desc')
        # print(desc)
        email = request.session['email']
        name = request.session['name']
        # uid = Student.objects.all().filter(email = request.session['email'])[0].id
        date = datetime.datetime.now().strftime("%d-%m-%Y,%H:%M:%S")
        # print(datetime.datetime.now())
        log = Forum_reply(forum_id = forum_id, desc = desc, email = email, username = name, date = date)
        log.save()
        # print(type(forum_id))
        # print('done')
        return HttpResponseRedirect(reverse('forum_topic',kwargs={'forum_id':forum_id}))
        
    return render(request, 'student/forum_add.html')




def doubt(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse('login'))

    k = ""

    if request.method == 'POST':
        myfile = request.FILES['myfile']
        print("jjjjjjjjjjjjjjjjjjjjkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        value=Image.open(myfile)
        text=pytesseract.image_to_string(value,config=tessdata_dir_config,lang = 'eng')
        print("text present in images:",text)
        k = text
    return render(request, 'student/doubt.html',{"k":k})


def analyze(request):
    return render(request, 'student/analyze.html')

