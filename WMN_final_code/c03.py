import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# 設定模擬參數
time = 30                      # 模擬時間
hop_rate = 1600                # 跳頻率
devices_nums = [25, 50, 75]    # 不同裝置數量
channel_num = 79               # 通道數量
poisson_prob = 0.4             # Poisson分布參數
bad_channel_upper_bound = 40   # 不良通道上限

# 初始化結果相關的列表
channel_used_times = [0] * channel_num        # 紀錄每個通道被使用的次數
collision_times = [0] * channel_num           # 紀錄每個通道碰撞的次數
avg_collision_result = [0] * channel_num      # 每個通道的平均碰撞機率
pre_devices = []                             # 紀錄每個裝置上一次使用的通道

# 初始化裝置上一次使用的通道
for i in range(max(devices_nums)):
    pre_devices.append([-1] * max(devices_nums))

# 生成壞通道數量
interference_channel_num = -1
while(interference_channel_num < 0 or interference_channel_num > 40):
    interference_channel_num = np.random.poisson(bad_channel_upper_bound * poisson_prob)
bad_channel = [random.randint(1, channel_num) for _ in range(interference_channel_num)]

# 迭代不同裝置數量
for devices_num in devices_nums:
    # 進行模擬
    t = time
    while(t > 0):
        h_r = hop_rate
        while(h_r > 0):
            devices = []

            # 每個裝置隨機選擇一個通道，確保通道不在不良通道中，且與上一次使用的通道不同
            for i in range(devices_num):
                random_num = random.randint(1, channel_num)
                while (random_num in bad_channel) or (random_num == pre_devices[i][devices_num - 1]):
                    random_num = random.randint(1, channel_num)
                devices.append(random_num)
                pre_devices[i][devices_num - 1] = random_num

            # 計算每個通道的使用次數和碰撞次數
            count = Counter(devices)
            for i in range(channel_num):
                if i+1 in count:
                    channel_used_times[i] += count[i+1]
                    # 如果有碰撞次數大於1，表示有碰撞，紀錄碰撞次數
                    if count[i+1] > 1:
                        collision_times[i] += 1
            h_r -= 1
        t -= 1

    # 計算每個通道的平均碰撞機率
    for i in range(channel_num):
        if channel_used_times[i] > 0:
            avg_collision_result[i] = collision_times[i] / channel_used_times[i]
        else:
            avg_collision_result[i] = 0

    # 計算不良通道數量結果
    bad_channel_count_result = []
    for i in range(1, 10, 1):
        threshold = i / 10
        bad_channel_count = 0
        for j in range(channel_num):
            if j + 1 in bad_channel:
                bad_channel_count += 1
            elif avg_collision_result[j] > threshold:
                bad_channel_count += 1
        bad_channel_count_result.append(bad_channel_count)

    # 繪圖
    plt.figure(figsize=(12, 5))

    # 繪製平均碰撞機率圖
    c_num = []
    for i in range(channel_num):
        c_num.append(i + 1)
    ax1 = plt.subplot(121)
    ax1.bar(c_num, avg_collision_result, width=0.35)
    ax1.xaxis.set_label_text("Channels ID")
    ax1.yaxis.set_label_text("Avg Collision Probability")

    # 繪製不良通道數量隨閾值變化圖
    t_num = []
    for i in range(1, 10):
        t_num.append(i / 10)
    ax2 = plt.subplot(122)
    ax2.bar(t_num, bad_channel_count_result, width=0.01)
    ax2.xaxis.set_label_text("Threshold")
    ax2.yaxis.set_label_text("Bad Channel Count")

    # 設定標題和儲存圖片
    plt.suptitle("Host = " + str(devices_num))
    plt.savefig('q3_' + str(devices_num) + '.png')
    plt.show()
