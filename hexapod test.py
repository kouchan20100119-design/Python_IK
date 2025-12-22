import math
#import serial
#import time

arm1 = float(input("アームの長さを入力してください: "))  
arm2 = arm1 #arm1とarm2の長さは同じ
target_x = float(input("目標X座標(mm)を入力してください: ")) 
target_y = float(input("目標Y座標(mm)を入力してください: "))
flag = 0


print(f"\n目標位置: ({target_x}mm, {target_y})mm") #目標位置の確認
print(f"アームの長さ: Arm1 = {arm1}mm, Arm2 = {arm2}mm") #アームの長さを確認

if target_y < 0:
    target_y = -1 * target_y
    flag = 1

distance = math.sqrt(target_x**2 + target_y**2) #目標位置までの直線距離を計算

if distance > (arm1 + arm2):
    print(f"\nエラー: 遠すぎます!(距離: {distance:.2f}mm, 最大: {arm1 + arm2}mm)")
    exit()
elif distance < abs(arm1 - arm2):
    print(f"\nエラー: 近すぎます!(距離: {distance:.2f}mm, 最小: {abs(arm1 - arm2)}mm)")
    exit()


cos_theta3 = (distance / 2) / arm1
theta3 = math.degrees(math.acos(cos_theta3))

if target_y == 0:
    print("エラー")
    tan_theta4 
else:
    tan_theta4 = target_x / target_y 
    
if flag == 1:
    print("\n=== 下の方の解 ===")
    theta1 = theta3 +  math.degrees(math.atan(tan_theta4))
    theta2 = 2 * theta3
    print(f"θ1 = {theta1:.2f}°, θ2 = -{theta2:.2f}°")

    print("\n=== 上の方の解 ===")
    theta1 = math.degrees(math.atan(tan_theta4)) - theta3
    theta2 = 2 * theta3
    print(f"θ1 = {theta1:.2f}°, θ2 = {theta2:.2f}°")
    exit()
else:
    print("\n=== 下の方の解 ===")
    theta1 = theta3 +  math.degrees(math.atan(tan_theta4))
    theta2 = 2 * theta3
    print(f"θ1 = {theta1:.2f}°, θ2 = -{theta2:.2f}°") #下の解はマイナスにする

    print("\n=== 上の方の解 ===")
    theta1 = math.degrees(math.atan(tan_theta4)) - theta3
    theta2 = 2 * theta3
    print(f"θ1 = {theta1:.2f}°, θ2 = {theta2:.2f}°") #上の解は特になし
    exit()

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





