import os
import csv
import re

# 資料夾路徑
folder_path = './data3'

# 取得資料夾中的所有檔案
files = os.listdir(folder_path)

# 只篩選出以數字開頭的檔案
filtered_files = [f for f in files if re.match(r'^\d+_', f)]

# 依數字排序檔案
sorted_files = sorted(filtered_files, key=lambda x: int(re.match(r'^(\d+)_', x).group(1)))

# 將結果儲存到 CSV 檔案中
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Filename'])  # 寫入標題
    for file in sorted_files:
        writer.writerow([file])

print("檔名已按順序儲存至 output.csv")
