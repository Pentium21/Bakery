from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty
from kivy.app import App

from kivymd.toast import toast

# Общая корзина
from data.mock_data import CART


class DetailScreen(MDScreen):
    product_name = StringProperty("")
    description = StringProperty("")
    image = StringProperty("")
    price = NumericProperty(0)
    qty = NumericProperty(1)   # количество товара

    def set_product(self, product: dict):
        self.product_name = product.get("name", "")
        self.description = product.get("description", "")
        self.image = product.get("image", "")
        self.price = product.get("price", 0)
        self.qty = 1  # сбрасываем количество при открытии товара

    def increase_qty(self):
        self.qty += 1

    def decrease_qty(self):
        if self.qty > 1:
            self.qty -= 1

    def add_to_cart(self):
        # защита
        if not self.product_name:
            return


        for item in CART:
            if item["name"] == self.product_name:
                item["qty"] += self.qty
                break
        else:
            CART.append({
                "name": self.product_name,
                "price": self.price,
                "qty": self.qty
            })


        toast(f"Добавлено в корзину: {self.product_name} × {self.qty}")



    def go_back(self):
        App.get_running_app().root.current = "catalog"
