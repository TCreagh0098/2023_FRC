# import libraries
import pandas
import math


# *** Functions go here ***

# checks that input is either a float or an
# integer that is more than zero. Takes in custom error message
def num_check(question, error, num_type):
    valid = False
    while not valid:

        try:
            response = num_type(input(question))

            if response <= 0:
                print(error)
            else:
                return response

        except ValueError:
            print(error)


# Checks that user has entered yes / no to a question
def yes_no(question):
    to_check = ["yes", "no"]

    valid = False
    while not valid:

        response = input(question).lower()

        for var_item in to_check:
            if response == var_item:
                return response
            elif response == var_item[0]:
                return var_item

        print("Please enter either yes or no...\n")


# Checks that string response is not blank
def not_blank(question, error):
    valid = False
    while not valid:
        response = input(question)

        if response == "":
            print(f"{error}. \nPlease try again. \n")
            continue

        return response


# Currency formatting function
def currency(x):
    return "${:.2f}".format(x)


# Gets expenses, returns lists which has
# the data frame and subtotal
def get_expenses(var_fixed):
    # Set up dictionaries and lists

    item_list = []
    quantity_list = []
    price_list = []

    expense_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    expense_ok = "no"

    item_name = ""
    while item_name.lower() != "xxx":
        item_name = not_blank("\nItem name: ", "The component name cannot be blank.")

        if item_name.lower() == "xxx" and expense_ok == "yes":
            break
        elif expense_ok == "no" and item_name.lower() == "xxx":
            print("Please enter at least one expense")
            item_name = ""
            continue

        if var_fixed == "variable":
            quantity = num_check("Quantity: ", "The amount must be a whole number.", int)
        else:
            quantity = 1

        price = num_check("How much for a single item? $", "The price must be a number more than 0.", float)

        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

        expense_ok = "yes"

    expense_frame = pandas.DataFrame(expense_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']

    # Find subtotal
    sub_total = expense_frame['Cost'].sum()

    # Currency formatting (uses currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, sub_total]


# Prints expense frames
def expense_print(heading, frame, subtotal):
    print()
    print(f"**** {heading} Costs ****")
    print(frame)
    print()
    print(f"{heading} Costs: ${subtotal:.2f}")
    return ""


# work out profit goal and total sales required
def profit_goal(total_costs):
    # Initialise variables and error message
    error = "Please enter a valid profit goal\n"

    valid = False
    while not valid:

        # ask for profit goal...
        response = input("What is your profit goal (eg $500 or $750)")

        # check if first character is $
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)
            amount = response[1:]

        # check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # Get amount (everything before the %)
            amount = response[:-1]

        else:
            # set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # Check amount is a number more than zero...
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no(f"Do you mean ${amount:.2f}. "
                                 f"ie {amount:.2f} dollars? ,"
                                 "y / n ")

            # set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no(f"Do you mean {amount}% , "
                                  "y / n")
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs


def round_up(amount, var_round_to):
    return int(math.ceil(amount / var_round_to)) * var_round_to


# Main routine goes here

# Get product name
product_name = not_blank("Product name: ",
                         "The product name cannot be blank.")

how_many = num_check("How many items will you be producing? ",
                     "The number of items must be a whole "
                     "number more than zero", int)

print()
print("Please enter your variable costs below...")
# Get variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub_total = variable_expenses[1]

print()
have_fixed = yes_no("Do you have fixed costs (y / n)? ")

if have_fixed == "yes":
    # Get fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub_total = fixed_expenses[1]
else:
    fixed_frame = ""
    fixed_sub_total = 0

# work out total costs and profit target
all_costs = variable_sub_total + fixed_sub_total
profit_target = profit_goal(all_costs)

# Calculates total sales needed to reach goal
sales_needed = all_costs + profit_target

# Ask user for rounding
round_to = num_check("Round to nearest...? $",
                     "Can't be 0", int)

# Calculate recommended price
selling_price = sales_needed / how_many
print(f"Selling Price (unrounded): "
      f"${selling_price:.2f}")

# Set up strings to write to file
variable_txt = pandas.DataFrame.to_string(variable_frame)
variable_heading = "==== Variable Costs ======"
variable_sub_text = f"--- Variable Costs Subtotal: ${variable_sub_total} ---\n\n"

if have_fixed == "yes":
    fixed_txt = pandas.DataFrame.to_string(fixed_frame)
    fixed_heading_txt = "==== Fixed Costs ===="
else:
    fixed_txt = ""
    fixed_heading_txt = ""

product_name_text = f"\n\n***** {product_name} *****\n"
sales_text = "\n==== Sales Advice ===="
profit_target_text = f"\nProfit Target: ${profit_target:.2f}"
required_sales = f"Required Sales: ${sales_needed:.2f}"
recommended_price = round_up(selling_price, round_to)
recommended_price_txt = f"Recommended Price: ${recommended_price:.2f}"
message_txt = f" \n=== Thank you for using this program to help you with {product_name}! === "

to_write = [product_name_text, variable_heading, variable_txt, variable_sub_text,
            fixed_heading_txt, fixed_txt, sales_text,
            profit_target_text, required_sales,
            recommended_price_txt, message_txt]


# Write data to file

file_name = f"{product_name}.txt"
text_file = open(file_name, "w+")


# heading
for item in to_write:
    text_file.write(item)
    text_file.write("\n\n")

# close file
text_file.close()

# Print Stuff
for item in to_write:
    print(item)

print(f"\n--- If you wish to view ticket data in a txt file, see file named '{product_name}'.txt")



