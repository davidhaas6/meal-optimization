import requests
import re
from optimize import *

headers = {
    'authority': 'www.instacart.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
    'cookie': 'device_uuid=2191862f-7d52-412d-81f6-3f22e699f3bf; _instacart_logged_in=1; ab.storage.deviceId.6f8d91cb-99e4-4ad7-ae83-652c2a2c845d=%7B%22g%22%3A%22f29a4630-fc05-5fbb-138f-043a35e5b1b4%22%2C%22c%22%3A1622312907388%2C%22l%22%3A1622312907388%7D; __stripe_mid=ed784535-8515-4dcd-bd14-8df2da9478f974bd78; G_ENABLED_IDPS=google; known_visitor=%7Cjosh.r.mosier%40gmail.com%7Cgoogle_sso; ab.storage.userId.6f8d91cb-99e4-4ad7-ae83-652c2a2c845d=%7B%22g%22%3A%2256907461%22%2C%22c%22%3A1633024308752%2C%22l%22%3A1633024308752%7D; __Host-instacart_sid=f93afec1cece2ba3ee6076faba68d702692106562c33cb2edcb31b9bff7ec938; forterToken=1a28c0f50e9142b8ae888b7f59830628_1634739248336_1069_UAL9_9ck; ab.storage.sessionId.6f8d91cb-99e4-4ad7-ae83-652c2a2c845d=%7B%22g%22%3A%22a2998256-bc0e-29d3-00cc-9a3cd8ebdec8%22%2C%22e%22%3A1634741049768%2C%22c%22%3A1634737593531%2C%22l%22%3A1634739249768%7D; ahoy_visit=0a0505b9-25a9-4c7d-9396-b6093fca16dc; ahoy_track=true; __cf_bm=Ko3fhTvzhgJtz4SD7F.JyQqeweMBYzOfCE_59kcwJrM-1634835690-0-ATIJUCUmnmhYBltn/DEjAPVko83MJ3QmwmjdJn8xAnz6O8CKTDfZdFSImJKRwmwt5vh44w9igFAWvkpTQZfdtyI=; ahoy_visitor=4f4c86da-7cf7-488d-83a0-111fc298c098; build_sha=30b00064edc6baf398ce846905955f526065fd9d; _instacart_session_id=eS80eFJ0czdJTk11MUtXMUNGaUpDT1JlVlpaeWozaFVZTEpTZ2ZacWFmYk9INnlIckJ2dHZEMjV6aTYrZlJCTDJ2dzJsVGQ5UnFlaU9ReVFRYWd3SmhQQ3dWaldIMDZUOFp1ajk3ZEVXaUYzVmxhOFlxMkNOUTJKck1EYXdHTGVna3pDVUF1UGY0REF4R1ZEWlhBV0RhYVE1VC9kbGowd0lweTF2STB4RzNqTXZMSTRXUzRXb1g4QlcrcTZpOGVrSnJRTEVrVXFmT1NNdFJ2Q201bFRsTFJCT3BPeVQwU091QUR4a0IrYzFTNDhhNmNPTEtiTUEvOVJGQ3JQQXVETi0tN1pscmI2czRWdzFQSmNKYU5WZVVVZz09--cd56ad69872aa78cdf6dac47f868ade2d984ef79',
}


# item_ids = ['808750234', '1414471631', '812380440', '812079813', '2971701912', '812793694', '813089764', '812228688', '812753249', '812108352', '811849927', '808748204', '808752261', '808749751', '811728053', '812521869', '808750122', '812761281', '812364282', '812075732', '812075992', '808749043', '811830256', '808740726', '808751010', '812426371', '812724444', '812956540', '1396373946', '808751023', '808752777', '812143565']
# item_names = ['Sanpellegrino Lemon Italian Sparkling Drinks', 'Sargento Natural String Cheese Snacks', "Nature's Own Honey Wheat Bread", 'Kroger 2% Reduced Fat Milk', 'Banana', 'Kroger Honeycrisp Apples Pouch Bag', 'Navel Orange', "Ben & Jerry's Ice Cream Strawberry Cheesecake", "Kellogg's Raisin Bran Breakfast Cereal, High Fiber Cereal, Original", 'Lucky Charms Marshmallow Breakfast Cereal with Unicorns, Gluten Free', "Mott's Original Applesauce", 'Nature Valley Granola Bars, Dark Chocolate Cherry, Trail Mix, Chewy', 'Toll House Chocolate Chip Cookie Dough', 'Kroger Large Eggs', 'Kroger Plain Cream Cheese', 'Thomas Cinnamon Raisin Pre-Sliced Bagels', 'El Monterey Chicken & Cheese Flour Taquitos', 'Kroger Cut & Peeled Baby Carrots', 'Kroger Fresh Selections Celery Hearts', 'Hot Pockets Italian Style Meatballs & Mozzarella Garlic Buttery Crust Frozen Snacks', 'Kraft Deluxe Original Cheddar Macaroni & Cheese Dinner', 'StarKist Chunk Light Tuna in Water, Pouch', 'Pillsbury Toaster Strudel Apple Toaster Pastries, Value Size, 12 Count', 'Sargento Balanced Breaks Natural Sharp Cheddar Cheese, Sea-Salted Cashews and Cherry Juice-Infused Dried Cranberries', 'noosa Lemon Yogurt', 'Tostitos Scoops Party Size Tortilla Chips', 'Tostitos Medium Chunky Salsa Dip', 'Chips Ahoy! Chewy Chocolate Chip Cookies, Family Size', 'Larabar Peanut Butter Chocolate Chip Fruit & Nut Bars', 'A&W Root Beer', 'Eggo Frozen Waffles, Frozen Breakfast, Chocolatey Chip', 'Kraft Singles American Cheese Slices']

item_ids = ['1584532493', '808741688', '812793694', '2971701912', '813089764', '812140762', '812551255', '812364282', '812118487', '811938956', '808749751', '812380440', '1414471631', '812079813', '812146846', '811849927', '812753249', '808751010', '812521869', '812428249', '3184483634', '812158531', '812090644', '812359817', '808750234', '811716865', '808742145', '812919252', '808748204']
item_names = ["One A Day Multivitamin/Multimineral Supplement, Men's, Gummies", 'Ice Breakers Gum, Sugar Free, Peppermint', 'Kroger Honeycrisp Apples Pouch Bag', 'Banana', 'Navel Orange', 'Organic Red Seedless Grapes', 'Kroger Cut & Peeled Baby Carrots', 'Kroger Fresh Selections Celery Hearts', 'Kroger Fresh Selections Italian Style Blend, Romaine Lettuce & Radicchio', "Ken's Steak House Dressing, Balsamic Vinaigrette", 'Kroger Large Eggs', "Nature's Own Honey Wheat Bread", 'Sargento Natural String Cheese Snacks', 'Kroger 2% Reduced Fat Milk', 'Toll House Semi Sweet Chocolate Chips', "Mott's Original Applesauce", "Kellogg's Raisin Bran Breakfast Cereal, High Fiber Cereal, Original", 'noosa Lemon Yogurt', 'Thomas Cinnamon Raisin Pre-Sliced Bagels', 'Sargento Balanced Breaks, Pepper Jack Natural Cheese, Honey Roasted Peanuts and Raisins', 'Melons - Cantaloupe', "Ben & Jerry's Ice Cream Chocolate Chip Cookie Dough", 'Kroger Probiotic Dried Apricots', 'Kroger Salted Mixed Nuts', 'San Pellegrino Lemon Italian Sparkling Drinks', 'Head & Shoulders Apple Head and Shoulders Green Apple 2-in-1 Anti-Dandruff Shampoo + Conditioner 13.5 Fl Oz Female Hair Care', 'noosa Tart Cherry Yoghurt', 'noosa Strawberry Rhubarb Yogurt', 'Nature Valley Chewy Trail Mix Granola Bar, Dark Chocolate Cherry, 12 Bars']

def get_nutrition_info(ids,names):
    foods = []
    for i,item_id in enumerate(item_ids):
        food = {}
        response = requests.get('https://www.instacart.com/v3/containers/items/item_' + str(item_id), headers=headers)
        for module in response.json()['container']['modules']:
            if module['id'].startswith('item_details_attributes'):
                print(item_names[i])
                if module['data']['nutrition']:
                    food['name'] = item_names[i]
                    food['calories'] = module['data']['nutrition']['calories']
                    if module['data']['nutrition']["servings_per_container"]:
                        servings = module['data']['nutrition']["servings_per_container"]
                        print("Servings: " + str(servings))
                        # print(int(re.findall(r'\d+', servings)[0])) #Servings --> Int
                        food['servings'] = int(re.findall(r'\d+', servings)[0])
                    for nutrient in module['data']['nutrition']['nutrients']:
                        total = float(re.search("[-+]?\d*\.\d+|\d+",nutrient['total'])[0])
                        if nutrient['total'].endswith('mg'):
                            total = total / 1000
                        food[nutrient['label']] = total
                        print('\t' + nutrient['label'] + " " + str(total))
                    foods.append(food)
    return foods

# foods = get_nutrition_info(item_ids,item_names)
# print(foods)
# foods = [{'name': 'Sanpellegrino Lemon Italian Sparkling Drinks', 'calories': 120.0, 'Total Fat': 0.0, 'Cholesterol': 0.0, 'Sodium': 0.005, 'Total Carbohydrate': 31.0, 'Protein': 0.0}, {'name': 'Sargento Natural String Cheese Snacks', 'calories': 80.0, 'Total Fat': 6.0, 'Cholesterol': 0.015, 'Sodium': 0.2, 'Total Carbohydrate': 0.0, 'Protein': 8.0}, {'name': "Nature's Own Honey Wheat Bread", 'calories': 70.0, 'Total Fat': 1.0, 'Cholesterol': 0.0, 'Sodium': 0.12, 'Total Carbohydrate': 14.0, 'Protein': 3.0}, {'name': 'Kroger 2% Reduced Fat Milk', 'calories': 120.0, 'Total Fat': 5.0, 'Cholesterol': 0.02, 'Sodium': 0.12, 'Total Carbohydrate': 12.0, 'Protein': 8.0}, {'name': "Ben & Jerry's Ice Cream Strawberry Cheesecake", 'calories': 340.0, 'Total Fat': 20.0, 'Cholesterol': 0.08, 'Sodium': 0.15, 'Total Carbohydrate': 37.0, 'Protein': 5.0}, {'name': "Kellogg's Raisin Bran Breakfast Cereal, High Fiber Cereal, Original", 'calories': 190.0, 'Total Fat': 1.0, 'Cholesterol': 0.0, 'Sodium': 0.2, 'Total Carbohydrate': 47.0, 'Protein': 5.0}, {'name': 'Lucky Charms Marshmallow Breakfast Cereal with Unicorns, Gluten Free', 'calories': 140.0, 'Total Fat': 1.0, 'Cholesterol': 0.0, 'Sodium': 0.17, 'Total Carbohydrate': 30.0, 'Protein': 2.0}, {'name': "Mott's Original Applesauce", 'calories': 90.0, 'Total Fat': 0.0, 'Cholesterol': 0.0, 'Sodium': 0.0, 'Total Carbohydrate': 24.0, 'Protein': 0.0}, {'name': 'Nature Valley Granola Bars, Dark Chocolate Cherry, Trail Mix, Chewy', 'calories': 150.0, 'Total Fat': 4.0, 'Cholesterol': 0.0, 'Sodium': 0.07, 'Total Carbohydrate': 25.0, 'Protein': 2.0}, {'name': 'Toll House Chocolate Chip Cookie Dough', 'calories': 80.0, 'Total Fat': 4.0, 'Cholesterol': 0.005, 'Sodium': 0.065, 'Total Carbohydrate': 11.0, 'Protein': 1.0}, {'name': 'Kroger Large Eggs', 'calories': 70.0, 'Total Fat': 5.0, 'Cholesterol': 0.185, 'Sodium': 0.07, 'Total Carbohydrate': 0.0, 'Protein': 6.0}, {'name': 'Thomas Cinnamon Raisin Pre-Sliced Bagels', 'calories': 280.0, 'Total Fat': 1.5, 'Cholesterol': 0.0, 'Sodium': 0.39, 'Total Carbohydrate': 56.0, 'Protein': 9.0}, {'name': 'El Monterey Chicken & Cheese Flour Taquitos', 'calories': 220.0, 'Total Fat': 11.0, 'Cholesterol': 0.01, 'Sodium': 0.28, 'Total Carbohydrate': 26.0, 'Protein': 7.0}, {'name': 'Kroger Fresh Selections Celery Hearts', 'calories': 20.0, 'Total Fat': 0.0, 'Cholesterol': 0.0, 'Sodium': 0.09, 'Total Carbohydrate': 3.0}, {'name': 'Hot Pockets Italian Style Meatballs & Mozzarella Garlic Buttery Crust Frozen Snacks', 'calories': 300.0, 'Total Fat': 12.0, 'Cholesterol': 0.015, 'Sodium': 0.46, 'Total Carbohydrate': 38.0, 'Protein': 10.0}, {'name': 'Kraft Deluxe Original Cheddar Macaroni & Cheese Dinner', 'calories': 310.0, 'Total Fat': 11.0, 'Cholesterol': 0.015, 'Sodium': 0.91, 'Total Carbohydrate': 42.0, 'Protein': 12.0}, {'name': 'StarKist Chunk Light Tuna in Water, Pouch', 'calories': 70.0, 'Total Fat': 0.0, 'Cholesterol': 0.035, 'Sodium': 0.3, 'Total Carbohydrate': 0.0, 'Protein': 17.0}, {'name': 'Pillsbury Toaster Strudel Apple Toaster Pastries, Value Size, 12 Count', 'calories': 350.0, 'Total Fat': 13.0, 'Cholesterol': 0.0, 'Sodium': 0.3, 'Total Carbohydrate': 53.0, 'Protein': 5.0}, {'name': 'Sargento Balanced Breaks Natural Sharp Cheddar Cheese, Sea-Salted Cashews and Cherry Juice-Infused Dried Cranberries', 'calories': 180.0, 'Total Fat': 11.0, 'Cholesterol': 0.02, 'Sodium': 0.18, 'Total Carbohydrate': 14.0, 'Protein': 7.0}, {'name': 'noosa Lemon Yogurt', 'calories': 320.0, 'Total Fat': 13.0, 'Cholesterol': 0.04, 'Sodium': 0.11, 'Total Carbohydrate': 39.0, 'Protein': 12.0}, {'name': 'Tostitos Scoops Party Size Tortilla Chips', 'calories': 140.0, 'Total Fat': 7.0, 'Cholesterol': 0.0, 'Sodium': 0.115, 'Total Carbohydrate': 19.0, 'Protein': 2.0}, {'name': 'Tostitos Medium Chunky Salsa Dip', 'calories': 10.0, 'Total Fat': 0.0, 'Cholesterol': 0.0, 'Sodium': 0.25, 'Total Carbohydrate': 2.0, 'Protein': 0.0}, {'name': 'Chips Ahoy! Chewy Chocolate Chip Cookies, Family Size', 'calories': 140.0, 'Total Fat': 6.0, 'Cholesterol': 0.0, 'Sodium': 0.09, 'Total Carbohydrate': 21.0, 'Protein': 1.0}, {'name': 'A&W Root Beer', 'calories': 160.0, 'Total Fat': 0.0, 'Cholesterol': 0.0, 'Sodium': 0.085, 'Total Carbohydrate': 44.0, 'Protein': 0.0}, {'name': 'Eggo Frozen Waffles, Frozen Breakfast, Chocolatey Chip', 'calories': 200.0, 'Total Fat': 7.0, 'Cholesterol': 0.005, 'Sodium': 0.37, 'Total Carbohydrate': 32.0, 'Protein': 4.0}, {'name': 'Kraft Singles American Cheese Slices', 'calories': 60.0, 'Total Fat': 4.0, 'Cholesterol': 0.015, 'Sodium': 0.24, 'Total Carbohydrate': 2.0, 'Protein': 4.0}]
foods2 = [
  {
    "name": "Smart Balance Buttery Spread, Made with Extra Virgin Olive Oil",
    "calories": 60,
    "servings": 33,
    "Total Fat": 7,
    "Cholesterol": 0,
    "Sodium": 0.07,
    "Total Carbohydrate": 0,
    "Protein": 0
  },
  {
    "name": "Nutella Hazelnut Spread, with Cocoa",
    "calories": 200,
    "servings": 5,
    "Total Fat": 11,
    "Cholesterol": 0.005,
    "Sodium": 0.015,
    "Total Carbohydrate": 22,
    "Protein": 2
  },
  {
    "name": "Simply Light Lemonade, Non-Gmo",
    "calories": 25,
    "servings": 7,
    "Total Fat": 0,
    "Sodium": 0.015,
    "Total Carbohydrate": 7,
    "Protein": 0
  },
  {
    "name": "Nature's Own Honey Wheat Bread",
    "calories": 70,
    "servings": 20,
    "Total Fat": 1,
    "Cholesterol": 0,
    "Sodium": 0.12,
    "Total Carbohydrate": 14,
    "Protein": 3
  },
  {
    "name": "Post Honey Bunches of Oats Honey Roasted",
    "calories": 160,
    "servings": 16,
    "Total Fat": 2,
    "Cholesterol": 0,
    "Sodium": 0.19,
    "Total Carbohydrate": 34,
    "Protein": 3
  },
  {
    "name": "Mott's No Sugar Added Applesauce",
    "calories": 50,
    "servings": 6,
    "Total Fat": 0,
    "Cholesterol": 0,
    "Sodium": 0,
    "Total Carbohydrate": 13,
    "Protein": 0
  },
  {
    "name": "Amy's Kitchen Black Bean Vegetables Burrito",
    "calories": 290,
    "servings": 1,
    "Total Fat": 9,
    "Cholesterol": 0,
    "Sodium": 0.68,
    "Total Carbohydrate": 44,
    "Protein": 8
  },
  {
    "name": "StarKist Chunk Light Tuna in Water, Pouch",
    "calories": 70,
    "servings": 1,
    "Total Fat": 0,
    "Cholesterol": 0.035,
    "Sodium": 0.3,
    "Total Carbohydrate": 0,
    "Protein": 17
  },
  {
    "name": "Jimmy Dean Delights Turkey Sausage, Egg White & Cheese English Muffin Breakfast Sandwiches",
    "calories": 270,
    "servings": 4,
    "Total Fat": 8,
    "Cholesterol": 0.03,
    "Sodium": 0.71,
    "Total Carbohydrate": 31,
    "Protein": 18
  },
  {
    "name": "Sargento Balanced Breaks Natural White Cheddar Cheese, Sea-Salted Roasted Almonds, Dried Cranberries, Six-Pack",
    "calories": 190,
    "servings": 6,
    "Total Fat": 13,
    "Cholesterol": 0.02,
    "Sodium": 0.17,
    "Total Carbohydrate": 12,
    "Protein": 7
  },
  {
    "name": "I Can't Believe It's Not Butter Vegetable Oil Spread, The Light One",
    "calories": 35,
    "servings": 30,
    "Total Fat": 4,
    "Cholesterol": 0,
    "Sodium": 0.085,
    "Total Carbohydrate": 0,
    "Protein": 0
  },
  {
    "name": "Barnana Organic Chewy Chocolate Banana Bites",
    "calories": 170,
    "servings": 2,
    "Total Fat": 9,
    "Cholesterol": 0,
    "Sodium": 0,
    "Total Carbohydrate": 18,
    "Protein": 4
  },
  {
    "name": "Nature Valley Granola Bar, Sweet & Salty Dark Chocolate Peanut & Almond, 6 Bars",
    "calories": 170,
    "servings": 6,
    "Total Fat": 8,
    "Cholesterol": 0,
    "Sodium": 0.125,
    "Total Carbohydrate": 22,
    "Protein": 3
  },
  {
    "name": "Amy's Kitchen Frozen Bean & Rice Burrito, Vegan, Non-Dairy",
    "calories": 310,
    "servings": 1,
    "Total Fat": 9,
    "Cholesterol": 0,
    "Sodium": 0.6,
    "Total Carbohydrate": 48,
    "Protein": 10
  },
  {
    "name": "SB Milk, Fat Free",
    "calories": 90,
    "servings": 8,
    "Total Fat": 0,
    "Cholesterol": 0.005,
    "Sodium": 0.13,
    "Total Carbohydrate": 12,
    "Protein": 8
  },
  {
    "name": "Sparkling Ice Sparkling Water Variety Pack",
    "calories": 5,
    "servings": 12,
    "Total Fat": 0,
    "Sodium": 0,
    "Total Carbohydrate": 0,
    "Protein": 0
  },
  {
    "name": "Birds Eye Broccoli Florets",
    "calories": 30,
    "servings": 3,
    "Total Fat": 0,
    "Cholesterol": 0,
    "Sodium": 0.02,
    "Total Carbohydrate": 4,
    "Protein": 1
  },
  {
    "name": "Jell-O Strawberry Sugar Free Ready-to-Eat Jello Cups Gelatin Snack",
    "calories": 10,
    "servings": 4,
    "Total Fat": 0,
    "Cholesterol": 0,
    "Sodium": 0.045,
    "Total Carbohydrate": 0,
    "Protein": 1
  },
  {
    "name": "Sargento Balanced Breaks, Pepper Jack Natural Cheese, Honey Roasted Peanuts and Raisins",
    "calories": 170,
    "servings": 3,
    "Total Fat": 11,
    "Cholesterol": 0.02,
    "Sodium": 0.19,
    "Total Carbohydrate": 12,
    "Protein": 7
  },
  {
    "name": "McVitie's HobNobs",
    "calories": 90,
    "servings": 16,
    "Total Fat": 4.5,
    "Cholesterol": 0,
    "Sodium": 0.06,
    "Total Carbohydrate": 12,
    "Protein": 1
  },
  {
    "name": "Coffee mate Zero Sugar French Vanilla Liquid Coffee Creamer",
    "calories": 15,
    "servings": 126,
    "Total Fat": 1,
    "Cholesterol": 0,
    "Sodium": 0.005,
    "Total Carbohydrate": 1,
    "Protein": 0
  },
  {
    "name": "Fiber One Cheesecake Bar, Strawberry, Dessert Bar, 5 Count",
    "calories": 160,
    "servings": 5,
    "Total Fat": 6,
    "Cholesterol": 0.015,
    "Sodium": 0.13,
    "Total Carbohydrate": 24,
    "Protein": 3
  },
  {
    "name": "Sun-Maid Vanilla Yogurt Covered Raisins",
    "calories": 120,
    "servings": 6,
    "Total Fat": 5,
    "Cholesterol": 0,
    "Sodium": 0.015,
    "Total Carbohydrate": 19,
    "Protein": 1
  },
  {
    "name": "Angie's White Cheddar Popcorn",
    "calories": 150,
    "servings": 4,
    "Total Fat": 9,
    "Cholesterol": 0.005,
    "Sodium": 0.27,
    "Total Carbohydrate": 15,
    "Protein": 3
  },
  {
    "name": "belVita Blueberry Breakfast Biscuits",
    "calories": 230,
    "servings": 5,
    "Total Fat": 8,
    "Cholesterol": 0,
    "Sodium": 0.21,
    "Total Carbohydrate": 36,
    "Protein": 4
  },
  {
    "name": "Thomas Plain Original Pre-Sliced Bagels",
    "calories": 270,
    "servings": 6,
    "Total Fat": 1.5,
    "Cholesterol": 0,
    "Sodium": 0.45,
    "Total Carbohydrate": 53,
    "Protein": 9
  },
  {
    "name": "Philadelphia Reduced Fat Cream Cheese Spread with a Third Less Fat",
    "calories": 60,
    "servings": 15,
    "Total Fat": 5,
    "Cholesterol": 0.02,
    "Sodium": 0.12,
    "Total Carbohydrate": 2,
    "Protein": 3
  },
  {
    "name": "Sweet Earth Cubano Empanada",
    "calories": 350,
    "servings": 1,
    "Total Fat": 20,
    "Cholesterol": 0.05,
    "Sodium": 0.52,
    "Total Carbohydrate": 29,
    "Protein": 15
  },
  {
    "name": "Harvest Snaps Green Pea Snack Crisps, Original, Lightly Salted",
    "calories": 130,
    "servings": 3,
    "Total Fat": 5,
    "Cholesterol": 0,
    "Sodium": 0.075,
    "Total Carbohydrate": 16,
    "Protein": 5
  },
  {
    "name": "Hippeas Organic Chickpea Puffs, Vegan White Cheddar",
    "calories": 130,
    "servings": 10,
    "Total Fat": 5,
    "Cholesterol": 0,
    "Sodium": 0.14,
    "Total Carbohydrate": 17,
    "Protein": 4
  },
  {
    "name": "belVita Breakfast Biscuits, Golden Oat Flavor",
    "calories": 230,
    "servings": 5,
    "Total Fat": 8,
    "Cholesterol": 0,
    "Sodium": 0.22,
    "Total Carbohydrate": 35,
    "Protein": 4
  },
  {
    "name": "Amy's Kitchen Frozen Southwestern Burrito, Made with Organic Corn, Beans and Cheese, Non-GMO",
    "calories": 300,
    "servings": 1,
    "Total Fat": 11,
    "Cholesterol": 0.015,
    "Sodium": 0.75,
    "Total Carbohydrate": 38,
    "Protein": 12
  },
  {
    "name": "Philadelphia Original Cream Cheese",
    "calories": 100,
    "servings": 8,
    "Total Fat": 10,
    "Cholesterol": 0.03,
    "Sodium": 0.11,
    "Total Carbohydrate": 1,
    "Protein": 2
  },
  {
    "name": "Sargento Balanced Breaks with Natural White Cheddar Cheese, Sea-Salted Roasted Almonds and Dried Cranberries, One.Five oz., Three-Pack",
    "calories": 180,
    "servings": 3,
    "Total Fat": 11,
    "Cholesterol": 0.02,
    "Sodium": 0.18,
    "Total Carbohydrate": 14,
    "Protein": 7
  }
]
results = get_daily_meals(foods2)
print(results)

# servings = results[2]

# def subtract_servings(foods,servings):
#     for i,item in enumerate(foods):
#         item['servings'] = int(item['servings']) - servings[i]
#     return foods

# def total_cals(foods):
#     cals = 0
#     for item in foods:
#         cals = cals + item['calories']*item['servings']
#     return cals

# print(total_cals(foods2))

# i = 0
# temp_foods = [{'name': 'Kroger Fresh Selections Celery Hearts', 'calories': 20.0, 'servings': 4, 'Total Fat': 0.0, 'Cholesterol': 0.0, 'Sodium': 0.09, 'Total Carbohydrate': 3.0}, {'name': 'Kroger Fresh Selections Italian Style Blend, Romaine Lettuce & Radicchio', 'calories': 15.0, 'servings': 3, 'Total Fat': 0.0, 'Cholesterol': 0.0, 'Sodium': 0.01, 'Total Carbohydrate': 3.0, 'Protein': 1.0}, {'name': "Ken's Steak House Dressing, Balsamic Vinaigrette", 'calories': 100.0, 'servings': 16, 'Total Fat': 10.0, 'Cholesterol': 0.0, 'Sodium': 0.28, 'Total Carbohydrate': 3.0, 'Protein': 0.0}, {'name': 'Kroger Large Eggs', 'calories': 70.0, 'servings': 12, 'Total Fat': 5.0, 'Cholesterol': 0.185, 'Sodium': 0.07, 'Total Carbohydrate': 0.0, 'Protein': 6.0}, {'name': "Nature's Own Honey Wheat Bread", 'calories': 70.0, 'servings': 20, 'Total Fat': 1.0, 'Cholesterol': 0.0, 'Sodium': 0.12, 'Total Carbohydrate': 14.0, 'Protein': 3.0}, {'name': 'Sargento Natural String Cheese Snacks', 'calories': 80.0, 'servings': 3, 'Total Fat': 6.0, 'Cholesterol': 0.015, 'Sodium': 0.2, 'Total Carbohydrate': 0.0, 'Protein': 8.0}, {'name': 'Kroger 2% Reduced Fat Milk', 'calories': 120.0, 'servings': 8, 'Total Fat': 5.0, 'Cholesterol': 0.02, 'Sodium': 0.12, 'Total Carbohydrate': 12.0, 'Protein': 8.0}, {'name': 'Toll House Semi Sweet Chocolate Chips', 'calories': 70.0, 'servings': 24, 'Total Fat': 4.0, 'Cholesterol': 0.0, 'Sodium': 0.0, 'Total Carbohydrate': 9.0, 'Protein': 1.0}, {'name': "Mott's Original Applesauce", 'calories': 90.0, 'servings': 6, 'Total Fat': 0.0, 'Cholesterol': 0.0, 'Sodium': 0.0, 'Total Carbohydrate': 24.0, 'Protein': 0.0}, {'name': "Kellogg's Raisin Bran Breakfast Cereal, High Fiber Cereal, Original", 'calories': 190.0, 'servings': 7, 'Total Fat': 1.0, 'Cholesterol': 0.0, 'Sodium': 0.2, 'Total Carbohydrate': 47.0, 'Protein': 5.0}, {'name': 'noosa Lemon Yogurt', 'calories': 320.0, 'servings': 1, 'Total Fat': 13.0, 'Cholesterol': 0.04, 'Sodium': 0.11, 'Total Carbohydrate': 39.0, 'Protein': 12.0}, {'name': 'Thomas Cinnamon Raisin Pre-Sliced Bagels', 'calories': 280.0, 'servings': 6, 'Total Fat': 1.5, 'Cholesterol': 0.0, 'Sodium': 0.39, 'Total Carbohydrate': 56.0, 'Protein': 9.0}, {'name': 'Sargento Balanced Breaks, Pepper Jack Natural Cheese, Honey Roasted Peanuts and Raisins', 'calories': 170.0, 'servings': 3, 'Total Fat': 11.0, 'Cholesterol': 0.02, 'Sodium': 0.19, 'Total Carbohydrate': 12.0, 'Protein': 7.0}, {'name': "Ben & Jerry's Ice Cream Chocolate Chip Cookie Dough", 'calories': 370.0, 'servings': 3, 'Total Fat': 20.0, 'Cholesterol': 0.1, 'Sodium': 0.07, 'Total Carbohydrate': 42.0, 'Protein': 6.0}, {'name': 'Kroger Salted Mixed Nuts', 'calories': 170.0, 'servings': 10, 'Total Fat': 15.0, 'Cholesterol': 0.0, 'Sodium': 0.12, 'Total Carbohydrate': 5.0, 'Protein': 6.0}, {'name': 'San Pellegrino Lemon Italian Sparkling Drinks', 'calories': 120.0, 'servings': 6, 'Total Fat': 0.0, 'Cholesterol': 0.0, 'Sodium': 0.005, 'Total Carbohydrate': 31.0, 'Protein': 0.0}, {'name': 'noosa Tart Cherry Yoghurt', 'calories': 260.0, 'servings': 1, 'Total Fat': 11.0, 'Cholesterol': 0.035, 'Sodium': 0.12, 'Total Carbohydrate': 31.0, 'Protein': 11.0}, {'name': 'noosa Strawberry Rhubarb Yogurt', 'calories': 270.0, 'servings': 1, 'Total Fat': 11.0, 'Cholesterol': 0.035, 'Sodium': 0.12, 'Total Carbohydrate': 32.0, 'Protein': 11.0}, {'name': 'Nature Valley Chewy Trail Mix Granola Bar, Dark Chocolate Cherry, 12 Bars', 'calories': 150.0, 'servings': 6, 'Total Fat': 4.0, 'Cholesterol': 0.0, 'Sodium': 0.07, 'Total Carbohydrate': 25.0, 'Protein': 2.0}]
# while i < 7:
#     day2 = subtract_servings(foods2,servings)
#     day2_res = get_daily_meals(day2)
#     print(day2_res)
#     i = i + 1 