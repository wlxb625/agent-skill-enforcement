# Contract Skills｜契约型技能包

**一种面向 Agent Skills 的实验性强执行扩展。**

Contract Skills 建立在开放的 [Agent Skills](https://github.com/agentskills/agentskills) 文件夹格式之上，保留普通 Agent Skill 的文件夹形态和 `SKILL.md` 入口，同时增加机器可读的执行契约：不可变策略、自适应策略边界、阶段、验证器、评估器、质量门禁、返修路径、审计记录和完成凭证。

> 普通 Skill：“你应该这样做。”  
> Contract Skill：“只有满足这些条件，任务才算完成。”

本项目是独立的社区实验，**不是 Agent Skills 官方规范的新版本**。

[English](README.md) · [规范草案](SPEC.md) · [作者指南](docs/authoring-guide.md) · [迁移指南](docs/migration-guide.md) · [常见问题](docs/faq.md)

## 它解决什么问题

普通 Skill 能够封装专业知识、方法、脚本、模板和参考资料，但在很多 Agent 中，AI 仍然可以：

- 选择性读取规则；
- 跳过中间阶段；
- 自行降低评分标准；
- 用自评高分替代真实检查；
- 未完成流程就宣布交付。

Contract Skills 在 `SKILL.md` 旁增加可选的 `EXECUTION.yaml`，让支持该扩展的宿主，或者能够执行包内脚本的 Agent，对流程进行更强约束。

## 和普通 Skills 有什么不同

| 能力 | 普通 Agent Skill | Contract Skill |
|---|---|---|
| 可下载、可安装的文件夹 | 支持 | 支持 |
| `SKILL.md` 方法说明 | 支持 | 支持 |
| 机器可读的阶段 | 通常是自然语言 | 明确声明 |
| 规则优先级 | 主要依赖提示词 | 明确分层 |
| 不可变专业底线 | 没有统一格式 | 可声明、可保护 |
| 用户自适应 | 多依赖聊天记忆 | 通过受约束 Patch 更新 |
| 验证与评估 | 容易混在一起 | 明确分离 |
| 质量门禁 | 多为建议 | 可以阻止进入下一阶段 |
| 返修路径 | AI 临时决定 | 契约预先声明 |
| 完成判定 | AI 认为写完 | 通过门禁并生成完成凭证 |
| 审计 | 依赖平台 | 契约级事件与记录 |

## 最关键的抽象

Contract Skills 不负责规定所有行业“什么才是好结果”。

它负责提供一套通用表达方式，让不同领域作者把自己的专业标准变成可执行规则：

- **Validator／验证器：** 检查格式、数量、引用、哈希、文件和确定性事实；
- **Evaluator／评估器：** 判断语义质量，并绑定具体证据；
- **Gate／门禁：** 综合验证和评估结果，决定 `PASS`、`CONDITIONAL` 或 `FAIL`；
- **Repair Contract／返修契约：** 规定必须改什么、保留什么、返回哪个阶段。

所以：

> 通用规范负责“怎么拦”；领域 Skill 负责“拦什么”。

导演 Skill 中的高潮、主题、人物年龄、视觉叙事等门禁，只是领域示例，不属于通用标准。

## 文件结构

```text
my-contract-skill/
├── SKILL.md
├── EXECUTION.yaml
├── constitution/
│   └── immutable.yaml
├── adaptive/
│   ├── default-policy.yaml
│   └── policy.schema.json
├── stages/
├── gates/
├── evaluators/
├── schemas/
├── scripts/
└── references/
```

## 快速使用

安装参考验证器：

```bash
python -m pip install -e .
```

验证最小示例：

```bash
contract-skill validate examples/minimal-contract-skill
```

查看契约摘要：

```bash
contract-skill inspect examples/minimal-contract-skill
```

已有 Skill 的升级步骤：

1. 保留原有 `SKILL.md`；
2. 提取不可变规则；
3. 把流程拆成阶段；
4. 为阶段定义结构化产物；
5. 分离验证器、评估器和门禁；
6. 设置失败与返修路径；
7. 定义最终完成凭证。

详见 [迁移指南](docs/migration-guide.md)。

## 执行等级

- **L0 普通 Skill：** 宿主只读取 `SKILL.md`；
- **L1 软契约：** AI读取契约，但宿主不强制生命周期；
- **L2 脚本验证：** 宿主能够运行包内状态与验证脚本；
- **L3 宿主原生强制：** 宿主管理状态、权限、评估隔离和最终交付。

低等级执行不能伪装成高等级执行。

## 策略优先级

```text
不可变契约策略
    > 用户／项目自适应策略
        > 当前任务策略
            > AI临时决策
```

第二层可以学习用户偏好，但不得降低第一层阈值、关闭必需门禁、跳过阶段或扩大禁止权限。

## 必须诚实说明的限制

内容包能够强制结构、状态、数量、权限、引用、必需检查和完成条件；但如果宿主不提供真正隔离的评估上下文，内容包自身不能证明语义评估一定诚实。

因此规范定义了评估可信等级：

```text
self_assessed < separate_context < separate_model < human_verified
```

详见 [语义评估限制](docs/semantic-evaluation-limitations.md)。

## 示例

- [`minimal-contract-skill`](examples/minimal-contract-skill/)：最小三阶段示例；
- [`film-director-contract-profile`](examples/film-director-contract-profile/)：导演领域示例，展示高潮、主题、年龄适配等自定义门禁。

## 项目状态

当前版本为 `0.1.0-draft`，用于公开讨论、原型开发和一致性测试。在 `1.0` 之前可能发生破坏性修改。
