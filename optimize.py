import pulp
import json


def optimize_food_counts(foods):
	foods = foods.interpolate()  # fill NaN via interpolation

	diet_model = pulp.LpProblem("The_Diet_Problem")
	X_dict = pulp.LpVariable.dict("x_%s", foods.descriptor, lowBound = 0, upBound = 2, cat=pulp.LpInteger)
	X = list(X_dict.values())

	#TODO: can we add a constraint on leftover servings? something like recipe_serving_amt - X > 0
	#TODO: add num_ingredient column
	#TODO: add num_ingredients_in_pantry column
	#TODO: add time_to_cook column

	diet_model += foods.calories.dot(X) >= 2100
	diet_model += foods.calories.dot(X) <= 2800
	diet_model += foods.protein.dot(X) >= 70
	diet_model += foods.fat.dot(X) >= 70
	diet_model += foods.fat.dot(X) <= 120
	# diet_model += foods.Cholesterol.dot(X) <= 1
	diet_model += foods.sodium.dot(X) <= 3
	diet_model += foods.carbohydrates.dot(X) >= 250
	diet_model += foods.fiber.dot(X) >= 15
	# diet_model += foods.recipe_serving_amt.dot(X) >= 300
	diet_model += foods.Breakfast.dot(X) >= 1
	diet_model += foods.Lunch.dot(X) >= 1
	diet_model += foods.Dinner.dot(X) >= 1
	diet_model += foods.Snack.dot(X) <= 1
	diet_model += (pulp.lpSum(X) <= 5, "Maximum_total_meals")
	diet_model += (pulp.lpSum(X) >= 2, "Minimum_total_meals") 
	diet_model.solve()

	# print(diet_model)

	foods['numMeals'] = [x.value() for x in X]

	return foods