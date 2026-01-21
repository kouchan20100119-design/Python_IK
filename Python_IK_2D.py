import math

arm1 = float(input("アームの長さを入力してください: "))  
arm2 = arm1 #arm1とarm2の長さは同じ
target_x = float(input("目標X座標(mm)を入力してください: ")) 
target_y = float(input("目標Y座標(mm)を入力してください: "))
flag = 0 #y座標が負の時のフラグ
flag2 = 0

#xまたはy座標が0の場合はいったん終了
if target_y == 0:
    print("Y座標が0なので終了します")
    exit()

if target_x == 0:
    print("X座標が0なので終了します")
    exit()


print(f"\n目標位置: ({target_x}mm, {target_y})mm") #目標位置の確認
print(f"アームの長さ: Arm1 = {arm1}mm, Arm2 = {arm2}mm") #アームの長さを確認

#y座標が負の時の迂回ルート
if target_y < 0: 
    target_y = -1 * target_y
    flag = 1

#目標との直線距離の計算
distance = math.sqrt(target_x**2 + target_y**2)

# 到達可能かのチェック
if distance > (arm1 + arm2):
    print(f"\nエラー: 遠すぎます!(距離: {distance:.2f}mm, 最大: {arm1 + arm2}mm)")
    exit()
elif distance < abs(arm1 - arm2):
    print(f"\nエラー: 近すぎます!(距離: {distance:.2f}mm, 最小: {abs(arm1 - arm2)}mm)")
    exit()
elif distance == 0:
    print("\nエラー: 目標位置がベース位置と同じです")
    exit()

#もろもろ計算
cos_theta3 = (distance / 2) / arm1
theta3 = math.degrees(math.acos(cos_theta3))
tan_theta4 = target_x / target_y 
    
if flag == 1:
    print("\n=== 下の方の解 (Elbow Down) ===")
    theta1 = theta3 +  math.degrees(math.atan(tan_theta4))
    theta2 = 2 * theta3
    print(f"θ1 = {theta1:.2f}°, θ2 = -{theta2:.2f}°")
    print(f"Note: Angles are measured from initial x-axis position (θ1=0°, θ2=0°)")

    print("\n=== 上の方の解 (Elbow Up) ===")
    theta1 = math.degrees(math.atan(tan_theta4)) - theta3
    theta2 = 2 * theta3
    print(f"θ1 = {theta1:.2f}°, θ2 = {theta2:.2f}°")
    print(f"Note: Angles are measured from initial x-axis position (θ1=0°, θ2=0°)")
else:
    print("\n=== 下の方の解 (Elbow Down) ===")
    theta1 = theta3 +  math.degrees(math.atan(tan_theta4))
    theta2 = 2 * theta3
    print(f"θ1 = {theta1:.2f}°, θ2 = -{theta2:.2f}°") 
    print(f"Note: Angles are measured from initial x-axis position (θ1=0°, θ2=0°)")

    print("\n=== 上の方の解 (Elbow Up) ===")
    theta1 = math.degrees(math.atan(tan_theta4)) - theta3
    theta2 = 2 * theta3
    print(f"θ1 = {theta1:.2f}°, θ2 = {theta2:.2f}°") 
    print(f"Note: Angles are measured from initial x-axis position (θ1=0°, θ2=0°)")

