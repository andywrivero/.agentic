---
name: java-member-ordering
description: Enforces the "Grouped Visibility" member-ordering convention for Java source files - constants, then static fields, then instance fields, then constructors, then public/protected methods, then private methods, then nested types. Use this whenever writing a new Java class, interface, or enum, or editing/refactoring an existing one, even if the user's request is just "add a method" or "fix this bug" and doesn't mention formatting or ordering at all - the convention should hold every time Java source is touched, not just when explicitly asked for. Also applies when reordering an existing file that violates the convention (fields scattered after methods, private helpers interleaved with public ones, etc.).
---

# Java Member Ordering

## Why this exists

Interleaved member ordering (a private helper sitting between two public methods, a field declared halfway down the file) makes a class harder to skim: a reader can't tell "what does this class offer" from "how does it do it" without reading the whole thing. Grouped Visibility fixes that by putting the public interface in one contiguous block and the implementation details in another, so opening any class answers the same question the same way every time - no per-file surprises, no fighting an auto-formatter that wants something else.

This is a standing convention, not a one-off request. Apply it any time you write or touch a `.java` file, whether the task is "add a method," "fix this bug," or "generate a new class" - not only when someone explicitly asks for reformatting.

## Member order

Organize every class top-to-bottom in this order. Skip any section that doesn't apply (e.g. a class with no constants just starts at static fields).

1. **Constants** — `static final` fields, in either visibility.
2. **Static fields** — mutable `static` state, plus static initializer blocks.
3. **Instance fields** — private by default; only widen visibility where encapsulation genuinely calls for it.
4. **Constructors & static factories** — including Lombok-generated ones where relevant (a `@Builder`-annotated constructor still counts as "constructors" for placement purposes).
5. **Public / protected methods** — the class's public interface: business/domain methods first, then overrides (`equals`, `hashCode`, `toString`, `@Override` methods) at the end of this section.
6. **Private helper methods** — implementation details, ordered by call flow (the method a public entry point calls first comes first; low-level or generic utility helpers sink toward the bottom).
7. **Nested types** — static nested classes, inner classes, and companion types (e.g. a `Builder`, a `RetryStrategy` used only by this class) go last, after every method section. A nested type follows the same ordering internally.

The core rule underneath all seven: every `public`/`protected` member precedes every `private` member, and fields never appear below a constructor or method.

## Formatting details

- One blank line between individual members (fields, methods, nested types). Closely related constants/fields may sit together without a blank line between them, but keep the constants block visually separate from the instance-fields block.
- Overloaded methods stay adjacent, in ascending parameter-count/complexity order (e.g. `process(String)` immediately followed by `process(String, Options)`).
- Within the private section, order by logical execution flow, not alphabetically: the first helper a public method calls appears first; a generic, reusable utility (string manipulation, validation) that several methods lean on sinks to the very end of the file.

## Interfaces

Interface fields are implicitly `public static final`, so there's no separate instance-fields section. Order:
1. Constants
2. Methods (abstract, default, static - in that rough order, overloads kept adjacent as above)
3. Nested types, if any

## Enums

Java requires the constant list first, syntactically. After that, an enum follows the normal class ordering (fields → constructors → methods → nested types) for everything else it declares.

## Refactoring an existing file

When a file doesn't already follow this order:
1. **Move fields to the top**, in constants → static → instance order, without changing their values or modifiers.
2. **Consolidate scattered private methods** to the bottom, preserving each method's body exactly.
3. **Never change behavior while reordering** - this is a pure structural move. If you notice an actual bug while you're in there, mention it separately rather than fixing it silently as part of the reorder.

## Canonical example

The `// 1. Constants`, `// 2. Static fields`, etc. comments below are annotations for this example only, mapping the code back to the numbered list above - do not insert section-marker comments like these into real code.

```java
package com.example.service;

import java.time.Instant;
import java.util.Objects;
import java.util.Optional;

public class OrderProcessingService {

    // 1. Constants
    private static final int MAX_RETRY_ATTEMPTS = 3;
    private static final String DEFAULT_CURRENCY = "USD";

    // 2. Static fields
    private static long totalOrdersProcessed = 0;

    // 3. Instance fields
    private final PaymentGateway paymentGateway;
    private final InventoryRepository inventoryRepository;
    private boolean active = true;

    // 4. Constructors
    public OrderProcessingService(PaymentGateway paymentGateway, InventoryRepository inventoryRepository) {
        this.paymentGateway = Objects.requireNonNull(paymentGateway, "paymentGateway must not be null");
        this.inventoryRepository = Objects.requireNonNull(inventoryRepository, "inventoryRepository must not be null");
    }

    // 5. Public interface
    public OrderResult processOrder(OrderRequest request) {
        validateRequest(request);

        boolean reserved = reserveInventoryWithRetry(request);
        if (!reserved) {
            return OrderResult.failed("Inventory unavailable");
        }

        TransactionId txId = paymentGateway.charge(request.getPaymentDetails());
        totalOrdersProcessed++;

        return OrderResult.success(txId);
    }

    public Optional<OrderDetails> fetchOrder(String orderId) {
        return Optional.empty();
    }

    @Override
    public String toString() {
        return "OrderProcessingService{active=" + active + "}";
    }

    // 6. Private helpers
    private void validateRequest(OrderRequest request) {
        if (request == null || request.getItems().isEmpty()) {
            throw new IllegalArgumentException("Invalid order request payload");
        }
    }

    private boolean reserveInventoryWithRetry(OrderRequest request) {
        for (int i = 0; i < MAX_RETRY_ATTEMPTS; i++) {
            if (inventoryRepository.tryReserve(request.getItems())) {
                return true;
            }
        }
        return false;
    }

    // 7. Nested types
    private static final class RetryBudget {
        private final int attemptsRemaining;

        private RetryBudget(int attemptsRemaining) {
            this.attemptsRemaining = attemptsRemaining;
        }
    }
}
```
