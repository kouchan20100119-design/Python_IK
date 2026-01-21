import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation

arm1 = float(input("アームの長さを入力してください: "))  
arm2 = arm1 #arm1とarm2の長さは同じ
target_x = float(input("目標X座標(mm)を入力してください: ")) 
target_y = float(input("目標Y座標(mm)を入力してください: "))
target_z = float(input("目標Z座標(mm)を入力してください: "))
flag = 0 #y座標が負の時のフラグ


if target_y == 0:
    print("Y座標が0なので終了します")
    exit()

if target_x == 0:
    print("X座標が0なので終了します")
    exit()
    
if target_z == 0:
    print("Z座標が0なので終了します")
    exit()

print(f"\n目標位置: ({target_x}mm, {target_y}mm, {target_z}mm)") #目標位置の確認
print(f"アームの長さ: Arm1 = {arm1}mm, Arm2 = {arm2}mm") #アームの長さを確認

#y座標が負の時の迂回ルート
#if target_y < 0: 
#    target_y = -1 * target_y
#    flag = 1

xz_distance = math.sqrt(target_x**2 + target_z**2) #目標位置までのxz平面での直線距離を計算
distance = math.sqrt(xz_distance**2 + target_y**2) #目標位置までの直線距離を計算

if distance > (arm1 + arm2): # 到達不可能な場合のチェック
    print(f"\nエラー: 遠すぎます!(距離: {distance:.2f}mm, 最大: {arm1 + arm2}mm)")
    exit()
elif distance < abs(arm1 - arm2):
    print(f"\nエラー: 近すぎます!(距離: {distance:.2f}mm, 最小: {abs(arm1 - arm2)}mm)")
    exit()
elif distance == 0:
    print("\nエラー: 目標位置がベース位置と同じです")
    exit()

# ===== 逆運動学計算処理 =====
tan_theta0 = target_x / target_z
cos_theta3 = (distance / 2) / arm1
tan_theta4 = target_y / distance

print("\n=== 下の方の解 ===")
theta0_lower = math.degrees(math.atan(tan_theta0))
theta1_lower = math.degrees(math.atan(tan_theta4)) + math.degrees(math.acos(cos_theta3))
theta2_lower = 2 * math.degrees(math.acos(cos_theta3))
print(f"θ0 = {theta0_lower:.2f}°, θ1 = -{theta1_lower:.2f}°, θ2 = {theta2_lower:.2f}°") #下の解においてはΘ2はホームポジションからマイナスの方向なので-をつける

print("\n=== 上の方の解 ===")
theta0_upper = math.degrees(math.atan(tan_theta0))
theta1_upper = math.degrees(math.atan(tan_theta4)) - math.degrees(math.acos(cos_theta3))
theta2_upper = 2 * math.degrees(math.acos(cos_theta3))
print(f"θ0 = {theta0_upper:.2f}°, θ1 = {theta1_upper:.2f}°, θ2 = {theta2_upper:.2f}°") #上は特になしでそのまんま
