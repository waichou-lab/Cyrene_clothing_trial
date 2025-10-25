from itertools import product

# === Basic Settings ===
Oneiric_Shard_quantity = [6480, 3280, 1980, 980, 300, 60]  # base shard quantity per pack
Oneiric_Shard_bonus = [1600, 600, 260, 110, 30, 0]        # bonus shards per pack
price_in_LD = [2759, 1419, 869, 414, 141, 28]             # price in LD
price_in_game = [3290, 1690, 990, 490, 170, 33]           # price in in-game currency

goal_shard = 20000         # target shards
max_buy = 3                # maximum purchase per pack type

# === Double flags per item: True = double shard available, False = double used up ===
double_flags = [True, True, True, True, True, True]

results = []
scheme_id = 1

# === Generate all possible purchase combinations ===
for combo in product(range(max_buy + 1), repeat=6):
    if sum(combo) == 0:
        continue  # skip buying nothing

    total_shard = 0
    for i, count in enumerate(combo):
        if count == 0:
            continue

        if double_flags[i]:
            # First purchase for this item gets double (quantity only)
            total_shard += Oneiric_Shard_quantity[i] * 2
            # Remaining purchases get normal quantity + bonus
            if count > 1:
                total_shard += (count - 1) * (Oneiric_Shard_quantity[i] + Oneiric_Shard_bonus[i])
        else:
            # No double left: all purchases get quantity + bonus
            total_shard += count * (Oneiric_Shard_quantity[i] + Oneiric_Shard_bonus[i])

    # Keep only combinations where goal < total_shard < goal + 5000
    if goal_shard < total_shard < goal_shard + 5000:
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
    print("❌ No combination yields shards within goal~goal+5000. Increase max_buy or adjust conditions.")
    exit()

# === Find the three most notable combinations ===
best_cp = max(results, key=lambda x: x["LD_cp"])
lowest_cost = min(results, key=lambda x: x["LD_cost"])
closest_to_goal = min(results, key=lambda x: abs(x["total_shard"] - goal_shard))

# === Output function ===
def show_scheme(title, r):
    print(f"\n🏷 {title}")
    print(f"Scheme ID: {r['id']}")
    print(f"Purchase combo: {r['combo']} (corresponds to [6480, 3280, 1980, 980, 300, 60])")
    print(f"Total Shards: {r['total_shard']}")
    print(f"LD Cost: {r['LD_cost']} | CP (per LD): {r['LD_cp']:.3f}")
    print(f"In-game Cost: {r['game_cost']} | CP (per game currency): {r['game_cp']:.3f}")
    print("-"*60)

print(f"=== Double flags: {double_flags}, showing combinations with shards in {goal_shard}~{goal_shard+5000} ===")
print(f"Total qualifying combinations found: {len(results)}")

show_scheme("① Highest CP Scheme", best_cp)
show_scheme("② Lowest Cost Scheme", lowest_cost)
show_scheme("③ Closest to Goal Scheme", closest_to_goal)

