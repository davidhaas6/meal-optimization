import pandas as pd
import optimize

df = pd.read_csv('data/bb_nutrition.csv',index_col=0)
bad_rows = '|'.join(['best-ever-avocado-dip'])
df = df[~df.descriptor.str.contains(bad_rows)]

df = df.sample(frac=0.75,axis=0)
df = optimize.optimize_food_counts(df)

mealplan = df[df.numMeals > 0]
mealplan['leftover_servings'] = mealplan.servings - mealplan.numMeals

total_macros = mealplan.iloc[:,1:-2].multiply(mealplan.numMeals,axis=0)
total_macros['descriptor'] = mealplan.descriptor

print("\n\nMeal Plan:")
print(mealplan)
# print("\n\nMacros:")
# print(total_macros)
print('\n', total_macros.sum())

