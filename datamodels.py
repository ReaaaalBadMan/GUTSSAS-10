class Activity:
    def __init__(self, name, category, averagePricePP, minGroupSize, maxGroupSize, rating, tags):
        self.name = name 
        self.category=category
        self.averagePricePP = averagePricePP
        self.minGroupSize = minGroupSize
        self.maxGroupSize = maxGroupSize
        self.rating = rating
        self.tags = tags








class Request():
    def __init__(self, mood, budget, groupSize):
        self.mood = mood
        self.budget= budget
        self.groupSize= groupSize







class Suggestion():
    def __init__(self, name, reason, score):
        self.reason = reason
        self.name = name
        self.score = score
