Good interfaces make testing natural:

1. **Accept dependencies, don't create them.**

   ```python
   # Testable — dependency is injected
   def process_order(order, payment_gateway):
       ...
   
   # Hard to test — dependency is hard-wired
   def process_order(order):
       gateway = StripeGateway()
       ...
   ```

2. **Return results, don't produce side effects.**

   ```python
   # Testable — returns a value, no side effects (pure function)
   def calculate_discount(cart) -> Discount:
       ...

   # Hard to test — mutates its argument in place, returns nothing
   def apply_discount(cart) -> None:
       cart.total -= discount
  ```

3. **Small surface area.** Fewer methods = fewer tests needed. Fewer params = simpler test setup.