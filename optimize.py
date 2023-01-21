import pulp
import json

def get_daily_meals(foods):
	# todo: make dataframe of foods

	# loads in food data
	names, cals, fat, cholesterol, protein, carb, servings = ([] for _ in range(7))
	for food in foods:
		names.append(food['name'])
		cals.append(float(food['calories']))
		if 'Total Fat' in food:
			fat.append(float(food['Total Fat']))
		else:
			fat.append(0)
		if 'Cholesterol' in food:
			cholesterol.append(float(food['Cholesterol']))
		else:
			cholesterol.append(0)
		if 'Protein' in food:
			protein.append(float(food['Protein']))
		else:
			protein.append(0)
		carb.append(float(food['Total Carbohydrate']))
		servings.append(float(food['servings']))

	# create {foodName: macro} mapping
	calories = dict(zip(names, cals))
	carbs = dict(zip(names, carb))
	fats = dict(zip(names, fat))
	proteins = dict(zip(names, protein))
	chols = dict(zip(names, cholesterol))

	# solve the linear optimization
	diet_model = pulp.LpProblem("The_Diet_Problem", pulp.LpMaximize)
	x = pulp.LpVariable.dict("x_%s", names, lowBound = 0, upBound = 3, cat=pulp.LpInteger)

	diet_model += sum([calories[i] * x[i] for i in names]) >= 1800
	diet_model += sum([calories[i] * x[i] for i in names]) <= 2800
	diet_model += sum([proteins[i]*x[i] for i in names]) >= 88
	diet_model += sum([fats[i]*x[i] for i in names]) >= 58
	diet_model += sum([chols[i]*x[i] for i in names]) <= 1

	diet_model.solve()

	# load the non-zero parameters of the model
	selected_foods = []
	servings = []
	for food in names:
		if x[food].value() != 0:
			selected_foods.append("%s servings of %s"%(x[food].value(),food))
		servings.append(x[food].value())

	# parse them back into total macros
	cal, f, ch, pr, car = (0 for i in range(5))
	for food in names:
		cal += x[food].value()*calories[food]
		pr += x[food].value()*proteins[food]
		f += x[food].value()*fats[food]
		car += x[food].value()*carbs[food]
		ch += x[food].value()*chols[food]

	# string-readable info
	nutrient_information = []
	nutrient_information.append("Calories: " + str(round(cal,4)))
	nutrient_information.append("Total Fat: " + str(round(f,4)))
	nutrient_information.append("Protein: " +  str(round(pr,4)))
	nutrient_information.append("Carbohydrates: " + str(round(car,4)))
	nutrient_information.append("Cholesterol: " + str(round(ch,4)))

	return [selected_foods,nutrient_information,servings]