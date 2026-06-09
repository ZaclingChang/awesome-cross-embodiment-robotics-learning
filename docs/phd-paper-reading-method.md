# PhD Paper Reading Method for Cross-Embodiment Robotics

这不是“如何快速看完论文”的技巧文档，而是一套更像博士生使用的**固定精读方法**。

目标不是记住更多论文，而是持续沉淀下面 4 类能力：

1. `问题判断力`
   这篇论文到底解决了什么，claim 强不强。
2. `方法地图感`
   这个方向现在有哪些主流设计空间。
3. `实验敏感度`
   什么评测是强的，什么评测其实很弱。
4. `研究问题提炼能力`
   从 related work 中提炼出自己的 research questions。

---

## 0. 读论文之前先明确你的目标

不要在“没有目标”的情况下读论文。

先选定你这次阅读属于哪一种：

- `建立地图`
  我还不熟悉这个方向，先看全局。
- `方法精读`
  我要搞懂某一类方法，例如 shared policy 或 latent action。
- `找实验设计`
  我想知道 benchmark、baseline、评测协议怎么做。
- `找研究空白`
  我想从几十篇论文里提炼自己的问题。
- `准备开题/组会`
  我要把这批论文转化成可讲述的叙事。

如果目标不明确，你很容易变成“读完有印象，但没有产出”。

---

## 1. 博士生精读的总原则

### 原则 1：先判断问题，再看方法

不要先问：

- 它用了什么网络
- loss 怎么写
- 结构是不是很复杂

先问：

- 它在解决什么问题？
- 这个问题是真问题，还是被包装过的问题？
- 这个 setting 和我的问题是否同一个层次？

### 原则 2：把论文当成 claim，不当成结论

每篇论文首先是一个 claim：

> 在某个 setting 下，用某种方法，取得了某种结果。

你要判断的是：

- claim 有多强
- claim 成立的前提是什么
- claim 能不能推广到你关心的 setting

### 原则 3：永远分清 shared 和 specific

cross-embodiment 论文里最容易被忽略的问题就是：

> 到底什么被共享了，什么没有被共享？

很多论文表面上在讲“一个统一方法”，本质上其实是：

- shared prior + robot-specific controller
- shared backbone + embodiment-specific decoder
- shared representation + heavy retargeting

这不是坏事，但必须说清楚。

### 原则 4：评测协议比 demo 更重要

demo 再酷，也不能替代强评测。

你要优先关心：

- seen embodiment 还是 unseen embodiment
- zero-shot 还是 few-shot
- sim-only 还是 sim-to-real
- same task family 还是 new task
- same morphology family 还是真正 morphology shift

---

## 2. 固定四阶段阅读法

## Stage A: 读前定位

这一阶段只花 3-5 分钟。

你要先写下这 5 个词：

- `bucket`
- `problem`
- `claim`
- `setting`
- `relevance`

然后快速回答：

1. 这篇论文属于哪个 taxonomy bucket？
2. 它的核心问题是什么？
3. 它最强的 claim 是什么？
4. 它的实验 setting 大概是什么？
5. 它和我的课题关系大吗？

如果这里都答不出来，不要直接进入细节。

---

## Stage B: 第一遍阅读，抓主线

建议只读：

- title
- abstract
- intro
- method overview figure
- experiment setup
- conclusion

这一遍不要抠公式，目标只有一个：

> 用自己的话复述这篇论文。

你至少要能说出：

- 它解决什么问题
- 为什么这个问题重要
- 它的方法大概是什么
- 它在哪些 setting 下验证
- 它的 claim 大不大

如果第一遍读完还不能复述，先不要看细节。

---

## Stage C: 第二遍阅读，拆方法

这一遍重点看结构，不是看花哨。

必须回答下面这些固定问题：

### 1. 问题边界

- 它到底在解决什么问题？
- 应用场景是什么？
- 是真正 cross-embodiment，还是同一本体多任务？
- 是 human-to-robot、robot-to-robot，还是 morphology-aware transfer？

### 2. Pipeline

- 它的 pipeline 是怎样的？
- 各模块分别干什么？
- 哪个模块是最关键的创新点？

### 3. Shared vs Specific

- 什么是可以 shared 的？
- 什么是 embodiment-specific 的？
- 它的“统一”到底统一到什么层？

### 4. Observation / Action

- observation 是什么？
- action 是什么？
- 有没有中间接口：
  - latent action
  - body-part command
  - contact plan
  - object-centric representation
  - language-action

### 5. Data / Training

- 数据怎么得到？
- human video / teleop / sim / real robot / synthetic retargeting？
- training recipe 是什么？
  - BC
  - RL
  - diffusion
  - world model
  - pretrain + finetune
  - distillation

### 6. Results / Evaluation

- 结果最好的是哪一项？
- evaluation protocol 是什么？
- unseen embodiment 是否真的存在？
- 零样本还是少样本？
- real robot 是否验证？

### 7. Failure Modes

- 它失败在哪里？
- perception
- embodiment gap
- contact dynamics
- action abstraction
- retargeting artifacts
- body-specific controller dependence

---

## Stage D: 第三遍阅读，做判断

这一遍不是“继续看懂”，而是做研究判断。

你要回答 5 个 synthesis 问题。

### A. 问题边界

- 哪些 claim 已经被验证过？
- 哪些 claim 只在弱 setting 下成立？
- 这个方向离真正强 claim 还有多远？

### B. 设计空间

- 它属于哪种方法路线？
- 这个路线相比其他路线的优缺点是什么？
- 它在整个 design space 里处于什么位置？

### C. 评价标准

- 这篇论文的 protocol 强不强？
- 如果我要做更强的实验，应该怎么改？

### D. 真正瓶颈

- 它最本质的瓶颈是什么？
- 是数据问题，还是接口问题，还是 low-level control 问题？

### E. 研究空白

- 这篇论文没有回答什么？
- 哪个关键问题被它绕开了？
- 这个空白值得不值得做成 research question？

---

## 3. 每篇论文最后必须产出的固定模板

每篇论文读完后，至少输出下面这 5 句话。

1. `这篇论文最强的 claim 是什么。`
2. `这个 claim 成立的 setting 有多强。`
3. `它真正共享的是什么，specific 的是什么。`
4. `它真正卡在哪里。`
5. `它对我的课题贡献了哪一块。`

如果你连这 5 句话都写不出来，说明还没真正读懂。

配合这个模板使用：

- [paper-note-template.md](paper-note-template.md)

---

## 4. 单篇笔记不够，还要做“跨论文综合”

博士生真正的进步，不在于单篇理解，而在于跨论文比较。

每读完一个 pack，强制做一次综合。

### 综合输出 1：方法对比表

列可以固定为：

- Paper
- Problem
- Shared component
- Embodiment-specific component
- Observation
- Action / Interface
- Data source
- Evaluation protocol
- Main limitation

### 综合输出 2：设计空间地图

例如：

- shared policy
- shared prior
- unified interface
- human prior
- morphology-aware structural prior

然后标注每篇论文属于哪一类。

### 综合输出 3：开放问题列表

每读完一个 pack，至少写 3 个 open problems。

例如：

- shared policy 到底共享到哪一层最合理？
- human video 里最 transferable 的信号是什么？
- locomotion 成熟了，manipulation 为什么还不成熟？
- interface 应该 object-centric 还是 contact-centric？

---

## 5. 博士生阅读最重要的 3 个习惯

### 习惯 1：不要追求“全懂”，先追求“会判断”

你不需要一开始就看懂所有公式和实现细节。

你更需要先学会判断：

- 问题是否重要
- claim 是否强
- 方法属于哪一类
- 瓶颈在哪里

### 习惯 2：论文不是知识点，是证据

每篇论文都只是一个证据点。

你的任务不是背诵论文，而是用这些证据点回答：

- 这个方向已经走到哪里了？
- 什么结论可以相信？
- 什么结论还不够稳？

### 习惯 3：读论文的终点是 research question

不要把阅读目标定成：

- “我把这篇看完了”

而要定成：

- “这篇论文让我更清楚自己该研究什么”

---

## 6. 一个建议的每周阅读节奏

### 周一

- 选 3-5 篇论文
- 先做 Stage A 和 Stage B

### 周二到周三

- 做 Stage C
- 把单篇笔记填到模板里

### 周四

- 做 Stage D
- 写 5 句话结论

### 周五

- 做跨论文综合
- 产出：
  - 1 张对比表
  - 1 段设计空间总结
  - 1 个研究问题草稿

如果你连续几周都这样做，related work 很快就会从“资料堆积”变成“研究判断”。

---

## 7. 什么时候可以停止继续读，转向做研究

当你满足下面 4 个条件，就应该开始转向问题定义和实验设计，而不是继续无限看 paper。

1. 你已经能把主流路线分成 4-6 类  
2. 你已经知道每类方法最典型的代表论文  
3. 你已经知道这个方向最常见的 failure modes  
4. 你已经能稳定写出 3 个 research questions  

到了这一步，继续读更多论文的边际收益会明显下降。

---

## 8. 一句话总结

博士生精读论文的核心不是：

> 把每一篇都看懂

而是：

> 持续把单篇论文转化成对问题边界、设计空间、评价标准、真实瓶颈和研究空白的判断。
