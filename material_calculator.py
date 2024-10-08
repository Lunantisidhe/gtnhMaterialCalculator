import sys
from functools import reduce


class Item:
    def __init__(self, quantity, actual_quantity, name, place, materials, indent_level=0):
        self.quantity = quantity
        self.actual_quantity = actual_quantity
        self.name = name
        self.place = place
        self.materials = materials
        self.indent_level = indent_level

    def __str__(self):
        indent = '  ' * self.indent_level
        return (f'{indent}{int(self.quantity)} {f"(Actual required quantity: {int(self.actual_quantity)}) "
                                                * (self.quantity != self.actual_quantity)}{self.name} {self.place}: '
                f'{", ".join(" ".join(map(str, m)) for m in self.materials)}')


class RawItem:
    def __init__(self, quantity, name):
        self.quantity = quantity
        self.name = name


# search the base recipe
def search_recipes(quantity_to_search, item_to_search, indent_level=0):
    raw_materials_list = []
    stack = [(quantity_to_search, item_to_search, indent_level)]

    while stack:
        quantity, item, current_indent = stack.pop()
        is_raw = True

        with open('recipes.txt', 'r') as file:
            lines = file.readlines()

        for line in lines:
            # cuts the line into its desired parts
            head, body = line.split(':')
            base_quantity_name, place = head.split(' [')
            base_quantity, name = base_quantity_name.split(' ', 1)

            # if it finds the recipe, it saves it and searches the recipes for the materials
            if name == item:
                is_raw = False

                place = '[' + place

                base_quantity = float(base_quantity)
                new_quantity = float(quantity)

                # if the quantity is not exact, move to the closer possible quantity
                if new_quantity % base_quantity != 0:
                    new_quantity = new_quantity + (base_quantity - (new_quantity % base_quantity))

                # gets materials
                materials = [get_material.split() for get_material in body.split(',')]
                for material_quantity in materials:
                    material_quantity[0] = int(float(material_quantity[0]) * new_quantity / base_quantity)

                # prints the item
                print(Item(new_quantity, quantity, name, place, materials, current_indent))

                # searches materials recipes with increased indentation
                for material_quantity in materials:
                    stack.append((material_quantity[0], ' '.join(material_quantity[1:]), current_indent + 1))

        if is_raw:
            item = RawItem(quantity, item)
            raw_materials_list.append(item)

    return raw_materials_list


# ask for recipe and quantity
item_to_craft = str(input('\nInput item to craft: ')).lower()
try:
    quantity_to_craft = float(input('Input quantity: '))

    if quantity_to_craft < 1 or quantity_to_craft > 999999999:
        raise ValueError

except ValueError:
    print("\nPlease enter a valid number (1 ~ 999 999 999)")
    sys.exit(1)

# prints crafting process
print('\nCrafting process:')
raw_materials = search_recipes(quantity_to_craft, item_to_craft)

# sum all raw materials
raw_materials_list_sum = reduce(lambda acc, x: acc.update({x.name: acc.get(x.name, 0) + x.quantity}) or acc,
                                raw_materials, {})
raw_materials_list_sum = [(quantity, name) for name, quantity in raw_materials_list_sum.items()]
raw_materials_list_sum = sorted(raw_materials_list_sum, reverse=True)

# not found item
if raw_materials_list_sum[0][1] == item_to_craft:
    print("Item not found")

# prints all raw materials
else:
    print('\nRaw materials:')
    for material in raw_materials_list_sum:
        print(f'{material[0]} {material[1]}')
