import random
import matplotlib.pyplot as plt

device_num=[25, 50, 70]
threshold=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
all_channel=[]
for i in range(1,80):
    all_channel+=[i]
run_second_1=5
run_second_2=25
hop_fequence=1600
loop_run_times_1=run_second_1*hop_fequence
loop_run_times_2=run_second_2*hop_fequence
all_collision_times_5s=[]
all_device_collision_probability_25s=[]

for i in range(len(device_num)):
    #生成每個裝置跳頻順序
    all_device_FH=[]
    for j in range(device_num[i]):
        device_FH=random.sample(all_channel,79)
        all_device_FH+=[device_FH]
    #計算前五秒碰撞次數
    collision_times_5s=[0]*79
    for j in range(loop_run_times_1):
        choice_channel=[0]*79
        for k in range(device_num[i]):
            choice_channel[all_device_FH[k][j%79]-1]=choice_channel[all_device_FH[k][j%79]-1]+1

        for k in range(len(choice_channel)):
            if choice_channel[k]>1:
                collision_times_5s[k]=collision_times_5s[k]+1
    all_collision_times_5s+=[collision_times_5s]

    
    #標記壞通道
    all_bad_channel=[]
    for j in range(len(threshold)):
        bad_channel=[]
        for k in range(0,79):
            if all_collision_times_5s[i][k]/loop_run_times_1>threshold[j]:
                bad_channel+=[k+1]
        all_bad_channel+=[bad_channel]


    #mapping
    mapping_channel=[]
    for j in range(len(all_bad_channel)):
        good_channel_1=[0]*79
        good_channel_2=list(set(all_channel)-set(all_bad_channel[j]))
        for k in range(len(good_channel_2)):
            good_channel_1[good_channel_2[k]-1]=good_channel_2[k]
        mapping_channel+=[good_channel_1]

    for j in range(len(all_bad_channel)):
        good_channel=[]
        good_channel+=mapping_channel[j]
        for k in range(len(all_bad_channel[j])):
            ptr1=all_bad_channel[j][k]
            ptr2=ptr1
            while 1:
                ptr1=ptr1+1
                ptr2=ptr2-1
                if ptr1==80:
                    if ptr2!=0:
                        if good_channel[ptr2-1]==ptr2:
                            mapping_channel[j][all_bad_channel[j][k]-1]=good_channel[ptr2-1]
                            break
                        while 1:
                            ptr2=ptr2-1
                            if ptr2==0:
                                mapping_channel[j][all_bad_channel[j][k]-1]=all_bad_channel[j][k]
                                break
                            if good_channel[ptr2-1]==ptr2:
                                mapping_channel[j][all_bad_channel[j][k]-1]=good_channel[ptr2-1]
                                break
                        break                                      
                    else:
                        mapping_channel[j][all_bad_channel[j][k]-1]=all_bad_channel[j][k]
                        break
                if ptr2==0:
                    if ptr1!=80:
                        if good_channel[ptr1-1]==ptr1:
                            mapping_channel[j][all_bad_channel[j][k]-1]=good_channel[ptr1-1]
                            break
                        while 1:
                            ptr1=ptr1+1
                            if ptr1==80:
                                mapping_channel[j][all_bad_channel[j][k]-1]=all_bad_channel[j][k]
                                break
                            if good_channel[ptr1-1]==ptr1:
                                mapping_channel[j][all_bad_channel[j][k]-1]=good_channel[ptr1-1]
                                break
                        break
                    else:
                        mapping_channel[j][all_bad_channel[j][k]-1]=all_bad_channel[j][k]
                        break
                if good_channel[ptr1-1]==ptr1:
                    mapping_channel[j][all_bad_channel[j][k]-1]=good_channel[ptr1-1]
                    break
                if good_channel[ptr2-1]==ptr2:
                    mapping_channel[j][all_bad_channel[j][k]-1]=good_channel[ptr2-1]
                    break
    
    #計算後26秒碰撞次數
    device_collision_times_25s=[]
    for m in range(len(threshold)):
        collision_times_25s=[0]*79
        for j in range(loop_run_times_2):
            choice_channel=[0]*79
            for n in range(device_num[i]):
                if all_device_FH[n][j%79]==mapping_channel[m][all_device_FH[n][j%79]-1]:
                    choice_channel[all_device_FH[n][j%79]-1]=choice_channel[all_device_FH[n][j%79]-1]+1
                else:
                    choice_channel[mapping_channel[m][all_device_FH[n][j%79]-1]-1]=choice_channel[mapping_channel[m][all_device_FH[n][j%79]-1]-1]+1
            for n in range(len(choice_channel)):
                if choice_channel[n]>1:
                    collision_times_25s[n]=collision_times_25s[n]+choice_channel[n]
        sum=0
        for j in range(len(collision_times_25s)):
            sum=sum+collision_times_25s[j]
        device_collision_times_25s+=[sum]


    #計算後26秒碰撞機率
    device_collision_probability_26s=[]
    for j in range(len(device_collision_times_25s)):
        a=device_num[i]*loop_run_times_2
        device_collision_probability_26s+=[device_collision_times_25s[j]/a]

    all_device_collision_probability_25s+=[device_collision_probability_26s]
    

#畫圖
for i in range(3):
    plt.bar(threshold,all_device_collision_probability_25s[i],width=0.05)
    plt.xlabel("threshold")
    plt.ylabel("Avg collision probability")

    # 設定標題和儲存圖片
    plt.suptitle("Host = " + str(device_num[i]))
    plt.savefig('q4_' + str(device_num[i]) + '.png')
    plt.show()