# 精读 05-01：Multi-Loco

论文：

- [Multi-Loco: Unifying Multi-Embodiment Legged Locomotion via Reinforcement Learning Augmented Diffusion](https://arxiv.org/abs/2506.11470)
- 项目页：[multi-loco.github.io](https://multi-loco.github.io/)
- PMLR / CoRL 2025：[PMLR 页面](https://proceedings.mlr.press/v305/yang25a.html)
- 代码：暂未公开

本笔记使用的一手材料：

- PMLR 正式论文页：[PMLR 页面](https://proceedings.mlr.press/v305/yang25a.html)
- 项目页框架与实验说明：[Project page](https://multi-loco.github.io/)

## 1. 一句话总结

这篇论文提出 **Multi-Loco**，通过一个**共享 diffusion action prior + 共享 residual policy** 的统一框架，在多种腿式机器人上学习通用 locomotion，并在真实世界四种平台上验证其鲁棒性与可部署性。

## 2. 它到底在解决什么问题？

这篇论文要解决的是一个很直接的问题：

> 不同腿式机器人在 observation / action 维度和动力学上差异很大，能否仍然训练一个统一的 locomotion policy？

作者的答案不是传统的单一 PPO policy，也不是显式 body graph 方法，而是：

- 先从跨本体数据里学一个 `morphology-invariant` 的 diffusion prior
- 再用一个共享 residual policy 做在线修正

所以它的核心问题不是：

> 能否完全抹平不同身体的差异？

而是：

> 能否先学一个足够稳的共享 locomotion prior，再让轻量 residual 去处理任务和执行层细节？

## 3. 问题设定与 claim 强度

### 它强在哪里

- 这是一个明确的 **multi-embodiment legged locomotion** 论文。
- 它不是只停留在 simulation，而是做了 **real-world deployment**。
- 它覆盖了四种平台：
  - biped
  - wheeled biped
  - humanoid
  - quadruped
- 项目页明确展示了统一策略在：
  - grass
  - slopes
  - stairs
  - gravel paths
  等复杂地形上的部署效果。

### 它没那么强的地方

- 它主要证明的是 **多本体统一训练**，不是严格的 **unseen embodiment transfer**。
- 论文和项目页都没有把重点放在“withheld robot zero-shot transfer”上。
- 它解决的是 locomotion，不是 manipulation 或 whole-body loco-manipulation。

所以，这篇论文更准确的定位是：

> 强多本体统一 locomotion 证据

而不是：

> 严格意义上对未见新身体的强 cross-embodiment transfer 证据

这点对你的 related work 判断很重要。

## 4. Pipeline 是怎样的？

项目页把框架说得很清楚，可以拆成三步。

### Step 1：对多机器人数据做统一预处理

作者先对多种机器人的 observation 和 action 做：

- zero-padding
- normalization

目标是把不同 embodiment 的输入输出放到一个统一格式中。

这里要特别注意：

> 这一步本质上还是一种工程化空间对齐，而不是天然的语义对齐。

### Step 2：训练共享 diffusion model

作者离线训练一个共享 diffusion model，使用：

- masked denoising score matching

它的作用是学习跨机器人共享的 locomotion action prior。

论文强调这个 diffusion model 是：

> morphology-agnostic generative diffusion model

也就是说，它想捕捉的是：

- 不同身体之间共享的 locomotion 结构
- 而不是每个机器人特有的控制细节

### Step 3：用共享 residual policy 在线修正

在推理时：

- diffusion model 先给出 action prior
- residual policy 再做 refinement

这个 residual policy 是 **shared across all embodiments**。

同时作者采用：

- multi-critic PPO

其中：

- `policy` 是共享的
- `critic` 是 robot-specific 的，每个 critic 对应一种机器人

这个设计其实非常值得你注意，因为它清楚体现了：

> shared actor + specific critic

是一种现实可行的 cross-embodiment / multi-embodiment 训练方式。

## 5. 什么是 shared，什么是 embodiment-specific？

这篇论文最大的价值之一，就是它的 shared vs specific 边界相对清楚。

### Shared 的部分

- diffusion action prior
- residual policy
- 多本体联合训练框架
- 统一的 padded / normalized observation-action 格式

### Embodiment-specific 的部分

- critic
- 具体 observation / action mask
- 各机器人自身动力学
- 最终部署时的执行细节

这说明它并不是“所有模块完全统一”，而是：

> 在 actor / prior 层共享，在 value estimation 和执行层保留本体差异。

这个设计比“完全 one-policy、完全不分本体”要现实得多。

## 6. Observation 和 Action 是怎么设计的？

根据项目页，Multi-Loco 采用的是一种非常直接的统一策略：

- 对不同机器人 observation / action 做 zero-padding
- 再做 normalization

然后把它们送进共享模型。

这说明它的方法并没有采用：

- graph body encoding
- object-centric interface
- contact-centric interface
- latent action token

而是更偏向：

> 在原始控制空间附近做统一建模，再让 diffusion prior 提升鲁棒性。

所以它很适合和你自己的 idea 对照：

- 它代表的是“对齐 raw-ish space + shared generative prior”这一路
- 而你更想走的是“shared semantic reference + embodiment-specific execution”

这两条路线有明显差别。

## 7. 数据和训练 recipe

### 数据来源

作者使用的是：

- 多机器人数据集
- 跨本体 locomotion 数据

从框架描述看，diffusion model 先离线学 prior，说明它依赖于已有的多机器人轨迹数据。

### Training recipe

整体训练是两阶段：

1. `offline diffusion prior learning`
2. `online residual policy refinement with multi-critic PPO`

这比单纯 PPO 多了一层生成式行为先验。

### 这条路线的意义

它其实验证了一个很重要的设计思想：

> 单一高斯 policy 对多本体统一控制可能不够稳，而 generative prior + residual correction 可能更适合共享 locomotion skill。

## 8. 主要结果是什么？

### 结果 1：相对 PPO 平均提升 10.35%

PMLR 摘要明确报告：

- 相比标准 PPO
- Multi-Loco 平均 return 提升 `10.35%`

### 结果 2：在 wheeled-biped 上提升最高可达 13.57%

PMLR 摘要明确提到：

- 在 wheeled-biped locomotion 上
- 提升最高达 `13.57%`

这说明它的收益不只是出现在“相对标准”的平台上，而是在更异质的 embodiment 上也明显成立。

### 结果 3：真实机器人统一部署

项目页显示统一策略部署在：

- biped
- wheeled biped
- humanoid
- quadruped

而且能处理多种 uneven terrain。

这说明它不仅是“多本体仿真统一训练”的结果，更是：

> 一个真正走到 real-world multi-platform deployment 的工作。

## 9. Failure modes 和局限

### 局限 1：不是严格 unseen embodiment generalization

这是最重要的 caveat。

虽然它是多本体统一 locomotion，但它没有像 URMA / H-Zero 那样把重点放在：

- withheld robots
- zero-shot transfer to unseen embodiments

所以如果你的研究问题是：

> 能否迁移到新身体？

那么这篇论文只能提供**间接支持**，不能作为最强证据。

### 局限 2：统一接口较工程化

它的统一方式主要依赖：

- zero-padding
- normalization

这是一种实用方案，但不一定是最优的语义接口设计。

### 局限 3：主要还是 locomotion

它还没有回答：

- manipulation 中共享什么
- loco-manipulation 中上肢语义如何表达
- 更高层行为 reference 是否更适合共享

## 10. 这篇论文对你的课题贡献了什么？

### 最有价值的思想

它给你的最大启发是：

> 对多本体统一控制来说，生成式行为先验可能比单纯高斯 policy 更稳。

### 它验证了什么

它验证了：

- 多本体 joint training 是可行的
- diffusion prior 可以作为共享 locomotion pattern 的载体
- shared actor + specific critic 是现实有效的设计

### 它没有验证什么

它没有验证：

- unseen embodiment zero-shot transfer
- semantic reference 是否优于 raw padded control space
- locomotion 之外的跨本体迁移

这正好是你后续可以接着往前推的地方。

## 11. 我的判断

### 值不值得精读？

`值得精读`

尤其如果你关心：

- multi-embodiment locomotion
- diffusion policy / generative prior
- shared actor vs specific critic
- 多平台真实部署

这篇论文是很好的代表工作。

### 它属于哪个 bucket？

- `cross-embodiment locomotion / whole-body control`
- `morphology-aware learning and scaling`
- `shared policy with generative prior`

### 最重要的一句话 takeaway

Multi-Loco 最重要的 takeaway 是：

> 在多本体 locomotion 中，共享 diffusion prior + 共享 residual actor + 本体特定 critic，是一条比单纯 PPO 更稳、更容易落地的统一控制路线。

## 12. 它留给你的研究问题

1. diffusion prior 学到的到底是 morphology-invariant locomotion pattern，还是只是更好的多任务先验？
2. 如果不用 raw padding，而改用 semantic motion reference，是否能比 Multi-Loco 更适合做 unseen embodiment transfer？
3. `shared actor + specific critic` 是否可以迁移到 mimic / loco-manipulation？
4. 生成式 prior 是否能和你想做的 `flow-matching semantic generator` 结合？

## 13. 五句话最终输出

1. 这篇论文的核心 claim 是：通过共享 diffusion locomotion prior 和共享 residual policy，可以在多种腿式机器人上学习统一 locomotion 控制，并优于标准 PPO。
2. 这个 claim 在多平台仿真和真实机器人上都较强，但它主要证明的是 seen multi-embodiment unification，而不是 strict unseen embodiment transfer。
3. 真正被共享的是 diffusion prior 和 actor；真正 embodiment-specific 的是 critic 以及具体执行层差异。
4. 它最重要的工程价值，是证明了 generative prior 可以提升多本体统一 locomotion 的鲁棒性和部署能力。
5. 对你的课题来说，它最有价值的地方，是提供了一个“共享先验 + 共享执行主干 + 局部本体特定模块”的现实设计范式。
