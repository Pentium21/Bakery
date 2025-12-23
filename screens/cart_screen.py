# screens/cart_screen.py

from kivy.app import App
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast

from data.mock_data import CART


class CartScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._checkout_dialog = None

    def on_enter(self, *args):
        self.refresh_cart()

    def refresh_cart(self):
        if "cart_list" not in self.ids or "total_label" not in self.ids:
            return

        self.ids.cart_list.clear_widgets()

        if not CART:
            self.ids.cart_list.add_widget(
                MDLabel(
                    text="Корзина пуста",
                    halign="center",
                    theme_text_color="Secondary"
                )
            )
            self.ids.total_label.text = "Итого: 0 ₽"
            return

        total = 0
        for item in CART:
            subtotal = item["price"] * item["qty"]
            total += subtotal

            row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(56),
                spacing=dp(8)
            )

            row.add_widget(
                TwoLineListItem(
                    text=item["name"],
                    secondary_text=f'{item["qty"]} × {item["price"]} ₽'
                )
            )

            row.add_widget(
                MDIconButton(
                    icon="minus",
                    on_release=lambda x, i=item: self.change_qty(i, -1)
                )
            )

            row.add_widget(
                MDIconButton(
                    icon="plus",
                    on_release=lambda x, i=item: self.change_qty(i, 1)
                )
            )

            row.add_widget(
                MDIconButton(
                    icon="delete",
                    on_release=lambda x, i=item: self.remove_item(i)
                )
            )

            self.ids.cart_list.add_widget(row)

        self.ids.total_label.text = f"Итого: {total} ₽"

    def change_qty(self, item, delta):
        item["qty"] += delta
        if item["qty"] <= 0:
            CART.remove(item)
        self.refresh_cart()

    def remove_item(self, item):
        if item in CART:
            CART.remove(item)
        self.refresh_cart()

    # ---------- ОФОРМЛЕНИЕ ЗАКАЗА ----------

    def checkout(self):
        if not CART:
            toast("Корзина пуста")
            return

        if self._checkout_dialog:
            return

        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        self.name_field = MDTextField(
            hint_text="Ваше имя",
            required=True
        )

        self.phone_field = MDTextField(
            hint_text="Телефон",
            required=True,
            input_filter="int"
        )

        content.add_widget(self.name_field)
        content.add_widget(self.phone_field)

        self._checkout_dialog = MDDialog(
            title="Данные клиента",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="Отмена",
                    on_release=self._dismiss_checkout
                ),
                MDFlatButton(
                    text="Подтвердить",
                    on_release=self._confirm_checkout
                ),
            ],
        )
        self._checkout_dialog.open()

    def _dismiss_checkout(self, *args):
        if self._checkout_dialog:
            self._checkout_dialog.dismiss()
            self._checkout_dialog = None

    def _confirm_checkout(self, *args):
        name = self.name_field.text.strip()
        phone = self.phone_field.text.strip()

        if not name or not phone:
            toast("Введите имя и телефон")
            return

        # 👉 здесь можно "отправить" заказ (эмуляция)
        print("НОВЫЙ ЗАКАЗ")
        print("Клиент:", name, phone)
        print("Товары:", CART)

        CART.clear()
        self._dismiss_checkout()
        self.refresh_cart()

        toast("Заказ оформлен. Спасибо!")

        App.get_running_app().root.current = "catalog"

    def go_back(self):
        App.get_running_app().root.current = "catalog"
