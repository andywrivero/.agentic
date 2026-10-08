# Worked example: reviewing `OrderService.changeStatus`

The project is the JavaStyle sample. It uses `java.util.logging`. The `java.util.logging` output below is real, from JDK 25.

```java
try {
    repository.save(order);
} catch (OrderException e) {
    LOGGER.log(Level.WARNING, "Save failed for order {0}", orderId);
    throw e;
}
```

## Findings

1. **Logged and rethrown:** it handles the failure *and* propagates it. Whoever catches it upstream will probably log it again.
2. **No stack trace:** `e` is not passed to the logger, so the log line says "save failed" without saying why.
3. **Ids reformatted:** `{0}` with a `long` goes through `MessageFormat`:

   ```
   WARNING: Save failed for order 1,234,567
   ```

   A search for `1234567` will not find this line.
4. **The throwable cannot go in the parameters:** this call does not attach the stack trace either.

   ```java
   LOGGER.log(Level.WARNING, "Save failed for order {0}", new Object[] {orderId, e});
   ```

   It prints only `WARNING: Save failed for order 1,234,567`.

## Fix options

The rethrown exception (`"disk full"`) lacks the order id, so the context has to go somewhere:

- **A. Wrap, don't log** (preferred when the caller handles the failure). Use `throw new OrderException("Save failed for order " + orderId, e);` and remove the log line. This changes the exception instance callers receive. An existing test asserting `assertSame(failure, e)` would fail, so check callers and ask first.
- **B. Keep the instance and log properly** (when this is the handling boundary). Use `LOGGER.log(Level.WARNING, "Save failed for order " + orderId, e);` and do not rethrow. This changes the method's contract, so ask first.
- **C. Minimal fix:** keep the current behavior, but use `String.valueOf(orderId)` and pass `e` with `log(Level, String, Throwable)`. This still logs and rethrows, so report that as a finding.
