from app.services.cart import add_to_cart, get_cart, remove_from_cart, clear_cart, set_qty

def test_cart_add_and_get(client):
    with client.session_transaction() as sess:
        sess["cart"] = {}

    with client:
        add_to_cart(10, 2)
        cart = get_cart()

    assert cart["10"] == 2


def test_cart_remove(client):
    with client.session_transaction() as sess:
        sess["cart"] = {"5": 1}

    with client:
        remove_from_cart(5)
        cart = get_cart()

    assert "5" not in cart


def test_cart_set_qty_and_clear(client):
    with client.session_transaction() as sess:
        sess["cart"] = {"1": 1}

    with client:
        set_qty(1, 3)
        assert get_cart()["1"] == 3

        set_qty(1, 0)
        assert "1" not in get_cart()

        clear_cart()
        assert get_cart() == {}
