
#mood matching
def mood_match(mood, tags):
    mood = mood.lower()
    tags = [t.lower() for t in tags]

    if mood in tags:
        return 1.0  # perfect match
    elif any(t in tags for t in ["social", "fun", "chill", "competitive", "teamwork", "party", "casual"]):
        return 0.5  # partial match (similar vibes)
    else:
        return 0.0  # not matching at all


#budget matching
def budget_fit(averagePricePP, budget):
    if budget is None:
        return 1.0  # no budget given, assume ok
    averagepricePP = int(averagePricePP)
    budget = int(budget)
    if averagePricePP <= budget:
        return 1.0
    elif averagePricePP <= budget * 1.2:  # up to 20% over budget still ok
        return 0.5
    else:
        return 0.0


#group size matching
def group_fit(groupSize, minGroupSize, maxGroupSize):
    groupSize = int(groupSize)
    if groupSize < minGroupSize:
        # Too small
        return groupSize / minGroupSize
    elif groupSize > maxGroupSize:
        # Too large
        return maxGroupSize / groupSize
    else:
        # Fits perfectly
        return 1.0