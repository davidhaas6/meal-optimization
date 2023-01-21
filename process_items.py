import json
f = open('parent_json.json', encoding="utf8")

# Input Data
data = json.load(f)
items = data["data"]["orderDelivery"]["orderItems"]

item_ids = []
item_names = []
# Get Item Ids
for item in items:
    item_ids.append(item['item']["legacyId"])
    item_names.append(item["item"]["name"])
    print(item["item"]["name"])
print(item_ids)
print(item_names)

# Get Nutrition Info

