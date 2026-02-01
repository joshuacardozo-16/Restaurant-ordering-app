from app import create_app
from app.models.user import User

def show(resp, label):
    print(f"\n✅ {label}: {resp.status_code}")
    try:
        print(resp.get_json())
    except Exception:
        print(resp.data.decode("utf-8")[:500])

def main():
    app = create_app()

    with app.app_context():
        admin = User.query.filter_by(role="admin").first()
        if not admin:
            print("❌ No admin user found. Run create_admin.py first.")
            return

        client = app.test_client()

        # Force login (no cookies needed)
        with client.session_transaction() as sess:
            sess["_user_id"] = str(admin.id)
            sess["_fresh"] = True

        # 1) LIST
        r = client.get("/api/admin/menu")
        show(r, "LIST")

        # 2) CREATE
        payload = {
            "name": "API Test Item",
            "category": "Drinks",
            "price": 3.50,
            "description": "Created via Admin API",
            "is_available": True,
        }
        r = client.post("/api/admin/menu", json=payload)
        show(r, "CREATE")

        data = r.get_json() or {}
        created = data.get("created")
        if not created:
            print("❌ Create failed, stopping (see response above).")
            return

        created_id = created["id"]

        # 3) UPDATE
        r = client.put(f"/api/admin/menu/{created_id}", json={"price": 4.25, "name": "API Test Item UPDATED"})
        show(r, "UPDATE")

        # 4) DELETE
        r = client.delete(f"/api/admin/menu/{created_id}")
        show(r, "DELETE")

if __name__ == "__main__":
    main()
