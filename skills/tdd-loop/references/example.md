# Worked example

The project is the JavaStyle sample (`com.example.style`) with JUnit 5. The request is: "Let callers remove a line item from an order; closed orders cannot change."

The failure messages below are real JUnit 5 output from running these exact steps. Test names are placeholders; follow the project's existing test naming.

Test list:
1. Removing a SKU drops its line and keeps the others.
2. Removing from a closed order throws `IllegalStateException`.

## Cycle 1

**Red.** Write the test, then a stub so it compiles.

```java
class OrderTest {
    @Test
    void removeItemDropsTheMatchingLine() {
        Order order = Order.builder("Ada").build();
        order.addItem(new Order.Item("A-1", 1, BigDecimal.ONE));
        order.addItem(new Order.Item("B-2", 2, BigDecimal.TEN));

        order.removeItem("A-1");

        assertEquals(1, order.getItems().size());
        assertEquals("B-2", order.getItems().get(0).getSku());
    }
}
```

```java
public void removeItem(String sku) {
}
```

`mvn -q test -Dtest='OrderTest#removeItemDropsTheMatchingLine'` gives `expected: <1> but was: <2>`. It fails on the assertion, for the expected reason.

**Green.** Write the minimum code. There is no closed-order check yet, because no test asks for one.

```java
public void removeItem(String sku) {
    items.removeIf(item -> item.getSku().equals(sku));
}
```

`OrderTest`: 1 passed. **Refactor:** nothing worth changing.

## Cycle 2

**Red.**

```java
@Test
void removeItemRejectsAClosedOrder() {
    Order order = Order.builder("Ada").build();
    order.setStatus(Status.DELIVERED);

    assertThrows(IllegalStateException.class, () -> order.removeItem("A-1"));
}
```

This gives `Expected java.lang.IllegalStateException to be thrown, but nothing was thrown.`

**Green.** Copy the guard `addItem` already uses.

```java
public void removeItem(String sku) {
    if (status.isTerminal()) {
        throw new IllegalStateException("Order is closed: " + status.getLabel());
    }

    items.removeIf(item -> item.getSku().equals(sku));
}
```

`OrderTest`: 2 passed.

**Refactor.** `addItem` and `removeItem` now share an identical guard. Move it to a private method, then run again. `java-member-ordering` puts private methods after the non-private ones, so `checkOpen` goes after `describe()`.

```java
public void removeItem(String sku) {
    checkOpen();
    items.removeIf(item -> item.getSku().equals(sku));
}
```

```java
private void checkOpen() {
    if (status.isTerminal()) {
        throw new IllegalStateException("Order is closed: " + status.getLabel());
    }
}
```

`OrderTest`: 2 passed. The list is empty, so run the full suite and report.
