# Supervisor relationship registry

`data/supervisor-map.json` is the sole canonical source for executor-to-supervisor relationships.

## Reconciliation decision (2026-09-28)

At baseline `5cac70cef1c33f8b393ef05d1aacd1ab8adcc701`, the generated operational map in `personas.json` and role prompts contained 32 relationships not displayed in the README table; the README also had one relationship absent from generated metadata. To avoid silently deleting currently effective relationships, this change preserves the existing generated-map relationships as the initial registry values and synchronizes the README projection to them. This is a data-preserving reconciliation; future relationship changes must be reviewed in this registry.

The registry has one explicit record for each executor (`roleId`, title, and a `supervisors` array; an empty array is explicit). No generated artifact is used as a fallback input. Every Supervisor must be a registered Supervisor role. The validator compares registry, README, generated prompt ownership fields, and `personas.json`.

## Update procedure

1. Change the registry only after reviewing the relationship.
2. Run `make prompts composites metadata skills` in that order. The prompt generator updates only the managed Prompt-link and Supervisor columns of the main README table.
3. Run `make validate`; any missing, stale, duplicate, or unknown relationship fails.

The role prompt content and Supervisor relationships have separate sources: other role fields remain in the README role data, while Supervisor relationships come only from the JSON registry.
