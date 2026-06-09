# How to Read Cross-Embodiment Robotics Papers

这份指南不是教你“怎么看完更多论文”，而是教你如何把论文读成自己的研究资产。

如果你想直接用一套更固定、更像博士生工作流的方法，请同时看：

- [phd-paper-reading-method.md](phd-paper-reading-method.md)

如果你的目标是研究：

> cross-embodiment robotics learning

那么你读论文时最容易犯的错是：

- 只记结论，不记假设
- 只记模型，不记接口
- 只记成功率，不记评测协议
- 只看 demo，不看 transfer setting

## 1. 先把论文分成 taxonomy bucket 再读

建议你先对照这个文件一起看：

- [docs/research-taxonomy.md](research-taxonomy.md)

不要先问“这篇论文用了什么网络”，先问它属于哪个 bucket：

- problem formulation
- multi-embodiment foundation
- policy transfer
- representation transfer
- human-to-robot
- locomotion / whole-body control
- manipulation / visual imitation
- interface / retargeting
- benchmark / dataset
- morphology-aware scaling

### A. 问题定义类

你首先要判断，这篇论文到底在解决什么。

- 真正的 cross-embodiment
- human-to-robot / human-to-humanoid
- multi-task on one body
- whole-body control
- generalist foundation model
- interface / retargeting
- benchmark / dataset
- policy transfer / morphology transfer

如果问题定义都没搞清楚，后面的技术细节基本没有可比性。

### B. 表示层类

这类论文最值得看的是“中间层”。

你要抓的是：

- 它共享的到底是什么
- joint action 还是 latent action
- body-part goal 还是 contact plan
- object motion 还是 language-action
- 是统一接口，还是只是在 backbone 里拼接 morphology token

对你的课题来说，这一层通常比 backbone 更重要。

### C. 数据来源类

你要问：

- human video 还是 robot demo
- teleop 还是 simulation
- real robot 还是 synthetic retargeting
- 有没有 robot-free data collection
- 数据和本体之间的 gap 是怎么弥合的

很多论文的方法看起来很强，但本质上吃的是“高质量对齐数据”。

### D. 评测协议类

这是最容易被忽略，但最重要的一类。

你必须区分：

- seen embodiment vs unseen embodiment
- zero-shot vs few-shot
- sim-only vs sim-to-real
- same task family vs new task
- same morphology family vs morphology shift

如果论文没有真正的 unseen embodiment 测试，它对你的课题参考价值会明显下降。

## 2. 每篇论文至少提取这 12 个信息

建议你读每篇 paper 时，固定抽取下面这些字段。

1. `Problem`
   这篇论文到底想解决什么具体问题？

2. `Embodiments`
   用了哪些 humanoid、biped、机械臂或其他平台？

3. `Task family`
   locomotion、loco-manipulation、teleop、manipulation、navigation 还是 benchmark？

4. `What is shared`
   shared backbone、shared policy、shared latent action、shared skill library，还是 shared dataset？

5. `What is embodiment-specific`
   action head、decoder、low-level controller、IK/WBC、adapter、prompt，还是 morphology token？

6. `Observation space`
   proprioception、ego-centric vision、third-person video、tactile、language、state estimation。

7. `Action/interface space`
   joint targets、torques、body-part commands、contact states、object-centric action、latent action、language-action。

8. `Data source`
   human egocentric、whole-body motion、teleoperation、simulation、real robot、internet video。

9. `Training recipe`
   behavior cloning、RL、diffusion policy、world model、pretraining + finetuning、distillation、retrieval。

10. `Evaluation protocol`
    是不是有 unseen embodiment？有多少 shot？是否有 real robot transfer？

11. `Failure modes`
    失败发生在 perception、contact、retargeting、stability、morphology mismatch，还是 data bias？

12. `Takeaway for my project`
    这篇论文对“cross-embodiment robotics learning”到底贡献了哪一块？

## 3. 你真正能从 related work 里拿到什么信息

不是“别人做过什么”，而是下面这几类信息。

### A. 问题边界

你会知道：

- 哪些 claim 已经被验证过
- 哪些 claim 只在弱 setting 下成立
- 你的问题该定义得多强、多现实

比如：
- “共享策略或共享表示跨多个本体迁移”已经不是空想
- 但很多工作其实还是 `shared prior + robot-specific adaptation`
- 真正严谨的 unseen embodiment whole-body transfer 仍然很少

### B. 设计空间

你会知道可选方案有哪些：

- morphology-conditioned policy
- graph policy
- behavior prior
- unified latent action
- object-centric interface
- contact-centric interface
- human-to-robot retargeting
- teleoperation-driven data collection

这能帮你避免“只会想到一个方案”。

### C. 评价标准

你会知道：

- 你的实验必须对比什么 baseline
- 什么 benchmark 才能说服审稿人
- 哪些评测协议太弱，不能支撑你的 claim

### D. 真正的瓶颈

你会逐渐发现，很多论文最后都卡在这几类问题：

- embodiment gap
- contact dynamics
- poor action abstraction
- retargeting artifacts
- lack of unseen-body evaluation
- too much dependence on body-specific low-level control

这就是你未来创新点最可能出现的地方。

### E. 研究空白

当你把几十篇论文按同一模板读完，你会很容易发现空白：

- 很多人做 shared policy，但很少解释“共享的到底是什么”
- 很多人做人到机迁移，但少有人系统比较不同中间接口
- 很多人说跨 humanoid，但 benchmark 不够严格
- locomotion 的跨本体比 manipulation 成熟得多

这些空白就是你的 research questions 来源。

## 4. 建议的阅读顺序

### Stage 1: 建立地图

先读这些，理解全局：

- Open X-Embodiment
- Octo
- CrossFormer
- Being-H0.5
- GR00T N1
- Gemini Robotics

目标：
- 搞清楚 generalist multi-embodiment 的大图景

### Stage 2: 锁定 human-to-robot 与 humanoid 主线

再读：

- Humanoid Policy ~ Human Policy
- Human-Humanoid Cross-Embodiment Behavior-Skill Transfer
- HumanoidExo
- HumanX
- ZeroWBC

目标：
- 搞清楚 human behavior 如何转化为 robot prior

### Stage 3: 盯住 shared policy / cross-embodiment control

重点读：

- HugWBC
- H-Zero
- XHugWBC
- General Humanoid Whole-Body Control via Pretraining and Fast Adaptation
- Behavior Foundation Model for Humanoid Robots

目标：
- 搞清楚共享策略跨本体控制当前最强能做到什么程度

### Stage 4: 找你的创新空间

重点读：

- CEI
- Latent Action Diffusion
- OPFA
- X-Sim
- LAP

目标：
- 找到 unified interface / action abstraction 的创新切口

### Stage 5: 找评测与 scaling 支撑

重点读：

- RoboMIND
- Humanoid-X
- PHUMA
- Humanoid Everyday
- AnyBody
- Towards Embodiment Scaling Laws

目标：
- 明确什么样的 benchmark 和 scaling 分析能支撑你的 claim

### Stage 5: 读 benchmark，准备自己的实验

重点读：

- RoboMIND
- Humanoid-X
- PHUMA
- Humanoid Everyday
- AnyBody

目标：
- 明确你未来实验要怎么设计，如何说服别人你的工作是“真正跨本体”

## 5. 读完一篇论文后，最少输出什么

如果时间紧，每篇论文至少产出 5 行：

1. 这篇论文的核心问题是什么  
2. 共享的是什么，专属的是什么  
3. 用了什么动作/接口表示  
4. 它的评测到底强不强  
5. 它对我自己的课题有什么直接启发

如果连这 5 行都写不出来，说明还没有真正读懂。

## 6. 如果你在读 related work 时想输出真正有用的结论

建议你每读完一个 bucket，就额外写 3 行：

1. 这个 bucket 里，大家默认共享的到底是什么  
2. 这个 bucket 里，最常见的失败原因是什么  
3. 这个 bucket 对我自己的方法设计限制了什么  

这样你最后写开题或 related work 的时候，不会只剩下“谁做过什么”。

## 7. 一句建议

不要把 related work 当成“背景综述材料”，要把它当成：

> 一套帮助你发现问题定义、设计空间、评价协议和研究空白的坐标系。

这样你最后写出来的论文集，才不只是“收集链接”，而是真正有研究方法论的仓库。
