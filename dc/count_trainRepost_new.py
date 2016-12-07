class weiboID:
    def __init__(self,weibo_id,publisher,width = 0,depth = 0):
        self.weibo_id = weibo_id 
        self.publisher = publisher
        #self.post_list = []
        self.son_list = {}
        self.width = width
        self.depth = depth
#存放深度和广度的时间序列，
    def create_ts(self):
        self.ts = {}
        i = 15
        while i < 5000:
            self.ts[i] = [0,0]#[深度，宽度]
            i = i+15
def find_dep(tnode,tnode_dep,weiboid):#递归函数由底向上改变树的深度
    if weiboid.son_list[tnode][0] != 'none':
        father = weiboid.son_list[tnode][0]
        father_dep = weiboid.son_list[father][1]
        if tnode_dep+1 > father_dep:
            weiboid.son_list[father][1] = tnode_dep+1
            find_dep(father,weiboid.son_list[father][1],weiboid)
            
def count_trainRepost():
    weiboID_list = []
    road = "E:/weibo/process/fusai/final_4time.txt"
    way = 'r'
    out_road = 'E:/weibo/process/fusai/count_finalRepost.txt'
    out_way = 'w'
    fr = open(road,way)
    fw = open(out_road,out_way)
    line = fr.readline()
    i = 0
    weiboid = weiboID('0','0')
    while line:
        reccord = line.strip('\n').split(',')
        wbID = reccord[0]
        posted = reccord[1]
        post = reccord[2]
        time = reccord[3]
        m = int(time)/60
        m15 = ((m//15)+1)*15
        if m15 > 5000:
            #i += 1# 记住 如果后面写i += 1的话就会卡在这
            line = fr.readline()
            #print(m15)
            continue
        #print(m15)
        if wbID not in weiboID_list:  #首先判断weiboID是否遇到过，没有生成新的对象
            if weiboid.weibo_id == '0':
                weiboid =weiboID(wbID,posted)
                weiboid.create_ts()
                #weiboID_list.append(wbID)#第一条记录还是没算进去
            if weiboid.weibo_id != '0' and wbID not in weiboID_list:
                #print(weiboID_list)
                fw.write(weiboid.weibo_id+','+weiboid.publisher+'\n')
                #print(weiboid.weibo_id)
                #print(wbID)
                min_list = []
                depth_list = []
                width_list = []
                sort_dic = sorted(weiboid.ts.items(), key=lambda d:d[0], reverse = False )
                #
                #对字典排好序后，每个时刻的深度和广度都是在之前记录上累加的
                #
                num = 0
                f_depth = 0
                #print(len(sort_dic))
                while num < len(sort_dic):
                    l = 0
                    
                    f_width = 0
                    #print(sort_dic[i][0])
                    min_list.append(str(sort_dic[num][0]))
                    while l <= num:
                        
                        f_width = sort_dic[l][1][1]+f_width  #宽度需要前面叠加
                        l = l + 1
                    if sort_dic[num][1][0]!=0:
                        f_depth = sort_dic[num][1][0]  #深度每个时刻都是最新的 不用叠加
                    depth_list.append(str(f_depth))
                    width_list.append(str(f_width))
                    num = num + 1
                #print(min_list)
                #print(depth_list)
                fw.write(','.join(min_list)+'\n')
                fw.write(','.join(depth_list)+'\n')
                fw.write(','.join(width_list)+'\n')
                del weiboid
                #新生成对象  对象初始化
                weiboID_list.append(wbID)#将wbID加入到weiboID列表中,用来遇到新的weiboID时将统计好的写入
                weiboid = weiboID(wbID,posted) #新申请的对象
                weiboid.son_list[weiboid.publisher] = ['none',1,[]]
                if post not in weiboid.son_list:
                    weiboid.son_list[weiboid.publisher][2].append(post)
                    weiboid.son_list[post] = [weiboid.publisher,0,[]]
                weiboid.create_ts()
                #在对初始化 时的数据记录
                weiboid.ts[m15][0] = weiboid.son_list[weiboid.publisher][1]
                weiboid.ts[m15][1] += 1
                weiboid.depth = weiboid.ts[m15][0]
                weiboid.width = weiboid.ts[m15][1]
        else:                         #遇到过的话，先看是不是微博的发布者，是的话 宽度增加
            #print(weiboid.publisher)
            if posted == weiboid.publisher:
                if post not in weiboid.son_list:
                    weiboid.son_list[post] = [weiboid.publisher,0,[]]
                    weiboid.son_list[weiboid.publisher][2].append(post)
                ##深度不增加
                #weiboid.ts[m15][0] += 1
                weiboid.ts[m15][1] += 1
                weiboid.depth = weiboid.ts[m15][0]
                weiboid.width = weiboid.ts[m15][1]
                    
                    #print("weiboid.width")
                    #print(weiboid.width)
            elif posted in weiboid.son_list: #当posted不是发布者,先判断post在不在son_list中，若不在，再判断在不在posted的儿子链表里
                    if post in weiboid.son_list:
                        weiboid.ts[m15][1] += 1  #宽度加1
                        weiboid.width = weiboid.ts[m15][1]
                    elif post not in weiboid.son_list[posted][2]:  #判断 post是否是posted的儿子
                          weiboid.son_list[posted][1] +=1 # 若posted没有儿子结点，判断是否在他的链表中
                          weiboid.son_list[posted][2].append(post)
                          find_dep(posted,weiboid.son_list[posted][1],weiboid) #递归改变树的深度
                          weiboid.depth = weiboid.son_list[weiboid.publisher][1]  #赋值给该时刻的深度
                          weiboid.ts[m15][0] = weiboid.depth
                            #weiboid.ts[m15][0] += 1
                          weiboid.ts[m15][1] += 1  #宽度加1
                          weiboid.width = weiboid.ts[m15][1]
                    else:                         #当posted和post 都在列表中时深度不增加
                          weiboid.ts[m15][1] += 1
                          #weiboid.depth = weiboid.ts[m15][0]
                          weiboid.width = weiboid.ts[m15][1]
            elif posted not in weiboid.son_list: #当posted 不是发布者，且不在list中时 不够成关系链，假设认为 posted上一级是发布者 
                    weiboid.son_list[posted] = [weiboid.publisher,0,[]]
                    if post in weiboid.son_list:
                        weiboid.ts[m15][1] += 1  #宽度加1
                        weiboid.width = weiboid.ts[m15][1]
                        
                    else:
                        weiboid.son_list[posted][1] +=1 
                        weiboid.son_list[posted][2].append(post)
                        if post not in weiboid.son_list:
                            weiboid.son_list[post] = [posted,0,[]]
                        find_dep(posted,1,weiboid)
                        weiboid.depth = weiboid.son_list[weiboid.publisher][1]  #赋值给该时刻的深度
                        weiboid.ts[m15][0] = weiboid.depth
                        weiboid.ts[m15][1] += 1  #宽度加1
                        weiboid.width = weiboid.ts[m15][1]
            
        #i = i + 1
        line = fr.readline()
    fw.write(weiboid.weibo_id+','+weiboid.publisher+'\n')
    #print(weiboid.weibo_id)
    #print(wbID)
    min_list = []
    depth_list = []
    width_list = []
    sort_dic = sorted(weiboid.ts.items(), key=lambda d:d[0], reverse = False )
                #
                #对字典排好序后，每个时刻的深度和广度都是在之前记录上累加的
                #
    num = 0
    f_depth = 0
                #print(len(sort_dic))
    while num < len(sort_dic):
        l = 0
        
        f_width = 0
        #print(sort_dic[i][0])
        min_list.append(str(sort_dic[num][0]))
        while l <= num:
            f_width = sort_dic[l][1][1]+f_width
            l = l + 1
        if sort_dic[num][1][0]!=0:
            f_depth = sort_dic[num][1][0]                 
        depth_list.append(str(f_depth))
        width_list.append(str(f_width))
        num = num + 1
            #print(min_list)
            #print(depth_list)
    fw.write(','.join(min_list)+'\n')
    fw.write(','.join(depth_list)+'\n')
    fw.write(','.join(width_list)+'\n')
    del weiboid
    print('work done')
    fr.close()
    fw.close()
    
    
if __name__ == "__main__":
    count_trainRepost()
