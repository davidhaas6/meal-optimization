import pulp
import json


def optimize_food_counts(foods, constraints):
	foods = foods.interpolate()  # fill NaN via interpolation

	
	#TODO: can we add a constraint on leftover servings? something like recipe_serving_amt - X > 0
	#			maybe like diet_model += (1/foods.servings).dot(X) <= pulp.lpSum(X) + 2
	#TODO: add num_ingredient column
	#TODO: add num_ingredients_in_pantry column

	diet_model = pulp.LpProblem("The_Diet_Problem")
	X_dict = pulp.LpVariable.dict("x_%s", foods.descriptor, lowBound = 0, upBound = 2, cat=pulp.LpInteger)
	X = list(X_dict.values())

	# apply the constraints
	for varName, varConstraints in constraints.iterrows():
		if varName not in foods.columns: continue
		if varConstraints['min'] > 0:
			diet_model += foods[varName].dot(X) >= varConstraints['min']	
		if varConstraints['max'] > 0:
			diet_model += foods[varName].dot(X) <= varConstraints['max']
			
	diet_model += (pulp.lpSum(X) <= 4, "Maximum_total_meals")
	diet_model += (pulp.lpSum(X) >= 0, "Minimum_total_meals") 

	try:
		diet_model.solve()
	except pulp.apis.core.PulpSolverError as e:
		print(e)
		foods['numMeals'] = [0 for _ in range(len(foods))]
		return foods

	foods['numMeals'] = [x.value() for x in X]
	return foods