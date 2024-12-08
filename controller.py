from model import Model
from view import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            choice_table = self.select_table()
            if choice_table == '1':
                while True:
                    choice = self.show_menu()
                    if choice == '1':
                        self.add_line(1)
                    elif choice == '2':
                        self.view_line(1)
                    elif choice == '3':
                        self.update_line(1)
                    elif choice == '4':
                        self.delete_line(1)
                    elif choice == '5':
                        break
                    elif choice == '6':
                        self.generate_random_strings(1)
            elif choice_table == '2':
                while True:
                    choice = self.show_menu()
                    if choice == '1':
                        self.add_line(2)
                    elif choice == '2':
                        self.view_line(2)
                    elif choice == '3':
                        self.update_line(2)
                    elif choice == '4':
                        self.delete_line(2)
                    elif choice == '5':
                        break
                    elif choice == '6':
                        self.generate_random_strings(2)
            elif choice_table == '3':
                while True:
                    choice = self.show_menu()
                    if choice == '1':
                        self.add_line(3)
                    elif choice == '2':
                        self.view_line(3)
                    elif choice == '3':
                        self.update_line(3)
                    elif choice == '4':
                        self.delete_line(3)
                    elif choice == '5':
                        break
                    elif choice == '6':
                        self.generate_random_strings(3)
            elif choice_table == '4':
                while True:
                    choice = self.show_menu()
                    if choice == '1':
                        self.add_line(4)
                    elif choice == '2':
                        self.view_line(4)
                    elif choice == '3':
                        self.update_line(4)
                    elif choice == '4':
                        self.delete_line(4)
                    elif choice == '5':
                        break
                    elif choice == '6':
                        self.generate_random_strings(4)
            elif choice_table == '5':
                break
            elif choice_table == '6':
                self.model.drop_all_tables()
                break
            elif choice_table == '7':
                self.show_inventory_count_by_warehouse()
            elif choice_table == '8':
                self.show_products_with_quantity()
            elif choice_table == '9':
                self.show_warehouse_with_most_inventories()

    def select_table(self):
        self.view.show_message("\nSelect a table or other function:")
        self.view.show_message("1. Warehouse")
        self.view.show_message("2. Inventory")
        self.view.show_message("3. Product")
        self.view.show_message("4. Warehouse_Products")
        self.view.show_message("5. Quit")
        self.view.show_message("6. Сlear all tables")
        self.view.show_message("7. Inventory Count by Warehouse")
        self.view.show_message("8. Products with Quantity")
        self.view.show_message("9. Warehouse with Most Inventories")
        return input("Enter your choice: ")

    def show_menu(self):
        self.view.show_message("\nMenu:")
        self.view.show_message("1. Add line")
        self.view.show_message("2. View line")
        self.view.show_message("3. Update line")
        self.view.show_message("4. Delete line")
        self.view.show_message("5. Quit in menu")
        self.view.show_message("6. Generate random strings")
        return input("Enter your choice: ")

    def add_line(self, choice_table):
        if choice_table == 1:
            Where = self.view.get_line_input(choice_table)
            self.model.add_line_Warehouse(Where)
            self.view.show_message("line added successfully!")
        elif choice_table == 2:
            User_id, Result, Warehouse_id = self.view.get_line_input(choice_table)
            check = self.model.add_line_Inventory(User_id, Result, Warehouse_id)
            if check != 0:
                self.view.show_message("line added successfully!")
        elif choice_table == 3:
            Product_Name, Quantity = self.view.get_line_input(choice_table)
            check = self.model.add_line_Product(Product_Name, Quantity)
            if check != 0:
                self.view.show_message("line added successfully!")
        elif choice_table == 4:
            Inventory_id, Product_id = self.view.get_line_input(choice_table)
            check = self.model.add_line_Warehouse_Products(Inventory_id, Product_id)
            if check != 0:
                self.view.show_message("line added successfully!")
        else:
            self.view.show_message("add_line error")

    def view_line(self, choice_table):
        if choice_table:
            lines = self.model.get_all_line(choice_table)
            self.view.show_lines(lines, choice_table)
        else:
            self.view.show_message("view_line error")

    def update_line(self, choice_table):
        if choice_table == 1:
            Warehouse_id = self.view.get_line_id()
            Where = self.view.get_line_input(choice_table)
            self.model.update_line_Warehouse(Warehouse_id, Where)
            self.view.show_message("line updated successfully!")
        elif choice_table == 2:
            Inventory_id = self.view.get_line_id()
            User_id, Result, Warehouse_id = self.view.get_line_input(choice_table)
            check = self.model.update_line_Inventory(Inventory_id, User_id, Result, Warehouse_id)
            if check != 0:
                self.view.show_message("line updated successfully!")
        elif choice_table == 3:
            Product_id = self.view.get_line_id()
            Product_Name, Quantity = self.view.get_line_input(choice_table)
            check = self.model.update_line_Product(Product_id, Product_Name, Quantity)
            if check != 0:
                self.view.show_message("line updated successfully!")
        elif choice_table == 4:
            old_Inventory_id, old_Product_id, new_Inventory_id, new_Product_id = self.view.get_line_in_Warehouse_Products()
            check = self.model.update_line_Warehouse_Products(old_Inventory_id, old_Product_id, new_Inventory_id, new_Product_id)
            if check != 0:
                self.view.show_message("line updated successfully!")
        else:
            self.view.show_message("update_line error")

    def delete_line(self, choice_table):
        if choice_table != 4:
            line_id = self.view.get_line_id()
            self.model.delete_line(line_id, choice_table)
            self.view.show_message("line deleted successfully!")
        elif choice_table == 4:
            Inventory_id, Product_id = self.view.get_line_input(choice_table)
            self.model.delete_line_Warehouse_Products(Inventory_id, Product_id)
            self.view.show_message("line deleted successfully!")
        else:
            self.view.show_message("delete_line error")

    def generate_random_strings(self, choice_table):
        if choice_table == 1:
            count = int(input("Enter rows for Warehouse: "))
            self.model.bulk_insert_warehouse(count)
            self.view.show_message(f"{count} rows added to Warehouse.")
        elif choice_table == 2:
            count = int(input("Enter rows for Inventory: "))
            self.model.bulk_insert_inventory(count)
            self.view.show_message(f"{count} rows added to Inventory.")
        elif choice_table == 3:
            count = int(input("Enter rows for Product: "))
            self.model.bulk_insert_product(count)
            self.view.show_message(f"{count} rows added to Product.")
        elif choice_table == 4:
            count = int(input("Enter rows for Warehouse_Products: "))
            self.model.bulk_insert_warehouse_products(count)
            self.view.show_message(f"{count} rows added to Warehouse_Products.")
        else:
            self.view.show_message("generate_random_strings error")

    # Скільки інвентаризацій було проведено на кожному складі
    def show_inventory_count_by_warehouse(self):
        result_filter = input("Enter Result filter (e.g., True, False, Planned): ")
        data, exec_time = self.model.get_inventory_count_by_warehouse(result_filter)
        self.view.show_search_results(data, f"Inventory Count by Warehouse (Filter: {result_filter})")
        self.view.show_message(f"Query executed in {exec_time:.2f} ms.")

    # Які продукти мають кількість більше заданого значення і прив'язані до складів
    def show_products_with_quantity(self):
        min_quantity = int(input("Enter minimum quantity: "))
        data, exec_time = self.model.get_products_with_quantity(min_quantity)
        self.view.show_search_results(data, f"Products with Quantity > {min_quantity}")
        self.view.show_message(f"Query executed in {exec_time:.2f} ms.")

    # Склад із найбільшою кількістю інвентаризацій
    def show_warehouse_with_most_inventories(self):
        data, exec_time = self.model.get_warehouse_with_most_inventories()
        self.view.show_search_results([data], "Warehouse with Most Inventories")
        self.view.show_message(f"Query executed in {exec_time:.2f} ms.")

