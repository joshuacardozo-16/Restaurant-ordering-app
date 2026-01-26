import sys
import os
from decimal import Decimal

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from app import create_app
from app.extensions import db
from app.models.order_item import OrderItem
from app.models.order import Order
from app.models.menu_item import MenuItem


MENU_ITEMS = [
    # -----------------
    # Starters
    # -----------------
    dict(
        name="Saffron Chicken Tikka Skewers",
        description="Chargrilled skewers, mint yoghurt, lemon.",
        price=Decimal("7.95"),
        category="Starters",
        image_url="https://images.unsplash.com/photo-1604908176997-125f25cc500f?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Smoked Paprika Halloumi Fries",
        description="Crispy halloumi fries, chilli honey dip.",
        price=Decimal("6.50"),
        category="Starters",
        image_url="https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Spiced Lentil Soup",
        description="Slow-cooked lentils, cumin, herbs.",
        price=Decimal("5.95"),
        category="Starters",
        image_url="https://images.unsplash.com/photo-1543353071-087092ec393a?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Garlic & Herb Flatbread",
        description="Warm flatbread with garlic butter.",
        price=Decimal("4.95"),
        category="Starters",
        image_url="https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Crispy Calamari",
        description="Lightly fried calamari, lemon aioli.",
        price=Decimal("7.50"),
        category="Starters",
        image_url="https://images.unsplash.com/photo-1559847844-5315695dadae?auto=format&fit=crop&w=1200&q=80",
    ),

    # -----------------
    # Sharers
    # -----------------
    dict(
        name="Sharer Platter (Mix Grill)",
        description="Chicken tikka, lamb kofta, halloumi, salad, dips.",
        price=Decimal("19.95"),
        category="Sharers",
        image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Loaded Nachos Sharer",
        description="Cheese, salsa, jalapeños, sour cream.",
        price=Decimal("11.95"),
        category="Sharers",
        image_url="https://images.unsplash.com/photo-1543339318-b43dc53e19b3?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Wings Sharer (12 pcs)",
        description="Choose: BBQ / Hot / Garlic. Served with dip.",
        price=Decimal("12.95"),
        category="Sharers",
        image_url="https://images.unsplash.com/photo-1604908176997-125f25cc500f?auto=format&fit=crop&w=1200&q=80",
    ),

    # -----------------
    # Mains
    # -----------------
    dict(
        name="Chargrilled Lamb Kofta",
        description="Kofta, warm flatbread, salad, tahini.",
        price=Decimal("15.95"),
        category="Mains",
        image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Butter Chicken Masala",
        description="Creamy tomato curry, served with rice.",
        price=Decimal("14.50"),
        category="Mains",
        image_url="https://images.unsplash.com/photo-1604908176997-125f25cc500f?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Paneer Tikka Curry",
        description="Spiced paneer curry, peppers, onions, rice.",
        price=Decimal("13.95"),
        category="Mains",
        image_url="https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Smoky BBQ Ribs",
        description="Half rack ribs, BBQ glaze, slaw.",
        price=Decimal("16.95"),
        category="Mains",
        image_url="https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Grilled Salmon Bowl",
        description="Salmon, herbs, seasonal veg, rice.",
        price=Decimal("15.50"),
        category="Mains",
        image_url="https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Veg Tagine",
        description="Slow-cooked veg, chickpeas, spices, couscous.",
        price=Decimal("12.95"),
        category="Mains",
        image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80",
    ),

    # -----------------
    # Meal Deals (Sales Boost)
    # -----------------
    dict(
        name="Burger Meal Deal",
        description="Any burger + fries + soft drink (save vs buying separately).",
        price=Decimal("15.95"),
        category="Meal Deals",
        image_url="https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Rice Bowl Meal Deal",
        description="Any rice bowl + side + soft drink (value deal).",
        price=Decimal("15.50"),
        category="Meal Deals",
        image_url="https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Wrap Meal Deal",
        description="Any wrap + fries + soft drink (customer favourite).",
        price=Decimal("13.95"),
        category="Meal Deals",
        image_url="https://images.unsplash.com/photo-1523986371872-9d3ba2e2f642?auto=format&fit=crop&w=1200&q=80",
    ),

    # -----------------
    # Rice Combos
    # -----------------
    dict(
        name="Saffron Rice Bowl – Chicken",
        description="Saffron rice, grilled chicken, salad, house sauce.",
        price=Decimal("12.95"),
        category="Rice Combos",
        image_url="https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Saffron Rice Bowl – Lamb",
        description="Saffron rice, lamb kofta, pickles, tahini drizzle.",
        price=Decimal("13.95"),
        category="Rice Combos",
        image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Saffron Rice Bowl – Veg",
        description="Saffron rice, roasted veg, chickpeas, garlic sauce.",
        price=Decimal("11.95"),
        category="Rice Combos",
        image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Spicy Chicken Rice Box",
        description="Spiced chicken, rice, salad, chilli mayo.",
        price=Decimal("12.50"),
        category="Rice Combos",
        image_url="https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Teriyaki Veg Rice Box",
        description="Veg, teriyaki glaze, sesame, rice.",
        price=Decimal("11.50"),
        category="Rice Combos",
        image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80",
    ),

    # -----------------
    # Wraps
    # -----------------
    dict(
        name="Chicken Tikka Wrap",
        description="Chicken tikka, salad, mint yoghurt, wrap.",
        price=Decimal("10.95"),
        category="Wraps",
        image_url="https://images.unsplash.com/photo-1523986371872-9d3ba2e2f642?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Lamb Kofta Wrap",
        description="Lamb kofta, pickles, tahini, wrap.",
        price=Decimal("11.95"),
        category="Wraps",
        image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Falafel & Hummus Wrap",
        description="Falafel, hummus, salad, garlic sauce.",
        price=Decimal("9.95"),
        category="Wraps",
        image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80",
    ),


    # -----------------
    # Burgers
    # -----------------
    dict(
        name="Saffron Smash Burger",
        description="Double beef, cheddar, onions, house sauce.",
        price=Decimal("12.95"),
        category="Burgers",
        image_url="https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Smoked BBQ Chicken Burger",
        description="Smoked chicken, slaw, pickles, BBQ glaze.",
        price=Decimal("12.50"),
        category="Burgers",
        image_url="https://images.unsplash.com/photo-1550317138-10000687a72b?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Plant Power Burger",
        description="Crispy plant patty, avocado, lettuce, vegan mayo.",
        price=Decimal("11.95"),
        category="Burgers",
        image_url="https://images.unsplash.com/photo-1520072959219-c595dc870360?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Double Cheese Burger",
        description="Beef, double cheddar, pickles, ketchup.",
        price=Decimal("13.50"),
        category="Burgers",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1200&q=80",
    ),

    # -----------------
    # Sides
    # -----------------
    dict(
        name="Skin-on Fries",
        description="Crispy fries, sea salt.",
        price=Decimal("3.50"),
        category="Sides",
        image_url="https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Loaded Fries (Cheese & Jalapeño)",
        description="Cheddar, jalapeño, sauce.",
        price=Decimal("5.95"),
        category="Sides",
        image_url="https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Garlic Naan",
        description="Warm naan brushed with garlic butter.",
        price=Decimal("2.95"),
        category="Sides",
        image_url="https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Side Salad",
        description="Mixed leaves, cucumber, house dressing.",
        price=Decimal("3.95"),
        category="Sides",
        image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Spiced Corn Ribs",
        description="Corn ribs, chilli-lime seasoning.",
        price=Decimal("4.95"),
        category="Sides",
        image_url="https://images.unsplash.com/photo-1617093727343-374698b1b08d?auto=format&fit=crop&w=1200&q=80",
    ),

    # -----------------
    # Kids Meals
    # -----------------
    dict(
        name="Kids Chicken Bites + Fries",
        description="Small portion chicken bites, fries, ketchup.",
        price=Decimal("6.95"),
        category="Kids Meals",
        image_url="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Kids Mini Burger + Fries",
        description="Mini beef burger, fries, ketchup.",
        price=Decimal("7.50"),
        category="Kids Meals",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Kids Veg Nuggets + Fries",
        description="Veg nuggets, fries, ketchup.",
        price=Decimal("6.50"),
        category="Kids Meals",
        image_url="https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=1200&q=80",
    ),

    # -----------------
    # Desserts
    # -----------------
    dict(
        name="Chocolate Fudge Brownie",
        description="Warm brownie, chocolate sauce.",
        price=Decimal("6.50"),
        category="Desserts",
        image_url="https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Mango Cheesecake",
        description="Creamy cheesecake with mango swirl.",
        price=Decimal("6.95"),
        category="Desserts",
        image_url="https://images.unsplash.com/photo-1542826438-bd32f43d626f?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Sticky Toffee Pudding",
        description="Warm sponge, toffee sauce, cream.",
        price=Decimal("6.95"),
        category="Desserts",
        image_url="https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=1200&q=80",
    ),

    # -----------------
    # Sauces
    # -----------------
    dict(
        name="Garlic Mayo Dip",
        description="Creamy garlic mayo (2oz).",
        price=Decimal("0.75"),
        category="Sauces",
        image_url="https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Smoky BBQ Dip",
        description="BBQ dip (2oz).",
        price=Decimal("0.75"),
        category="Sauces",
        image_url="https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Chilli Honey Dip",
        description="Sweet heat dip (2oz).",
        price=Decimal("0.95"),
        category="Sauces",
        image_url="https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Mint Yoghurt Dip",
        description="Cool mint yoghurt (2oz).",
        price=Decimal("0.75"),
        category="Sauces",
        image_url="https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80",
    ),

    # -----------------
    # Drinks
    # -----------------
    dict(
        name="Coke (330ml)",
        description="Chilled can.",
        price=Decimal("2.00"),
        category="Drinks",
        image_url="https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Sparkling Water",
        description="Refreshing and cold.",
        price=Decimal("2.20"),
        category="Drinks",
        image_url="https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Mango Lassi",
        description="Sweet mango yoghurt drink.",
        price=Decimal("3.95"),
        category="Drinks",
        image_url="https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=1200&q=80",
    ),
    dict(
        name="Fresh Lemonade",
        description="Homemade lemonade, mint.",
        price=Decimal("3.50"),
        category="Drinks",
        image_url="https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=1200&q=80",
    ),
]

def reset_and_seed():
    app = create_app()
    with app.app_context():
        # Ensure tables exist
        db.create_all()

        # IMPORTANT: delete in FK-safe order
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(MenuItem).delete()
        db.session.commit()

        # Insert new menu
        for d in MENU_ITEMS:
            item = MenuItem(
                name=d["name"],
                description=d.get("description"),
                price=d["price"],
                category=d["category"],
                image_url=d.get("image_url"),
                is_available=True,
            )
            db.session.add(item)

        db.session.commit()

        print("✅ Reset complete: deleted old orders + menu items.")
        print(f"✅ Seeded menu items: {len(MENU_ITEMS)}")


if __name__ == "__main__":
    reset_and_seed()
