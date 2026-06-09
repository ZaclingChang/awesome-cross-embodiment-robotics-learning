# 精读 01：One Policy to Run Them All

论文：

- [One Policy to Run Them All: an End-to-end Learning Approach to Multi-Embodiment Locomotion](https://arxiv.org/abs/2409.06366)
- 项目页：[nico-bohlinger.github.io/one_policy_to_run_them_all_website](https://nico-bohlinger.github.io/one_policy_to_run_them_all_website/)
- 代码：[github.com/nico-bohlinger/one_policy_to_run_them_all](https://github.com/nico-bohlinger/one_policy_to_run_them_all)

本笔记使用的一手材料：

- PMLR 页面与摘要：[PMLR 页面](https://proceedings.mlr.press/v270/bohlinger25a.html)
- 论文 PDF：[PDF](https://www.ias.informatik.tu-darmstadt.de/uploads/Team/NicoBohlinger/one_policy_to_run_them_all.pdf)
- 项目页结构示意：[Project page](https://nico-bohlinger.github.io/one_policy_to_run_them_all_website/)

## 1. 一句话总结

这篇论文提出了 **URMA（Unified Robot Morphology Architecture）**，通过一个**形态无关的 encoder-decoder 策略结构**，在多种腿式机器人本体上训练**单一 locomotion policy**，并在仿真和真实四足机器人上实现对新本体的迁移。

## 2. 它到底在解决什么问题？

这篇论文在解决一个非常直接的问题：

> 能不能不再给每台机器人各训练一个 locomotion policy，而是训练一个跨异构腿式本体共享的 locomotion policy？

它的应用场景是**低层 locomotion 控制**，覆盖：

- 四足
- 人形
- 双足
- 六足

它比“同一类四足上的多任务训练”更强的地方在于，作者明确希望解决：

- 多种 morphology family
- 关节数不同
- 对 unseen embodiment 的 zero-shot / few-shot transfer

这篇论文的重要性在于，它把问题从：

- `一个 policy 控很多四足`

推进到了：

- `一个 policy 控很多不同 body plan 的腿式机器人`

## 3. 问题设定与 claim 强度

### 它强在哪里

- 这篇论文是真正意义上的 **multi-embodiment**，不是单一本体上的多任务。
- 它使用了 **16 个仿真机器人**，来自 **3 类 morphology family**：
  - `9 个 quadruped`
  - `5 个 humanoid`
  - `1 个 biped`
  - `1 个 hexapod`
  来源：论文 Sec. 6 与 Appendix A。
- 它评估了对 withheld robots 的 **zero-shot transfer**，包括：
  - `Unitree A1`
  - `MAB Silver Badger`
  来源：论文 Sec. 6 的 zero-shot / few-shot 迁移实验。
- 它还把同一个 policy **zero-shot 部署到了真实四足机器人**上，其中包含一个未见过的真实机器人。
  来源：论文 Sec. 6 的真实世界部署部分。

### 它没那么强的地方

- 这篇论文只解决 **locomotion**，不是通用控制。
- 真实世界验证只在 **四足** 上，不是 humanoid。
- humanoid 最强的结论仍然停留在仿真里。
- 作者明确承认：对**远超训练分布**的新本体，zero-shot transfer 仍然困难。
  来源：论文讨论与结论中的 limitations。

所以，这是一篇在 **cross-embodiment locomotion** 上非常强的论文，但它还不能说明：

> 一个 policy 已经能稳健地解决 `unseen humanoid` 上的通用 whole-body behavior。

## 4. Pipeline 是怎样的？

URMA 的 pipeline 非常清楚，可以拆成 4 步。

### Step 1：把 observation 拆开

它把 observation 分成三类：

- `joint-specific observations`
- `feet-specific observations`
- `general observations`

在 locomotion setting 下，具体是：

- joint-specific observations：
  - 关节位置
  - 关节速度
  - 上一步动作
- feet-specific observations：
  - 是否接触地面
  - 距离上一次足接触经过了多久
- general observations：
  - 躯干线速度
  - 躯干角速度
  - 速度指令
  - 重力方向
  - 高度
  - PD controller 参数
  - 机器人质量和尺寸

来源：Appendix A，`Environment Details`。

### Step 2：用 morphology description 编码各部件

每个 joint 都有：

- joint-specific observation `o_j`
- joint description 向量 `d_j`

这个 joint description 包含的信息有：

- 相对 3D 位置
- 旋转轴
- 直接子关节数量
- nominal position
- 扭矩 / 速度限制
- damping / inertia / stiffness / friction
- 控制范围
- 机器人级别属性，比如总质量和几何尺寸

来源：论文方法部分与 Appendix A。

这些 joint-specific 信息先分别编码，再通过一个带可学习温度参数的简单 attention encoder 融合起来。

### Step 3：构造共享 latent controller

encoder 会先把所有 joints 聚合成 joint latent，同样把 feet 聚合成 feet latent，然后与 general observations 拼接，再通过共享核心网络得到一个 `action latent`。

来源：论文方法部分和项目页中的架构图。

### Step 4：再 decode 回 robot-specific actions

universal decoder 使用：

- action latent
- 编码后的 joint description
- joint latent

输出每个关节对应的动作分布。

来源：论文方法部分和项目页中的架构图。

这篇论文最关键的架构思想就是：

> 中间层共享抽象 locomotion control，而具体机器人通过 morphology-conditioned encoder / decoder 去实现。

## 5. 什么是 shared，什么是 embodiment-specific？

这是这篇论文对你最有价值的地方。

### Shared 的部分

- 单一架构
- 单一核心 locomotion controller
- 共享 latent action space
- 共享的 morphology-agnostic encoder / decoder 设计
- 在所有机器人上共享 PPO 训练

### Embodiment-specific 的部分

- joint description vectors
- feet description vectors
- robot-specific observation set
- robot-specific control gains 和 scaling factor
- reward coefficient
- domain randomization 范围
- 环境定义和 XML 资产

而且代码仓库本身也明确说明：新增一个机器人时，仍然需要手动修改：

- reward coefficients
- controller gains
- scaling factor
- domain randomization 范围
- environment metadata

来源：代码仓库 README 和新机器人接入说明。

所以这篇论文**不是**：

> 完全零本体适配的绝对 one-policy

它更准确的描述应该是：

> 一个共享的 locomotion policy 架构，加上本体相关的 embodiment metadata，以及低层环境/控制器调节。

这个区别非常重要。

## 6. Observation 和 Action 是怎么设计的？

### Observation 设计

这篇论文的 observation 设计很强，因为它显式区分了：

- 哪些信息随着 morphology 变化
- 哪些信息在不同本体之间仍有统一语义

这个思想对 cross-embodiment 非常可复用。

### Action 设计

它的 action 并不是 world-level 的 object-centric 或 contact-centric 接口。  
它最终仍然是一个**每关节的低层动作分布**，只不过这个动作是从共享 latent 里 decode 出来的。

在环境里，最终动作会作为一个缩放后的 position offset：

- `q_target = q_nominal + sigma_a * a`

再通过 PD controller 执行。

来源：Appendix A，`Environment Details`。

这意味着：

> 虽然中间 latent controller 是共享的，但执行层仍然属于 robot-specific actuation regime。

## 7. 数据和训练 recipe

### 数据来源

- 完全基于 simulation 的 locomotion 数据
- MuJoCo CPU 仿真
- 16 个机器人，每个 3 个并行环境，总计 48 个环境

来源：Sec. 6，training setup。

### Training recipe

- PPO
- JAX 实现
- 基于 RL-X codebase
- 用 domain randomization 做 sim-to-real

来源：Sec. 6 与实现细节说明。

这不是一篇 dataset-pretraining 论文。  
它本质上是一篇：

> 共享多本体训练的 end-to-end RL 论文。

## 8. 它和哪些 baseline 比？

baseline 设计是有意义的，因为它对应了两个非常自然的替代方案。

### Multi-head baseline

- 共享主干
- 为不同 morphology 设计不同 head
- 同一类 morphology 的 observation 会对齐到一致顺序

缺点：

- 新增关节或新增 morphology 需要增设新 head 或扩 head

来源：Sec. 6 baseline setup。

### Padding baseline

- 把 observation / action pad 到统一长度
- 再加 one-hot task ID

缺点：

- 新机器人本质上就像一个新任务
- 很难适配结构差异很大的 observation / action

来源：Sec. 6 baseline setup。

### Single-robot training

- 每个机器人单独训一个 policy
- 作为另一类参考点

## 9. 结果和 evaluation protocol

### 训练设定

- 16 个机器人一起训练
- 和 single-robot training、MTRL baselines 做对比
- 每机器人训练 100M steps
- 5 个随机种子，报告 95% 置信区间

来源：Sec. 6, training and evaluation protocol。

### 主要结果

1. **训练效率**
   URMA 和 multi-head 都明显比 single-robot training 学得更快，而 URMA 最终性能高于 multi-head baseline。  
   来源：Sec. 6，主学习曲线讨论。

2. **对 Unitree A1 的 zero-shot transfer**
   URMA 对 withheld quadruped 的 zero-shot transfer 效果不错，尤其当新机器人与训练 quadrupeds 相似时。  
   来源：Sec. 6, zero-shot transfer experiment。

3. **对 MAB Silver Badger 的 zero-shot + few-shot transfer**
   这个机器人更有代表性，因为它：
   - 多了一个 spine joint
   - 没有 feet observations  
   URMA 是唯一在 fine-tuning 后能学出较好 gait、并且对 feet observation 缺失更鲁棒的方法。  
   来源：Sec. 6, OOD embodiment transfer discussion。

4. **对 observation dropout 的鲁棒性**
   去掉 feet observations 后，URMA 依然比基线稳定。  
   来源：Sec. 6, foot observation ablation。

5. **真实机器人 zero-shot 部署**
   同一个 URMA policy 被 zero-shot 部署到：
   - Unitree A1
   - MAB Silver Badger
   - MAB Honey Badger  
   包括一个未见过的真实机器人。  
   来源：Sec. 6, real-world deployment section。

## 10. Failure modes 和局限

这篇论文比较可贵的一点是，它对局限写得相对清楚。

### 局限 1：transfer 仍然严重依赖训练覆盖范围

作者明确承认：对**明显超出训练分布**的新本体，zero-shot transfer 仍然困难。  
来源：论文讨论与结论中的 limitations。

这是这篇论文最重要的 caveat。

### 局限 2：没有 exteroceptive sensing

这篇论文没有使用外感知，因此在复杂环境中的可扩展性有限。  
来源：论文讨论与 future work。

### 局限 3：没有 humanoid 的真实世界验证

虽然训练中包含 humanoid，但真实世界部署并没有验证 humanoid。  
来源：论文讨论与 future work。

### 局限 4：仍然需要 robot-specific 环境和控制调参

虽然网络本身是共享的，但完整系统离“任意新本体直接 plug-and-play”还有距离。

这对你的课题意味着：

> 这篇论文的“共享策略”更强地成立在 representation / architecture 层，而不是完整部署栈层。

## 11. 这篇论文对你的课题贡献了什么？

### 最有价值的思想

这篇论文最有价值的地方，不只是“one policy”。

而是它给了一个非常清楚的设计原则：

> robot-specific structured observations + morphology descriptions -> shared latent controller -> universal morphology-conditioned decoder

这对你思考下面几个问题很有帮助：

- 什么应该放在 shared policy 里
- 什么应该通过 embodiment conditioning 处理
- shared 和 specific 的边界应该画在哪里

### 它验证了什么

它验证了：

- 跨不同 body plan 的共享低层 locomotion policy 是可能的
- morphology-agnostic encoder/decoder 比简单 padding 更有效
- 对“中等程度新颖”的 unseen embodiment，zero-shot transfer 是现实可行的

### 它还没有验证什么

它没有证明：

- 一个 policy 能对真正任意的新身体都稳健泛化
- 这种 shared control 能自然扩展到 manipulation
- shared policy 可以消除 embodiment-specific 的 low-level tuning

## 12. 我的判断

### 值不值得精读？

`必须精读`

如果你的课题涉及：

- one policy for many bodies
- morphology-aware policy transfer
- cross-embodiment locomotion
- shared encoder/decoder architecture

那这篇论文就是基础文献。

### 它属于哪个 bucket？

- `policy transfer`
- `cross-embodiment locomotion / whole-body control`
- `morphology-aware learning`

### 最重要的一句话 takeaway

URMA 是目前最清楚地说明以下观点的工作之一：

> 当 morphology-specific 信息通过结构化 description 和 universal encoder-decoder 处理时，共享的 locomotion controller 可以在异构腿式机器人之间出现。

## 13. 它留给你自己的研究问题

这篇论文自然引出下面这些问题：

1. URMA 这套思路能否从 locomotion 扩展到 **whole-body loco-manipulation**？
2. 最合适的共享接口是否仍然是 **joint-centric**，还是应该变成 **contact-centric** 或 **object-centric**？
3. 能不能用 learned embodiment adapter，减少剩余的手工 controller / environment tuning？
4. 当新本体真正远离训练分布时，zero-shot transfer 的边界到底在哪里？

## 14. 五句话最终输出

1. 这篇论文的核心 claim 是：一个共享的 locomotion policy 架构可以跨异构腿式机器人训练，并迁移到新本体。  
2. 这个 claim 在 locomotion 上相当强，因为它包含 16 个机器人、withheld embodiments 和真实四足部署，但还达不到“通用 cross-embodiment control”的强度。  
3. 真正被共享的是 latent locomotion controller 和 morphology-agnostic encoder/decoder 设计；真正不共享的是机器人元信息、controller tuning、reward 和部署配置。  
4. 它最主要的瓶颈仍然是 out-of-distribution embodiment transfer，以及对 robot-specific 低层细节的依赖。  
5. 对你的课题来说，这篇论文最重要的价值，是它清楚展示了 shared policy 与 embodiment-specific realization 之间的边界应该如何架构。  
