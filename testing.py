# # import os

# # def getDrones():
# #     ans = os.listdir('runs/detect/')
# #     # print(ans)
# #     all_files = []
# #     for i in ans:
# #         # print(i)
# #         try:
# #             ans1 = os.listdir('runs/detect/'+i+'/crops/Drone')
# #             all_files.append('runs/detect/'+i+'/crops/Drone/'+ans1[-1])
            
# #         except:
# #             pass    

# #     return (all_files)

# import os





# files = os.listdir('runs/detect/exp5/labels')
# print(files)
# prev_area = 0
# area = 0
# h=480.0
# w=640.0
# for i in files:
#     prev_area = area
#     with open('D:/program/devrev/yolov5/runs/detect/exp5/labels/'+i,'r') as f:
#         f = f.readline()
#     f = f.split(" ")
#     if f[0] != '0':
#         continue

#     hh = float(f[4])*h
#     ww = float(f[3])*w
#     x1 = (float(f[1])*w-ww/2)
#     y1 = (float(f[2])*h-hh/2)

#     area = hh*ww
#     if prev_area > area:
#         print("receding")
#     elif prev_area < area:
#         print("approaching")
#     else:
#         print("detected")

import firebase_admin
from firebase_admin import credentials




cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def send_push(title,body,token,dataobject=None):
    message = messaging.MultiCastMessage(
        
    )

