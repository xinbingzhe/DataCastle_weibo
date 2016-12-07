road1 = "E:/weibo/original/userRelations/weibo_dc_parse2015_link_filter"
way1 = 'r'
road2 = "E:/weibo/process/count_relationship.txt"
way2 = 'w'
fr = open(road1,way1)
fw = open(road2,way2)
line = fr.readline()
user_dic = {}
i = 0
while line:
    #reccord = line.decode('gbk','ignore').split(',')
    #print(reccord)
    li = line.split('\t')
    fan = li[0]
    friend = li[1].strip('\n').split('\x01')
    #print(fan)
    #print(friend)
    for user in friend:
        if user not in user_dic:
            user_dic[user] = 1
        else:
            user_dic[user] += 1
    #print(user_dic)
    #i +=1
    line = fr.readline()
#print(user_dic)
j = 0
user_list = []
for user in user_dic:
    if j == 100:
        fw.write(','.join(user_list)+'\n')
        j = 0
        user_list = []
    else :
        user_list.append(str(user)+':'+str(user_dic[user]))
        j += 1

#fw.write('##'+'\n')
fw.write(','.join(user_list)+'\n')
print('work done')
fr.close()
fw.close()
