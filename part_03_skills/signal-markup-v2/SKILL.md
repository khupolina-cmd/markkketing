---
name: signal-markup-v2
description: Use when raw marketplace reviews or marketplace questions for one product need fast semantic signal markup with a readable markdown result. Make sure to use this whenever the user provides one array of reviews or one array of questions plus product context and wants normalized rows, inline colored signal evidence, stats, and a lightweight time-aware reading of the material.
---

# Signal Markup V2

`signal-markup-v2` is a fast first-pass markup skill.

Its job is not to invent strategy.

Its job is to:

- accept one clean input type;
- read product context once;
- route to the correct runtime guide;
- classify signal fragments in one pass;
- return one complete readable markdown artifact.

## What Input This Skill Expects

The user should provide:

1. exactly one array type:
   - reviews
   - or questions
2. product context:
   - full product name
   - product type
   - seller description / promises / claims
   - optional size, volume, ingredients, attributes, or other card details
3. source material:
   - pasted raw array
   - or PDF export of reviews/questions
4. optional time filter:
   - for example `use only the last year`

There are only two valid runtime modes:

- `reviews`
- `questions`

Do not expect mixed input inside one run.

PDF input is allowed.

If the source is a review PDF, first normalize it with:

- [scripts/wb_pdf_review_parser.py](scripts/wb_pdf_review_parser.py)

then do markup.

Do not invent a new parser when this script already fits the source.

## First Decision: Route The Input

Before reading any reference file, determine what the user gave you.

### If the input is reviews

Read only:

- [references/core-semantic-principles.md](references/core-semantic-principles.md)
- [references/review-signal-markup-guide.md](references/review-signal-markup-guide.md)

Do not read the question guide.

### If the input is questions

Read only:

- [references/core-semantic-principles.md](references/core-semantic-principles.md)
- [references/question-signal-markup-guide.md](references/question-signal-markup-guide.md)

Do not read the review guide.

### If the input is anything else

Stop and ask for one clean input type.

Do not improvise mixed processing.

## Execution Discipline

This skill should be cheap and fast.

Do not create a long setup ritual.

Do not explore the workspace unless the user explicitly says the source lives in a file and has not pasted the actual array.

If the raw array is already present in the user message, treat that message as the source of truth.

Do not search for old dashboards, old overlays, old drafts, or related notes.

Do not inspect neighboring files "for context".

Do not reread the corpus category by category.

Do not build a registry-first draft.

Do not create extra helper documents unless the user explicitly asks for them.

Do not add extra passes unless correctness would otherwise break.

Do not design a one-off parser or mini-pipeline in the middle of the run.

Do not switch from the skill contract to ad hoc extraction logic just because the source is messy.

Do not write a second implementation of the skill inside the run.

Forbidden examples:

- a giant Python classifier for one current file;
- a big `exact = {...}` map with manual row-by-row overrides for dozens of ids;
- post-hoc patching of the markdown artifact by replacing lines one by one;
- writing an intermediate technical format and then spending most of the run maintaining that side artifact.

Use this rhythm:

1. read the product context once;
2. if the source is a review PDF, run the bundled parser script;
3. normalize the input units;
4. scan each unit once;
5. classify fragments during that same read;
6. build the output from the completed rows.

If classification cannot be done within this rhythm, the correct fallback is:

- keep the same artifact;
- leave a narrow `manual` bucket;
- do not build a second custom processing engine.

## No-Wandering Rule

When the user already pasted:

- product card context;
- raw review array;
- or raw question array,

you already have enough material to start.

In that case:

- do not search the filesystem for alternative sources;
- do not compare with earlier local outputs;
- do not look for previous runs;
- do not spend time checking whether a cleaner source exists.

Start the markup flow immediately.

If the source is difficult, reduce ambiguity with the existing normalization rules.

Do not replace the skill with a bespoke script-first workflow.

## Semantic Rule

Classification is semantic, not keyword-based.

Do not search for exact words only.

Determine what the fragment means inside buyer logic:

- happened result;
- expected result;
- open risk;
- explicit comparison;
- usage context.

## Evidence Rule

Evidence must stay literal.

Do not paraphrase the source fragment in the primary markup.

## Product Context Precedence

The product context given by the user is the source of truth.

If:

- the pasted card description says one product;
- and the file name suggests another product,

trust the user-provided product context first.

Do not silently switch the task to the file-name product.

If:

- the PDF file name contains another brand, SKU, or product wording;
- but the user already gave the product context in the message,

the file name is only a locator for the source file.

It is not allowed to replace:

- the product name in the heading;
- the product identity in the artifact;
- the seller claims context;
- the product type;
- the interpretation frame.

## Output Rule

The output must stay readable by a human first.

For review inputs, the main artifact is the overlay table.

For question inputs, use the lighter question-oriented output defined in the question guide.

The format must stay stable across runs.

Do not invent a new presentation shape for convenience.

Do not switch to a compact summary if the contract asks for a full row-by-row artifact.

Do not replace the artifact with a short report.

Do not output a selective excerpt, representative sample, or reviewer-style commentary instead of the artifact.

Do not prepend a prose “first-pass findings” report before the required artifact.

If some fields are unavailable after normalization:

- keep the same artifact shape;
- mark only those fields as unavailable;
- do not change the output format.

## Exact File Routing

For this skill, the file map is closed.

Allowed read paths:

- `SKILL.md`
- `references/core-semantic-principles.md`
- `references/review-signal-markup-guide.md`
- `references/question-signal-markup-guide.md`

Do not look for:

- prompts;
- legacy skill files;
- old category files;
- archived contracts;
- neighboring markdown notes.

## Usage Reminder

If the user asks for markup:

- take the array they gave;
- keep the original review or question text visible;
- add signal markup in a separate `signals` column;
- keep the result human-readable;
- return the final artifact directly.

## What Is Forbidden In The Final Output

Do not:

- replace the full overlay with a sample or showcase slice;
- say that the full dump can be generated later;
- compress the table just because it is long;
- append strategic advice, next-step ideas, or card recommendations;
- append buyer-facing recommendations unless the user explicitly asks for a second task;
- silently skip file creation when the task implies a markdown artifact.
- output a different product identity than the one the user provided in product context.
- emit a custom exploratory report because the source is a PDF.
- replace the skill runtime with ad hoc shell parsing logic that changes the contract.
