import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation
#import serial
#import time

arm1 = float(input("アームの長さを入力してください: "))  
arm2 = arm1 #arm1とarm2の長さは同じ
target_x = float(input("目標X座標(mm)を入力してください: ")) 
target_y = float(input("目標Y座標(mm)を入力してください: "))
target_z = float(input("目標Z座標(mm)を入力してください: "))

print(f"\n目標位置: ({target_x}mm, {target_y})mm, {target_z}") #目標位置の確認
print(f"アームの長さ: Arm1 = {arm1}mm, Arm2 = {arm2}mm") #アームの長さを確認

xz_distance = math.sqrt(target_x**2 + target_z**2) #目標位置までのxz平面での直線距離を計算
distance = math.sqrt(xz_distance**2 + target_y**2) #目標位置までの直線距離を計算

if distance > (arm1 + arm2): # 到達不可能な場合のチェック
    print(f"\nエラー: 遠すぎます!(距離: {distance:.2f}mm, 最大: {arm1 + arm2}mm)")
    exit()
elif distance < abs(arm1 - arm2):
    print(f"\nエラー: 近すぎます!(距離: {distance:.2f}mm, 最小: {abs(arm1 - arm2)}mm)")
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

# アニメーション用：上の方の解を採用
target_theta0 = theta0_upper
target_theta1 = theta1_upper
target_theta2 = theta2_upper

#ここからarduinoで動かすやつ（現状コメントアウト済み）

# Arduinoのポート（"COM3", "/dev/ttyUSB0"など）
#ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
#time.sleep(2)  

# 計算結果
#line = f"A 1 {theta1:.2f} {theta2:.2f}\n"
#ser.write(line.encode('ascii'))
#print("送信:", line)

# 応答表示
#ack = ser.readline().decode().strip()
#print("Arduino:", ack)

#ser.close()

# ===== アニメーション処理 =====

def forward_kinematics(theta0_deg, theta1_deg, theta2_deg, arm1_len, arm2_len):
    """順運動学：関節角度から各関節位置を計算"""
    theta0 = math.radians(theta0_deg)
    theta1 = math.radians(theta1_deg)
    theta2 = math.radians(theta2_deg)
    
    # ベース（関節0）
    p0 = np.array([0, 0, 0])
    
    # 関節1の位置（Y軸回転）
    p1 = np.array([
        arm1_len * math.sin(theta0) * math.cos(theta1),
        arm1_len * math.sin(theta1),
        arm1_len * math.cos(theta0) * math.cos(theta1)
    ])
    
    # 関節2の位置（関節1を中心に関節1+関節2で回転）
    combined_angle = theta1 + theta2
    p2 = p1 + np.array([
        arm2_len * math.sin(theta0) * math.cos(combined_angle),
        arm2_len * math.sin(combined_angle),
        arm2_len * math.cos(theta0) * math.cos(combined_angle)
    ])
    
    return p0, p1, p2

# アニメーション設定
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# アニメーション用フレーム数
num_frames = 60
frame_counter = [0]

# 直線補間で角度を生成
def get_interpolated_angles(frame, total_frames):
    t = frame / total_frames
    theta0 = 0 + (target_theta0 - 0) * t
    theta1 = 0 + (target_theta1 - 0) * t
    theta2 = 0 + (target_theta2 - 0) * t
    return theta0, theta1, theta2

def animate(frame):
    ax.clear()
    
    # 現在のフレーム対応の角度を計算
    theta0, theta1, theta2 = get_interpolated_angles(frame, num_frames)
    
    # 順運動学で各関節位置を計算
    p0, p1, p2 = forward_kinematics(theta0, theta1, theta2, arm1, arm2)
    
    # アームをプロット
    arm_x = [p0[0], p1[0], p2[0]]
    arm_y = [p0[1], p1[1], p2[1]]
    arm_z = [p0[2], p1[2], p2[2]]
    
    ax.plot(arm_x, arm_y, arm_z, 'b-o', linewidth=2, markersize=8)
    
    # 目標位置をプロット
    ax.scatter([target_x], [target_y], [target_z], color='red', s=100, label='Target')
    
    # 軸設定
    max_range = arm1 + arm2
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([0, max_range])
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title(f'Robot Arm Animation - Frame {frame+1}/{num_frames}\nθ0={theta0:.1f}°, θ1={theta1:.1f}°, θ2={theta2:.1f}°')
    ax.legend()
    
    # グリッド表示
    ax.grid(True)

# アニメーション実行
anim = animation.FuncAnimation(fig, animate, frames=num_frames, interval=50, repeat=True)
plt.show()





