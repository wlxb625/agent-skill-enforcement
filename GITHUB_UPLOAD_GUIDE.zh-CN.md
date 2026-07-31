# GitHub 发布与改名指南

## 正式名称

- 项目：`Agent Skill Enforcement`
- 规范：`Agent Skill Enforcement Protocol (ASEP)`
- 仓库：`agent-skill-enforcement`
- 类型：`Enforced Skill / 强执行型 Skill`

## GitHub Description

```text
An enforcement layer for Agent Skills: stage locks, validators, blocking gates, repair routes, protected rules, and receipt-backed completion.
```

中文简介：

```text
面向 Agent Skills 的强执行扩展：通过阶段锁、验证器、阻断式门禁、返修路径、受保护规则和完成凭证控制任务能否继续与交付。
```

## Topics

```text
agent-skills
ai-agents
llm-agents
enforcement
workflow
policy-as-code
guardrails
agent-governance
```

## 将现有仓库改名

GitHub 仓库页面：`Settings` → `General` → `Repository name`，将 `contract-skills` 改为：

```text
agent-skill-enforcement
```

GitHub 会为旧地址建立重定向。之后本地执行：

```bash
git remote set-url origin https://github.com/<YOUR_NAME>/agent-skill-enforcement.git
```

## Release

```text
Tag: v0.2.0-draft
Title: Agent Skill Enforcement Protocol (ASEP) 0.2 Draft
```
