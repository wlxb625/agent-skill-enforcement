# 上传 GitHub 指南

## 建议仓库名称

```text
contract-skills
```

## GitHub Description

```text
An experimental execution-contract extension for Agent Skills: immutable policies, adaptive layers, stages, gates, repairs, and completion receipts.
```

中文简介可写：

```text
面向 Agent Skills 的实验性强执行扩展：通过不可变策略、自适应层、阶段、门禁、返修和完成凭证，把方法说明升级为执行契约。
```

## Topics

```text
agent-skills
ai-agents
llm-agents
workflow
policy-as-code
guardrails
agent-governance
execution-contracts
```

## 新建并上传

```bash
git init
git add .
git commit -m "Initial Contract Skills 0.1 draft"
git branch -M main
git remote add origin https://github.com/<YOUR_NAME>/contract-skills.git
git push -u origin main
```

## 首个 Release

建议标签：

```text
v0.1.0-draft
```

Release 标题：

```text
Contract Skills Specification 0.1 Draft
```

Release 说明重点：

- experimental and not official;
- preserves ordinary Agent Skills compatibility;
- adds execution contract primitives;
- includes reference validator and examples;
- semantic evaluation still depends on host attestation.
