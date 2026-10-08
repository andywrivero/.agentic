# Default order example

Numbered comments map to the class order in SKILL.md and are for illustration only. Do not add them to real code.

```java
public class OrderService {
    // 1. Constants
    private static final int MAX_RETRIES = 3;

    // 2. Static fields
    private static long processedCount;

    // 3. Instance fields
    private final PaymentGateway gateway;
    private final InventoryRepository inventory;

    // 4. Constructors, then static factories
    public OrderService(PaymentGateway gateway, InventoryRepository inventory) {
        this.gateway = Objects.requireNonNull(gateway, "gateway");
        this.inventory = Objects.requireNonNull(inventory, "inventory");
    }

    public static OrderService withDefaults() {
        return new OrderService(new DefaultGateway(), new InMemoryInventory());
    }

    // 5. Public methods (overloads adjacent, overrides last)
    public OrderResult process(OrderRequest request) {
        validate(request);
        if (!reserveWithRetry(request)) {
            return OrderResult.failed("Inventory unavailable");
        }
        processedCount++;
        return OrderResult.success(gateway.charge(request.payment()));
    }

    public OrderResult process(OrderRequest request, Options options) {
        return process(options.apply(request));
    }

    @Override
    public String toString() {
        return "OrderService{processed=" + processedCount + "}";
    }

    // 5. Protected, then package-private methods
    protected boolean isRetryable(Exception e) {
        return e instanceof TransientException;
    }

    // 6. Private methods in call order
    private void validate(OrderRequest request) {
        if (request == null || request.items().isEmpty()) {
            throw new IllegalArgumentException("Empty order");
        }
    }

    private boolean reserveWithRetry(OrderRequest request) {
        for (int i = 0; i < MAX_RETRIES; i++) {
            if (inventory.tryReserve(request.items())) {
                return true;
            }
        }
        return false;
    }

    // 7. Nested types
    public static final class Options {
        // same rules apply inside
    }
}
```
