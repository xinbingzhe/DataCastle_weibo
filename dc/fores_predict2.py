#from sklearn.linear_model import BayesianRidge
#from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt  
import pandas as pd
from sklearn.pipeline import Pipeline
#from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn import ensemble
from sklearn.ensemble.forest import RandomForestRegressor
### err var ###
def rmse(y_test, y_predict):  
    #return sp.sqrt(sp.mean((y_test - y) ** 2))  
     return np.mean((y_test - y_predict) ** 2)
rmse_all_d = 0
rmse_all_w = 0
    
### RandomForest ###
def RandomForest(weiboid,x_train,y_train,x_test,y_test,d):
     params = {'n_estimators': 1000, 'max_depth': d, 'min_samples_split': 1,'warm_start':True,'oob_score':True}
     clf = RandomForestRegressor(**params)
     clf.fit(x_train, y_train)          
     y_predict = clf.predict(x_test)
     r = rmse(y_test, y_predict)
     #fig(weiboid,y_test,y_predict)
     return y_predict,r
    
def fig(weiboid,y_test,y_predict):
    len_t1 = y_test.shape[0]
    x_test = []
    for t in range(0,len_t1):
        x_test.append(t)
    
    len_tp = y_predict.shape[0]
    x_pre = []
    for xt in range(4,len_tp+4):
        x_pre.append(xt)
    plt.grid()
    plt.plot(x_test,y_test,color='red')
    plt.plot(x_pre,y_predict,color='green')
    path = "E:/weibo/fig/train_fig/"+weiboid
    plt.savefig(path+".png")
    plt.clf()
    

road1 = "E:/weibo/process/feature/features_train.txt"
road2 = "E:/weibo/process/feature/features_test.txt"
road3 = "E:/weibo/process/feature/result_test.txt"
way1 = 'r'
way2 = 'w'
fr1 = open(road1,way1)
fr2 = open(road2,way1)
fw = open(road3,way2)
#fw2 = open('E:/tianchi/season2(1)/p2/data//train_Model1.txt','w')
line1 = fr1.readline()
####训练特征###
x_train_d = []
x_train_w = []
#######
y_train_di = []
y_train_wi = []
#######
i = 0
while i< 800:
    f1 = line1.strip('\n').split(',')
    dep = fr1.readline().strip('\n').split(',')
    wid = fr1.readline().strip('\n').split(',')
    ### create Y_train_d ###
    y_train_d = map(float,dep)
    
    for d in y_train_d:
        y_train_di.append(d)
    #Y_train_d = np.array(y_train_di)#最后放
    lenght = len(dep)
    ### create Y_train_w ###
    y_train_w = map(float,wid)
    
    for w in y_train_w:
        y_train_wi.append(w)
    #Y_train_w = np.array(y_train_wi)
    ### create x_train ###
    for num in range(0,lenght):
        publisher = float(f1[1])
        fans = float(f1[2])
        pubtime = float(f1[3])
        d_dis1 = float(f1[4])
        d_dis2 = float(f1[5])
        d_dis3 = float(f1[6])
        d_mdis = float(f1[7])
        feature_d = [publisher,fans,pubtime,d_dis1,d_dis2,d_dis3,d_mdis,float(num)]
        x_train_d.append(feature_d)
        w_dis1 = float(f1[8])
        w_dis2 = float(f1[9])
        w_dis3 = float(f1[10])
        w_mdis = float(f1[11])
        feature_w = [publisher,fans,pubtime,w_dis1,w_dis2,w_dis3,w_mdis,float(num)]
        x_train_w.append(feature_w)
    line1 = fr1.readline()
    i = i+1
#print(len(y_train_di))
##read_test##
#min_max_scaler = preprocessing.MinMaxScaler()
testBHF_wID = []
Y_test_d = []
Y_test_w = []
test_feature_d = []
test_feature_w = []

line2 = fr2.readline()


j = 0
while j<50:
    f2 = line2.strip('\n').split(',')
    weiboid = f2[0]
    testBHF_wID.append(weiboid)
    dept = fr2.readline().strip('\n').split(',')
    dep_t1 = dept[0:4]
    dep_t2 = dept[4:]
    widt = fr2.readline().strip('\n').split(',')
    wid_t1 = widt[0:4]
    wid_t2 = widt[4:]

    y_test_d1 = map(float,dep_t1)
    for d in y_test_d1:
        y_train_di.append(d)
    len_tt= len(dep_t1)

    y_test_w1 = map(float,wid_t1)
    for w in y_test_w1:
        y_train_wi.append(w)
    #print(len(y_train_di))
   
    ### add test train feature ###
    for num in range(0,len_tt):
        publisher = float(f2[1])
        fans = float(f2[2])
        pubtime = float(f2[3])
        d_dis1 = float(f2[4])
        d_dis2 = float(f2[5])
        d_dis3 = float(f2[6])
        d_mdis = float(f2[7])
        feature_d = [publisher,fans,pubtime,d_dis1,d_dis2,d_dis3,d_mdis,float(num)]
        x_train_d.append(feature_d)
        w_dis1 = float(f2[8])
        w_dis2 = float(f2[9])
        w_dis3 = float(f2[10])
        w_mdis = float(f2[11])
        feature_w = [publisher,fans,pubtime,w_dis1,w_dis2,w_dis3,w_mdis,float(num)]
        x_train_w.append(feature_w)
    ##-------------------------
    X_train_d = np.array(x_train_d)
    X_train_w = np.array(x_train_w)
    #X_train_d_scale = min_max_scaler.fit_transform(X_train_d)
    #X_train_w_scale = min_max_scaler.fit_transform(X_train_w)
    ### add test y value ###
    
    y_test_d2 = map(float,dep_t2)
    for d2 in y_test_d2:
        Y_test_d.append(d2)
    len_f = len(dep_t2)
    #------------
    
    #Y_test_d_scale = min_max_scaler.fit_transform(Y_test_d)
    #------------
    
    y_test_w2 = map(float,wid_t2)
    for w2 in y_test_w2:
        Y_test_w.append(w2)
    ##--------------------
    
    #Y_test_w_scale =min_max_scaler.fit_transform(Y_test_w)
    ##--------------------
    ### add test feature ###

    for num in range(0,len_f):
        feature_d = [publisher,fans,pubtime,d_dis1,d_dis2,d_dis3,d_mdis,float(num)]
        test_feature_d.append(feature_d)
        feature_w = [publisher,fans,pubtime,w_dis1,w_dis2,w_dis3,w_mdis,float(num)]
        test_feature_w.append(feature_w)
    
    #X_test_d_scale = min_max_scaler.fit_transform(X_test_d)
    #X_test_w_scale = min_max_scaler.fit_transform(X_test_w)
    

    line2 = fr2.readline()
    print(j)
    j +=1
##--------------------------------
### create Y_train_w ###
Y_train_d = np.array(y_train_di)
Y_train_w = np.array(y_train_wi)
##----------------------------
X_train_d = np.array(x_train_d)
X_train_w = np.array(x_train_w)
#----------------------------
Y_test_d = np.array(Y_test_d)
Y_test_w = np.array(Y_test_w)
#-----------------------------
X_test_d = np.array(test_feature_d)
X_test_w = np.array(test_feature_w)
##------------------------------
result_d,rd = RandomForest(weiboid+'_d',X_train_d,Y_train_d,X_test_d,Y_test_d,2)
result_w,rw = RandomForest(weiboid+'_w',X_train_w,Y_train_w,X_test_w,Y_test_w,2)
print(len(result_d))
print(testBHF_wID)

l = int(len(result_d)/len(testBHF_wID))
###  写表头 ###
scale = []
depth = []
for sc in range(1,l):
    scale.append('scaleT'+str((sc+4)*15))
for de in range(1,l):
    depth.append('depthT'+str((de+4)*15))
fw.write('WeiboID (Time Unit: Minutes)'+','+','.join(scale)+','+','.join(depth)+'\n')
#print(l)
### 输出结果 ####
r = 0
for wID in testBHF_wID:
    r_wid = []
    r_dep = []
    for rd in result_d[r:r+l]:
        r_dep.append(str(int(rd)))
    for rw in result_w[r:r+l]:
        r_wid.append(str(int(rw)))
    fw.write('testWeibo'+wID+','+','.join(r_wid)+','+','.join(r_dep)+'\n')
    r += l


print('rmse_all_d:')
print(rd)
print('rmse_all_w:')
print(rw)
### output  ###



##----------------------------------
'''print(X_train_d.shape)
print(Y_train_d.shape)
print(X_test_d.shape)
print(Y_test_d.shape)'''
#result_d = RandomForest(X_train_w_scale,Y_train_w_scale,X_test_w_scale,Y_test_w_scale,2)
#result_d = RandomForest(X_train_d,Y_train_d,X_test_d,Y_test_d,8)

fr1.close()
fr2.close()
fw.close()

    
    
