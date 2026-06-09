# Related Work: Cross-Embodiment Robotics Learning

下面这份 Related Work 面向的核心问题是：

> 如何在不同机器人本体之间迁移策略、表示、技能或数据，使机器人能力不再被单一本体所绑死？

这里的“cross-embodiment”既包括：

- `robot-to-robot` 的跨本体迁移
- `human-to-robot` / `human-to-humanoid` 的跨本体迁移
- `same policy / same backbone / same interface` 在不同本体上的共享
- `morphology-aware` 的本体条件化建模
- `data / benchmark / scaling law` 层面的多本体研究

本文按照研究脉络而不是简单按任务分类，系统梳理这一方向的相关工作。

---

## 1. 大规模多本体共训与通用机器人策略

cross-embodiment 研究最直接的起点，是尝试通过**多机器人、多任务、多数据源的联合训练**来学习共享策略或共享先验。该方向的核心思想是：如果不同机器人能够共享部分任务结构，那么将多本体数据混合训练，理论上可以提升对新任务、新环境、甚至新本体的泛化能力。

这一方向的代表性工作是 [Open X-Embodiment / RT-X](https://robotics-transformer-x.github.io/)。该工作汇集了来自 22 种机器人本体、60 个数据集、1M+ 条真实机器人轨迹的数据混合，并训练 RT-1-X 与 RT-2-X 等模型，证明大规模多本体共训能够带来跨平台的正迁移。其重要意义不在于某一个具体架构，而在于它首次系统性回答了这样一个问题：机器人学习是否也能像 NLP 和视觉一样，形成“通用预训练模型 + 下游适配”的范式。

在此基础上，[Octo](https://arxiv.org/abs/2405.12213) 进一步把“通用策略初始化”做成了一个开源、可复现、可微调的基线。Octo 强调的是：即便 observation space 和 action space 会变化，一个足够大的 transformer policy 仍可以作为多平台、多场景、多任务的共同起点。与 RT-X 相比，Octo 更偏向“如何把 generalist policy 作为实际研究工具”。

随后，[CrossFormer](https://arxiv.org/abs/2408.11812) 将 cross-embodiment 的问题进一步推广到 manipulation、navigation、locomotion 和 aviation 等不同 embodiment family。该工作最重要的贡献在于提出了一个能消费任意 embodiment 数据的 transformer policy，而不再要求 observation / action 事先手工对齐。与早期工作相比，这意味着“多本体共训”开始从“机械臂之间的迁移”扩大到“不同机体类型之间的共享”。

近一步的工业与基础模型工作，如 [Being-H0.5](https://arxiv.org/abs/2601.12993)、[GR00T N1](https://arxiv.org/abs/2503.14734)、[Gemini Robotics](https://arxiv.org/abs/2503.20020) 和 [Gemini Robotics 1.5](https://arxiv.org/abs/2510.03342)，则进一步体现了一个共识：未来机器人学习大概率不会沿着“每台机器人单独训练一套模型”的路线发展，而是更接近“共享大脑 + 本体适配层”。其中，Being-H0.5 特别强调 human traces 作为 physical interaction 的“母语”，而 Gemini Robotics 1.5 则显式提出 motion transfer 来支持 heterogeneous multi-embodiment adaptation。

总体来看，这一类工作解决的是“**是否值得做多本体共训**”的问题，并初步证明了答案是肯定的。但它们通常仍有一个共同局限：多数方法虽然共享 backbone 或共享 prior，却仍然需要不同程度的 embodiment-specific fine-tuning、prompting、decoder 或执行层适配，因此“真正的一脑多形”依然没有完全实现。

---

## 2. 共享策略、策略迁移与跨本体 locomotion / whole-body control

如果说上一类工作重点是“共享表示或共享预训练”，那么另一条主线则更激进：**是否可以用一个共享 policy 直接控制多种本体？**

在这一问题上，腿式 locomotion 尤其是 humanoid / biped locomotion 是当前最成熟的试验场。一个重要原因是：locomotion 的目标和 reward 结构通常相对统一，而 manipulation 中的物体接触、任务语义和末端执行器差异要复杂得多。

这条线最具代表性的工作之一是 [One Policy to Run Them All](https://openreview.net/forum?id=HVWusz2zv5) 及其正式版本 [One Policy to Run Them All: an End-to-end Learning Approach to Multi-Embodiment Locomotion](https://arxiv.org/abs/2409.06366)。该工作提出 URMA（Unified Robot Morphology Architecture），通过 morphology-aware 的 encoder-decoder，将 joint-specific / feet-specific / general observations 与 joint descriptions 结合，学习一个共享的 locomotion controller。它证明了单一策略架构可以在 quadruped、humanoid、biped、hexapod 等不同腿式本体上训练，并 zero-shot / few-shot 转移到 withheld robots，甚至 zero-shot 部署到真实四足平台。其真正的价值不只是“one policy”，而是清晰展示了 shared controller 与 embodiment-specific realization 之间的边界应如何建模。

在 humanoid 方向，[HugWBC](https://arxiv.org/abs/2502.03206) 表明统一 whole-body controller 可以在一个 humanoid 平台上支持丰富且可组合的 locomotion command space，并进一步支持上肢 intervention，为 loco-manipulation 奠定基础。基于这一思路，[H-Zero](https://arxiv.org/abs/2512.00971) 进一步将问题推进到**跨 humanoid 预训练**：通过在少量 humanoid embodiments 上预训练共享 locomotion base policy，实现对 unseen humanoids 的 zero-shot 和 few-shot 迁移，甚至 few-shot 适配到 upright quadrupeds。相比 URMA，H-Zero 更强调“shared prior + 新本体快速适配”的范式，而不是完全端到端统一。

更进一步，[XHugWBC](https://arxiv.org/abs/2602.05791) 明确主张跨 humanoid 的通用控制器可以通过一次训练获得。其关键技术包括 physics-consistent morphological randomization、语义对齐的 observation / action space，以及能建模 morphology 与 dynamics 的策略结构。实验覆盖 12 个仿真人形和 7 个真实机器人，是目前“single policy for multiple humanoids”最有代表性的工作之一。

此外，[General Humanoid Whole-Body Control via Pretraining and Fast Adaptation](https://arxiv.org/abs/2602.11929) 与 [Behavior Foundation Model for Humanoid Robots](https://arxiv.org/abs/2509.13780) 等工作，则代表了“共享行为先验 + 快速适配”的路线。它们不一定追求严格意义上的“一个 policy 无适配控制所有本体”，但通过 behavior prior 或 promptable behavior model，将跨 humanoid 的 whole-body control 转化为“先学共享行为空间，再对新本体低成本适配”的问题。

这一类工作总体说明：**shared policy 并不是空想**。但从当前证据看，最强结果主要集中在 locomotion 或 locomotion-like whole-body control；真正跨本体的 whole-body manipulation 仍然显著更难。换句话说，shared policy 在 locomotion 上已经进入“可验证阶段”，但在 manipulation 上还远未成熟。

---

## 3. Human-to-Robot / Human-to-Humanoid：把人类经验变成机器人先验

对于 cross-embodiment 来说，最深层也最具吸引力的一条线并不是 robot-to-robot，而是：

> human-to-robot / human-to-humanoid

也就是说，能否把人类示范、第一视角视频、人体运动和人类交互结构，转化成机器人可执行的控制先验。

早期代表工作包括 [Manipulator-Independent Representations for Visual Imitation (MIR)](https://arxiv.org/abs/2103.09016) 与 [XIRL](https://arxiv.org/abs/2106.03911)。MIR 的核心思想是学到与具体操控器无关的视觉表示；XIRL 则进一步提出 cross-embodiment inverse reinforcement learning，从不同 embodiment 的视频中抽取可迁移的任务进度与奖励结构。这两篇工作的重要性在于，它们把“跨本体迁移”从动作层提升到了**视觉表示**和**任务奖励**层。

随后，[WHIRL](https://arxiv.org/abs/2207.09450) 将 human-video-to-robot imitation 带到了真实世界 setting。WHIRL 的意义不在于它完全解决了 embodiment gap，而在于它证明了：即便没有严格的人机对齐动作标签，人类视频依然可以在真实机器人上提供有用的 imitation signal。

在 skill representation 方向，[XSkill](https://arxiv.org/abs/2307.09955) 和 [UniSkill](https://arxiv.org/abs/2505.08787) 分别从无标签 human/robot 视频中发现 cross-embodiment skill prototype，或从大规模 cross-embodiment video 中学 embodiment-agnostic skill representation。相比直接从 human joint 到 robot action 的映射，这类方法更强调 skill、task progress 或 latent representation 的共享，因此更适合大规模扩展。

在 humanoid 主线上，[Humanoid Policy ~ Human Policy](https://arxiv.org/abs/2503.13441) 是非常关键的一篇。它把 human 和 humanoid 明确视为不同 embodiment，并尝试在共享 state-action representation 中学习可迁移行为。与传统人到机 retargeting 不同，这一思路更接近“同一任务结构在不同身体中的不同实现”。[HumanoidExo](https://arxiv.org/abs/2510.03022) 则从数据采集层面缩小 human-humanoid gap：通过 wearable exoskeleton，让 human demonstration 本身更接近 humanoid control space。[HumanX](https://arxiv.org/abs/2602.02473) 与 [ZeroWBC](https://arxiv.org/abs/2603.09170) 进一步推动了“robot-free human data -> humanoid visuomotor skill”的范式。

这条线目前已经证明：

- human data 确实可以成为 robot / humanoid 的有效先验
- 直接映射 human motion 往往很脆弱
- 更可迁移的通常是 task progress、skill representation、object motion、whole-body interaction structure 等中间信号

但它的关键难点依然在于：**human embodiment 与 robot embodiment 的 gap 太大**，尤其当涉及 contact dynamics、stability、precise control 和 dexterous hands 时，很多方法仍需要 retargeting、teleoperation、exoskeleton 或 simulation bridging。

---

## 4. 表示迁移、技能抽象与世界模型：什么才是真正可迁移的？

如果进一步追问 cross-embodiment 的本质，会发现问题并不只是“policy 能不能迁移”，而是：

> 到底哪些 latent 结构才是 embodiment-invariant 的？

这一视角把研究重点从“单一控制器”转向“可迁移的任务结构”。

在 reward / progress 层面，[XIRL](https://arxiv.org/abs/2106.03911) 已经表明，不同本体的视频中可以学到共享的任务进度表示，从而用于逆强化学习和奖励构建。相比直接对齐动作，这种方法把共享部分放在“任务阶段”而不是“执行方式”。

在技能抽象层面，[XSkill](https://arxiv.org/abs/2307.09955) 与 [UniSkill](https://arxiv.org/abs/2505.08787) 试图从 human 和 robot 的跨本体视频中抽取 skill prototypes 或 skill representations。这条思路的重要性在于：一旦 skill 是共享的，那么不同机器人只需要学会如何“实现 skill”，而不是从头学任务。

在 retrieval / composition 方向，[R+X](https://arxiv.org/abs/2407.12957) 展示了从日常 human videos 中检索和执行相应行为的可能性。这类工作说明，cross-embodiment 也可以不只是“表示对齐”，还可以通过 retrieval-based execution 把 human behavior 作为结构化先验调用。

与此相关的另一条主线是“世界模型 / behavior prior”，例如前面提到的 [Behavior Foundation Model for Humanoid Robots](https://arxiv.org/abs/2509.13780)。这些工作共同体现出一个趋势：未来 cross-embodiment 不一定依赖单一策略直接迁移，更可能通过共享 latent behavior space、shared world model 或 shared task structure 实现。

总体来看，这一方向最重要的贡献在于：

- 它把“共享的到底是什么”从 joint/action 层抬升到 skill / reward / behavior / world dynamics 层
- 它更接近“任务智能”的本质，而不是单一机体上的行为模仿

但目前这一方向的不足是：很多工作在 representation 学得很好时，最终执行仍依赖于相对简单或 task-specific 的下游 policy，因此 representation transfer 与 actual control transfer 之间仍有明显断层。

---

## 5. 统一接口、latent action 与 retargeting：找到正确的动作抽象层

随着 cross-embodiment 问题的深入，一个越来越清楚的共识是：

> raw joint action 往往不是最好的共享接口。

因为不同本体之间最不统一的，恰恰就是 action space：关节数不同、自由度不同、手型不同、控制频率不同、低层控制器也不同。如果仍然坚持在 joint-level 对齐，往往会使共享学习变得极其脆弱。

在这种背景下，[CEI](https://arxiv.org/abs/2601.09163) 提出了一个非常有代表性的思路：构造一个跨本体的 3D space unified interface，通过功能相似性与轨迹对齐，把不同臂型和末端执行器映射到共享空间。它的重要贡献不只是 transfer ratio 本身，而是明确提出：

> cross-embodiment 的核心问题是“接口设计”，而不只是“把数据混在一起训练”。

在 latent action 方向，[Latent Action Diffusion](https://arxiv.org/abs/2506.14608) 将不同末端执行器的 action 映射到一个语义对齐的 latent action space，并在其上做跨本体 co-training。相比直接对齐 raw actions，这种做法更适合 hand / gripper / anthropomorphic hand 之间的迁移。

[One-Policy-Fits-All (OPFA)](https://arxiv.org/abs/2603.14522) 则进一步提出 geometry-aware latent action，结合统一 latent retargeting decoder，在多种 gripper 和 dexterous hand 上实现 end-to-end co-training。与 CEI 相比，OPFA 更强调“latent representation + decoder”；与 LAD 相比，它更突出 geometry-aware 的先验。

[X-Sim](https://arxiv.org/abs/2505.07096) 代表了另一种重要思路：不是对齐动作，而是对齐**物体变化**。它从 RGBD human video 中重建 photorealistic simulation，跟踪 object trajectory，并把 object motion 作为 dense, transferable signal 来定义 reward。这个结果的意义很大，因为它表明：对于明显不同的本体，人类动作轨迹本身可能不可迁移，但**物体应该如何变化**往往是更稳健的共享目标。

[LAP](https://arxiv.org/abs/2602.10556) 则走得更远：直接把低层 robot action 用自然语言表示，使 action supervision 与 vision-language model 的输入输出分布对齐，从而实现 zero-shot cross-embodiment transfer。它的重要启发是：shared action interface 甚至可以是**语言化的动作表示**，而不一定必须是连续控制变量。

此外，[Contact-conditioned learning of locomotion policies](https://arxiv.org/abs/2408.00776) 也很值得注意。它虽然不是严格意义上的多本体论文，但它明确提出 contact-conditioned goal representation 可以作为单一低层策略的通用目标表达。这对 future cross-embodiment locomotion / loco-manipulation 很有借鉴意义，因为 contact 往往比 velocity 或 joint target 更接近任务本质。

总的来看，这一类工作正在共同回答一个根本问题：

> 如果想让能力跨身体迁移，动作应该定义在 joint、contact、object、skill，还是 language 这一层？

这也是当前 cross-embodiment 研究最有可能产生突破的地方。

---

## 6. Dexterous hands 与细粒度 manipulation：跨本体最难、但也最有价值的子问题

在 manipulation 领域，最难的跨本体问题并不是机械臂之间的迁移，而是：

- anthropomorphic hand 与 robot hand 之间
- 不同 dexterous hand 之间
- dexterous hand 与 parallel-jaw gripper 之间

由于接触模式、自由度、指间协同和 grasp manifold 差异极大，这一子问题比 locomotion 更具挑战性。

[Object-Centric Dexterous Manipulation from Human Motion Data](https://arxiv.org/abs/2411.04005) 说明，人类手部运动数据中更稳定可迁移的部分，未必是手指本身的动作，而可能是 object-centric 的交互结构。这个观察与 X-Sim 形成了呼应：在 embodiment gap 足够大时，物体运动与接触关系往往比 raw body motion 更值得迁移。

[Latent Action Diffusion](https://arxiv.org/abs/2506.14608) 则展示了通过 contrastive latent action space，把 human hand、robotic hands 和 parallel gripper 的动作对齐起来的可能性。它说明 dexterous manipulation 的跨本体学习，未必非要先统一所有 action dimensions，而可以通过 latent semantics 进行对齐。

[Cross-Hand Latent Representation for Vision-Language-Action Models](https://arxiv.org/abs/2603.10158) 进一步将这种思想推进到 VLA setting：在不同手型之间构造共享 latent representation，以支持跨手型的视觉-语言-动作建模。[DexFormer](https://arxiv.org/abs/2602.08278) 则直接朝 shared policy 方向推进，试图用 history-conditioned transformer 实现 heterogeneous hands 之间的 manipulation transfer。

[CEDex](https://arxiv.org/abs/2509.24661) 的重要性在于它把“human-like contact representation”引入 cross-embodiment grasp generation，从而强调：接触结构本身可能比手型更稳定。[Cross-embodied Co-design for Dexterous Hands](https://arxiv.org/abs/2512.03743) 更进一步，把 cross-embodiment 问题从控制迁移扩展到了 morphology-control co-design：如果目标是某类 manipulation family，那么也许 hand design 本身就该作为变量进入优化。

这一子方向目前仍处于快速发展阶段。它的意义不仅在于 dexterous hands 本身，更在于它逼迫研究者直面 cross-embodiment 的本质难点：当 action space 和 contact topology 都显著变化时，**到底该在什么层上做迁移**。

---

## 7. Teleoperation、数据采集系统与 embodiment gap 缩小

很多 cross-embodiment 方法之所以成立，不只是因为模型设计得好，还因为它们拥有**更好对齐的数据**。因此，teleoperation 和数据采集系统是这个方向不可忽略的一部分。

在人形 whole-body 控制里，[TWIST](https://arxiv.org/abs/2505.02833) 与 [TWIST2](https://arxiv.org/abs/2511.02832) 提供了可扩展 whole-body imitation data collection 系统；[HOMIE](https://arxiv.org/abs/2502.13013)、[TRILL](https://arxiv.org/abs/2309.01952)、[ACE](https://arxiv.org/abs/2408.11805)、[Open-TeleVision](https://arxiv.org/abs/2407.01512) 则从 exoskeleton、沉浸式视觉反馈、whole-body teleoperation 等角度缩小 human-humanoid gap。

这些系统工作的学术贡献，不应仅仅理解为“帮忙采数据”。更准确地说，它们在改变 cross-embodiment 学习的可行边界：如果 human demonstration 能更接近 robot embodiment，那么 learning problem 会从“从极大 gap 中恢复可迁移结构”，变成“从较小 gap 中做适配”。这也是为什么 HumanoidExo 这类系统工作在理论上同样重要。

因此，teleoperation 相关工作在 related work 中应被视为：

> cross-embodiment 学习的基础设施

而不只是工程配套。

---

## 8. 数据集、benchmark 与 scaling law：如何定义“真的跨本体”

随着越来越多工作声称具备 cross-embodiment 能力，一个关键问题变成：

> 什么样的 benchmark 和 evaluation protocol，才足以支撑这种 claim？

在多本体 manipulation 数据方面，[RoboMIND](https://arxiv.org/abs/2412.13877) 提供了在统一平台与标准协议下采集的 multi-embodiment dataset，覆盖 Franka、UR5e、双臂平台和带双灵巧手的 humanoid，同时还包含 failure demonstrations 和 digital twin environment。它的意义在于：不同 embodiment 的数据不再只是“拼起来”，而是在统一协议下形成更可比较的 benchmark。

在人形数据方面，[Humanoid-X / UH-1](https://arxiv.org/abs/2412.14172) 体现了“从海量 human video 提取 humanoid control data”的路线，[PHUMA](https://arxiv.org/abs/2510.26236) 则进一步指出：单纯从 human video 直接 retarget 会产生大量物理伪影，例如 floating、penetration、foot skating，因此需要 physics-constrained retargeting 和 physically grounded curation。[Humanoid Everyday](https://arxiv.org/abs/2510.08807) 则从 open-world humanoid manipulation 的角度，提供了更丰富任务、多模态输入和 cloud-based evaluation。相比以往只关注机械臂的 benchmark，这些工作为 humanoid cross-embodiment 研究打下了更现实的实验基础。

在 benchmark 设计层面，[AnyBody](https://arxiv.org/abs/2505.14986) 代表了对 embodied model 跨本体评测协议的进一步抽象；而在 scaling 分析层面，[Towards Embodiment Scaling Laws in Robot Locomotion](https://arxiv.org/abs/2505.05753) 则第一次系统回答了：

> 增加 training embodiments 是否比增加单一本体的数据量更有效？

该工作通过程序化生成约 1000 个 varied embodiments，发现扩大 embodiment diversity 在 unseen embodiment generalization 上比单纯扩数据量更有效，并在真实 Go2 与 H1 上展示了 zero-shot transfer。沿着同一条线，[Multi-Embodiment Locomotion at Scale with extreme Embodiment Randomization](https://arxiv.org/abs/2509.02815) 则进一步把 URMA 思想推向更大规模的 embodiment randomization。

这些 benchmark 与 scaling 工作的重要意义在于：

- 它们帮助社区区分“弱 transfer”与“强 transfer”
- 它们迫使研究者说明：自己的方法是否真正面对 unseen embodiment，而不是只在同一分布内插值
- 它们为未来研究提供了更系统的问题定义与实验标准

---

## 9. Morphology-aware 学习与结构先验：身体信息该如何进入模型？

除了共享 policy、共享数据和统一接口之外，另一条重要主线是：

> 身体结构本身是否应被显式编码进模型？

这条线可以追溯到 [NerveNet](https://arxiv.org/abs/1810.09759)，它通过 graph neural network 让策略感知机器人身体图结构。虽然不是为 cross-embodiment 明确提出，但它奠定了 morphology-aware policy 的思想基础。

在 transformer 时代，[Body Transformer](https://arxiv.org/abs/2408.06316) 明确指出 vanilla transformer 没有充分利用机器人身体结构，因此引入 body graph 与 masked attention，把 embodiment 作为 inductive bias 注入策略学习中。[Structure-Aware Transformer Policy for Inhomogeneous Multi-Task Reinforcement Learning](https://openreview.net/forum?id=fy_XRVHqly) 则从 inhomogeneous task / action dimension setting 出发，探索了结构感知 transformer 在不同 action/state 维度下的迁移能力。

最近的 [GCNT](https://arxiv.org/abs/2505.15211) 与 [McARL](https://arxiv.org/abs/2505.18418) 代表了 morphology-aware transfer 在 quadrupedal locomotion 等任务中的进一步发展：前者强调 graph-transformer policy，后者强调 morphology-control-aware conditioning。更进一步，[Articulated-Body Dynamics Network Improves Policy Learning for Diverse Robotic Systems](https://arxiv.org/abs/2603.19078) 则把“结构先验”从 link connectivity 推向了 dynamics prior：通过模仿 articulated body algorithm 的惯量传播结构，把动力学传播规律直接嵌入策略网络。

这一类工作的贡献在于，它们将 cross-embodiment 问题从“多本体数据混训”提升到了“如何把身体知识变成 inductive bias”。对于未来 humanoid/biped shared policy，这一点尤其关键，因为高自由度本体之间的差异，不只是 observation / action 维数不同，更在于动力学耦合和运动传播模式不同。

---

## 10. 小结：当前 Related Work 的整体格局与空白

综合来看，cross-embodiment robotics learning 已经形成了较清晰的研究版图：

第一，**多本体预训练和通用模型**已经证明“跨本体共享”具有现实价值，Open X-Embodiment、Octo、CrossFormer、Being-H0.5、GR00T、Gemini Robotics 等工作构成了这一方向的大背景。

第二，**shared policy / one-policy** 在 locomotion 尤其是 humanoid / biped locomotion 上已经出现了可信的实证进展。URMA、H-Zero、XHugWBC 等工作说明，跨本体共享策略不再只是概念，但它们大多仍然依赖不同程度的 morphology conditioning、low-level tuning 或 limited transfer regime。

第三，**human-to-robot / human-to-humanoid** 正在成为最重要的数据来源方向。MIR、XIRL、WHIRL、Humanoid Policy、HumanX、ZeroWBC 等工作表明，人类数据不只是便宜的数据源，更可能是跨本体学习中的“任务母语”。

第四，**统一接口与 latent action** 是当前最关键的瓶颈与机会所在。CEI、LAD、OPFA、X-Sim、LAP 等工作共同表明：如果不能找到合适的共享动作/表示层，单纯混合多本体数据往往难以真正解决 embodiment gap。

第五，**benchmark 与 scaling law** 开始让这个方向走向更严格的科学化。RoboMIND、Humanoid-X、PHUMA、Humanoid Everyday、AnyBody 以及 embodiment scaling law 相关工作，让研究者能够更系统地判断哪些结论是真正成立的，哪些只是弱设定下的局部成功。

但与此同时，这一方向仍存在几个突出的研究空白：

- 很多论文提出 shared policy，却没有清晰解释“到底共享的是什么”
- 很多 human-to-robot 方法证明人类数据有用，但较少系统比较不同中间接口
- 很多跨 humanoid 结果集中在 locomotion，whole-body manipulation 仍显著滞后
- 很多看似强的 transfer 结果，仍然依赖 body-specific low-level controller、reward tuning 或 environment engineering
- 严格意义上的 unseen embodiment、zero-shot、real-world whole-body transfer 依然稀缺

因此，未来真正有潜力的研究方向，很可能集中在以下几个问题上：

- shared policy 与 embodiment-specific execution 的边界应该如何划分？
- 最优的 unified interface 应定义在 joint、contact、object、skill 还是 language 层？
- human prior 在何种层次最值得迁移：motion、skill、progress、contact，还是 object dynamics？
- benchmark 应如何设计，才能真正区分“插值式泛化”和“跨本体迁移”？

从这个意义上说，cross-embodiment 的核心已经不再只是“能不能迁移”，而是：

> 如何精确刻画哪些能力应当独立于身体存在，哪些能力必须通过身体来实现。

---

## 可直接引用的一手来源

- [Open X-Embodiment / RT-X](https://robotics-transformer-x.github.io/)
- [Octo](https://arxiv.org/abs/2405.12213)
- [CrossFormer](https://arxiv.org/abs/2408.11812)
- [Being-H0.5](https://arxiv.org/abs/2601.12993)
- [GR00T N1](https://arxiv.org/abs/2503.14734)
- [Gemini Robotics](https://arxiv.org/abs/2503.20020)
- [Gemini Robotics 1.5](https://arxiv.org/abs/2510.03342)
- [One Policy to Run Them All](https://arxiv.org/abs/2409.06366)
- [HugWBC](https://arxiv.org/abs/2502.03206)
- [H-Zero](https://arxiv.org/abs/2512.00971)
- [XHugWBC](https://arxiv.org/abs/2602.05791)
- [Humanoid Policy ~ Human Policy](https://arxiv.org/abs/2503.13441)
- [HumanoidExo](https://arxiv.org/abs/2510.03022)
- [HumanX](https://arxiv.org/abs/2602.02473)
- [ZeroWBC](https://arxiv.org/abs/2603.09170)
- [MIR](https://arxiv.org/abs/2103.09016)
- [XIRL](https://arxiv.org/abs/2106.03911)
- [WHIRL](https://arxiv.org/abs/2207.09450)
- [XSkill](https://arxiv.org/abs/2307.09955)
- [UniSkill](https://arxiv.org/abs/2505.08787)
- [R+X](https://arxiv.org/abs/2407.12957)
- [CEI](https://arxiv.org/abs/2601.09163)
- [Latent Action Diffusion](https://arxiv.org/abs/2506.14608)
- [One-Policy-Fits-All](https://arxiv.org/abs/2603.14522)
- [X-Sim](https://arxiv.org/abs/2505.07096)
- [LAP](https://arxiv.org/abs/2602.10556)
- [Contact-conditioned learning of locomotion policies](https://arxiv.org/abs/2408.00776)
- [Cross-Hand Latent Representation for Vision-Language-Action Models](https://arxiv.org/abs/2603.10158)
- [DexFormer](https://arxiv.org/abs/2602.08278)
- [CEDex](https://arxiv.org/abs/2509.24661)
- [RoboMIND](https://arxiv.org/abs/2412.13877)
- [Humanoid-X / UH-1](https://arxiv.org/abs/2412.14172)
- [PHUMA](https://arxiv.org/abs/2510.26236)
- [Humanoid Everyday](https://arxiv.org/abs/2510.08807)
- [AnyBody](https://arxiv.org/abs/2505.14986)
- [Towards Embodiment Scaling Laws in Robot Locomotion](https://arxiv.org/abs/2505.05753)
- [Body Transformer](https://arxiv.org/abs/2408.06316)
- [Structure-Aware Transformer Policy for Inhomogeneous Multi-Task Reinforcement Learning](https://openreview.net/forum?id=fy_XRVHqly)
- [GCNT](https://arxiv.org/abs/2505.15211)
- [McARL](https://arxiv.org/abs/2505.18418)
- [Articulated-Body Dynamics Network Improves Policy Learning for Diverse Robotic Systems](https://arxiv.org/abs/2603.19078)
- [NerveNet](https://arxiv.org/abs/1810.09759)
