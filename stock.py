import sqlite3
import tkinter as tk
from tkinter import messagebox

class Product:
    def __init__(self, name, category, stock, price, sold=0):
        self.name = name
        self.category = category
        self.stock = stock
        self.price = price
        self.sold = sold

    def sell(self, quantity):
        if quantity <= self.stock:
            self.stock -= quantity
            self.sold += quantity
            return True
        else:
            return False

class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ระบบจัดการ Stockสินค้า North boy 17 Shop")

        self.conn = sqlite3.connect('store.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        self.products = self.load_products()

        # Label และ Entry สำหรับเพิ่มสินค้า
        self.name_label = tk.Label(root, text="ชื่อสินค้า:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        self.category_label = tk.Label(root, text="ประเภทสินค้า:")
        self.category_label.grid(row=1, column=0)
        self.category_var = tk.StringVar(root)
        self.category_var.set("วง")  # Default category
        self.category_menu = tk.OptionMenu(root, self.category_var, "วง", "การ์ตูน", "หนัง", "ลานมันส์")
        self.category_menu.grid(row=1, column=1)

        self.stock_label = tk.Label(root, text="จำนวนสินค้าในสต็อก:")
        self.stock_label.grid(row=2, column=0)
        self.stock_entry = tk.Entry(root)
        self.stock_entry.grid(row=2, column=1)

        self.price_label = tk.Label(root, text="ราคาสินค้า ฿ :")
        self.price_label.grid(row=3, column=0)
        self.price_entry = tk.Entry(root)
        self.price_entry.grid(row=3, column=1)
        self.price_entry.bind("<KeyRelease>", self.update_price_display)  # Binding to update display on key release

        self.add_button = tk.Button(root, text="เพิ่มสินค้า", command=self.add_product)
        self.add_button.grid(row=4, column=1)

        # Label และ Entry สำหรับขายสินค้า
        self.sell_label = tk.Label(root, text="ชื่อสินค้า (ขาย):")
        self.sell_label.grid(row=5, column=0)
        self.sell_entry = tk.Entry(root)
        self.sell_entry.grid(row=5, column=1)

        self.quantity_label = tk.Label(root, text="จำนวนที่ขาย:")
        self.quantity_label.grid(row=6, column=0)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=6, column=1)

        self.sell_button = tk.Button(root, text="ขายสินค้า", command=self.sell_product)
        self.sell_button.grid(row=7, column=1)

        # ปุ่มแสดงข้อมูลสินค้า
        self.list_button = tk.Button(root, text="แสดงข้อมูลสินค้า", command=self.list_products)
        self.list_button.grid(row=8, column=0)

        # ปุ่มรวมยอดที่ขายได้ทั้งหมด
        self.total_sales_button = tk.Button(root, text="รวมยอดขายทั้งหมด", command=self.show_total_sales)
        self.total_sales_button.grid(row=8, column=1)

        # ปุ่มเคลียร์ข้อความ
        self.clear_button = tk.Button(root, text="เคลียร์ข้อความ", command=self.clear_text)
        self.clear_button.grid(row=9, column=0)

        # ปุ่มล้างข้อมูลเก่า
        self.clear_data_button = tk.Button(root, text="เคลียร์ข้อมูลเก่า", command=self.clear_data)
        self.clear_data_button.grid(row=9, column=1)

        # Text widget สำหรับแสดงข้อมูลสินค้า
        self.output_text = tk.Text(root, height=10, width=50)
        self.output_text.grid(row=10, column=0, columnspan=2)

    def create_table(self):
        """สร้างตารางสำหรับเก็บข้อมูลสินค้าในฐานข้อมูล"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            stock INTEGER,
            price REAL,
            sold INTEGER
        )
        ''')
        self.conn.commit()

    def load_products(self):
        """โหลดข้อมูลสินค้าจากฐานข้อมูล"""
        self.cursor.execute("SELECT name, category, stock, price, sold FROM products")
        rows = self.cursor.fetchall()
        products = [Product(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        return products

    def add_product(self):
        name = self.name_entry.get()
        category = self.category_var.get()
        try:
            stock = int(self.stock_entry.get())
            price = float(self.price_entry.get().replace(' ฿', '').replace(',', ''))  # รับค่าราคาและแปลงเป็น float
        except ValueError:
            messagebox.showerror("Error", "จำนวนสินค้าและราคาต้องเป็นตัวเลข")
            return

        new_product = Product(name, category, stock, price)
        self.products.append(new_product)

        # บันทึกข้อมูลลงฐานข้อมูล
        self.cursor.execute("INSERT INTO products (name, category, stock, price, sold) VALUES (?, ?, ?, ?, ?)", 
                            (name, category, stock, price, new_product.sold))
        self.conn.commit()

        messagebox.showinfo("Success", f"เพิ่มสินค้า {name} สำเร็จ")
        self.clear_entries()

    def sell_product(self):
        name = self.sell_entry.get()
        try:
            quantity = int(self.quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "จำนวนที่ขายต้องเป็นตัวเลข")
            return

        for product in self.products:
            if product.name == name:
                if product.sell(quantity):
                    # อัปเดตข้อมูลในฐานข้อมูล
                    self.cursor.execute("UPDATE products SET stock = ?, sold = ? WHERE name = ?", 
                                        (product.stock, product.sold, product.name))
                    self.conn.commit()

                    messagebox.showinfo("Success", f"ขาย {name} จำนวน {quantity} ชิ้น สำเร็จ")
                else:
                    messagebox.showerror("Error", f"สินค้า {name} มีจำนวนไม่พอ (คงเหลือ {product.stock})")
                return
        messagebox.showerror("Error", f"ไม่พบสินค้า {name}")

    def list_products(self):
        self.output_text.delete(1.0, tk.END)
        for product in self.products:
            self.output_text.insert(tk.END, f"ชื่อสินค้า: {product.name}, ประเภท: {product.category}, คงเหลือ: {product.stock}, ราคา: {product.price:.2f} บาท, ขายแล้ว: {product.sold}\n")

    def show_total_sales(self):
        total_sales = sum((product.price or 0) * product.sold for product in self.products)
        messagebox.showinfo("ยอดขายทั้งหมด", f"ยอดขายทั้งหมด: {total_sales:.2f} บาท")

    def clear_text(self):
        self.output_text.delete(1.0, tk.END)

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)  # ล้างช่องกรอกราคา
        self.sell_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def clear_data(self):
        """ลบข้อมูลทั้งหมดจากฐานข้อมูล"""
        self.cursor.execute("DELETE FROM products")
        self.conn.commit()
        self.products = []  # รีเซ็ตรายการสินค้าในโปรแกรม
        self.clear_text()  # ล้างข้อมูลใน Text widget
        messagebox.showinfo("Success", "ล้างข้อมูลทั้งหมดสำเร็จ")

    def update_price_display(self, event):
        """อัพเดตการแสดงผลของช่องกรอกราคา"""
        current_value = self.price_entry.get().replace(' ฿', '').replace(',', '')
        if current_value and not current_value[-1].isdigit():
            current_value = current_value[:-1]
        if current_value:
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, f"{current_value} ฿")

# เริ่มโปรแกรม
root = tk.Tk()
app = StoreApp(root)
root.mainloop()
