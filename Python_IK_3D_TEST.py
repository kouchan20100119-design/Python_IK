#このプログラムにおいて第三象限と第四象限の処理は未実装です
import math

arm = float(input("Armの長さをmm単位で入力してください: "))  
target_x = float(input("目標X座標(mm)を入力してください: "))
target_y = float(input("目標Y座標(mm)を入力してください: "))
target_z = float(input("目標Z座標(mm)を入力してください: "))
flag_y = 0

print(f"\n目標位置: ({target_x}mm, {target_y}, {target_z}mm)") #目標位置の確認
print(f"アームの長さ: Arm1 = {arm}mm, Arm2 = {arm}mm") #アームの長さを確認

#目標との直線距離の計算
distance = math.sqrt((math.sqrt(target_x**2 + target_z**2))**2 + target_y**2)

if distance > (arm + arm):
    print(f"\nエラー: 遠すぎます!(距離: {distance:.2f}mm, 最大: {arm + arm}mm)")
    exit()
elif distance == 0:
    print("\nエラー: 目標位置が初期位置と同じです")
    exit()

#とりあえずどこでも共通のΘ0だけ求めておく
theta0 = math.degrees(math.atan(target_z / target_x))
target_x = math.sqrt(target_x**2 + target_z**2) #x-z平面での距離に置き換えてしまう　イマココ！

if target_x < 0:
    print("\nエラー: 第三象限と第四象限の処理は未実装です")
    exit()
elif target_x == 0:
    #まずはy座標が正の場合をもとめておく
    theta1 = 90 - math.degrees(math.acos( (target_y / 2) / arm))
    theta2 = 2 * math.degrees(math.acos((target_y / 2) / arm))
    if target_y > 0:
        print("\n=== 解 ===")
        print(f"θ0 = {theta0:.2f}°, θ1 = {theta1:.2f}°, θ2 = {theta2:.2f}°")
    elif target_y < 0:
        print("\n=== 解 ===")
        print(f"θ0 = {theta0:.2f}°, θ1 = -{theta1:.2f}°, θ2 = -{theta2:.2f}°")
exit()

if target_y == 0:
    #まずはx座標が正の場合をもとめておく
    theta1 = math.degrees(math.acos((target_x / 2) / arm))
    theta2 = -2 * theta1
    print("\n=== 上の方の解 (Elbow Up) ===")
    print(f"θ0 = {theta0:.2f}°, θ1 = {theta1:.2f}°, θ2 = {theta2:.2f}°")
    
    print("\n=== 下の方の解 (Elbow Down) ===")
    print(f"θ0 = {theta0:.2f}°, θ1 = -{theta1:.2f}°, θ2 = -{theta2:.2f}°")
exit()

#とりあえずx座標が負の場合でも一度正にして計算する
if target_y < 0:
    target_y = -1 * target_y
    flag_y = 1

theta4 = math.degrees(math.atan(target_y / target_x))
theta3 = math.degrees(math.acos((distance/2) / arm))

#以下のelbow_up,elbow_downはx座標が正の場合のもの
elbow_up_theta1 = theta3 + theta4
elbow_up_theta2 = -2 * theta3

elbow_down_theta1 = theta4 - theta3
elbow_down_theta2 = 2 * theta3


if flag_y == 1: #y座標が負の場合の処理 → このとき符号は逆転し、elbow_upと_elbow_downも逆転する
    print("\n=== 上の方の解 (Elbow Up) ===")
    print(f"θ0 = {theta0:.2f}°, θ1 = {-1 * elbow_down_theta1:.2f}°, θ2 = {-1 * elbow_down_theta2:.2f}°")

    print("\n=== 下の方の解 (Elbow Down) ===")
    print(f"θ0 = {theta0:.2f}°, θ1 = {-1 * elbow_up_theta1:.2f}°, θ2 = {-1 * elbow_up_theta2:.2f}°")
else: #y座標が正の場合の処理
    print("\n=== 上の方の解 (Elbow Up) ===")
    print(f"θ0 = {theta0:.2f}°, θ1 = {elbow_up_theta1:.2f}°, θ2 = {elbow_up_theta2:.2f}°")

    print("\n=== 下の方の解 (Elbow Down) ===")
    print(f"θ0 = {theta0:.2f}°, θ1 = {elbow_down_theta1:.2f}°, θ2 = {elbow_down_theta2:.2f}°")