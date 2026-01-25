from app import create_app
from app.extensions import db
from app.models.menu_item import MenuItem

MENU_ITEMS = [
    ("Margherita Pizza", "Pizza", 9.99, "Classic tomato & mozzarella"),
    ("Pepperoni Pizza", "Pizza", 11.49, "Pepperoni & cheese"),
    ("BBQ Chicken Pizza", "Pizza", 12.49, "BBQ sauce, chicken, onion"),
    ("Chicken Burger", "Burgers", 8.99, "Crispy chicken burger"),
    ("Beef Burger", "Burgers", 9.49, "Juicy beef patty"),
    ("Veggie Burger", "Burgers", 8.49, "Plant based option"),
    ("Large Fries", "Sides", 3.49, "Golden fries"),
    ("Onion Rings", "Sides", 3.99, "Crispy rings"),
    ("Garlic Bread", "Sides", 3.49, "Toasted garlic bread"),
    ("Coca Cola", "Drinks", 1.99, "Cold drink"),
    ("Sprite", "Drinks", 1.99, "Lemon drink"),
    ("Water", "Drinks", 1.49, "Still water"),
    ("Chocolate Cake", "Desserts", 4.99, "Rich chocolate cake"),
    ("Cheesecake", "Desserts", 5.49, "Creamy cheesecake"),
]

def main():
    app = create_app()
    with app.app_context():
        added = 0
        for name, category, price, desc in MENU_ITEMS:
            exists = MenuItem.query.filter_by(name=name).first()
            if not exists:
                item = MenuItem(
                    name=name,
                    category=category,
                    price=price,
                    description=desc,
                    is_available=True,
                )
                db.session.add(item)
                added += 1

        db.session.commit()
        print(f"Seeded {added} menu items ✅")

if __name__ == "__main__":
    main()
