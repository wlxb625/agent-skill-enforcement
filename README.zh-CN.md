# Agent Skill Enforcement｜Agent Skill 强制执行规范

**一种面向可移植 Agent Skills 的强执行扩展。**

Agent Skill Enforcement 定义了 **Agent Skill Enforcement Protocol（ASEP）**。它把 Skill 中的专业方法和流程要求，从“供 AI 参考的说明”升级为可以阻止跳步、阻止错误推进、要求返修并限制最终交付的生命周期义务。

> 普通 Skills 描述应该怎样做。  
> 强执行 Skills 控制任务是否允许继续，以及是否有资格宣布完成。

ASEP 保留普通 Agent Skill 的文件夹形态与 `SKILL.md` 入口，在旁边增加机器可读的 `EXECUTION.yaml`，用于声明阶段锁、必需产物、验证器、语义评估器、阻断式门禁、返修路径、受保护规则、审计记录和完成凭证。

本项目是独立的社区实验，**不是 Agent Skills 官方规范的新版本**。

[English](README.md) · [ASEP 规范](SPEC.md) · [作者指南](docs/authoring-guide.md) · [迁移指南](docs/migration-guide.md) · [常见问题](docs/faq.md)

## 它解决什么问题

普通 Skill 可以写得非常完整，但 AI 仍可能：

- 选择性读取规则；
- 跳过中间阶段；
- 自行降低评分阈值；
- 门禁失败后继续写最终稿；
- 用自评代替真实检查；
- 没有完成流程就宣布交付。

ASEP 将这些要求变成可执行生命周期：

```text
激活
→ 只开放当前允许阶段
→ 提交必需产物
→ 验证确定性事实
→ 评估语义质量
→ 执行阻断式门禁
   ├─ PASS：进入下一阶段
   ├─ CONDITIONAL：返修
   └─ FAIL：退回或终止
→ 只有合法完成凭证才能最终交付
```

## 和普通 Skills 有什么不同

| 能力 | 普通 Agent Skill | ASEP 强执行 Skill |
|---|---|---|
| 可下载的文件夹包 | 支持 | 支持 |
| `SKILL.md` 方法说明 | 支持 | 支持 |
| 机器可读生命周期 | 通常是自然语言 | 由 `EXECUTION.yaml` 声明 |
| 阶段推进 | AI自行决定 | 可以锁定阶段 |
| 阶段产物 | 多为建议 | 必须通过 Schema |
| 质量检查 | 可被忽略 | 门禁可以阻止推进 |
| 失败处理 | AI临时决定 | 预先声明返修和退回路径 |
| 专业底线 | 容易被重新解释 | 下层规则不能削弱 |
| 完成判定 | AI认为写完 | 必须生成 `ASEP_COMPLETE` 凭证 |
| 可审计性 | 依赖平台 | 记录阶段、证据和门禁结果 |

## 强执行的核心原语

- **阶段锁：** 只允许执行当前获得授权的阶段；
- **验证器：** 检查格式、数量、引用、哈希、文件和其他确定性事实；
- **评估器：** 判断语义质量，并绑定具体证据；
- **门禁：** 综合结果，返回 `PASS`、`CONDITIONAL` 或 `FAIL`；
- **返修路径：** 规定必须改什么、保留什么、返回哪个阶段；
- **受保护规则：** 自适应层、任务层和 AI 临时决策不得降低；
- **完成凭证：** 证明必需阶段和门禁已经按声明的执行等级完成。

ASEP 负责定义“怎样强制”；具体领域 Skill 负责定义“强制什么专业标准”。

导演 Skill 中的高潮、主题、年龄、视觉叙事等只是领域示例，不属于通用规范。

## 文件结构

```text
my-enforced-skill/
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

## 最小声明

```yaml
enforcement:
  protocol: ASEP
  spec_version: "0.2.0-draft"
  kind: enforced-agent-skill
  name: evidence-brief
  version: "0.2.0"
```

## 快速使用

```bash
python -m pip install -e .
asep validate examples/minimal-enforced-skill
asep inspect examples/minimal-enforced-skill
```

## 执行等级

- **L0 普通 Skill：** 宿主只读取 `SKILL.md`，不得声称已执行 ASEP；
- **L1 声明式强执行：** AI读取规则，但宿主不掌管状态迁移；
- **L2 脚本强制：** 包内验证和状态脚本可以阻止非法推进；
- **L3 宿主原生强制：** 宿主管理状态、权限、评估隔离、门禁和最终交付。

实际运行在哪一级，就只能声称哪一级，不能把软约束包装成宿主强制。

## 必须诚实说明的限制

内容包可以强制结构、状态、权限、必需检查和完成条件，但如果宿主不提供独立评估上下文，它无法单独证明语义评估一定诚实。因此 ASEP 记录评估可信等级：

```text
self_assessed < separate_context < separate_model < human_verified
```

## 示例

- [`minimal-enforced-skill`](examples/minimal-enforced-skill/)：通用三阶段示例；
- [`film-director-enforcement-profile`](examples/film-director-enforcement-profile/)：导演领域强执行示例。

## 当前状态

`0.2.0-draft` 是一次破坏性草案改名。原先短暂使用的 `Contract Skills 0.1.0-draft` 容易让人把重点理解为“契约描述”，新名称明确强调真正核心：**能够阻断执行和完成的强制机制**。详见[迁移说明](docs/migration-from-contract-skills.md)。
