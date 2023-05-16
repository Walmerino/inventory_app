import csv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class InventoryManagement(App):
    inventory = {}

    def build(self):
        # Load inventory from CSV file
        self.load_inventory()

        # Main layout
        layout = BoxLayout(orientation='horizontal', spacing=10)

        # Left side layout
        left_layout = BoxLayout(orientation='vertical', spacing=10)

        # Category Entry
        category_label = Label(text="Category:")
        self.category_entry = TextInput()
        left_layout.add_widget(category_label)
        left_layout.add_widget(self.category_entry)

        # Product Entry
        product_label = Label(text="Product:")
        self.product_entry = TextInput()
        left_layout.add_widget(product_label)
        left_layout.add_widget(self.product_entry)

        # Quantity Entry
        quantity_label = Label(text="Quantity:")
        self.quantity_entry = TextInput()
        left_layout.add_widget(quantity_label)
        left_layout.add_widget(self.quantity_entry)

        # Add Category Button
        add_category_button = Button(text="Add Category")
        add_category_button.bind(on_release=self.add_category)
        left_layout.add_widget(add_category_button)

        # Category Buttons
        self.category_buttons = []

        # Add Product Button
        add_product_button = Button(text="Add Product")
        add_product_button.bind(on_release=self.add_product)
        left_layout.add_widget(add_product_button)

        # Update Product Button
        update_product_button = Button(text="Update Product")
        update_product_button.bind(on_release=self.update_product)
        left_layout.add_widget(update_product_button)

        # Delete Category Button
        delete_category_button = Button(text="Delete Category")
        delete_category_button.bind(on_release=self.delete_category)
        left_layout.add_widget(delete_category_button)

        # Delete Product Button
        delete_product_button = Button(text="Delete Product")
        delete_product_button.bind(on_release=self.delete_product)
        left_layout.add_widget(delete_product_button)

        layout.add_widget(left_layout)

        # Right side layout
        self.right_layout = BoxLayout(orientation='vertical', spacing=10)
        layout.add_widget(self.right_layout)

        # Display inventory
        self.display_inventory()

        return layout

    def load_inventory(self):
        with open('inventory1.6.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                category, product, quantity = row
                if category not in self.inventory:
                    self.inventory[category] = {}
                self.inventory[category][product] = int(quantity)

    def save_inventory(self):
        with open('inventory1.6.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for category, products in self.inventory.items():
                for product, quantity in products.items():
                    writer.writerow([category, product, quantity])

    def add_category(self, instance):
        category = self.category_entry.text
        if category in self.inventory:
            self.show_message("Error", "Category already exists.")
            return
        self.inventory[category] = {}
        self.show_message("Success", "Category added successfully.")
        self.update_category_buttons()
        self.save_inventory()

        # Clear input fields
        self.category_entry.text = ""
       
    def update_category_buttons(self):
        for button in self.category_buttons:
            self.right_layout.remove_widget(button)
        self.category_buttons.clear()
        for category in self.inventory:
            button = Button(text=category)
            button.bind(on_release=lambda btn: self.display_products(btn.text))
            self.category_buttons.append(button)
            self.right_layout.add_widget(button)

    def display_products(self, category):
        self.right_layout.clear_widgets()
        self.right_layout.add_widget(Label(text=category))
        for product, quantity in self.inventory[category].items():
            self.right_layout.add_widget(Label(text=f"{product}: {quantity}"))

    def add_product(self, instance):
        category = self.category_entry.text
        product = self.product_entry.text
        quantity = self.quantity_entry.text

        if not category:
            self.show_message("Error", "Please select a category.")
            return

        if not product:
            self.show_message("Error", "Please enter a product.")
            return

        if not quantity.isdigit():
            self.show_message("Error", "Please enter a valid quantity.")
            return

        quantity = int(quantity)
        self.inventory[category][product] = quantity
        self.show_message("Success", "Product added successfully.")
        self.display_products(category)
        self.save_inventory()

        # Clear input fields
        self.product_entry.text = ""
        self.quantity_entry.text = ""

    def update_product(self, instance):
        category = self.category_entry.text
        product = self.product_entry.text
        quantity = int(self.quantity_entry.text)
        self.inventory[category][product] = quantity
        self.show_message("Success", "Product updated successfully.")
        self.display_products(category)
        self.save_inventory()

    def delete_category(self, instance):
        category = self.category_entry.text
        if category not in self.inventory:
            self.show_message("Error", "Category does not exist.")
            return
        del self.inventory[category]
        self.show_message("Success", "Category deleted successfully.")
        self.update_category_buttons()
        self.category_entry.text = ""
        self.right_layout.clear_widgets()
        self.save_inventory()

    def delete_product(self, instance):
        category = self.category_entry.text
        product = self.product_entry.text
        if category not in self.inventory:
            self.show_message("Error", "Category does not exist.")
            return
        if product not in self.inventory[category]:
            self.show_message("Error", "Product does not exist.")
            return
        del self.inventory[category][product]
        self.show_message("Success", "Product deleted successfully.")
        self.display_products(category)
        self.save_inventory()

    def show_message(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def display_inventory(self):
        for category in self.inventory:
            button = Button(text=category)
            button.bind(on_release=lambda btn: self.display_products(btn.text))
            self.category_buttons.append(button)
            self.right_layout.add_widget(button)

    def on_stop(self):
        self.save_inventory()

if __name__ == '__main__':
    InventoryManagement().run()
