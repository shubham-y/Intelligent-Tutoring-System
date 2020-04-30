perm = [0,1,0,1,0,1,1,0,1]
pred_list = [0.82]
kcdi = [0.82,1]
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