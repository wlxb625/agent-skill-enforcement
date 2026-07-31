# Agent Skill Enforcement

**解决“明明调用了Skill，结果却还是模型默认套路”的问题。**

Agent Skill Enforcement定义了实验性的 **ASEP** 写作与校验方式。它不重新发明一种Skill格式，而是继续使用原有的`SKILL.md`、`references/`、`scripts/`和`assets/`，把Skill中的核心方法、禁止替代方式、检查要求和返修方式写得更清楚，让AI在理解、决策、生成和修改时更难把它们悄悄忽略。

> 普通Skill让AI读取一套方法。  
> ASEP让这些方法在AI生成过程中持续生效。

ASEP不取代Agent Skills，也不要求先安装一个新的Agent运行框架。经过ASEP增强的包仍然是普通、可移植的Skill；不认识ASEP的Agent仍然能读取Markdown，支持ASEP的工具则可以进一步校验可选的结构化遵循配置。

本项目是独立的社区实验，**不是Agent Skills官方规范的新版本**。

[English](README.md) · [规范草案](SPEC.md) · [编写指南](docs/authoring-guide.md) · [示例](examples/) · [常见问题](docs/faq.md)

## 它解决什么问题

一个Skill可以写得很专业，但AI加载以后，仍然可能按照自己最熟悉的默认模式生成。

例如网站设计Skill已经要求：

- 不要把卡片网格作为主要页面结构；
- 滚动必须改变空间、焦点或叙事状态；
- 图片和视频必须承担信息表达；
- 不能把重复淡入当作主要动效系统。

AI最后却还是做出：深色背景、大标题、卡片、渐变，以及每个区块相同的进入动画。

形式上Skill被调用了，真正决定质量的方法却没有充分参与生成。

ASEP针对的正是这一段偏差：

```text
Skill说明
→ 提取不可忽略的要求
→ 转换为当前任务的具体原则
→ 生成时持续保留相关要求
→ 按Skill检查实际结果
→ 定向修改偏离部分
```

AI仍然可以自主选择工具、技术和实现方式，但不能悄悄用更容易的默认套路替代Skill的核心方法。

## 和普通Skills有什么不同

| 能力 | 普通Agent Skill | ASEP增强Skill |
|---|---|---|
| 标准`SKILL.md`结构 | 支持 | 完全保留 |
| `references/`、`scripts/`、`assets/` | 可选 | 直接沿用 |
| 核心要求 | 容易混在长篇说明里 | 明确分级 |
| 禁止替代方式 | 经常没有写清 | 明确指出 |
| 当前任务解释 | 依赖AI自行理解 | 生成前要求转化 |
| 长任务中的要求保持 | 容易逐渐遗忘 | 按当前工作重新注入 |
| 检查重点 | 是否生成了结果 | 是否按照Skill生成 |
| 修改方式 | 容易整段重做 | 针对偏离部分返修 |
| 是否必须安装新运行时 | 不需要 | 核心模式同样不需要 |

## 设计原则

### 扩展原始Skills，而不是替代

ASEP继续采用标准结构：

```text
my-skill/
├── SKILL.md
├── references/
│   ├── adherence.yaml          # 可选的结构化遵循配置
│   ├── core-requirements.md
│   ├── quality-criteria.md
│   └── anti-patterns.md
├── scripts/
│   └── review_adherence.py
└── assets/
    └── templates/
```

基础格式仍然只要求`SKILL.md`。`references/adherence.yaml`只是可选增强，用于让工具检查要求结构；AI主要阅读的内容仍然是Markdown。

### 限制偏离，而不是限制创造

ASEP不规定唯一实现。网站Skill可以要求“滚动必须产生有意义的空间变化”，但AI仍然可以自由选择sticky场景、遮罩、视频序列、SVG、WebGL或其他适合的方法。

### 明确拒绝容易的替代方案

好的要求不仅说明“要什么”，还要说明哪些常见做法不能冒充满足要求。例如“滚动叙事”不能被“只有透明度变化”或“所有章节使用相同动画”替代。

### 检查是为了纠偏，不是为了写证明材料

检查的作用是发现结果何时回到了模型默认套路，然后要求继续修改，不是让AI写一份看起来很完整的自我证明。

## 一个普通的ASEP增强Skill

`SKILL.md`仍然是主入口：

```markdown
## Required references

开始设计前必须阅读：

- `references/core-requirements.md`
- `references/anti-patterns.md`
- `references/quality-criteria.md`

## Core requirements

1. 不得把卡片网格作为首页主要构图。
2. 滚动必须改变空间、焦点、信息关系或叙事状态。
3. 图片和视频必须承担内容表达，不能只做装饰。

## How to apply this Skill

正式实现前，把每条核心要求转换为当前页面的具体设计决定；开发每个区块时，持续保留与该区块相关的要求。

## Review and revision

渲染实际页面，按照质量标准检查，并修改所有退回禁止模式的部分。
```

可选的`references/adherence.yaml`可以把同样的要求写成便于工具检查的形式：

```yaml
profile:
  protocol: ASEP
  spec_version: 0.3.0-draft
  mode: strict
  skill: cinematic-web-designer

required_references:
  - references/core-requirements.md
  - references/quality-criteria.md
  - references/anti-patterns.md

requirements:
  - id: scroll-narrative
    level: hard
    statement: 滚动必须改变空间、焦点、信息关系或叙事状态。
    prohibited_substitutions:
      - 只有透明度变化
      - 所有章节使用相同进入动画

application:
  interpret_for_current_task: true
  keep_relevant_requirements_active: true

review:
  required: true
  criteria: references/quality-criteria.md
  revise_drifted_parts: true
```

## 快速使用

```bash
python -m pip install -e .
asep validate examples/minimal-adherence-skill
asep inspect examples/web-design-adherence-skill
```

改造已有Skill时：

1. 保留原有`SKILL.md`、`references/`、`scripts/`和`assets/`；
2. 将不可忽略的核心要求从一般建议中分离；
3. 写清禁止事项和不能冒充合格的替代方式；
4. 要求AI在生成前把规则转化为当前任务原则；
5. 增加按Skill检查和定向返修说明；
6. 有需要时再添加`references/adherence.yaml`。

详见[迁移指南](docs/migration-guide.md)。

## 示例

- [`minimal-adherence-skill`](examples/minimal-adherence-skill/)：使用标准Skill结构的最小示例；
- [`web-design-adherence-skill`](examples/web-design-adherence-skill/)：展示如何避免卡片网格和重复淡入等默认模式，同时不规定唯一视觉方案；
- [`optional-workflow-enforcement`](docs/optional-workflow-enforcement.md)：说明确实需要严格过程控制时，怎样额外加入阶段和门禁。

## ASEP不能保证什么

ASEP不能让能力不足的模型突然拥有专业审美，也不能保证AI自检一定正确。它更实际的目标是：减少AI明明加载了Skill，生成时却又回到默认套路的情况。

## 当前状态

`0.3.0-draft`把项目核心重新聚焦为：**提高AI在生成过程中的Skill遵循程度**。状态机、阻断式完成和凭证降为可选高级机制，不再是所有Skill的默认前提。
