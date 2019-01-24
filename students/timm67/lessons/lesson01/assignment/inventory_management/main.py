"""
Launches the command line interface for the inventory management system
"""

import sys
from inventory_management import market_prices
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances

FULL_INVENTORY = {}

def main_menu(user_prompt=None):
    """ Menu-driven CLI using dictionary """
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print("Choose from the following options ({0}):".format(options_str))
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input("> ")
    return valid_prompts.get(user_prompt)


def get_price(item_code):
    """ get price method """
    return inventory_management.market_prices.get_latest_price(item_code)


def add_furniture(item_code, item_description, item_price,
                  item_rental_price, item_material, item_size):
    """ add furniture method to decouple UI/bus logic for unit test """
    new_item = Furniture(item_code, item_description, item_price,
                         item_rental_price, item_material, item_size)
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def add_appliance(item_code, item_description,
                  item_price, item_rental_price,
                  item_brand, item_voltage):
    """ add appliance method to decouple UI/bus logic for unit test """
    new_item = ElectricAppliances(item_code, item_description,
                                  item_price, item_rental_price,
                                  item_brand, item_voltage)
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def add_inventory(item_code, item_description,
                  item_price, item_rental_price):
    """ add inventory method to decouple UI/bus logic for unit test """
    new_item = Inventory(item_code, item_description,
                         item_price, item_rental_price)
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def add_new_item():
    """ add a new item to the inventory """
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = get_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        add_furniture(item_code, item_description, item_price,
                      item_rental_price, item_material, item_size)
    else:
        is_electric_appliance = input("Is this an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            add_appliance(item_code, item_description,
                          item_price, item_rental_price,
                          item_brand, item_voltage)
        else:
            add_inventory(item_code, item_description,
                          item_price, item_rental_price)


def item_info():
    """ display the inventory """
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for key, value in print_dict.items():
            print("{}:{}".format(key, value))
    else:
        print("Item not found in inventory")


def get_item(item_code):
    """ needed for unit test"""
    ret_item = None
    try:
        ret_item = FULL_INVENTORY[item_code]
    except KeyError():
        print("Key {} not found in database".format(item_code))
    return ret_item


def exit_program():
    """ exit inventory management """
    sys.exit()


if __name__ == '__main__':
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
