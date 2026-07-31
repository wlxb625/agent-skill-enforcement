# What ASEP is—and is not

## Is ASEP RAG?

No. RAG retrieves information. ASEP controls lifecycle progression and completion. An Enforced Skill may use RAG inside a stage.

## Is ASEP tool calling or MCP?

No. Tools provide actions and MCP exposes tools/resources. ASEP can require or restrict tool use, but its main abstraction is enforceable lifecycle state.

## Is ASEP a workflow engine?

No. ASEP is a portable declaration protocol. A host may implement it with a state machine, graph, hooks, scripts, or another engine.

## Does ASEP guarantee quality?

It can enforce deterministic requirements and prevent unverified completion. Semantic quality still depends on evaluator quality and attestation.

## Is policy layering the main feature?

No. Layering protects enforcement-critical rules from being weakened. The main feature is the ability to block progression and completion.
