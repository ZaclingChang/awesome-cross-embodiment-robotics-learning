# Paper Note Template for Cross-Embodiment Robotics Learning

## 0. Basic Info

- Title:
- Authors:
- Venue / Year:
- URL:
- Project page:
- Code:
- Taxonomy bucket:
  - problem formulation
  - foundation
  - policy transfer
  - representation transfer
  - human-to-robot
  - locomotion / whole-body control
  - manipulation / visual imitation
  - interface / retargeting
  - benchmark / dataset
  - scaling / morphology-aware learning

## 1. One-Sentence Summary

用一句话说清楚：

> 这篇论文想解决什么问题，用什么核心方法，在什么 setting 下验证？

## 2. Problem Definition

- Is it really cross-embodiment?
- Human-to-robot, human-to-humanoid, humanoid-to-humanoid, or general multi-embodiment?
- Main task:
  - locomotion
  - loco-manipulation
  - whole-body control
  - teleoperation
  - benchmark
  - representation / interface
  - policy transfer
  - morphology transfer

## 3. Embodiments

- Training embodiments:
- Testing embodiments:
- Unseen embodiments:
- Humanoid / biped / other robot types:

## 4. What Is Shared vs Embodiment-Specific

### Shared

- backbone
- policy
- latent skill space
- action interface
- world model
- behavior prior

### Embodiment-specific

- decoder
- action head
- morphology token
- low-level controller
- IK / WBC / MPC
- prompt / adapter

## 5. Observation and Action Interface

### Observation

- proprioception
- ego-centric vision
- third-person vision
- tactile
- language
- morphology parameters

### Action / Interface

- raw joint targets
- torques
- body-part goals
- contact states
- object-centric goals
- latent action
- language-action

## 6. Data and Training

- Data source:
  - human egocentric video
  - human whole-body motion
  - teleoperation
  - simulation
  - real robot
  - synthetic retargeting
- Training recipe:
  - BC
  - RL
  - diffusion
  - world model
  - pretraining + finetuning
  - distillation

## 7. Evaluation Protocol

- Seen embodiment?
- Unseen embodiment?
- Zero-shot?
- Few-shot?
- Sim-only?
- Real robot?
- Same tasks or new tasks?

## 8. Main Results

- Strongest quantitative result:
- Real robot evidence:
- What transfer actually worked:
- What did not work:

## 9. Failure Modes and Limitations

- Perception gap:
- Contact / dynamics gap:
- Morphology mismatch:
- Data bottleneck:
- Weak evaluation:

## 10. Relevance to My Project

### Useful ideas

- 

### Not directly useful

- 

### What gap remains

- 

## 11. Final Judgment

- Must-read / useful / skimmable:
- Which chapter of my thesis does it belong to?
- Should it appear in:
  - related work
  - baseline
  - benchmark
  - methodology inspiration
  - discussion
- Which bucket in the repository should it be filed under?
