
from dataseed import load_activities
from scoring import mood_match, budget_fit, group_fit
from datamodels import Activity, Request, Suggestion

def score_activity(user_mood, user_budget, user_group_size, activity):
    mood_score = mood_match(user_mood, activity["moods"])
    budget_score = budget_fit(activity["price"], user_budget)
    group_score = group_fit(user_group_size, activity["min"], activity["max"])

    # Weighted total score
    total_score = (
        0.3 * mood_score +
        0.5 * budget_score +
        0.2 * group_score
    )

    # Build explanation for GUI / API to show
    reasons = []
    if mood_score >= 1.0:
        reasons.append("Match made in heaven!")
    elif mood_score >= 0.5:
        reasons.append("Vibe is kinda close")

    if budget_score == 1.0:
        reasons.append("Within budget")
    elif budget_score == 0.5:
        reasons.append("Slightly above budget")

    if group_score == 1.0:
        reasons.append("Good for your group size")
    elif group_score >= 0.5:
        reasons.append("lets hope someone cancels!")

    return total_score, reasons


def recommend(mood, budget, groupSize, top_n=3, allowedCategories=None):
   
    activities = load_activities()

    # optional category filter
    if allowedCategories:
        activities = [
            a for a in activities
            if a["category"] in allowedCategories
        ]

    scored = []
    for a in activities:
        s, reasons = score_activity(mood, budget, groupSize, a)
        scored.append({
            "name": a["name"],
            "price_per_person": a["price"],
            "group_min": a["min"],
            "group_max": a["max"],
            "score": round(s, 3),
            "reasons": reasons
        })

    # sort by score high to low
    scored.sort(key=lambda item: item["score"], reverse=True)

    # return top N
    return scored[:top_n]


# Lets you run this file directly for testing
if __name__ == "__main__":
    print("=== Night Out Recommender ===")
    mood = input("Mood (party/chill/competitive/teamwork/foodie/etc): ").strip().lower()
    budget = float(input("Max budget per person (£): ").strip())
    groupSize = int(input("Group size: ").strip())

    results = recommend(mood=mood, budget=budget, groupSize=groupSize, top_n=3)

    print("\nTop suggestions:\n")
    for r in results:
        print(f"- {r['name']} ({r['category']}, ~£{r['price_per_person']}pp, {r['location']})")
        print(f"  Score: {r['score']}")
        print(f"  Why: {', '.join(r['reasons']) if r['reasons'] else 'No specific reason'}")
        print()
