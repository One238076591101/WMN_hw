import random
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# 設定模擬參數
time = 30                # 模擬時間(30s)
hop_rate = 1600            # 跳頻率
devices_num = 20            # 裝置數量
channel_num = 79           # 通道數量

# 初始化結果相關的列表
result = [0] * channel_num              # 紀錄每個通道的碰撞次數
channel_used_times = [0] * channel_num  # 紀錄每個通道被使用的次數
pre_devices = [-1] * devices_num         # 紀錄每個裝置上一次使用的通道

# 進行模擬
for _ in range(time):
    for _ in range(hop_rate):
        # 每個裝置隨機選擇一個通道
        devices = [random.randint(1, channel_num) for _ in range(devices_num)]
        
        # 檢查每個裝置的通道是否和上一次相同，若相同則重新選擇
        for i, r_num in enumerate(devices):
            while r_num == pre_devices[i]:
                r_num = random.randint(1, channel_num)
            devices[i] = r_num
            pre_devices[i] = r_num

        # 計算每個通道的使用次數
        count = Counter(devices)
        
        for i in range(channel_num):
            if i+1 in count:
                channel_used_times[i] += count[i+1]
                # 如果有碰撞次數大於1，表示有碰撞，紀錄碰撞次數
                if count[i+1] > 1:
                    result[i] += 1


# 計算每個通道的平均碰撞機率
for i in range(channel_num):
    if channel_used_times[i] > 0:
        result[i] /= channel_used_times[i]
    else:
        result[i] = 0
    print(f"Channel {i+1}: Avg Collision Probability = {result[i]:.4f}")    

# 印出平均碰撞機率
print("Avg collison probality：", np.mean(result))

# 繪圖
channels = range(1, channel_num + 1)
plt.bar(channels, result, width=0.35)
plt.axhline(y=np.mean(result), c='r', ls="--", label=('Avg collision = ', np.mean(result)))
plt.xlabel("Channels ID")
plt.ylabel("Avg collision probability")
plt.legend()
plt.show()
