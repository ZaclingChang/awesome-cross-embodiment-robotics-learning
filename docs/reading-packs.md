# Reading Packs for Cross-Embodiment Robotics Learning

这份文档不是论文列表，而是“带目标的精读包”。

每个 reading pack 都服务于一个具体研究目的，例如：

- 我想快速建立全局地图
- 我想做 shared policy
- 我想做 human-to-robot transfer
- 我想做 unified interface
- 我想设计 benchmark

建议使用方式：

1. 先选一个最贴近当前问题的 pack  
2. 按建议顺序读  
3. 每篇论文都用 [paper-note-template.md](paper-note-template.md) 做记录  
4. 读完一整包之后，再写自己的 1 页总结  

---

## Pack 0: 7-Day Quick Start

适合：

- 刚进入这个方向
- 需要准备第一次组会
- 想先建立全局地图

### 阅读顺序

1. [Open X-Embodiment / RT-X](https://robotics-transformer-x.github.io/)
2. [Octo](https://arxiv.org/abs/2405.12213)
3. [Being-H0.5](https://arxiv.org/abs/2601.12993)
4. [Humanoid Policy ~ Human Policy](https://arxiv.org/abs/2503.13441)
5. [H-Zero](https://arxiv.org/abs/2512.00971)
6. [CEI](https://arxiv.org/abs/2601.09163)
7. [Towards Embodiment Scaling Laws in Robot Locomotion](https://arxiv.org/abs/2505.05753)

### 读完后你应该回答

- 什么算“真正的 cross-embodiment”
- 共享 backbone、共享 policy、共享 interface 分别是什么
- human data 在这个方向里的地位是什么
- locomotion 和 manipulation 哪个更成熟
- 未来最核心的瓶颈是 data、interface 还是 morphology gap

### 建议输出

- 一页“方向地图”
- 一页“我最感兴趣的 2 个切口”

---

## Pack 1: Shared Policy for Many Bodies

适合：

- 你要做 shared policy / one-policy
- 你关心 humanoid、biped、legged morphologies 的统一控制

### 阅读顺序

1. [One Policy to Run Them All: Towards an End-to-end Learning Approach to Multi-Embodiment Locomotion](https://openreview.net/forum?id=HVWusz2zv5)
2. [One Policy to Run Them All: an End-to-end Learning Approach to Multi-Embodiment Locomotion](https://arxiv.org/abs/2409.06366)
3. [LocoFormer](https://arxiv.org/abs/2509.23745)
4. [H-Zero](https://arxiv.org/abs/2512.00971)
5. [Scalable and General Whole-Body Control for Cross-Humanoid Locomotion](https://arxiv.org/abs/2602.05791)
6. [General Humanoid Whole-Body Control via Pretraining and Fast Adaptation](https://arxiv.org/abs/2602.11929)
7. [One Policy but Many Worlds](https://arxiv.org/abs/2505.18780)
8. [Learning to Get Up Across Morphologies: Zero-Shot Recovery with a Unified Humanoid Policy](https://arxiv.org/abs/2512.12230)

### 重点问题

- shared policy 真正共享的是 backbone、latent，还是 action head 之前的表征？
- 哪些方法依赖 morphology token，哪些依赖图结构，哪些依赖 pretraining？
- unseen embodiment 上的 transfer 是 zero-shot 还是 few-shot？
- 这些方法在 real robot 上有没有成立？

### 建议输出

- 一张“shared policy 设计空间”表
- 一段你自己的判断：
  `完全统一`、`共享主干 + adapter`、`共享接口 + robot-specific controller`
  你更看好哪种

---

## Pack 2: Human-to-Robot / Human-to-Humanoid Transfer

适合：

- 你想利用 human data
- 你关心 human video、egocentric data、retargeting、exoskeleton

### 阅读顺序

1. [Manipulator-Independent Representations for Visual Imitation](https://arxiv.org/abs/2103.09016)
2. [XIRL](https://arxiv.org/abs/2106.03911)
3. [WHIRL](https://arxiv.org/abs/2207.09450)
4. [Humanoid Policy ~ Human Policy](https://arxiv.org/abs/2503.13441)
5. [HumanoidExo](https://arxiv.org/abs/2510.03022)
6. [HumanX](https://arxiv.org/abs/2602.02473)
7. [ZeroWBC](https://arxiv.org/abs/2603.09170)

### 重点问题

- human data 里真正 transferable 的是什么：
  visual task structure、skill progress、object motion、whole-body contact，还是 raw motion
- retargeting 是必须的吗，还是可以绕开
- egocentric human video 和 exoskeleton data 各自解决什么问题
- 哪些 human prior 更适合 humanoid，哪些更适合 manipulation

### 建议输出

- 一张“human signal -> robot prior”映射图
- 一页总结：
  `human data 最适合用来学什么，不适合用来学什么`

---

## Pack 3: Unified Interfaces and Action Abstraction

适合：

- 你想做中间表示
- 你不满意 raw joint action 作为统一动作空间

### 阅读顺序

1. [XSkill](https://arxiv.org/abs/2307.09955)
2. [UniSkill](https://arxiv.org/abs/2505.08787)
3. [CEI](https://arxiv.org/abs/2601.09163)
4. [Latent Action Diffusion](https://arxiv.org/abs/2506.14608)
5. [One-Policy-Fits-All](https://arxiv.org/abs/2603.14522)
6. [X-Sim](https://arxiv.org/abs/2505.07096)
7. [Language-Action Pre-training Enables Zero-Shot Cross-Embodiment Transfer](https://arxiv.org/abs/2602.10556)
8. [Contact-conditioned learning of locomotion policies](https://arxiv.org/abs/2408.00776)

### 重点问题

- shared action / interface 应该定义在什么层：
  latent action、skill token、object motion、contact plan、language-action
- 哪种接口更适合 locomotion，哪种更适合 manipulation
- object-centric 和 body-centric 的边界在哪里
- action abstraction 是否一定需要 embodiment-specific decoder

### 建议输出

- 一张“接口层级图”
- 一页总结：
  `我认为最适合自己课题的 unified interface 是什么，为什么`

---

## Pack 4: Dex Hands and Fine-Grained Manipulation

适合：

- 你对多手型、多末端执行器、多灵巧手的 transfer 更感兴趣

### 阅读顺序

1. [Object-Centric Dexterous Manipulation from Human Motion Data](https://arxiv.org/abs/2411.04005)
2. [Latent Action Diffusion](https://arxiv.org/abs/2506.14608)
3. [Cross-Hand Latent Representation for Vision-Language-Action Models](https://arxiv.org/abs/2603.10158)
4. [DexFormer](https://arxiv.org/abs/2602.08278)
5. [CEDex](https://arxiv.org/abs/2509.24661)
6. [Cross-embodied Co-design for Dexterous Hands](https://arxiv.org/abs/2512.03743)

### 重点问题

- dexterous hand transfer 应该看 action、contact，还是 hand morphology
- grasp transfer 和 manipulation transfer 是不是同一个问题
- VLA 在多手型 setting 下到底学到的是语义，还是 action prior

### 建议输出

- 一页“dexterous cross-embodiment”的专题笔记
- 一张“contact-centric vs latent-action-centric”对比表

---

## Pack 5: Morphology-Aware Learning and Structural Priors

适合：

- 你想显式编码 body graph、geometry、dynamics
- 你想知道 morphology-aware 是否真的值得做

### 阅读顺序

1. [NerveNet](https://arxiv.org/abs/1810.09759)
2. [MY BODY IS A CAGE](https://arxiv.org/abs/2010.01856)
3. [Structure-Aware Transformer Policy for Inhomogeneous Multi-Task Reinforcement Learning](https://openreview.net/forum?id=fy_XRVHqly)
4. [Body Transformer: Leveraging Robot Embodiment for Policy Learning](https://arxiv.org/abs/2408.06316)
5. [GCNT: Graph-Based Transformer Policies for Morphology-Agnostic Reinforcement Learning](https://arxiv.org/abs/2505.15211)
6. [McARL](https://arxiv.org/abs/2505.18418)
7. [Multi-Loco](https://arxiv.org/abs/2506.11470)
8. [Articulated-Body Dynamics Network Improves Policy Learning for Diverse Robotic Systems](https://arxiv.org/abs/2603.19078)

### 重点问题

- morphology 是应该作为 token、graph，还是 dynamics prior 注入
- geometry-aware 和 dynamics-aware 有什么本质区别
- 哪些 structural prior 真正提升了 unseen embodiment transfer

### 建议输出

- 一张“morphology-aware 方法谱系图”
- 一页总结：
  `我是否需要显式 body encoding`

---

## Pack 6: Benchmark, Evaluation, and Scaling

适合：

- 你准备设计自己的 benchmark
- 你不确定论文里的 transfer claim 是否足够强

### 阅读顺序

1. [RoboMIND](https://arxiv.org/abs/2412.13877)
2. [Humanoid-X / UH-1](https://arxiv.org/abs/2412.14172)
3. [PHUMA](https://arxiv.org/abs/2510.26236)
4. [Humanoid Everyday](https://arxiv.org/abs/2510.08807)
5. [AnyBody](https://arxiv.org/abs/2505.14986)
6. [Towards Embodiment Scaling Laws in Robot Locomotion](https://arxiv.org/abs/2505.05753)
7. [Multi-Embodiment Locomotion at Scale with extreme Embodiment Randomization](https://arxiv.org/abs/2509.02815)

### 重点问题

- 什么样的 protocol 才能支撑 cross-embodiment claim
- seen / unseen embodiment 该怎么拆
- total data scale 和 embodiment diversity 应该怎么平衡
- benchmark 里最容易藏水分的地方是什么

### 建议输出

- 一张“评测协议 checklist”
- 一个你自己项目可用的 benchmark 设计草案

---

## Pack 7: If Your Goal Is a PhD Proposal

适合：

- 你准备开题
- 你要把方向压成 research questions

### 最小组合

1. Open X-Embodiment
2. Being-H0.5
3. Humanoid Policy ~ Human Policy
4. H-Zero
5. XHugWBC
6. CEI
7. Latent Action Diffusion
8. X-Sim
9. RoboMIND
10. Towards Embodiment Scaling Laws

### 读完后必须输出

1. `问题定义`
   你的 cross-embodiment 问题到底是 policy transfer、representation transfer，还是 interface learning？

2. `研究缺口`
   当前工作最缺的是：
   - 更严格评测
   - 更好的 interface
   - 更强 human prior
   - 更稳定的 shared policy
   - 更好的 morphology-aware adaptation

3. `研究问题`
   最后至少写出 3 个可落地 research questions。

---

## 建议的阅读节奏

- `第一次读`
  只抓问题定义、setting、claim
- `第二次读`
  抓方法细节，尤其是 shared / specific 边界
- `第三次读`
  抓评测协议和 failure mode

不要一次就试图“全懂”，你真正要积累的是：

> 对 design space、evaluation protocol、open problems 的判断力。
