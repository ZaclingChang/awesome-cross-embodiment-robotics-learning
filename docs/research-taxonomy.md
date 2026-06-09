# Research Taxonomy for Cross-Embodiment Robotics Learning

这份文档的作用，是帮你把 related work 读成“研究地图”，而不是“论文清单”。

## 1. Problem Formulations and Transfer Taxonomy

核心问题：

- 什么算真正的 cross-embodiment？
- multi-task on one body 和 cross-embodiment 有什么区别？
- shared policy、shared prior、shared interface、shared dataset 之间有什么差异？

你读完这一类论文后，应该能回答：

- 你的课题到底属于哪一种 transfer
- 你的 claim 应该有多强
- 你的实验必须包含哪些 unseen-setting

## 2. General Multi-Embodiment Foundations

核心问题：

- 大规模 heterogeneous data 能否产生通用 embodied prior？
- 多本体共训是否真的有正迁移？

你读完这一类论文后，应该能回答：

- shared backbone 是否值得做
- prompting / adapter / fine-tuning 分别适合什么 setting

## 3. Policy Transfer, Distillation, and Fast Adaptation

核心问题：

- 如何把一个已有 policy 转移到新 embodiment？
- shared policy 和 fast adaptation 的边界在哪里？

你读完这一类论文后，应该能回答：

- one-policy 是否现实
- 轻量 adapter 是否足够
- 需要多大的 embodiment-specific tail

辅助概念阅读：

- `Understanding transfer learning and gradient-based meta-learning techniques`
  这不是机器人论文，但很适合帮助你区分：
  - `transfer learning` 更偏向学广义可迁移表征
  - `gradient-based meta-learning` 更偏向学快速适配初始化
  这对判断 shared policy 与 fast adaptation 的边界很有帮助。

- `LocoFormer`
  很适合帮助你理解另一条路线：
  - 不通过显式 finetuning 做适配
  - 而通过 `long-context / in-context adaptation` 让策略在交互过程中隐式形成 embodiment-specific 控制能力

## 4. Representation Transfer, Skill Abstraction, and World Models

核心问题：

- 哪些 latent 结构更可能是 embodiment-invariant？
- transferable signal 是 reward、skill、state progression 还是 world dynamics？

你读完这一类论文后，应该能回答：

- 任务不变量应该定义在哪一层
- 是否值得先学 reward / skill / progress representation

## 5. Human-to-Robot and Human-Prior Transfer

核心问题：

- human data 里哪些信号能转移到 robot？
- 如何缩小 human-robot embodiment gap？

你读完这一类论文后，应该能回答：

- human video 是否适合作为 pretraining source
- exoskeleton、teleoperation、retargeting 各自解决了什么问题

## 6. Cross-Embodiment Locomotion and Whole-Body Control

核心问题：

- locomotion 和 whole-body behavior 能否在多个 humanoid/biped 上共享？
- morphology shift 下，什么还保留，什么必须适配？

你读完这一类论文后，应该能回答：

- locomotion 里 shared policy 的上限在哪里
- humanoid 与 biped 之间的 transfer 该如何定义

## 7. Cross-Embodiment Manipulation, Visual Imitation, and Retrieval

核心问题：

- manipulation 中到底什么能跨身体转移？
- 是 hand motion、object motion、skill token，还是 retrieval prior？

你读完这一类论文后，应该能回答：

- manipulation 最适合 object-centric 还是 body-centric
- retrieval / imitation / diffusion policy 各自适合什么问题

## 8. Unified Interfaces, Latent Actions, and Retargeting

核心问题：

- shared action space 应该长什么样？
- raw joint action 为什么不够好？

你读完这一类论文后，应该能回答：

- 应不应该用 latent action
- contact-centric、body-part-centric、object-centric 哪种更合适

## 9. Teleoperation and Data Collection Systems

核心问题：

- 没有 aligned data 的情况下，cross-embodiment 方法怎么落地？

你读完这一类论文后，应该能回答：

- 哪种采集系统最适合你的任务
- 什么样的数据对齐程度是必须的

## 10. Datasets and Benchmarks

核心问题：

- 如何定义强评测协议？
- 什么 benchmark 才真的能检验 transfer，而不是插值？

你读完这一类论文后，应该能回答：

- 你的实验要用什么 benchmark
- seen / unseen embodiment 应该怎么拆

## 11. Morphology-Aware Learning and Scaling Laws

核心问题：

- 是增加数据量更重要，还是增加 embodiment diversity 更重要？
- morphology 是否需要显式编码？

你读完这一类论文后，应该能回答：

- 未来实验里该优先扩数据，还是扩本体
- graph / geometry / token conditioning 是否必要

辅助概念阅读：

- `MY BODY IS A CAGE`
  这篇论文很重要，因为它提供了一个反例：
  - `morphology-aware` 不一定天然更好
  - body graph 先验如果放错层，可能并不能带来更强泛化
  它很适合用来提醒自己：结构先验必须被实证证明，而不能默认成立。

## 12. Strong Auxiliary Baselines

核心问题：

- 如果你的方法没有明显超过这些 baseline，就很难说明 cross-embodiment 真有帮助。

你读完这一类论文后，应该能回答：

- 你的方法到底是在解决 transfer，还是只是换了一个弱 baseline
