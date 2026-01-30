import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import requests


def send_email(to_email: str, subject: str, html_content: str) -> bool:
    api_key = os.getenv("SENDGRID_API_KEY", "")
    from_email = os.getenv("SENDGRID_FROM_EMAIL", "")
    from_name = os.getenv("SENDGRID_FROM_NAME", "Saffron & Smoke")

    if not api_key or not from_email:
        # Missing config -> fail safely
        return False

    message = Mail(
        from_email=(from_email, from_name),
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(api_key)
        resp = sg.send(message)
        return 200 <= resp.status_code < 300
    except Exception:
        return False
    



def send_order_confirmation_via_cloudrun(order, order_items, user_email: str) -> bool:
    """
    Calls Cloud Run email function. Returns True if ok, else False.
    Does NOT raise (safe for checkout).
    """
    url = os.environ.get("ORDER_EMAIL_FUNCTION_URL", "").strip()
    secret = os.environ.get("FUNCTION_SHARED_SECRET", "").strip()

    if not url or not secret or not user_email:
        return False

    payload = {
        "to": user_email,
        "order_id": order.id,
        "total": str(order.total_price),
        "order_type": order.order_type,
        "items": [
            {
                "name": oi.menu_item.name if getattr(oi, "menu_item", None) else f"Item {oi.menu_item_id}",
                "qty": int(oi.quantity),
                "price": str(oi.unit_price_at_time),
            }
            for oi in order_items
        ],
    }

    # delivery address only if delivery
    if order.order_type == "delivery":
        payload["address"] = {
            "line1": order.delivery_address_line1 or "",
            "city": order.city or "",
            "postcode": order.postcode or "",
        }

    try:
        r = requests.post(
            url,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "X-FUNCTION-SECRET": secret,
            },
            timeout=10,
        )
        # Cloud function returns {"ok": true} on success
        data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
        return bool(r.ok and data.get("ok") is True)
    except Exception:
        return False

