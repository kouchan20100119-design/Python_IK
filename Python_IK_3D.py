import math

# 入力値を取得する関数
def get_float_input(prompt):
    while True:
        try:
            value = input(prompt)
            if value.strip() == "":
                print("入力してください")
                continue
            return float(value)
        except ValueError:
            print("無効な値です。数字を入力してください")

# アームの長さを入力（0以下はNG）
while True:
    arm1 = get_float_input("アームの長さを入力してください: ")
    if arm1 <= 0:
        print("アームの長さは0より大きい値を入力してください")
        continue
    break

arm2 = arm1 #arm1とarm2の長さは同じ

# 座標を入力（すべてが0の場合はNG）
while True:
    target_x = get_float_input("目標X座標(mm)を入力してください: ") 
    target_y = get_float_input("目標Y座標(mm)を入力してください: ")
    target_z = get_float_input("目標Z座標(mm)を入力してください: ")
    
    if target_x == 0 and target_y == 0 and target_z == 0:
        print("座標がすべて0なので、別の値を入力してください")
        continue
    
    if target_y == 0:
        print("Y座標が0なので再入力してください")
        continue

    if target_x == 0:
        print("X座標が0なので再入力してください")
        continue
        
    if target_z == 0:
        print("Z座標が0なので再入力してください")
        continue
    
    break

flag = 0 #y座標が負の時のフラグ

print(f"\n目標位置: ({target_x}mm, {target_y}mm, {target_z}mm)") #目標位置の確認
print(f"アームの長さ: Arm1 = {arm1}mm, Arm2 = {arm2}mm") #アームの長さを確認

#y座標が負の時の迂回ルート
if target_y < 0: 
    target_y = -1 * target_y
    flag = 1

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

if flag == 1: #y座標が負の時の補正
    tan_theta4 = -1 * tan_theta4   #イマココ

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
