import csv
import os
import pdb#; pdb.set_trace()

def menu(username="mswolf05", products_count=100):
    # this is a multi-line string, also using preceding `f` for string interpolation
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome {username}!
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
        'Reset'   | Reset the current product csv file.
    Please select an operation: """ # end of multi- line string. also using string interpolation
    return menu

def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"READING PRODUCTS FROM FILE: '{filepath}'")
    products = []
    #product_names = ""

    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file) # assuming your CSV has headers, otherwise... csv.reader(csv_file)
        for row in reader:
            #print(row["name"], row["price"])
            products.append(dict(row))
            #product_names += "\n" + row["name"]
    return products
    #print(product_names)

#    def number_of_products():
#        number_of_products = len(products)
#        return number_of_products


def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")

    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "name", "aisle", "department", "price"])
        writer.writeheader() # uses fieldnames set above

        for p in products:
            writer.writerow(p)


def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    write_products_to_file(filename, products)

#def enlarge(my_number):
#    return my_number*100

def auto_incremented_id(products):
    #return int(products[-1]["id"]) + 1
    #next_id = 0
    all_ids = [int(p["id"]) for p in products]
    max_id = max(all_ids)
    next_id = int(max_id) + 1
    return next_id

def inputNumber(message):
  while True:
    try:
       userInput = float(input(message))
    except ValueError:
       print("Price not valid! Try again.")
       continue
    else:
       return userInput
       break

def inputInteger(message):
  while True:
    try:
       userInput = int(input(message))
    except ValueError:
       print("Input must be an integer! Try again.")
       continue
    else:
       return userInput
       break

def run():
    # First, read products from file...
    products = read_products_from_file()
    #current_aisles = []
    #current_departments = []
    #for p in products:
    current_aisles = [p["aisle"] for p in products]
    current_aisles = set(current_aisles)
    current_aisles = sorted(current_aisles)

    current_departments = [p["department"] for p in products]
    current_departments = set(current_departments)
    current_departments = sorted(current_departments)

    number_of_products = len(products)
    my_menu = menu(username="@mswolf05", products_count=number_of_products)
    # Then, prompt the user to select an operation...
    #print(my_menu) #TODO instead of printing, capture user input
    operation = input(my_menu)
    operation = operation.title()

    # Then, handle selected operation: "List", "Show", "Create", "Update", "Destroy" or "Reset"...
    if operation == "List":
        print("----------------------")
        print("LISTING PRODUCTS")
        print("----------------------")
        for p in products:
            print(" + " + p["id"] + " " + p["name"])

    elif operation == "Show":

        product_id = inputInteger("What is the ID for the product that you would like to display: ")

        matching_products = [p for p in products if int(p["id"])==int(product_id)]

        #if there are no matching products (len(matching_products)=0) ask for input again
        while len(matching_products) == 0:
            product_id = inputInteger("ID unrecognized, please try again: ")
            matching_products = [p for p in products if int(p["id"])==int(product_id)]

        matching_product = matching_products[0]
        print("----------------------")
        print("SHOWING A PRODUCT")
        print("----------------------")
        print(matching_product)

    elif operation == "Create":
        print("----------------------")
        print("CREATING A PRODUCT")
        print("----------------------")

        new_id = auto_incremented_id(products)
        new_name= input("Enter the name: ")
        new_aisle = input("Enter an updated aisle (current aisles to choose from include: " + str(current_aisles) + "): ")
        new_department = input("Enter an updated department (current departments to choose from include: " + str(current_departments) + "): ")
        new_price = inputNumber("Enter the price: ")

        new_product={"id": new_id,
        "name": new_name,
        "aisle": new_aisle,
        "department": new_department,
        "price": new_price
        }
        products.append(new_product)

        print("Product created!")

    elif operation == "Update":
        print("----------------------")
        print("UPDATING A PRODUCT")
        print("----------------------")
        product_id = inputInteger("What is the ID for the product that you would like to update: ")
        matching_products = [p for p in products if int(p["id"])==int(product_id)]

        while len(matching_products) == 0:
            product_id = inputInteger("ID unrecognized, please try again: ")
            matching_products = [p for p in products if int(p["id"])==int(product_id)]

        matching_product = matching_products[0]

        #show user current attributes and prompt user for new attributes
        print("----------------------")
        print("Current Information for Product ID " + str(product_id))
        print("----------------------")
        print(" + Name: " + matching_product["name"])
        print(" + Aisle: " + matching_product["aisle"])
        print(" + Department: " + matching_product["department"])
        print(" + Price: " + matching_product["price"])

        new_name= input("Enter an updated name: ")
        new_aisle = input("Enter an updated aisle (current aisles to choose from include: " + str(current_aisles) + "): ")
        new_department = input("Enter an updated department (current departments to choose from include: " + str(current_departments) + "): ")
        new_price = inputNumber("Enter the updated price: ")
        #new_price = input("Enter the updated price: ")
        #TODO check price format - 2 decimals
        #while type(new_price) != int or type(new_price) != float:
            #new_price = input("Input must be numeric, please try again: ")

        matching_product["name"] = new_name
        matching_product["aisle"] = new_aisle
        matching_product["department"] = new_department
        matching_product["price"] = new_price

        print("Product updated!")

    elif operation == "Destroy":
        print("----------------------")
        print("DELETING A PRODUCT")
        print("----------------------")

        product_id = inputInteger("What is the ID for the product that you would like to delete: ")
        matching_products = [p for p in products if int(p["id"])==int(product_id)]

        while len(matching_products) == 0:
            product_id = inputInteger("ID unrecognized, please try again: ")
            matching_products = [p for p in products if int(p["id"])==int(product_id)]

        matching_product = matching_products[0]
        del products[products.index(matching_product)]

        print("Product deleted!")

    elif operation == "Reset":
        reset_products_file()
    else:
        print("OOPS, unrecognized operation, please input on from: List, Show, Create, Update, Destroy, Reset")

    # Finally, save products to file so they persist after script is done...
    write_products_to_file(products=products)

# only prompt the user for input if this script is run from the command-line
# this allows us to import and test this application's component functions
if __name__ == "__main__":
    run()
