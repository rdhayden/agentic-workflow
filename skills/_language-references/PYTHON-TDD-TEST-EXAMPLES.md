# Good and Bad Tests

## Test behaviour users care about not mocks of internals, call counts and sequencing

```python
# GOOD: Tests observable behavior
async def test_user_can_checkout_with_valid_cart():
    cart = create_cart()
    cart.add(product)
    result = await checkout(cart, payment_method)
    assert result.status == "confirmed"
```

Good test characteristics:

- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

```python
# BAD: Tests implementation details
async def test_checkout_calls_payment_service_process(mocker):
    mock_payment = mocker.patch("shop.payment_service")
    await checkout(cart, payment)
    mock_payment.process.assert_called_once_with(cart.total)
```

Bad test red flags:

- Mocking internal collaborators
- Testing private methods
- Asserting on call counts or call order
- Test breaks when refactoring without behavior change
- Test name describes HOW it works not WHAT it does
- Verifies through external means instead of interface response

## Use interface instead of bypassing it

```python
# GOOD: Verifies through interface
async def test_create_user_makes_user_retrievable():
    user = await create_user(name="Alice")
    retrieved = await get_user(user.id)
    assert retrieved.name == "Alice"


# BAD: Bypasses interface to verify
async def test_create_user_saves_to_database(db):
    await create_user(name="Alice")
    row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"])
    assert row is not None
```

## Avoid tautological tests

```python
# BAD: Expected value is recomputed the way the code computes it
def test_calculate_total_sums_line_items():
    items = [{"price": 10}, {"price": 5}]
    expected = sum(item["price"] for item in items)
    assert calculate_total(items) == expected


# GOOD: Expected value is an independently known literal
def test_calculate_total_sums_line_items():
    assert calculate_total([{"price": 10}, {"price": 5}]) == 15
```
