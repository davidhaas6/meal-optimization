# A web scraper for the recipe site: https://www.budgetbytes.com/cheese-enchiladas/
# David Haas

from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup
import requests
import time
import json
from recipe_scrapers._schemaorg import SchemaOrg



BASE_URL = "https://www.budgetbytes.com"
NUM_RECIPE_PAGES = 60


@dataclass
class RecipeIngredient:
    amount: str = None
    unit: str = None
    name: str = None
    notes: str = None
    err: bool = False  # True if there was an error parsing the ingredient
    price = None

    def __str__(self) -> str:
        return f'{self.name}, {self.amount} {self.unit}'


@dataclass
class NutritionItem:
    label: str
    value: str
    unit: str

    def __str__(self) -> str:
        return f'{self.label} {self.value} {self.unit}'


@dataclass
class RecipeNutrition:
    components: List[NutritionItem]
    # servings: str = None
    # calories: int = None       # kcal
    # carbohydrates: int = None  # g
    # protein: int = None        # g
    # fat: int = None            # g
    # sodium: int = None         # mg
    # fiber: int = None          # g

    def __str__(self) -> str:
        return '\n'.join(map(str, self.components))


def pull_text(html: BeautifulSoup, class_name: str, el_type: str) -> str:
    el = html.find(el_type, {"class": class_name})
    return el.text if el else ''


def pull_nested_img(html: BeautifulSoup, class_name: str, el_type: str) -> str:
    parent = html.find(el_type, {"class": class_name})
    if not parent:
        return ''
    img_tag = parent.find("img")
    return img_tag["data-src"] if 'data_src' in img_tag else ''


def parse_url(url: str) -> BeautifulSoup:
    """ Parses a url into a beautiful soup object """
    return BeautifulSoup(requests.get(url).text, "html.parser")


def load_recipe_html(descriptor: str) -> BeautifulSoup:
    """ Parses a url to return a beautiful soup object """
    try:
        return parse_url(f'{BASE_URL}/{descriptor}/')
    except Exception as e:
        print("Error:", e)
        return None


def pull_ingredients(page: BeautifulSoup) -> List[RecipeIngredient]:
    """ Pulls ingredients from a parsed page """

    ing_divs = page.find_all("li", {"class": "wprm-recipe-ingredient"})
    prop_map = {
        "wprm-recipe-ingredient-unit": "unit",
        "wprm-recipe-ingredient-amount": "amount",
        "wprm-recipe-ingredient-name": "name",
        "wprm-recipe-ingredient-notes": "notes"
    }

    ingredients = []
    for div in ing_divs:
        i = RecipeIngredient()
        for prop, attr_name in prop_map.items():
            span = div.find("span", {"class": prop})
            if span:
                setattr(i, attr_name, span.text.title())
            else:
                setattr(i, 'err', True)
        ingredients += [i]

    return ingredients


def pull_nutrition(page: BeautifulSoup) -> RecipeNutrition:
    """ Pulls listed nutrition info from recipe """
    # Get generic nutrition items
    prefix = "wprm-nutrition-label-text-nutrition-"
    spans = page.find_all("span", {"class": prefix + "container"})

    nutrition_items = []
    for item_span in spans:
        name = pull_text(item_span, prefix + "label", "span")
        value = pull_text(item_span, prefix + "value", "span")
        unit = pull_text(item_span, prefix + "unit", "span")
        nutrition_items.append(NutritionItem(name, value, unit))

    return RecipeNutrition(nutrition_items)


def pull_time(page: BeautifulSoup) -> str:
    """ Pulls the total time (prep + cook) """
    return pull_text(page, "wprm-recipe-time", "span")


def pull_name(page: BeautifulSoup) -> str:
    return pull_text(page, "wprm-recipe-name", "h2")


def pull_instructions(page: BeautifulSoup) -> str:
    return pull_text(page, "wprm-recipe-instruction-group", "div")


def pull_thumb_img(page: BeautifulSoup) -> str:
    return pull_nested_img(page, "wprm-recipe-image", "div")


def pull_servings_count(page: BeautifulSoup) -> int:
    """ Pulls the number of servings """
    text = pull_text(page, "wprm-recipe-servings", "span")
    try:
        return int(text)
    except:
        return None


def pull_categories(page: BeautifulSoup) -> List[str]:
    footer = page.find("footer", {"class": "post-meta"})
    if (footer == None): 
        return
    return [cat.text for cat in footer.find_all("a", {"rel": "category"})]


def pull_meal_types(page: BeautifulSoup) -> List[str]:
    return SchemaOrg(str(page.html)).category()


def pull_cost_string(page: BeautifulSoup) -> str:
    return pull_text(page, "cost-per", "span")


def pull_score(page: BeautifulSoup) -> str:
    return pull_text(page, "wprm-recipe-rating-average", "span")


def pull_vote_count(page: BeautifulSoup) -> str:
    return pull_text(page, "wprm-recipe-rating-count", "span")


def page_to_dict(page: BeautifulSoup, descriptor: str) -> dict:
    """ Creates a JSON from the relevant recipe info """
    object = dict()
    object['nutrition'] = [x.__dict__ for x in pull_nutrition(page).components]
    object['ingredients'] = [x.__dict__ for x in pull_ingredients(page)]
    object['descriptor'] = descriptor
    object['url'] = f'{BASE_URL}/{descriptor}/'
    object['thumb_img'] = pull_thumb_img(page)
    object['instructions'] = pull_instructions(page)
    object['name'] = pull_name(page)
    object['servings'] = pull_servings_count(page)
    object['score'] = pull_score(page)
    object['vote_count'] = pull_vote_count(page)
    object['cost_str'] = pull_cost_string(page)
    object['categories'] = pull_categories(page)

    schema = SchemaOrg(str(page.html))
    object['mealType'] = schema.category()
    object['cuisine'] = schema.cuisine()  if 'recipeCuisine' in schema.data.keys() else ''
    object['prepTime'] = schema.prep_time() if 'prepTime' in schema.data.keys() else 0
    object['cookTime'] = schema.cook_time() if 'cookTime' in schema.data.keys() else None
    try: object['totalTime'] = schema.total_time()
    except: object['totalTime'] = None

    return object


def pull_recipe_links(pages):
    """ Pulls all recipe links from the site """
    links = []
    for i in range(1, pages+1):
        page = parse_url(f'{BASE_URL}/category/recipes/page/{i}/')
        page_recipes = page.find_all("article", {"class": "post"})
        links += [post.find("a")['href'] for post in page_recipes]
        if i < pages:
            time.sleep(0.25)
    return links


def links_to_descriptors(linksfile: str) -> List[str]:
    """ Parses a list of links to recipe descriptors """
    with open(linksfile, 'r') as f:
        links = f.readlines()
    return [link.split('/')[-2] for link in links]


def build_json_db(descriptors: List[str], filename) -> dict:
    """ This builds a large JSON file out of recipies in the descriptors list """
    recipes = []
    import tqdm
    for desc in tqdm.tqdm(descriptors):
        page = load_recipe_html(desc)
        if not page:
            print(f'Error on page: {desc}')
            continue
        recipes.append(page_to_dict(page, desc))
        time.sleep(0.1)

    with open(filename, 'w') as f:
        json.dump(recipes, f)
