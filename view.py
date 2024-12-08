class View:
    def show_lines(self, lines, choice_table):
        print("Lines:")
        if choice_table == 1:
            for line in lines:
                print(f"Warehouse_id: {line[0]}, Where: {line[1]}")
        elif choice_table == 2:
            for line in lines:
                print(f"Inventory_id: {line[0]}, User_id: {line[1]}, Result: {line[2]}, Warehouse_id: {line[3]}")
        elif choice_table == 3:
            for line in lines:
                print(f"Product_id: {line[0]}, Product_Name: {line[1]}, Quantity: {line[2]}")
        elif choice_table ==4:
            for line in lines:
                print(f"Inventory_id: {line[0]}, Product_id: {line[1]}")
        else:
            self.show_message("show_lines error")

    def get_line_input(self, choice_table):
        if choice_table == 1:
            while True:
                Where = input("Enter Where: ")
                if Where:
                    return Where
                else:
                    self.show_message("Error: The input cannot be empty!")
        elif choice_table == 2:
            while True:
                User_id = input("Enter User_id: ")
                Result = input("Enter Result: ")
                Warehouse_id = input("Enter Warehouse_id: ")
                if User_id and Result and Warehouse_id and User_id.isdigit() and Warehouse_id.isdigit():
                    return User_id, Result, Warehouse_id
                else:
                    self.show_message("Error: Something is clearly wrong -_-")
        elif choice_table == 3:
            while True:
                Product_Name = input("Enter Product_Name: ")
                Quantity = input("Enter Quantity: ")
                if Product_Name and Quantity and Product_Name.isalpha() and Quantity.isdigit():
                    return Product_Name, Quantity
                else:
                    self.show_message("Error: Something is clearly wrong -_-")
        elif choice_table == 4:
            while True:
                Inventory_id = input("Enter Inventory_id: ")
                Product_id = input("Enter Product_id: ")
                if Inventory_id and Product_id and Inventory_id.isdigit() and Product_id.isdigit():
                    return Inventory_id, Product_id
                else:
                    self.show_message("Error: Something is clearly wrong -_-")

    def get_line_id(self):
        while True:
            check = input("Enter line ID: ").strip()
            if check:
                return int(check)
            else:
                self.show_message("Error: ID cannot be empty!")

    def get_line_in_Warehouse_Products(self):
        while True:
            self.show_message("Since this table uses a composite key, please provide the current (old) and new values.")
            old_Inventory_id = input("Enter old_Inventory_id: ")
            old_Product_id = input("Enter old_Product_id: ")
            new_Inventory_id = input("Enter new_Inventory_id: ")
            new_Product_id = input("Enter new_Product_id: ")
            if old_Inventory_id and old_Product_id and old_Inventory_id.isdigit() and old_Product_id.isdigit() and new_Inventory_id and new_Product_id and new_Inventory_id.isdigit() and new_Product_id.isdigit():
                return old_Inventory_id, old_Product_id, new_Inventory_id, new_Product_id
            else:
                self.show_message("Error: Something is clearly wrong -_-")

    def show_message(self, message):
        print(message)

    def show_search_results(self, lines, header):
        print(header)
        for line in lines:
            if isinstance(line, tuple):
                print(" | ".join(map(str, line)))
            else:
                print(line)
        if not lines:
            print("No results found.")

