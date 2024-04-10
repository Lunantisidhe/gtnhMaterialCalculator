from functools import reduce


class Item:
    def __init__(self, quantity, name, place, materials):
        self.quantity = quantity
        self.name = name
        self.place = place
        self.materials = materials

    def __str__(self):
        return f'{int(self.quantity)} {self.name} {self.place}: {self.materials}'


class RawItem:
    def __init__(self, quantity, name):
        self.quantity = quantity
        self.name = name

    def __str__(self):
        return f'{int(self.quantity)} raw {self.name}'


# search the base recipe
def search_recipes(quantity_to_search, item_to_search):
    is_raw = True

    file = open("recipes.txt", "r")
    lines = file.readlines()

    for line in lines:
        # if it finds the recipe, it saves it and searches the recipes for the materials
        if line.split()[1] == item_to_search:
            is_raw = False

            head, body = line.split(':')
            quantity, name, place = head.split(' ')
            quantity = float(quantity)
            new_quantity = float(quantity_to_search)

            # if the quantity is not exact, move to the closer possible quantity
            if new_quantity % quantity != 0:
                new_quantity = new_quantity + (quantity - (new_quantity % quantity))

            # gets materials
            materials = [get_material.split() for get_material in body.split(',')]
            for material_quantity in materials:
                material_quantity[0] = int(float(material_quantity[0]) * new_quantity / quantity)

            # searches materials recipes recursively
            for search_material in materials:
                search_recipes(search_material[0], search_material[1])

            # prints the item
            item = Item(new_quantity, name, place, materials)
            print(item)

    file.close()

    # prints and stores raw items
    if is_raw is True:
        item = RawItem(quantity_to_search, item_to_search)
        print(item)
        raw_materials_list.append(item)


raw_materials_list = []

# ask for recipe and quantity
item_to_craft = str(input('\nInput item to craft: '))
quantity_to_craft = str(input('Input quantity: '))

# prints crafting process
print("\nCrafting process:")
search_recipes(quantity_to_craft, item_to_craft)

# sum all raw materials
raw_materials_list_sum = reduce(lambda acc, x: acc.update({x.name: acc.get(x.name, 0) + x.quantity}) or acc,
                                raw_materials_list, {})
raw_materials_list_sum = [(quantity, name) for name, quantity in raw_materials_list_sum.items()]
raw_materials_list_sum = sorted(raw_materials_list_sum, reverse=True)

# prints all raw materials
print("\nRaw materials:")
for material in raw_materials_list_sum:
    print(material)
