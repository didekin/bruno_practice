---
name: bapi-skill
description: "Analyze one or more Jira user stories to identify required OS+ data, find and select the most suitable DABA Jira tickets for accessing that data, and identify the latest endpoint specification attached to each selected DABA ticket."
---

# BAPI Skill

## Purpose and input

Identify the OS+ data and operations required by each Jira user story, select the smallest suitable set of DABA tickets, identify their latest endpoint specifications, and assess requirement coverage.

Accept one or more Jira user-story keys, for example `BRLI-1234, BRLI-1250`. Analyze and report each story independently, including candidate selection, coverage, and its output file. Do not pool evidence or selections across stories.

## Project paths

- OS+ specifications: `/Users/p.nevado/PycharmProjects/boa_project/specifications/osplus`
- Stage-one reports: `/Users/p.nevado/PycharmProjects/boa_project/gap_stage_one`

## Source precedence

Use the user-story ticket as the source for business requirements. Use endpoint specifications as the primary source for endpoint data and behavior, and DABA ticket content when no corresponding specification is available. Report conflicts instead of resolving them silently.

## Workflow

### 1. Analyze the user story

Retrieve the story through Jira and identify the OS+ data and operations required to satisfy it, including data to retrieve, data to submit, and required endpoint behavior.

Distinguish explicit requirements from requirements inferred as necessary. Label inferred requirements and do not invent unsupported requirements.

When the story requires selecting a returned record for subsequent processing, identify the stable identifier needed to carry that selection forward. Treat the identifier as an inferred requirement when the story does not name it. If the specification offers several plausible identifiers or the required one cannot be determined, classify the requirement as **Uncertain**.

Record every explicit field, value mapping, validation rule, response rule, and behavioral condition for the analysis. Do not omit a requirement from the assessment because it is unsupported, ambiguous, or outside the endpoint contract.

Distinguish a new endpoint call from reuse of a result produced by an earlier workflow step. For reused results, assess the required response data but do not treat the endpoint's request parameters as requirements of the current story unless it performs a new call.

### 2. Group the requirements

Group requirements by OS+ endpoint or logical data source. Keep unresolved requirements as separate data needs until candidate evaluation provides enough evidence to group them.

### 3. Find candidate DABA tickets

For each endpoint or data group, search both Jira and the complete local OS+ specification inventory. Use business operations, endpoint names, methods, paths, relevant field names, German and English aliases, and linked DABA tickets. Do not limit the local search to specifications associated with Jira candidates already found. When a local specification appears relevant, identify and evaluate its corresponding DABA ticket in Jira. Treat DABA tickets named in the user story as strong candidates, not automatic selections. If a search is unsuccessful, broaden it using fewer or alternative terms.

Evaluate candidates by the data and behavior they provide, not merely by similar terminology. Assess the named ticket and the strongest materially relevant alternatives before selection. A candidate may satisfy one or several requirements. Keep candidates for each endpoint or data group separate until selection.

Prioritize alternatives that provide the same business capability or a plausible part of it. Treat defect, release, authorization, and access-enablement tickets as supporting evidence rather than alternative endpoints unless they define or provide the required capability themselves.

### 4. Check local OS+ specifications

Check the local specifications found during candidate discovery and look for corresponding specifications for every Jira candidate. Use each matching specification to verify the endpoint's fields, inputs, outputs, and behavior against the story requirements.

Identify mandatory technical or control parameters even when the story does not mention them. If their required values cannot be derived from the story or specification, report the unresolved parameters and classify endpoint coverage as **Uncertain**.

A local specification corresponds to a DABA attachment when its numeric version matches exactly and its meaningful filename component is contained in the attachment filename, after ignoring file extensions, version notation, separators, and capitalization. Generic components such as `OSPlus`, `API`, `specification`, or `service` are not sufficient by themselves.

If no match exists, continue using Jira evidence and report that no corresponding local specification was found. Distinguish conclusions supported by a specification from those based only on Jira.

### 5. Select the DABA tickets

Select the smallest set that best covers the complete user story:

- Select one ticket whenever it adequately covers the requirements; this should be the most frequent result.
- Prefer no more than two tickets. Exceed two only when the story explicitly requires additional independent OS+ operations.
- Select a complementary ticket for a missing field only when Jira or a matching specification explicitly confirms that it provides the field.
- Select no ticket when no candidate is supported by sufficient evidence; report the affected requirements as **Not covered** or **Uncertain**.
- Reuse one ticket when it satisfies several endpoint or data requirements.

For each selected ticket, record the endpoint or data need, covered requirements, selection rationale, and whether the evidence comes from Jira, a local specification, or both.

### 6. Identify the latest endpoint specification

For each selected DABA ticket, inspect its specification attachments and select the attachment with the highest numeric version shown in its filename or Jira metadata. Return its exact filename, for example:

`DABA-983 → P49902456_Fachliche_Spezifikation_Steuerlaender_GET_v1.1.pdf`

Do not interpret an empty or incomplete attachment result as proof that no specification exists. Before reporting that a DABA ticket has no specification, retrieve the ticket directly with its complete attachment field. If the result is truncated or uncertain, retry with an attachment-only request. If the complete attachment list contains no specification, report that none was found; if completeness cannot be verified, report that the attachments could not be verified. If versions cannot be compared confidently, list the relevant filenames and explain the uncertainty. Do not invent filenames or versions.

When a corresponding local specification exists, compare it with the latest attachment. Report only its filename when it matches. Explain the comparison only when the match is missing, uncertain, or indicates a different version. Do not assume that a local copy is latest merely because it exists.

Include the specification download URL when a usable URL is available. If none is available, omit the URL and state that no usable download URL was available.

### 7. Assess coverage

Split compound requirements into independently assessable parts. Assess field availability separately from value transformation, validation, derivation, and application behavior. Classify a requirement as **Covered** only when every part represented by that row is supported by the selected DABA evidence.

Verify every explicitly required field against an exact specification field. A semantically related field does not provide coverage; for example, `geburtsname` does not cover `geburtsort`.

Do not report complete coverage while mandatory endpoint parameters or implementation-critical continuation data remain unresolved. Report them as coverage exceptions.

Classify every requirement as:

- **Covered** — a selected DABA ticket provides the required data or behavior.
- **Partially covered** — a selected ticket provides only part of the requirement.
- **Not covered** — no suitable selected ticket provides the requirement.
- **Uncertain** — the available evidence is insufficient or ambiguous.
- **Outside OS+ scope** — the user story requires it, but it is implemented by the consuming application rather than an OS+ endpoint.

### 8. Chain to gap analysis when local specifications are complete

After saving the stage-one report, verify that every OS+ specification identified there as required for the selected DABA tickets is available locally and matches the corresponding specification attachment.

If all required specifications are available locally, continue immediately by executing `gap-analysis-skill` for the same user-story key. The saved stage-one report is the input for the gap analysis.

If any required specification is missing, mismatched, or cannot be verified, stop after completing stage one and report the issue. Do not chain to gap analysis when no DABA ticket was selected.

## Report format

Create a separate report for each story using this structure:

```markdown
# <USER-STORY> — DABA Selection

## Required OS+ data and operations

## Required OS+ endpoints

## Candidate DABA tickets

## Selected DABA tickets

## Sources

## Latest specifications

## Coverage

## Gaps and uncertainties
```

Prefer lists and compact tables over dense paragraphs. When a requirement contains three or more fields, endpoints, tickets, attachments, mappings, or uncertainties, present them as a nested list or table with one item per line.

Present collections of three or more fields as a nested list or table. Show each literal field name and its English meaning on a separate line.

In **Required OS+ data and operations**, group requirements by endpoint or logical data source when possible. Do not add methodological labels such as `Explicit requirements` or state that no requirements were inferred. Report an inferred requirement only when one exists and identify that item as inferred. Omit application-only requirements unless they affect DABA selection or constitute a material coverage exception.

In **Required OS+ endpoints**, identify the data or operation expected from each endpoint. Describe unresolved data needs instead of inventing endpoint names.

In **Candidate DABA tickets**, include the selected candidate and any materially relevant alternatives that were rejected, with a concise rejection reason. Do not include weak search results merely to enlarge the candidate list.

In **Selected DABA tickets**, group selections by endpoint or data need and include the evidence recorded during selection.

In **Sources**, include the Jira user-story URL and each selected DABA-ticket URL.

In **Latest specifications**, use `DABA-<key> → <exact latest specification filename>`. Include a usable download URL when available. Otherwise, omit it and state that no usable download URL was available. Report the corresponding local filename without explaining a successful name or version match; include comparison details only for a missing, uncertain, or different match.

In **Coverage**, state once that all listed OS+ requirements are **Covered** except those reported below. Report only requirements classified as **Partially covered**, **Not covered**, **Uncertain**, or materially relevant **Outside OS+ scope** in a table titled **Coverage exceptions**. Do not repeat individually supported fields, requirements, or application-only behavior that does not affect DABA selection. If there are no exceptions, omit the table and state `All identified OS+ requirements are covered by the selected DABA ticket. No coverage exceptions were identified.`

In **Gaps and uncertainties**, list only unresolved findings that require clarification or prevent complete coverage. Do not repeat the complete coverage assessment or treat application behavior classified as **Outside OS+ scope** as an endpoint gap.

## Language and terminology

On first meaningful occurrence, preserve each German term or technical identifier and add an English translation or semantic explanation when its meaning can be established. This applies to German business terms, statuses, roles, actions, and field values copied from Jira, including literal values shown in backticks. Keep the exact German literal and place the English meaning in parentheses immediately after it, for example `Wartet - Termin` (waiting - appointment). Do not translate or replace the literal Jira value.

Do not alter literal identifiers or repeatedly explain them. Preserve exact Jira and DABA keys, endpoint identifiers and paths, field and property names, filenames, code values, and other technical identifiers. If a meaning cannot be established confidently, state that it is uncertain rather than guessing.

## Output

Save each report as `/Users/p.nevado/PycharmProjects/boa_project/gap_stage_one/<ISSUE_KEY_WITH_UNDERSCORE>.md`. Create the directory if needed and do not overwrite an existing report without approval.

## Integrity rule

Do not fabricate requirements, endpoint capabilities, mappings, attachment names, versions, or specification relationships. Distinguish Jira evidence, specification evidence, and inference; state what is missing when evidence is insufficient.
