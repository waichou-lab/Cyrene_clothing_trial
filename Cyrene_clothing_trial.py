from itertools import product

# === 基本設定 ===
Oneiric_Shard_quantity = [6480, 3280, 1980, 980, 300, 60]
Oneiric_Shard_bonus = [1600, 600, 260, 110, 30, 0]
price_in_LD = [2759, 1419, 869, 414, 141, 28]
price_in_game = [3290, 1690, 990, 490, 170, 33]

Oneiric_Shard_get_goal = 20000
max_buy = 3  # 每種方案最多買幾單

# === 雙倍設定，每個品項單獨設定是否還有雙倍 ===
# True = 該品項還有雙倍，False = 無雙倍
double_flags = [True, True, True, True, True, True]

results = []
scheme_id = 1

for combo in product(range(max_buy + 1), repeat=6):
    if sum(combo) == 0:
        continue  # 不買的不算

    total_shard = 0
    for i, count in enumerate(combo):
        if count == 0:
            continue

        if double_flags[i]:  # 該品項有雙倍
            # 第一單雙倍，只套 quantity，不加 bonus
            total_shard += Oneiric_Shard_quantity[i] * 2
            # 其餘單數加正常+bonus
            if count > 1:
                total_shard += (count - 1) * (Oneiric_Shard_quantity[i] + Oneiric_Shard_bonus[i])
        else:  # 無雙倍
            total_shard += count * (Oneiric_Shard_quantity[i] + Oneiric_Shard_bonus[i])

    # 只保留 goal < Shard < goal+5000
    if Oneiric_Shard_get_goal < total_shard < Oneiric_Shard_get_goal + 5000:
        total_cost_LD = sum(c * p for c, p in zip(combo, price_in_LD))
        total_cost_game = sum(c * p for c, p in zip(combo, price_in_game))
        cp_LD = total_shard / total_cost_LD
        cp_game = total_shard / total_cost_game

        results.append({
            "id": scheme_id,
            "combo": combo,
            "total_shard": total_shard,
            "LD_cost": total_cost_LD,
            "game_cost": total_cost_game,
            "LD_cp": cp_LD,
            "game_cp": cp_game
        })
        scheme_id += 1

if not results:
    print("❌ 沒有任何方案的 Shard 介於 goal~goal+5000，請提高 max_buy 或調整條件。")
    exit()

# 找出三個最特別方案
best_cp = max(results, key=lambda x: x["LD_cp"])
best_cost = min(results, key=lambda x: x["LD_cost"])
closest = min(results, key=lambda x: abs(x["total_shard"] - Oneiric_Shard_get_goal))

# 輸出函數
def show_scheme(title, r):
    print(f"\n🏷 {title}")
    print(f"方案編號：{r['id']}")
    print(f"購買組合：{r['combo']} (對應 [6480, 3280, 1980, 980, 300, 60])")
    print(f"獲得 Shard：{r['total_shard']}")
    print(f"LD花費：{r['LD_cost']} 元，CP值：{r['LD_cp']:.3f}")
    print(f"遊戲內花費：{r['game_cost']} 元，CP值：{r['game_cp']:.3f}")
    print("-"*60)

print(f"=== 顯示 Shard 在 {Oneiric_Shard_get_goal}~{Oneiric_Shard_get_goal+5000} 的方案 ===")
print(f"共找到 {len(results)} 個符合條件的組合。")

show_scheme("① CP值最高方案", best_cp)
show_scheme("② 總花費最少方案", best_cost)
show_scheme("③ 獲得 Shard 最接近 20000 的方案", closest)
