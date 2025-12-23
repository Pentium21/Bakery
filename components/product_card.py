from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty

class ProductCard(MDCard):
    name = StringProperty()
    price = NumericProperty()
    image = StringProperty()
