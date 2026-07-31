# What Contract Skills is—and is not

## Is it RAG?

No. RAG retrieves information. A Contract Skill defines obligations for how a task progresses and when it may be completed. A Contract Skill may use RAG inside a stage.

## Is it tool calling or MCP?

No. Tools provide actions and MCP provides a protocol for tools and resources. A Contract Skill can declare when tools are allowed or required, but its main abstraction is the execution contract.

## Is it a workflow engine?

Not by itself. The specification is a portable declaration format. A host may implement it using a state machine, graph workflow, hooks, scripts, or another engine. Contract Skills should not reinvent scheduling, queues, retries, or distributed orchestration.

## Is it just a longer prompt?

No. In L1 fallback it may behave like a structured prompt, but L2 and L3 modes move state, validation, policy protection, and completion outside model discretion.

## Does it guarantee high-quality output?

No. It can enforce process and evidence obligations. Semantic quality still depends on evaluators and their attestation.

## Are film gates part of the standard?

No. Climax force, thematic necessity, character age fit, and visual narrative are domain examples. Other Skills define their own gates.

## Can an ordinary Agent Skills host still use the package?

Yes, when `compatibility.ordinary_skill` is true. The host may ignore the extension or use `soft-contract` fallback, but it must not claim stronger enforcement than actually occurred.
