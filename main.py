from kivymd.app import MDApp
from kivy.lang import Builder


from screens.catalog_screen import CatalogScreen
from screens.detail_screen import DetailScreen
from screens.cart_screen import CartScreen
from components.product_card import ProductCard


class BakeryApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Pink"

        Builder.load_file("kv/product_card.kv")
        Builder.load_file("kv/catalog_screen.kv")
        Builder.load_file("kv/detail_screen.kv")
        Builder.load_file("kv/cart_screen.kv")

        return Builder.load_file("kv/main.kv")


BakeryApp().run()
