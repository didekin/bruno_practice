---
name: gap-analysis-skill
description: Analyze one or more PGVP Jira user stories against the OS+ endpoints selected during stage-one analysis, then rewrite each initial local ticket using the gap-analysis results. Use the existing stage-one reports, OS+ source specifications, and reusable JSON/YAML contracts to produce concise field-level gap analyses with realistic request and response examples.
---

# Gap Analysis Skill

## Purpose and input

Produce a field-level OS+ gap analysis for one or more PGVP Jira stories using their stage-one reports and selected endpoint specifications.

Input: one or more PGVP issue keys, for example `PGVP-2843` or `PGVP-2843, PGVP-3095`.

When multiple issue keys are provided, analyze each story independently. Keep its Jira requirements, selected DABA tickets, specifications, mappings, gaps, examples, gap-analysis report, and revised local ticket separate; do not pool evidence or selections across stories.

## Project paths

- Stage-one reports: `/Users/p.nevado/PycharmProjects/boa_project/gap_stage_one`
- OS+ specifications and extracted contracts: `/Users/p.nevado/PycharmProjects/boa_project/specifications/osplus`
- Gap-analysis reports: `/Users/p.nevado/PycharmProjects/boa_project/gap_analysis`

### Stage-one reports

The expected input filename is `PGVP_<number>.md`, for example `PGVP_2843.md`. The report identifies the required OS+ data and endpoints, selected DABA tickets, relevant specification filenames, and stage-one gaps or uncertainties.

Do not rely solely on the `bapi-skill` result to determine whether a local specification exists. Recheck the OS+ specifications directory because the specification may have been downloaded after stage one.

### OS+ specifications

The OS+ specifications directory contains source specifications and any extracted JSON/YAML endpoint contracts. Reuse an existing suitable contract when available.

A local specification matches the specification identified in the stage-one report when its numeric version matches exactly and its meaningful filename component is contained in the downloadable specification filename, after ignoring file extensions, version notation, separators, and capitalization. Generic components such as `OSPlus`, `API`, `specification`, or `service` are not sufficient by themselves. If no matching specification is available, report the discrepancy and stop the analysis.

### Existing gap-analysis reports

`/Users/p.nevado/PycharmProjects/boa_project/gap_analysis`
Existing reports in this directory, including reports such as:
`PGVP_2741_gap_analysis.md`
and:
`PGVP_2781_gap_analysis.md`
are examples of the expected type of analysis.
Use them as guidance for:
- terminology;
- level of technical detail;
- field-level mapping;
- gap classifications;
- treatment of business rules and contract mismatches.
The new reports should normally be more compact and avoid repeating the same information in multiple sections.

## Source precedence

For ticket requirements, use both the stage-one report and the live Jira story. Preserve the stage-one DABA selection, but restore any explicit Jira requirement omitted from the report and report conflicts between the two sources.

For endpoint behavior, use sources in this order:

1. OS+ source specification.
2. Faithfully extracted JSON/YAML contract.
3. DABA Jira information.

Follow the higher-precedence source and report conflicts. Distinguish sourced facts from inference.

## Workflow

### 1. Load the stage-one report

For each issue key, open its `PGVP_<number>.md` report from the stage-one reports directory. If a report is missing, stop the analysis for that story and report the missing input; do not use another story's report as a substitute.

Read its requirements, selected endpoints and DABA tickets, specification filenames, gaps, and uncertainties. Retrieve the live Jira story and verify that every explicit input, output, mapping, validation rule, and response rule is represented. Add omitted requirements to the analysis and report conflicts. Preserve all DABA tickets selected in the stage-one report; do not add or replace tickets, and do not reject the report solely because it contains more than two.

If no DABA ticket was selected, create a brief report confirming that no OS+ endpoint analysis is required. Include any unresolved OS+-related dependency identified by stage one, then stop.

### Multiple-story execution

When more than one issue key is provided, repeat steps 1–8 independently for each story. A missing report, missing specification, or other blocking condition for one story must not cause evidence from another story to be reused or combined with it.

### 2. Read the endpoint specifications

For each selected endpoint, read only the contract details relevant to the ticket: method and path, request and response fields, types, requiredness, enumerations, validation and selection rules, business semantics, and relevant HTTP responses.

### 3. Obtain a machine-readable contract

Reuse a suitable JSON/YAML contract when available. Otherwise, extract an embedded JSON, YAML, OpenAPI, Swagger, or equivalent machine-readable definition from the source specification and save it with a filename clearly related to the source and endpoint.

Do not synthesize a contract from prose, tables, examples, or inference; add undocumented content; or overwrite an existing contract without approval.

### 4. Extract the requirements

From the verified stage-one and Jira requirements, identify required inputs, outputs, business behavior, validation, selection rules, and response behavior. Distinguish explicit requirements from inferred requirements; do not invent requirements.

Distinguish a new endpoint call from reuse of a result produced by an earlier workflow step. For reused results, assess the response data and any required cross-step identifier, but do not treat the endpoint's request parameters as requirements of the current story.

### 5. Map requirements and assess gaps

Map each requirement to its endpoint and relevant field, rule, behavior, or derivation. When multiple endpoints are involved, keep the source endpoint explicit.

Classify each requirement as:

- **Supported** — directly satisfied by the contract.
- **Supported with adaptation** — sufficient contract support exists, but transformation, selection, conversion, or derivation is required.
- **Partial** — only part of the requirement is supported; the remainder is unresolved.
- **Gap** — a required element is missing or conflicts with the ticket.
- **Uncertain** — the available evidence is insufficient or ambiguous.

Use only these classifications and explain the specific issue in the assessment. Ignore irrelevant optional elements. If an element absent from the ticket affects implementation, classify it as **Gap** or **Uncertain** and explain why. Compare semantics, not only names.

### 6. Identify unresolved issues

List only **Partial**, **Gap**, or **Uncertain** findings that require implementation work or clarification. Do not repeat explanations already present in the mapping table.

### 7. Generate examples

When the specification provides enough detail, create one realistic request and successful response per newly invoked endpoint. Use fictional values and respect documented structures, types, enumerations, required fields, and ticket-relevant optional fields.

For operations without a request or response body, show the applicable parameters, status, or headers instead of inventing a body. Add an error example only when it clarifies a material gap. Otherwise, omit examples and report the limitation.

For a reused result, do not generate a request example. Show a response example only when it helps clarify the reused data or a material gap, and omit the **Request** subsection.

### 8. Create the revised local ticket

After completing the gap analysis, create the revised local version of the initial ticket using the analysis results. Jira is read-only for this workflow; do not modify the Jira issue.

- Check whether `/Users/p.nevado/PycharmProjects/boa_project/apollo_tickets/pgvp-<number>.md` already exists:
  - If the local ticket exists, use it as the initial ticket and rewrite it in place.
  - If the local ticket does not exist, retrieve the Jira story through the connected Jira, use its content as the initial ticket, and create `/Users/p.nevado/PycharmProjects/boa_project/apollo_tickets/pgvp-<number>.md` with the revised version.
- In either case, the local file is the final deliverable and must contain the complete revised ticket, not only a patch or commentary.

- Preserve the ticket’s business intent and existing useful structure.
- Incorporate supported endpoint mappings, request parameters, response fields, transformations, defaults, and behaviors established by the gap analysis.
- Remove or rephrase unsupported claims, procedural acceptance criteria, and mappings contradicted by the selected specification.
- Resolve a gap when the specification supports a precise rule or adaptation; otherwise retain it as an explicit, concise open point in the ticket rather than inventing a solution.
- Keep application behavior, such as field editability and screen presentation, separate from OS+ contract requirements.
- Use the ticket’s detailed data and technical-context sections to define the requirements; make acceptance criteria observable and refer to those sections instead of repeating field lists.
- Re-read the rewritten ticket against **Gaps requiring clarification** and the mapping table. Every material **Partial**, **Gap**, or **Uncertain** finding must be resolved, removed from scope, or explicitly represented in the rewritten ticket.
- Verify that the rewritten ticket does not introduce fields, endpoint behavior, or business rules absent from the evidence.
- Normalize Jira markup when creating or rewriting the local Markdown file. Jira headings and list-like lines must be converted to valid Markdown structure; do not copy Jira `#` prefixes mechanically when they represent acceptance-criterion items.
- Keep acceptance criteria as an ordered Markdown list (`1.`, `2.`, `3.`, ...) or, where numbering is not needed, as bullet-list items. Never format an individual acceptance criterion as a heading such as `# When ...` or `### When ...`.
- Preserve the wording and order of source acceptance criteria when the task is to copy the Jira story; normalization may change only markup needed for valid Markdown rendering.

## Report format

Use this structure:

```markdown
# PGVP-<number> — OS+ Gap Analysis

## Scope

## Ticket requirements

## Endpoint contract

### <Endpoint name>

## Mapping and gap assessment

## Gaps requiring clarification

## Example requests and responses

### <Endpoint name>

#### Request

#### Successful response
```

Prefer lists and compact tables over dense paragraphs. When a section contains three or more requirements, fields, endpoints, mappings, rules, or uncertainties, present them as a nested list or table with one item per line.

### Markdown and acceptance-criteria integrity

The local ticket must be valid, readable Markdown rather than a mechanical copy of Jira wiki markup.

- Use one document title (`# ...`) and use `##`/`###` for sections and subsections.
- Use list syntax for collections of requirements and acceptance criteria. A criterion beginning with `When`, `If`, `After`, or similar is still a list item, not a heading.
- Keep exactly one acceptance-criteria section heading, normally `## Acceptance criteria`.
- Put a blank line before and after tables, lists, and fenced code blocks where required for unambiguous Markdown rendering.
- Before saving the ticket, inspect the rendered structure or perform a text check. In particular, confirm that no acceptance-criterion line begins with one or more Markdown heading markers (`#`) and that the criteria are numbered or bulleted.
- If the source uses Jira wiki headings for criteria, convert them to ordered-list items while retaining the criterion text and sequence.

Present collections of three or more fields as a nested list or table. Show each literal field name and its English meaning on a separate line.

In **Scope**, briefly identify the PGVP ticket, selected DABA tickets and endpoints, source specifications, and machine-readable contracts used. Label the contract column **Contract (JSON/YAML)**.

In **Ticket requirements**, summarize the required data and behavior without reproducing the Jira story.

In **Endpoint contract**, create one subsection per endpoint, show `<HTTP method> <endpoint path>`, and include only ticket-relevant contract details.

In **Mapping and gap assessment**, use this compact table:

| Ticket requirement | Endpoint | OS+ field / contract element | Assessment |
|---|---|---|---|
| <requirement> | `<endpoint>` | `<field/path>` | **Supported.** <short explanation> |

In **Gaps requiring clarification**, list unresolved decisions, mappings, code lists, business rules, ticket questions, or contract questions. If none exist, state `No material gaps identified.`

Include an **Example requests and responses** subsection only for each endpoint whose specification supports reliable examples. Use fenced `json` or `yaml` blocks as appropriate.

For reused results, follow the reduced example structure defined above instead of the full request-and-response hierarchy.

Do not add a conclusion or duplicate assessments across sections.

When no DABA ticket was selected, use only this reduced structure:

```markdown
# PGVP-<number> — OS+ Gap Analysis

## Scope

No DABA ticket or OS+ endpoint was selected during stage one.

## Assessment

<Brief explanation of why no OS+ analysis is required.>

## Gaps requiring clarification

<Only unresolved OS+-related dependencies, or `No material gaps identified.`>
```

## Language and terminology

On first occurrence, give every German business term and technical field identifier a concise English meaning when it can be established. Apply this even when the identifier appears self-explanatory or forms part of a parameter list. For three or more identifiers, use a list or table with one identifier and its meaning per line. Translate each identifier only once.

Do not alter literal identifiers or repeatedly explain them. Preserve exact Jira and DABA keys, endpoint identifiers and paths, field and property names, filenames, code values, and other technical identifiers. If a meaning cannot be established confidently, state that it is uncertain rather than guessing.

## Output

For each input story, save one complete report as `/Users/p.nevado/PycharmProjects/boa_project/gap_analysis/PGVP_<number>_gap_analysis.md`, replacing the issue-key hyphen with an underscore. Create the output directory if needed, do not combine multiple stories into one report, and do not overwrite an existing report without approval.

For each input story, also save one complete revised ticket as `/Users/p.nevado/PycharmProjects/boa_project/apollo_tickets/pgvp-<number>.md`, rewriting the existing local ticket or creating the file from the Jira story as specified in step 8. Do not modify Jira.

## Integrity rule

Do not fabricate requirements, fields, mappings, rules, contracts, endpoint behavior, or specification content. When evidence is insufficient, classify the requirement as **Uncertain** and state what is missing.
