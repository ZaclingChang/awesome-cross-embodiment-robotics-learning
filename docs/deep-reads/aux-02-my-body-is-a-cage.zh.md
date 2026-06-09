# 辅助精读 02：MY BODY IS A CAGE

论文：

- [MY BODY IS A CAGE: the role of morphology in graph-based incompatible control](https://arxiv.org/abs/2010.01856)
- OpenReview：[OpenReview 页面](https://openreview.net/forum?id=N3zUDGN5lO)
- 代码：[GitHub](https://github.com/jhejna/incompatible-control)

本笔记使用的一手材料：

- 论文摘要与元信息：[OpenReview 页面](https://openreview.net/forum?id=N3zUDGN5lO)
- arXiv 页面：[arXiv](https://arxiv.org/abs/2010.01856)

## 1. 一句话总结

这篇论文不是严格意义上的 cross-embodiment 机器人论文，而是一篇非常重要的**反例型文献**：作者研究在 `incompatible control` 设定下，显式利用 morphology graph 的方法是否真的有帮助，结果发现**物理身体结构信息并没有带来预期中的性能提升**，甚至一个不显式编码 morphology 的 Transformer 方法 `Amorpheus` 反而更强。

## 2. 为什么它值得放进这个仓库？

因为这个方向里一个很常见但并不总成立的假设是：

> 只要把身体结构编码进图网络，跨本体迁移就会更好。

这篇论文的重要性就在于，它给出了一个非常清楚的提醒：

> `morphology-aware` 不是默认正确答案，结构先验是否有效，必须靠实验说话。

对你的课题来说，这是一篇很好的“防止想当然”的辅助文献。

## 3. 它到底在解决什么问题？

这篇论文讨论的是所谓 **incompatible control**：

- 不同任务 / 不同身体
- 状态维度不同
- 动作维度不同
- 很难直接共享一个传统策略网络

作者要问的是：

> 在这种设定下，显式的 morphology information 到底是不是关键？

更具体地说，它在比较两种路线：

- **基于 morphology graph 的结构化方法**
- **不显式依赖物理结构、而把输入当作集合/序列来建模的方法**

## 4. 问题设定与 claim 强度

### 它强在哪里

- 它直接挑战了“图结构一定更好”的普遍直觉。
- 它不是只报结果，而是讨论为什么 morphology 信息可能没有帮助。
- 它提出了新的 Transformer 方法 `Amorpheus`，用于处理 incompatible control。

### 它没那么强的地方

- 它主要研究的是一般连续控制，不是你现在最关心的人形/locomotion/whole-body 机器人实验。
- 它不是在处理你现在意义上的 human-to-robot 或 robot-to-robot skill transfer。
- 它更像是在讨论**结构先验的有效性**，而不是直接讨论 cross-embodiment policy transfer 的完整 pipeline。

所以它的价值不在“直接给你方案”，而在：

> 帮你判断 morphology-aware 方法到底有没有被过度神化。

## 5. 方法主线是什么？

这篇论文的方法主线很简单：

### 路线 1：显式 morphology-aware 方法

代表思路是：

- 用 graph neural network
- 用身体节点和连接关系建模
- 希望网络通过身体拓扑获得更好的归纳偏置

### 路线 2：Amorpheus

作者提出 `Amorpheus`，它是一个基于 Transformer 的方法，但不显式把物理 morphology graph 当作核心归纳偏置。

作者的结论是：

> 在 incompatible control 上，显式 morphology 信息并没有如预期那样带来性能优势。

## 6. 什么是 shared，什么是 embodiment-specific？

虽然这篇论文不完全是 cross-embodiment transfer，但它仍然可以用你的 shared vs specific 框架来读。

### Shared 的部分

- 共享策略架构
- 统一的序列/集合式建模方式
- 兼容不同维度输入输出的建模框架

### Embodiment-specific 的部分

- 各身体自身的状态维度
- 各身体自身的动作维度
- 具体控制环境中的动力学差异

它对你的启发是：

> shared 不一定非要建立在显式 body graph 上，也可以建立在更弱、更通用的输入组织方式上。

## 7. Observation 和 Action 视角下怎么理解？

这篇论文最关键的接口问题不是视觉，也不是 language，而是：

> 不同身体的 state/action 维度不兼容时，统一策略该如何表示输入输出？

它真正讨论的是一种更底层的统一接口问题：

- 如何让一个共享模型吃下不同身体的输入
- 如何让它输出不同身体可执行的控制量

因此，它和你仓库里的很多 interface 论文虽然不在同一任务上，但在更抽象的层面是相关的。

## 8. 数据和训练 recipe

### 数据来源

- 强化学习环境
- 一般连续控制任务

### Training recipe

- 比较 morphology-aware 图方法与 Transformer 方法
- 看谁在 incompatible control 上表现更好

### Evaluation protocol

- 多任务 / 多身体
- 状态、动作维度不一致
- 测试统一策略在这种不兼容设定下的表现

## 9. 主要结果是什么？

### 结果 1：显式 morphology 信息没有带来预期优势

这是整篇论文最重要的结论。

它说明：

> 身体图结构并不自动等于更好的控制归纳偏置。

### 结果 2：Amorpheus 优于图方法

作者提出的 Transformer 方法效果更好，这表明更弱、更一般的架构先验，有时反而更适合处理 incompatible control。

### 结果 3：message passing 可能不是关键瓶颈的正确解法

如果结构信息本身没有提供有效增益，那么说明问题可能不在“图建得不够精细”，而在于：

- 控制任务本身需要的抽象层不对
- graph prior 约束错了位置

## 10. Failure modes 和局限

### 局限 1：不是直接的机器人 cross-embodiment 论文

它没有回答：

- unseen humanoid 迁移
- human-to-robot transfer
- loco-manipulation 共享策略

### 局限 2：负面结论有边界

它说明的是：

> 在它研究的 incompatible control 设定下，显式 morphology information 没有明显帮助。

这不等于说 morphology-aware 方法在所有机器人设定下都无用。

### 局限 3：没有更高层任务语义

它讨论的是低层控制共享，而不是：

- task semantics
- object-centric representation
- skill abstraction

## 11. 这篇论文对你的课题贡献了什么？

### 最有价值的思想

它给你的最大帮助不是正面答案，而是一个负面提醒：

> 不要默认“只要把身体结构编码进去，迁移就会更好”。

### 它对你课题的直接启发

如果你后面要做 morphology-aware 或 graph-based 方法，这篇论文要求你必须回答：

- 为什么你的结构先验在这个任务上真的有必要？
- 它比更弱、更一般的共享架构到底多带来了什么？

### 它不能替你回答什么

它不能告诉你：

- locomotion 里最适合的共享接口是什么
- human prior 该怎么迁移到 humanoid
- whole-body behavior 是否更需要显式 morphology prior

## 12. 我的判断

### 值不值得精读？

`有用，属于辅助精读`

如果你想做：

- graph-based morphology encoding
- body-aware transformer
- structure prior

这篇论文非常值得读，因为它会逼你把论证做扎实。

### 它属于哪个 bucket？

- `morphology-aware learning`
- `strong auxiliary baseline`
- `negative evidence / cautionary reading`

### 最重要的一句话 takeaway

这篇论文最重要的 takeaway 是：

> 在 incompatible control 里，显式 morphology graph 并不自动带来更强泛化；更一般的共享架构有时反而更有效。

## 13. 它留给你的研究问题

1. morphology-aware prior 在机器人 locomotion 里到底什么时候有效？
2. 如果 morphology graph 没有帮助，是不是应该把共享定义在 skill / contact / object 层，而不是 body graph 层？
3. 对 humanoid 和 loco-manipulation 来说，结构先验的有效层级到底在哪里？

## 14. 五句话最终输出

1. 这篇论文最强的 claim 是：在 incompatible control 设定下，显式 morphology 信息并没有带来预期中的性能提升。
2. 这个 claim 在一般连续控制任务上有说服力，但它不是直接的人形机器人 cross-embodiment 证据。
3. 真正被共享的是统一策略架构；真正不兼容的是不同身体的状态和动作维度。
4. 它最重要的意义，是对“graph-based morphology prior 一定有效”这一常见假设提出了实证挑战。
5. 对你的课题来说，它最大的价值是提醒你：任何 morphology-aware 设计都必须证明自己比更一般的共享架构真的更好。
