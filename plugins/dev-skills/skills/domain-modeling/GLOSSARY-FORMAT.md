# Glossary Format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.

## Single vs multi-context repos

**Single context (most repos):** `docs/dev-skills/glossary.md` holds the terms.

**Area pages or multiple contexts:** `docs/dev-skills/glossary.md` is the map. It lists the pages (Areas) or contexts, where they live, and how they relate to each other:

```md
# Glossary Map

## Contexts

- [Ordering](./glossary/ordering.md): receives and tracks customer orders
- [Billing](./glossary/billing.md): generates invoices and processes payments
- [Fulfillment](./glossary/fulfillment.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

(In a multi-context repo the links point at `../../src/<context>/GLOSSARY.md` instead.)

The skill infers which structure applies:

- If `docs/dev-skills/glossary.md` is a map (it lists pages, not terms), read it. If it points into `src/`, the repo is multi-context; if it points at `docs/dev-skills/glossary/`, it lists Area pages of one glossary
- If it holds terms, single context
- If it does not exist, create it lazily when the first term is resolved

When there are several pages, infer which one the current topic relates to. If unclear, ask which Area (or, in a multi-context repo, which context).
