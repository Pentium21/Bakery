# screens/catalog_screen.py
from kivy.app import App
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from components.product_card import ProductCard
from data.mock_data import PRODUCTS


class CatalogScreen(MDScreen):

    def on_enter(self, *args):
        Clock.schedule_once(self.populate_grid, 0)

    def populate_grid(self, dt):
        grid = self.ids.get("grid")
        if not grid:
            return

        grid.clear_widgets()

        for product in PRODUCTS:
            card = ProductCard(
                name=product["name"],
                price=product["price"],
                image=product["image"]
            )
            card.bind(on_release=lambda x, p=product: self.open_detail(p))
            grid.add_widget(card)

    def open_detail(self, product):
        root = App.get_running_app().root
        detail = root.get_screen("detail")
        detail.set_product(product)
        root.current = "detail"

    def go_to_cart(self):
        App.get_running_app().root.current = "cart"
