import psycopg2
import random
import time

class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='1111',
            host='localhost',
            port=5432
        )
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()

        # Warehouse
        c.execute('''
            CREATE TABLE IF NOT EXISTS Warehouse (
                Warehouse_id SERIAL PRIMARY KEY,
                "Where" VARCHAR NOT NULL
            )
        ''')

        # Inventory
        c.execute('''
            CREATE TABLE IF NOT EXISTS Inventory (
                Inventory_id SERIAL PRIMARY KEY,
                User_id INTEGER NOT NULL,
                Result TEXT NOT NULL,
                Warehouse_id INTEGER NOT NULL,
                FOREIGN KEY (Warehouse_id) REFERENCES Warehouse(Warehouse_id) ON DELETE CASCADE
            )
        ''')

        # Product
        c.execute('''
            CREATE TABLE IF NOT EXISTS Product (
                Product_id SERIAL PRIMARY KEY,
                Product_Name TEXT NOT NULL,
                Quantity INTEGER NOT NULL
            )
        ''')

        # Warehouse_Products
        c.execute('''
            CREATE TABLE IF NOT EXISTS Warehouse_Products (
                Inventory_id INTEGER NOT NULL,
                Product_id INTEGER NOT NULL,
                PRIMARY KEY (Inventory_id, Product_id),
                FOREIGN KEY (Inventory_id) REFERENCES Inventory(Inventory_id) ON DELETE CASCADE,
                FOREIGN KEY (Product_id) REFERENCES Product(Product_id) ON DELETE CASCADE
            )
        ''')

        self.conn.commit()

    def add_line_Warehouse(self, Where):
        c = self.conn.cursor()
        c.execute('INSERT INTO Warehouse ("Where") VALUES (%s)', (Where,))
        self.conn.commit()

    def add_line_Inventory(self, User_id, Result, Warehouse_id):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM Warehouse WHERE Warehouse_id = %s', (Warehouse_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: Warehouse_id {Warehouse_id} does not exist.")
            return 0
        c.execute('INSERT INTO Inventory (User_id, Result, Warehouse_id) VALUES (%s, %s, %s)', (User_id, Result, Warehouse_id))
        self.conn.commit()

    def add_line_Product(self, Product_Name, Quantity):
        c = self.conn.cursor()
        c.execute('INSERT INTO Product (Product_Name, Quantity) VALUES (%s, %s)', (Product_Name, Quantity))
        self.conn.commit()

    def add_line_Warehouse_Products(self, Inventory_id, Product_id):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM Inventory WHERE Inventory_id = %s', (Inventory_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: Inventory {Inventory_id} does not exist.")
            return 0
        c.execute('SELECT COUNT(*) FROM Product WHERE Product_id = %s', (Product_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: Product_id {Product_id} does not exist.")
            return 0
        c.execute('INSERT INTO Warehouse_Products (Inventory_id, Product_id) VALUES (%s, %s)', (Inventory_id, Product_id))
        self.conn.commit()

    def get_all_line(self, choice_table):
        c = self.conn.cursor()
        if choice_table == 1:
            c.execute('SELECT * FROM Warehouse')
        elif choice_table == 2:
            c.execute('SELECT * FROM Inventory')
        elif choice_table == 3:
            c.execute('SELECT * FROM Product')
        elif choice_table == 4:
            c.execute('SELECT * FROM Warehouse_Products')
        else:
            print("get_all_line error")
        return c.fetchall()


    def update_line_Warehouse(self, Warehouse_id, Where):
        c = self.conn.cursor()
        c.execute('UPDATE Warehouse SET "Where"=%s WHERE Warehouse_id=%s', (Where, Warehouse_id))
        self.conn.commit()

    def update_line_Inventory(self, Inventory_id, User_id, Result, Warehouse_id):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM Warehouse WHERE Warehouse_id = %s', (Warehouse_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: Warehouse_id {Warehouse_id} does not exist.")
            return 0
        c.execute('UPDATE Inventory SET User_id=%s, Result=%s, Warehouse_id=%s WHERE Inventory_id=%s',(User_id, Result, Warehouse_id, Inventory_id))
        self.conn.commit()

    def update_line_Product(self, Product_id, Product_Name, Quantity):
        c = self.conn.cursor()
        c.execute('UPDATE Product SET Product_Name=%s, Quantity=%s WHERE Product_id=%s',  (Product_Name, Quantity, Product_id))
        self.conn.commit()

    def update_line_Warehouse_Products(self, old_Inventory_id, old_Product_id, new_Inventory_id, new_Product_id):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM Product WHERE Product_id = %s', (new_Product_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: new_Product_id {new_Product_id} does not exist.")
            return 0
        c.execute('SELECT COUNT(*) FROM Inventory WHERE Inventory_id = %s', (new_Inventory_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: new_Inventory_id {new_Inventory_id} does not exist.")
            return 0
        c.execute('UPDATE Warehouse_Products SET Product_id=%s, Inventory_id=%s WHERE Product_id=%s AND Inventory_id=%s',(new_Product_id, new_Inventory_id, old_Product_id, old_Inventory_id))
        self.conn.commit()

    def delete_line(self, line_id, choice_table):
        c = self.conn.cursor()
        if choice_table == 1:
            c.execute('DELETE FROM Warehouse WHERE Warehouse_id=%s', (line_id,))
        elif choice_table == 2:
            c.execute('DELETE FROM Inventory WHERE Inventory_id=%s', (line_id,))
        elif choice_table == 3:
            c.execute('DELETE FROM Product WHERE Product_id=%s', (line_id,))
        else:
            print("delete_line error")
        self.conn.commit()

    def delete_line_Warehouse_Products(self, Inventory_id, Product_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM Warehouse_Products WHERE Inventory_id=%s AND Product_id=%s', (Inventory_id, Product_id))
        self.conn.commit()

    def bulk_insert_warehouse(self, count):
        c = self.conn.cursor()
        query = f"INSERT INTO Warehouse (\"Where\") SELECT 'location' || trunc(1 + random()*100)::int FROM generate_series(1, {count})"
        c.execute(query)
        self.conn.commit()

    def bulk_insert_inventory(self, count):
        c = self.conn.cursor()
        c.execute('SELECT Warehouse_id FROM Warehouse')
        warehouse_ids = [row[0] for row in c.fetchall()]
        if not warehouse_ids:
            print("Error: No warehouses exist. Please populate the Warehouse table first.")
            return
        results = ['True', 'False', 'Unsuccessful', 'In process', 'Planned']
        weights = [0.45, 0.45, 0.02, 0.03, 0.05]
        for _ in range(count):
            user_id = random.randint(1, 300)
            result = random.choices(results, weights)[0]
            warehouse_id = random.choice(warehouse_ids)
            c.execute('INSERT INTO Inventory (User_id, Result, Warehouse_id) VALUES (%s, %s, %s)',
                      (user_id, result, warehouse_id))
        self.conn.commit()

    def bulk_insert_product(self, count):
        c = self.conn.cursor()
        for _ in range(count):
            product_name = f'product{random.randint(1, 1000)}'
            quantity = random.randint(1, 1500)
            c.execute('INSERT INTO Product (Product_Name, Quantity) VALUES (%s, %s)', (product_name, quantity))
        self.conn.commit()

    def bulk_insert_warehouse_products(self, count):
        c = self.conn.cursor()
        c.execute('SELECT Inventory_id FROM Inventory')
        inventory_ids = [row[0] for row in c.fetchall()]
        c.execute('SELECT Product_id FROM Product')
        product_ids = [row[0] for row in c.fetchall()]

        if not inventory_ids or not product_ids:
            print("Error: Inventory or Product table is empty.")
            return

        combinations = [(inventory_id, product_id) for inventory_id in inventory_ids for product_id in product_ids]
        if len(combinations) < count:
            print(f"Error: Not enough unique combinations. Maximum possible is {len(combinations)}.")
            return

        random.shuffle(combinations)
        unique_combinations = combinations[:count]

        c.executemany('INSERT INTO Warehouse_Products (Inventory_id, Product_id) VALUES (%s, %s)', unique_combinations)
        self.conn.commit()

    def drop_all_tables(self):
        c = self.conn.cursor()
        try:
            c.execute('DROP TABLE IF EXISTS Warehouse_Products')
            c.execute('DROP TABLE IF EXISTS Inventory')
            c.execute('DROP TABLE IF EXISTS Product')
            c.execute('DROP TABLE IF EXISTS Warehouse')
            self.conn.commit()
            print("All tables dropped successfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error while dropping tables: {e}")

    def get_inventory_count_by_warehouse(self, result_filter):
        query = '''
            SELECT w."Where", COUNT(i.Inventory_id) AS inventory_count
            FROM Warehouse w
            JOIN Inventory i ON w.Warehouse_id = i.Warehouse_id
            WHERE i.Result = %s
            GROUP BY w."Where"
        '''
        c = self.conn.cursor()
        start_time = time.time()
        c.execute(query, (result_filter,))
        rows = c.fetchall()
        execution_time = (time.time() - start_time) * 1000  # в миллисекундах
        return rows, execution_time

    def get_products_with_quantity(self, min_quantity):
        query = '''
            SELECT p.Product_Name, COUNT(wp.Inventory_id) AS linked_warehouses
            FROM Product p
            JOIN Warehouse_Products wp ON p.Product_id = wp.Product_id
            WHERE p.Quantity > %s
            GROUP BY p.Product_Name
        '''
        c = self.conn.cursor()
        start_time = time.time()
        c.execute(query, (min_quantity,))
        rows = c.fetchall()
        execution_time = (time.time() - start_time) * 1000
        return rows, execution_time

    def get_warehouse_with_most_inventories(self):
        query = '''
            SELECT w."Where", COUNT(i.Inventory_id) AS inventory_count
            FROM Warehouse w
            JOIN Inventory i ON w.Warehouse_id = i.Warehouse_id
            GROUP BY w."Where"
            ORDER BY inventory_count DESC
            LIMIT 1
        '''
        c = self.conn.cursor()
        start_time = time.time()
        c.execute(query)
        row = c.fetchone()
        execution_time = (time.time() - start_time) * 1000
        return row, execution_time

