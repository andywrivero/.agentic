# Worked example

The project is the JavaStyle sample (`com.example.style`) with JUnit 5 and no mocking library. The request is: "Backfill tests for `Order` and `OrderService`." All results below are real output from running these tests.

## Gaps and cases

| Behavior | Cases chosen |
|---|---|
| `Order.addItem` | boundary: item `MAX_ITEMS` accepted, item `MAX_ITEMS + 1` rejected with `"Too many items"`; null rejected with `NullPointerException("item")` |
| `Order.Item` constructor | boundary: quantity `0` rejected |
| `Order.getItems` | returned data: the list cannot be modified |
| `Order.total` | empty: zero for an order with no items |
| `BaseEntity.equals` | equality: two unsaved orders |
| `OrderService.changeStatus` | errors: unknown id (`"Unknown order: 7"`), closed order, and a save failure rethrown as the same instance |

Not covered:
- `Order.Item` accepts a null `sku` and `unitPrice`, and `changeStatus` accepts a null `newStatus`. The contract is silent on all three, so they are reported as questions rather than tested.
- `createdAt` comes from `Instant.now()`, which has no seam, so it is reported and not asserted.

## External dependency

`OrderRepository` is a constructor-injected interface and the project has no mocking library, so the tests use a small fake:

```java
private static final class FakeRepository implements OrderRepository {
    private final Map<Long, Order> orders = new HashMap<>();
    private OrderException saveFailure;

    void failOnSave(OrderException failure) {
        this.saveFailure = failure;
    }

    @Override
    public void save(Order order) throws OrderException {
        if (saveFailure != null) {
            throw saveFailure;
        }

        orders.put(order.getId(), order);
    }

    // findById and findByStatus read from orders
}
```

```java
@Test
void changeStatusRethrowsASaveFailure() {
    repository.add(1L, Status.PENDING);
    OrderException failure = new OrderException("disk full");
    repository.failOnSave(failure);

    OrderException e = assertThrows(OrderException.class,
            () -> service.changeStatus(1L, Status.PAID));

    assertSame(failure, e);
}
```

## Boundary test

```java
@Test
void addItemRejectsOneItemOverTheLimit() {
    Order order = orderWithItems(Order.MAX_ITEMS);

    IllegalStateException e = assertThrows(IllegalStateException.class,
            () -> order.addItem(item()));

    assertEquals("Too many items", e.getMessage());
}
```

## Results

- 9 of 10 tests pass.
- **Bug found (`on-bug: report`):** `twoUnsavedOrdersAreNotEqual` fails with `expected: not equal but was: <Order[Grace, 0 items, PENDING]>`. `BaseEntity.equals` compares only `id`, and every unsaved entity has `UNSAVED_ID`, so any two new orders are equal and share a hash code. A `HashSet` of new orders would keep only one. The test is left out and the bug is reported, with an offer to fix it through `tdd-loop`.
- **Mutation check:**

  | Mutation | Test that failed |
  |---|---|
  | `items.size() >= MAX_ITEMS` changed to `>` | `addItemRejectsOneItemOverTheLimit` |
  | `quantity <= 0` changed to `< 0` | `itemRejectsZeroQuantity` |

  Both mutations were reverted, and the production code matched the original afterwards.
