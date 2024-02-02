class Product:
    def __init__(self, name, available_quantity, price_per_kg):
        self.name = name
        self.available_quantity = available_quantity
        self.price_per_kg = price_per_kg

    def __str__(self):
        return f"{self.name}, {self.available_quantity} kg available, {self.price_per_kg} RON/kg"
