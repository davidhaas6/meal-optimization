import pandas as pd
import optimize

# load and preprocess our data
dataset = pd.read_csv('data/nutrition.csv', index_col=0)
bad_rows = '|'.join(['best-ever-avocado-dip'])
dataset = dataset[~dataset.descriptor.str.contains(bad_rows)]
# print(dataset.head(3))

# incorporate user preferences
constraints = pd.DataFrame(index=dataset.columns.unique())
constraints['min'] = {
    'calories': 2100,
    'protein': 70,
    'fat': 50,
    'carbohydrates': 50,
    'fiber': 10,
    'Breakfast': 1,
    'Lunch': 1,
    'Dinner': 1,
}
constraints['max'] = {
    'calories': 2800,
    'protein': 150,
    'fat': 120,
    'carbohydrates': 400,
    'sodium': 4,
    'totalTime': 60,
    'cookTime': 60,
    'Breakfast': 2
}
# print(constraints)

# optimize
days = []
for i in range(1):
    sample = dataset.sample(frac=.75, axis=0)
    mealplan = optimize.optimize_food_counts(sample, constraints)
    mealplan = mealplan[mealplan.numMeals > 0]
    print(f"\nDaily meal plan {i+1}")
    days.append(', '.join(mealplan.descriptor))
    print(', '.join(mealplan.descriptor))

for i, day in enumerate(days):
    print(f"\nDaily meal plan {i+1}:")
    print(day.replace('-', ' '))

# postprocess and print
mealplan = mealplan[mealplan.numMeals > 0]
mealplan['leftover_servings'] = mealplan.servings.subtract(mealplan.numMeals)
total_macros = mealplan.iloc[:, 1:-2].multiply(mealplan.numMeals, axis=0)
total_macros['descriptor'] = mealplan.descriptor

print("\n\nMeal Plan:")
print(mealplan)
# print("\n\nMacros:")
# print(total_macros)
print('\n', total_macros.sum())
