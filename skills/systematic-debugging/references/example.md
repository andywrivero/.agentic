# Worked examples

Both use the JavaStyle sample (`com.example.style`) with JUnit 5. All output is real, from code compiled with `--release 8` and run on JDK 25.

## A. A set loses orders

**Symptom:** "When I collect new orders in a `HashSet`, only one is kept."

**Reproduce:**

```java
@Test
void setKeepsTwoNewOrders() {
    Set<Order> orders = new HashSet<>();
    orders.add(Order.builder("Ada").build());
    orders.add(Order.builder("Grace").build());

    assertEquals(2, orders.size());
}
```

This gives `expected: <2> but was: <1>`. The failure reproduces.

**Isolate:**

| # | Hypothesis | Probe | Result |
|---|---|---|---|
| 1 | The two orders are equal under `equals`/`hashCode` | `// DEBUG` print of ids, hashes, and `equals` | `ids=-1,-1 hashes=31,31 equals=true`. Confirmed |

**Root cause:**
1. `Order` does not override `equals`, so it inherits `BaseEntity.equals`, which compares only `id`.
2. Every unsaved entity has `id = UNSAVED_ID` (`-1L`).
3. So any two unsaved entities are equal and share a hash code.
4. So `HashSet` keeps only the first one.

**Before fixing:** the obvious fix is to compare object identity while `id` is unsaved. But that alone leaves a second failure, because `hashCode` uses `id`, which changes when the order is saved. A probe confirms it:

```java
orders.add(order);
order.setId(5L);
assertTrue(orders.contains(order)); // expected: <true> but was: <false>
```

Equality for entities without an id is a design choice, so list the options and ask:
- Identity until saved, with a hash code that does not change, such as one per class.
- Equality by business key.
- No `equals` override at all.

Then hand the fix to `tdd-loop`, with `setKeepsTwoNewOrders` as the first red test. Remove the `// DEBUG` print.

## B. Where it crashed is not where it broke

**Symptom:** `Order.total()` throws.

```
java.lang.NullPointerException: Cannot invoke "java.math.BigDecimal.multiply(java.math.BigDecimal)" because "this.unitPrice" is null
    com.example.style.model.Order$Item.total(Order.java:116)
    com.example.style.model.Order.total(Order.java:62)
    com.example.style.model.OrderSetReproTest.totalOfItemWithoutPrice(OrderSetReproTest.java:31)
```

**Read the trace:** the first frame in project code is `Order$Item.total`, line 116. The detailed message names the null field because the code ran on JDK 25. On a Java 8 runtime the message would be empty, and line 116 is all you would have.

**Trace the bad value back:** `unitPrice` is assigned only in the `Order.Item` constructor, which does not check for null. The bad state was created when the item was built, not when the total was calculated.

**Conclusion:** adding `if (unitPrice == null)` inside `total()` would only hide the symptom. Whether `Item` should reject a null `unitPrice` (and `sku`) is a contract question. Ask, then fix it in the constructor through `tdd-loop`.
