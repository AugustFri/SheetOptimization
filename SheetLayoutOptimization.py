import math
import heapq
import customtkinter as ctk



def return_scrap(orders):

    # Constants
    CARDS_PER_COLUMN = 12
    COLUMNS_PER_SHEET = 10
    CARDS_PER_SHEET = CARDS_PER_COLUMN * COLUMNS_PER_SHEET

    # Calculate total quantity
    total_quantity = sum(qty for _, qty in orders)
    total_orders = len(orders)

    # Initialize variables
    columns_per_order = {}
    remaining_columns = COLUMNS_PER_SHEET
    temp_portion = 0

    # Calculate the proportion of each number and calculate the number of columns needed
    for order, qty in orders:
        temp_portion = qty / total_quantity
        columns_per_order[order] = max(1, round(temp_portion * COLUMNS_PER_SHEET))
        remaining_columns -= columns_per_order[order]
    
    
    # Ensure that too many columns were not allocated
    while remaining_columns < 0:
        max_key = max(columns_per_order, key=columns_per_order.get)
        columns_per_order[max_key] -= 1
        remaining_columns += 1

    #ensure that all columns are allocated
    if remaining_columns > 0:
        max_key = max(columns_per_order, key=columns_per_order.get)
        columns_per_order[max_key] += remaining_columns

    max_sheets_required = math.ceil(max(qty / (columns_per_order[order] * CARDS_PER_COLUMN) for order, qty in orders))
    
    #count cards that were printed that exceeded the order quantity
    scrap_cards = sum(columns_per_order[order] * CARDS_PER_COLUMN * max_sheets_required - qty for order, qty in orders)
    

    return scrap_cards

def allocate_orders(orders):

    # Constants
    CARDS_PER_COLUMN = 12
    COLUMNS_PER_SHEET = 10

    # Calculate total quantity
    total_quantity = sum(qty for _, qty in orders)
    total_orders = len(orders)

    # Initialize variables
    columns_per_order = {}
    remaining_columns = COLUMNS_PER_SHEET
    temp_portion = 0

    # Calculate the proportion of each number and calculate the number of columns needed
    for order, qty in orders:
        temp_portion = qty / total_quantity
        columns_per_order[order] = max(1, round(temp_portion * COLUMNS_PER_SHEET))
        remaining_columns -= columns_per_order[order]
    
    
    # Ensure that too many columns were not allocated
    while remaining_columns < 0:
        max_key = max(columns_per_order, key=columns_per_order.get)
        columns_per_order[max_key] -= 1
        remaining_columns += 1

    #ensure that all columns are allocated
    if remaining_columns > 0:
        max_key = max(columns_per_order, key=columns_per_order.get)
        columns_per_order[max_key] += remaining_columns

    max_sheets_required = math.ceil(max(qty / (columns_per_order[order] * CARDS_PER_COLUMN) for order, qty in orders))

    # Create the order sheet with allocated columns
    design_sheet = [(order, columns_per_order[order]) for order in columns_per_order]
    
    #count cards that were printed that exceeded the order quantity
    scrap_cards = sum(columns_per_order[order] * CARDS_PER_COLUMN * max_sheets_required - qty for order, qty in orders)


    return design_sheet, max_sheets_required, scrap_cards


def partitionn(collection):
    COLUMNS_PER_SHEET = 10
    if len(collection) == 1:
        yield [collection]
        return
    
    first = collection[0]
    for smaller in partitionn(collection[1:]):
        for n, subset in enumerate(smaller):
            new_subset = [first] + subset
            if len(new_subset) <= COLUMNS_PER_SHEET:
                yield smaller[:n] + [new_subset] + smaller[n+1:]
        yield [[first]] + smaller

def format_output(design_sheet, total_sheets, scrap):
    design_sheet = f"Design Sheet: {str(design_sheet)}"
    total_sheets = f"Total Sheets: {str(total_sheets)}"
    scrap = f"Scrap Cards: {str(scrap)}"

    formatted = f"{design_sheet:<100}{total_sheets:<30} {scrap}\n"
    return formatted

def check_all_scrap(partitions):
    scrap_list = []
    for partition in partitions:
        scrap_sum = 0
        for i, lst in enumerate(partition):
            scrap = return_scrap(lst)
            scrap_sum += scrap
            if i == len(partition) - 1:
                scrap_list.append(scrap_sum)
    return scrap_list

def print_scrap_mins(partitions, min_heap):
    smallest_indices = []
    for i in range(3):
        smallest_value, smallest_index = heapq.heappop(min_heap)
        smallest_indices.append(smallest_index)
        result_text.insert(ctk.END, f"\nOption #{i+1}: \nTOTAL SCRAP: {smallest_value}\n")
        for lst in partitions[smallest_index]:
            min_scrap_sheets, total_sheets, scrap = allocate_orders(lst)
            result_text.insert(ctk.END, format_output(min_scrap_sheets, total_sheets, scrap))


    
'''
orders = [("Card A", 34000), ("Card B", 28000), ("Card C", 27600), ("Card D", 18600), ("Card E", 16200), ("Card F", 8400), ("Card G", 7500), ("Card H", 5500), 
("Card I", 4000), ("Card J", 3000)]
#design_sheet, total_sheets, scrap = allocate_orders(orders)

scrap_list = []
partitions = list(partitionn(orders))

#run every partition through allocate_orders and collect data
print(f"number of partitions: {len(partitions)}")
scrap_list = check_all_scrap(partitions)

#find and display info of first scrap min(which should be the one with the the fewest sheets also)
min_heap = [(value, index) for index, value in enumerate(scrap_list)]
heapq.heapify(min_heap)

print_scrap_mins(partitions, min_heap)

'''


# All tkinter things for the window
# Function to add tuple to the list
def add_tuple():
    string_value = string_entry.get()
    int_value = int_entry.get()
    if string_value and int_value.isdigit():
        tuples_list.append((string_value, int(int_value)))
        result_text.insert(ctk.END, f"Added Order: ({string_value}, {int(int_value)})\n")
        string_entry.delete(0, ctk.END)
        int_entry.delete(0, ctk.END)
        if len(tuples_list) > 11:
            result_text.insert(ctk.END, "Program will take an extended amount of time to process due to number of orders.\n")
    else:
        result_text.insert(ctk.END, "Invalid input. Please enter a valid string and integer.\n")

# Function to run the program
def run_program():
    if len(tuples_list) == 0:
        result_text.insert(ctk.END, "Please add at least one order.\n")
    else:
        result_text.insert(ctk.END, "\n\n\nRunning program...\n")

        scrap_list = []
        partitions = list(partitionn(tuples_list))

        #run every partition through allocate_orders and collect scrap amounts in correct indexes
        scrap_list = check_all_scrap(partitions)

        #find and display info of first scrap min(which should be the one with the the fewest sheets also)
        min_heap = [(value, index) for index, value in enumerate(scrap_list)]
        heapq.heapify(min_heap)

        print_scrap_mins(partitions, min_heap)
        result_text.insert(ctk.END, "\nProgram finished.\n\n\n")

def reset_program():
    tuples_list.clear()
    result_text.delete(1.0, ctk.END)
    result_text.insert(ctk.END, "\nAll orders cleared.\n\n\n")

def show_all_orders():
    result_text.insert(ctk.END, "All Orders:\n")
    for order in tuples_list:
        result_text.insert(ctk.END, f"{order}\n")
    result_text.insert(ctk.END, "\n\n\n")

# Initialize the main window
ctk.set_appearance_mode("dark")  # Options: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Options: "blue" (default), "green", "dark-blue"

root = ctk.CTk()
root.title("Sheet Order Optimizer")

# Create input fields for string and integer
ctk.CTkLabel(root, text="Order Name").grid(row=0, column=0, padx=10,pady=5, sticky="e")
string_entry = ctk.CTkEntry(root)
string_entry.grid(row=0, column=1, padx= 10, pady=5, sticky="w")

ctk.CTkLabel(root, text="Quantity").grid(row=1, column=0, padx = 10, pady=5, sticky="e")
int_entry = ctk.CTkEntry(root)
int_entry.grid(row=1, column=1, padx = 10, pady=5, sticky="w")

# Button to add tuple to the list
add_button = ctk.CTkButton(root, text="Add Order", command=add_tuple)
add_button.grid(row=2, column=0, columnspan=2, pady=10)

# Button to run the program
run_button = ctk.CTkButton(root, text="Run Program", command=run_program)
run_button.grid(row=3, column=0, columnspan=2, pady=10)

# Button to reset the list
add_button = ctk.CTkButton(root, text="RESET PROGRAM", command=reset_program)
add_button.grid(row=5, column=0, columnspan=2, pady=10)

monospaced_font = ("Courier", 14)  # Change size as needed

# Create CTkTextbox with monospaced font
result_text = ctk.CTkTextbox(root, width=1500, height=700, font=monospaced_font)
result_text.grid(row=4, column=0, columnspan=2, padx = 10, pady=10)

# List to hold the tuples
tuples_list = []

# Run the application
root.mainloop()