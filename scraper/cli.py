import budgetbytes

def print_page(page):
    print('\n',budgetbytes.pull_name(page),'-',budgetbytes.pull_time(page),'\n')
    print('\n'.join(map(str, budgetbytes.pull_ingredients(page))), '\n')
    print(budgetbytes.pull_nutrition(page))
    print("\nservings:",budgetbytes.pull_servings_count(page))
    print("Categories: ", budgetbytes.pull_categories(page))
    print("cost: ", budgetbytes.pull_cost_string(page))


def save_links(num_pages, filename='links.txt'):
    """ Saves the recipe links from N recipe list pages 
    https://www.budgetbytes.com/category/recipes/
    """
    links = budgetbytes.pull_recipe_links(num_pages)
    with open(filename, 'w') as f:
        f.write('\n'.join(links))
    print(f"Wrote {len(links)} links to {filename}")


def load_args():
    """ Configures and returns CLI arguments """
    import argparse
    parser = argparse.ArgumentParser("Budget bytes scraper e.g. 'cheese-enchiladas'")
    parser.add_argument('page', nargs='?', type=str, help='A recipe descriptor')
    parser.add_argument('-p','--print',action='store_true', help="Print info for a recipe descriptor")
    parser.add_argument('--text',nargs='*',help="Pull text from [class] [el type]")
    parser.add_argument('-j','--json',action="store_true", help="View the json for a recipe descriptor")
    parser.add_argument('-l', '--links', nargs='?', type=int, help="# of pages to get recipe links from")
    parser.add_argument('--db', action='store_true', help="Build a JSON DB")
    parser.add_argument('-w', '--write', action='store_true', help="Write the page to disk")
    parser.add_argument('-t', '--table',  nargs='*', help="Write the [JSON DB] to a [folder] as tabular data")
    return parser.parse_args()

def main():
    args = load_args()
    page = budgetbytes.load_recipe_html(args.page)
    if args.print: 
        print_page(page)
    if args.text:
        print(budgetbytes.pull_text(page, args.text[0], args.text[1]))
    if args.json:
        import json
        d = budgetbytes.page_to_dict(page, args.page)
        print(json.dumps(d, indent=4))
    if args.links:
        save_links(args.links)
    if args.db:
        descriptors = budgetbytes.links_to_descriptors('links.txt')
        budgetbytes.build_json_db(descriptors, 'recipes.json')
    if args.write:
        with open(f'{args.page}.html','w') as f:
            f.write(str(page))
    if args.table:
        import os, dataset
        if len(args.table) == 0:
            print('usage: cli.py --table [recipes.json] [./dest/folder/]')
            return
        if len(args.table) == 1: 
            args.table[1] = './'
        dataset.write_dataset_from_json(args.table[0], args.table[1])

if __name__ == "__main__": 
    main()
