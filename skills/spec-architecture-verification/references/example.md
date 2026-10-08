# Worked example

The project is the JavaStyle sample (`com.example.style`), and the request is: "Let callers cancel an order and record why."

## Architecture map

| Component | Owns | Depends on | Evidence |
|---|---|---|---|
| `model` | Aggregate `Order` (root) with nested `Order.Item`; enums `Status`, `Priority`; `BaseEntity`, `Identifiable` | nothing in the project | no `com.example` imports |
| `service` | Use cases (`OrderService`), the storage port (`OrderRepository`), the checked `OrderException` | `model` | imports `model.Order`, `model.Status` |
| `util` | Generic helpers (`Strings`, `Cache`, `@Audited`) | nothing in the project | no `com.example` imports |

The map shows these patterns:
- `Order` enforces its item invariants itself (`addItem` throws `IllegalStateException`) and exposes items read-only.
- `Order` instances come from `Order.builder(…)`; its constructor is private.
- The repository interface lives in `service`, as a port, not in `model`.
- Service operations load the order, check it, mutate it, save it, and throw `OrderException`. They log failures and rethrow.
- Status-transition rules (the terminal-state check) live in `OrderService.changeStatus`, not in `Order`. This is inconsistent with the item invariants; report it, do not fix it here.

## Design note

- **Acceptance criteria:**
  - (1) A non-terminal order moves to `CANCELLED`.
  - (2) Cancelling a terminal order fails with `OrderException`.
  - (3) The reason is stored.
  - Open question: is the reason required, and does it need persisting beyond the `Order` object?
- **Placement:** `OrderService.cancel(long orderId, String reason)` reuses the `changeStatus` path, so the terminal check stays in one place. The reason becomes a field on `Order`, the aggregate that owns it, set through an `Order` method rather than from outside.
- **Dependencies:** none new; `service → model` only.
- **Contracts:** `OrderService` gains a public method, which is additive. Adding a field to `Order` changes what `OrderRepository` implementations must store, so the persistence schema is affected. This trips the contract rule: stop and ask before adding it.
- **Patterns followed:** `changeStatus` for load, check, mutate, save; `Objects.requireNonNull(x, "name")` for argument checks.

## Plans that would trip a drift rule

- Throwing `OrderException` from `Order`: `model` would depend on `service` (direction).
- Logging inside `Order`: the domain model would take on a logging concern it does not have today (direction).
- Copying the terminal check into `cancel` instead of reusing it: the rule would be duplicated (domain).
- Adding a generic `StateMachine` abstraction for one transition: new machinery.
