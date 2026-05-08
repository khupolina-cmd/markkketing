---
name: signal-category-analysis
description: Use when the user already has one or more signal registries and wants analytics for one chosen category such as positive, negative, expectations, doubts, comparisons, or scenarios. Make sure to use this whenever the user brings `units_registry` plus `signals_registry`, asks to analyze only one signal category, wants clustering or theme counts across one or many products, or needs full quote context restored through `unit_index` rather than extracting signals again.
---

# Signal Category Analysis

`signal-category-analysis` is a second-layer analytics skill.

Its job is not to re-markup raw reviews.

Its job is to take already prepared registry packages, isolate one requested category, group that category into themes, count it, and restore full quote context without breaking the link back to the source unit.

## Use This Skill Only In The Right Stage

Use this skill when the user already has structured registry packages and wants analysis for one chosen category:

- positive
- negative
- expectations
- doubts
- comparisons
- scenarios

This skill is a good fit when the user wants:

- analysis for one category only, not a fresh full markup pass;
- cross-product category comparison;
- theme clustering inside one category;
- counts and frequency view for a category;
- quote restoration through `product_key` and `unit_index`.

Do not use this skill when the user only has:

- raw reviews;
- raw marketplace questions;
- screenshots;
- a product card without registries.

If the user needs first-pass extraction from raw reviews or questions, route to `signal-markup-v2` instead of improvising the missing registry layer.

## What Input This Skill Expects

The user should provide:

1. one category;
2. one or more registry packages.

Each registry package should contain:

- `product_key`
- `units_registry`
- `signals_registry`
- `stats`

If any of these are missing, stop and say exactly what is absent.

Do not silently substitute another file or infer a missing registry from a nearby folder.

## First Decision: Validate The Task Shape

Before reading deeper references, decide which of these cases you are in.

### Case 1: Correct input

The user gave:

- one category;
- one or more registry packages.

Proceed with the category analysis flow.

### Case 2: Raw-source request disguised as category analysis

The user asks for category analytics, but the actual material is still raw reviews, raw questions, or a PDF dump with no registries.

Do not fake the registry layer inside this skill.

State that this skill expects prepared registries and that the correct upstream step is first-pass markup.

### Case 3: Mixed request across many categories

If the user asks for "analyze everything", "give the full picture", or several categories at once, do not pretend that is the same task.

This skill is designed for one category at a time because that keeps clustering logic, counts, and quote recovery coherent.

If useful, suggest running the same flow separately per category instead of collapsing all categories into one blended report.

## Execution Discipline

This skill should stay narrow, cheap, and registry-bound.

Do not:

- search for new signals in raw text;
- reclassify fragments into new categories;
- merge all products into one unlabeled pile;
- restore quotes from memory or paraphrase;
- search the workspace for alternative data if the user already supplied the registries;
- invent a custom mini-pipeline outside the skill contract.

Preferred rhythm:

1. validate the category and package structure;
2. unify the registries without losing product boundaries;
3. filter only the requested category;
4. cluster filtered signals into themes;
5. count frequencies;
6. restore full quotes from `units_registry`;
7. produce one readable report.

If the user pasted the registries directly in the conversation, treat that as the source of truth and begin.

Do not wander through neighboring files "for context".

## Non-Negotiable Rules

1. Never search for new signals in the original reviews.
2. Never change the assigned category of an existing signal.
3. Never lose the bridge from a signal back to its full quote.
4. Never blend multiple categories into one report when the user asked for one.
5. Never mix product identities when several registry packages are present.

## Category Handling

The category is already decided upstream.

Your responsibility is to analyze it faithfully, not reinterpret it.

When clustering:

- for comparisons, preserve the comparative relation instead of flattening it into a generic sentiment theme;
- for expectations and doubts, keep the phrasing close to the original buyer logic rather than rewriting it into abstract labels;
- for scenarios, preserve the use-case frame;
- for positive and negative signals, group by buyer-relevant meaning, not by surface keywords alone.

Semantic grouping matters more than exact word overlap.

## Multi-Product Rule

If there is more than one registry package:

- keep per-product counts;
- also produce a combined market view;
- explicitly show where products converge and diverge;
- preserve `product_key` on every quote-context row.

Do not collapse differences just to make the summary shorter.

## Quote Context Rule

Full quote restoration must come from `units_registry` through the identifiers already present in the registries.

Use:

- `product_key`
- `unit_index`

The quote context layer should let a human verify that the theme really comes from the cited unit.

Do not:

- reconstruct the full quote from memory;
- paraphrase the quote as if it were the original;
- drop the source reference when building the report.

## Output Rule

The output should be human-readable first, but it must still cover the full contract.

Always return these six components in one final artifact:

1. `filtered_signals`
2. `themes`
3. `counts`
4. `quote_context_block`
5. `category_report`
6. `TAGS`

## Report Structure

Use this structure unless the user explicitly asks for another stable format:

```markdown
# Category Analysis: <category>

## Scope
- category
- number of products
- product keys
- total filtered signals

## Filtered Signals
- concise registry-bound listing or table of the signals used in this run

## Themes
- grouped themes for the chosen category

## Counts
- `R_signal`
- `% B_total`
- `% B_clean`
- if relevant, per-product view plus overall view

## Quote Context
- `product_key`
- `unit_index`
- `signal_fragment`
- `full_quote`

## Category Report
- what this category means in buyer terms
- top themes
- strongest examples
- differences across products if there are several

## TAGS
- short reusable tags for later synthesis
```

Do not replace this with a short prose summary only.

Do not output only the counts and omit the quote layer.

Do not output only selected example quotes if the contract expects the category structure.

## File Routing

Read these files as needed:

### References

- [Input contract](references/input-contract.md)
- [Category rules](references/category-rules.md)
- [Output contract](references/output-contract.md)

### Prompt checkpoints

- [01 — Load registries](prompts/01-load-registries.md)
- [02 — Filter category](prompts/02-filter-category.md)
- [03 — Cluster and count](prompts/03-cluster-and-count.md)
- [04 — Quote context](prompts/04-quote-context.md)
- [05 — Final report](prompts/05-final-report.md)

Treat the prompt files as execution checkpoints, not as five separate user-facing outputs.

## Success Standard

The skill is working well when:

- it stays inside one category;
- it does not re-open raw extraction work;
- the final themes are semantically coherent;
- counts are explicit and interpretable;
- quote context is fully restorable;
- multi-product differences remain visible instead of being blurred away.
