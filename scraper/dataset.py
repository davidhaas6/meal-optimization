import pandas as pd
from os import path

def write_dataset_from_json(data_path: str, output_path: str):
    recipes = read_recipes_json(data_path)
    nutrition = get_nutrition_df(recipes)
    mealType_df = get_meal_type_df(recipes)

    minimalMealType = mealType_df[['Breakfast','Lunch','Dinner','Snack','descriptor']]
    dataset = pd.merge(nutrition, minimalMealType, how='inner', on='descriptor')
    dataset = pd.merge(dataset, recipes[['servings','totalTime','cookTime','descriptor']], on='descriptor')

    dataset.to_csv(path.join(output_path, 'nutrition.csv'),index_label='index')

def read_recipes_json(path: str) -> pd.DataFrame:
    recipes = pd.read_json(path)
    recipes['mealType'] = recipes.mealType.fillna('')
    recipes['mealType'] = recipes.mealType.str.replace('Diner', 'Dinner')
    return recipes


def get_nutrition_df(recipes: pd.DataFrame) -> pd.DataFrame:
    raw_nutrition = df_from_list_of_json(recipes,'nutrition')
    raw_nutrition['label'] = raw_nutrition.label.apply(lambda s: s[:-2]).str.lower()  # truncate the colon
    raw_nutrition['value'] = raw_nutrition.value.astype(float)
    raw_nutrition = raw_nutrition.drop(raw_nutrition[raw_nutrition.label == 'serving'].index)  # drop Serving size entries

    # Convert mg to grams
    mg_idxs = raw_nutrition.unit=='mg'
    raw_nutrition.loc[mg_idxs,'value'] /= 1000
    raw_nutrition.loc[mg_idxs,'unit'] = 'g'
    raw_nutrition

    # turn the macros from the 'label' column into their own columns
    nutrition = raw_nutrition.pivot_table('value', columns='label', index=['descriptor'])
    return nutrition.reset_index()


def get_meal_type_df(recipes: pd.DataFrame) -> pd.DataFrame:
    unique_meal_types = set(
        mealType for mealTypes in recipes.mealType.str.split(",") for mealType in mealTypes
    )
    mealType = pd.DataFrame(
        {
            mealType: [1 if mealType in cell else 0 for cell in recipes.mealType]
            for mealType in unique_meal_types
        }
    )
    mealType["descriptor"] = recipes["descriptor"]
    return mealType


def df_from_list_of_json(srcDf,srcColumn):
    dfs = srcDf[srcColumn].apply(pd.DataFrame)
    megaDf = pd.DataFrame()
    for i,df in enumerate(dfs):
        df.insert(0,'descriptor', srcDf.loc[i,'descriptor'])
        megaDf = pd.concat([megaDf, df])
    return megaDf

