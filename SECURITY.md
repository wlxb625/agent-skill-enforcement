# Security policy

Agent Skill Enforcement may contain executable scripts. Treat third-party packages as untrusted code.

Hosts should:

- sandbox scripts;
- use least-privilege tools;
- verify protected-file hashes or signatures;
- prevent model write access to immutable policy and host-owned state;
- validate policy patches;
- record external side effects;
- require human approval for high-risk actions.

Report security issues privately to the repository maintainer before public disclosure.
