**1. Use dependency injection**

Pass external dependencies in rather than creating them internally:

# Easy to mock — dependency is injected
def process_payment(order, payment_client):
    return payment_client.charge(order.total)


# Hard to mock — dependency is constructed inside
def process_payment(order):
    client = StripeClient(os.environ["STRIPE_KEY"])
    return client.charge(order.total)

**2. Prefer SDK-style interfaces over generic fetchers**

# GOOD: Each function is independently mockable
class Api:
    def get_user(self, id):
        return requests.get(f"/users/{id}")

    def get_orders(self, user_id):
        return requests.get(f"/users/{user_id}/orders")

    def create_order(self, data):
        return requests.post("/orders", json=data)


# BAD: Mocking requires conditional logic inside the mock
class Api:
    def fetch(self, endpoint, method="GET", **options):
        return requests.request(method, endpoint, **options)