road1 = "E:/weibo/process/count_testRepostBeforeFirstHour.txt"
way1 = 'r'
fr1 = open(road1,way1)
road2 = "E:/weibo/process/feature/weiboid_testbhf_feature.txt"
way2 = 'r'
fr2 = open(road2,way2)
road3 = "E:/weibo/process/feature/testbhf_features.txt"
way3 = 'w'
fw = open(road3,way3)

feature_dic = {}
line2 = fr2.readline()
#将所有文件加入字典中
i = 0
while line2:
    feature_list = line2.strip('\n').split(',')
    weiboid = feature_list[0]
    if weiboid not in feature_dic:
        feature_dic[weiboid] = feature_list[1:]
    
    #i +=1
    line2 = fr2.readline()

j = 0
line1 = fr1.readline()
while line1:
    wp_list = line1.strip('\n').split(',')
    weiboID = wp_list[0]
    if weiboID in feature_dic:
        fw.write(weiboID+','+','.join(feature_dic[weiboID])+'\n')
    else:
        fw.write(line1.strip('\n')+','+'none'+'\n')
    time = fr1.readline()
    dep = fr1.readline().strip('\n').split(',')
    fw.write(','.join(dep[0:4])+'\n')
    wid = fr1.readline().strip('\n').split(',')
    fw.write(','.join(wid[0:4])+'\n')
    j += 1
    line1 = fr1.readline()
print('work out')
fr1.close()
fr2.close()
fw.close()
