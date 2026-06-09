# Deep Read 01: One Policy to Run Them All

Paper:

- [One Policy to Run Them All: an End-to-end Learning Approach to Multi-Embodiment Locomotion](https://arxiv.org/abs/2409.06366)
- Project page: [nico-bohlinger.github.io/one_policy_to_run_them_all_website](https://nico-bohlinger.github.io/one_policy_to_run_them_all_website/)
- Code: [github.com/nico-bohlinger/one_policy_to_run_them_all](https://github.com/nico-bohlinger/one_policy_to_run_them_all)

Primary sources used for this note:

- PMLR / paper abstract and metadata: [PMLR page](https://proceedings.mlr.press/v270/bohlinger25a.html)
- Paper PDF: [PDF](https://www.ias.informatik.tu-darmstadt.de/uploads/Team/NicoBohlinger/one_policy_to_run_them_all.pdf)
- Project page summary and architecture description: [Project page](https://nico-bohlinger.github.io/one_policy_to_run_them_all_website/)

## 1. One-sentence summary

This paper proposes **URMA (Unified Robot Morphology Architecture)**, a morphology-agnostic encoder-decoder policy that learns a **single locomotion policy** across many legged embodiments and transfers to unseen robots in simulation and to real quadrupeds.

## 2. What problem is it solving?

This paper targets a very concrete question:

> Can we train one locomotion policy across heterogeneous legged embodiments instead of training one policy per robot?

The target application is **low-level locomotion control** for:

- quadrupeds
- humanoids
- bipeds
- hexapods

The claim is stronger than ordinary multi-task learning on one morphology family because the authors explicitly want:

- multiple morphology classes
- varying numbers of joints
- zero-shot or few-shot transfer to unseen embodiments

This is an important paper because it moves from:

- `one policy for many quadrupeds`

to:

- `one policy for many legged body plans`

## 3. Problem setting and strength of claim

### What is strong

- It is genuinely **multi-embodiment**, not just multi-task on one robot.
- It uses **16 simulated robots** from **3 morphology families**:
  - `9 quadrupeds`
  - `5 humanoids`
  - `1 biped`
  - `1 hexapod`
  Source: paper Sec. 6 and Appendix A.
- It evaluates **zero-shot transfer** to withheld robots, including:
  - `Unitree A1`
  - `MAB Silver Badger`
  Source: paper Sec. 6, zero-shot and few-shot transfer experiments.
- It deploys the same policy zero-shot on **real quadrupeds**, including an unseen one.
  Source: paper Sec. 6, real-world deployment.

### What is weaker than it may first appear

- The paper is about **locomotion only**, not general control.
- Real-world deployment is on **quadrupeds**, not humanoids.
- The strongest humanoid claim is still in simulation.
- The authors explicitly admit zero-shot transfer to embodiments **far outside the training distribution** remains difficult.
  Source: paper discussion and concluding limitations.

So this is a strong paper for **cross-embodiment locomotion**, but not yet evidence that one policy can robustly solve general humanoid whole-body behavior across unseen bodies.

## 4. Pipeline

URMA has a clean 4-stage pipeline.

### Step 1: Split the observations

The observation is split into:

- `joint-specific observations`
- `feet-specific observations`
- `general observations`

For locomotion, the split is:

- joint-specific observations:
  - joint position
  - joint velocity
  - previous action
- feet-specific observations:
  - contact flag
  - time since last foot contact
- general observations:
  - torso linear velocity
  - angular velocity
  - velocity commands
  - gravity orientation
  - height
  - PD controller parameters
  - robot mass and dimensions

Source: Appendix A, “Environment Details”.

### Step 2: Encode morphology-specific parts with descriptions

Each joint gets:

- joint-specific observation `o_j`
- joint description vector `d_j`

The joint description includes properties such as:

- relative 3D position
- rotation axis
- number of direct child joints
- nominal position
- torque / velocity limits
- damping / inertia / stiffness / friction
- control range
- robot-level attributes such as mass and dimensions

Source: main method section and Appendix A.

These are encoded separately and fused through a **simple attention encoder** with a learnable temperature.

### Step 3: Build a shared latent controller

The encoder aggregates all joints into a single latent representation for joints, similarly for feet, then concatenates them with general observations and passes them through a shared core network to produce an `action latent`.

Source: method section and project page architecture summary.

### Step 4: Decode back into robot-specific actions

The universal decoder uses:

- the action latent
- encoded joint descriptions
- joint latent information

to produce per-joint action distributions.

Source: method section and project page architecture summary.

This is the crucial architectural idea:

> shared abstract locomotion control in the middle, robot-specific realization only at the morphology-conditioned encoder/decoder boundary.

## 5. What is shared, and what is embodiment-specific?

This is the single most important question for your thesis.

### Shared

- a single architecture
- a single core locomotion controller
- a shared latent action space
- a shared morphology-agnostic encoder/decoder design
- shared training over all robots with PPO

### Embodiment-specific

- joint description vectors
- feet description vectors
- robot-specific observation sets
- robot-specific control gains and scaling factors
- reward coefficients
- domain randomization settings
- environment definitions and XML assets

The repository itself confirms that adding a new robot still requires editing:

- reward coefficients
- controller gains
- scaling factor
- domain randomization ranges
- environment metadata

Source: code repository README and setup instructions for adding new robots.

So the paper is **not** "absolutely one policy with zero robot-specific work".  
It is better described as:

> one shared locomotion policy architecture plus robot-specific embodiment metadata and low-level environment/controller tuning.

That distinction matters a lot.

## 6. Observation and action design

### Observation design

The paper’s observation design is strong because it explicitly separates:

- what varies with morphology
- what remains globally meaningful

This is a very reusable idea for cross-embodiment work.

### Action design

The policy action is not a world-level object-centric or contact-centric interface.  
It remains a **low-level per-joint action distribution**, decoded from the shared latent.

In the environment, the final policy action is used as a scaled position offset:

- `q_target = q_nominal + sigma_a * a`

under a PD controller.

Source: Appendix A, “Environment Details”.

This means the paper still operates in a **robot-specific actuation regime**, even though the latent controller is shared.

## 7. Data and training recipe

### Data source

- fully simulation-driven locomotion data
- CPU-based MuJoCo
- 48 parallel environments from 16 robots x 3 environments

Source: Sec. 6, training setup.

### Training recipe

- PPO
- JAX implementation
- RL-X codebase
- domain randomization for sim-to-real

Source: Sec. 6 and implementation details.

This is not a dataset-pretraining paper.  
It is an **end-to-end RL paper** with shared multi-embodiment training.

## 8. Baselines

The comparison is meaningful because the baselines represent two natural alternatives.

### Multi-head baseline

- shared core
- morphology-specific heads
- same-morphology observations aligned into a consistent order

Weakness:

- adding new joints or new morphologies requires new heads or head expansion

Source: Sec. 6 baseline setup.

### Padding baseline

- pad observations and actions to a common length
- add one-hot task ID

Weakness:

- a new robot behaves like a new task
- hard to transfer across differently structured observations/actions

Source: Sec. 6 baseline setup.

### Single-robot training

- one policy per robot
- used as another reference point

## 9. Results and evaluation protocol

### Training setting

- train on all 16 robots simultaneously
- compare to single-robot training and MTRL baselines
- 100M steps per robot
- 5 seeds with 95% confidence intervals

Source: Sec. 6, training and evaluation protocol.

### Main results

1. **Training efficiency**
   URMA and multi-head learn much faster than single-robot training, and URMA reaches higher final performance than the multi-head baseline.
   Source: Sec. 6, main learning curve discussion.

2. **Zero-shot transfer to Unitree A1**
   URMA transfers well to a withheld quadruped whose embodiment is similar to training quadrupeds.
   Source: Sec. 6, zero-shot transfer experiment.

3. **Zero-shot + few-shot transfer to MAB Silver Badger**
   This is a more interesting OOD embodiment because it has:
   - an extra spine joint
   - no feet observations
   URMA is the only one that achieves a good gait after fine-tuning and handles missing feet observations better.
   Source: Sec. 6, OOD embodiment transfer discussion.

4. **Robustness to observation dropout**
   URMA is more robust when feet observations are removed.
   Source: Sec. 6, foot observation ablation.

5. **Real-robot zero-shot deployment**
   The same URMA policy transfers zero-shot to:
   - Unitree A1
   - MAB Silver Badger
   - MAB Honey Badger
   including one unseen real robot.
   Source: Sec. 6, real-world deployment section.

## 10. Failure modes and limitations

The paper is refreshingly clear about its limitations.

### Limitation 1: transfer still depends heavily on data coverage

The authors explicitly say zero-shot transfer to embodiments that are **completely outside the training distribution** remains problematic.
Source: paper discussion and concluding limitations.

This is the single most important caveat.

### Limitation 2: no exteroceptive sensing

They omit exteroceptive sensors, which limits use in complex environments.
Source: paper discussion and future work.

### Limitation 3: humanoid real-world transfer is not shown

They note that humanoids were not tested in the real world.
Source: paper discussion and future work.

### Limitation 4: still needs robot-specific environment/controller tuning

Although the network is shared, the overall system is not plug-and-play for arbitrary new bodies.

This matters for your research because:

> the shared policy claim is stronger at the representation level than at the full deployment stack level.

## 11. What this paper contributes to your project

### The most useful idea

The most reusable contribution is not simply "one policy".

It is this design principle:

> Split the system into robot-specific structured observations + morphology descriptions -> shared latent controller -> universal morphology-conditioned decoder.

This gives you a very clear template for thinking about:

- what belongs in the shared policy
- what belongs in embodiment conditioning
- where the boundary between shared and specific should live

### What it validates

This paper validates that:

- shared low-level locomotion policies across different body plans are possible
- morphology-agnostic encoder/decoder design is better than simple padding
- zero-shot transfer to moderately novel embodiments is realistic

### What it does **not** yet validate

It does **not** prove that:

- one policy can control arbitrary unseen bodies robustly
- shared control extends naturally from locomotion to manipulation
- shared policy can eliminate embodiment-specific low-level controller tuning

## 12. My judgment

### Must-read or not?

`Must-read`

If your topic is anything like:

- one policy for many bodies
- morphology-aware policy transfer
- cross-embodiment locomotion
- shared encoder/decoder architectures

then this paper is foundational.

### Which bucket does it belong to?

- `policy transfer`
- `cross-embodiment locomotion / whole-body control`
- `morphology-aware learning`

### Best one-line takeaway

URMA is one of the clearest examples showing that a **shared locomotion controller** can emerge across heterogeneous legged robots when morphology-specific information is handled through structured descriptions and a universal encoder-decoder interface.

## 13. Questions left open for your own research

This paper naturally leads to the following questions:

1. Can the URMA idea scale from locomotion to **whole-body loco-manipulation**?
2. Is the best shared interface still **joint-centric**, or should it become **contact-centric** or **object-centric**?
3. Can we reduce the remaining robot-specific engineering burden by replacing hand-tuned controller parameters with learned embodiment adapters?
4. How far can zero-shot transfer go when the new body is truly out-of-distribution, not just moderately novel?

## 14. Five-sentence final output

1. The paper claims that a single locomotion policy architecture can be trained across heterogeneous legged embodiments and transfer to unseen robots.  
2. This claim is fairly strong for locomotion because it includes 16 robots, withheld embodiments, and real quadruped deployment, but it is still weaker than general cross-embodiment control.  
3. What is truly shared is the latent locomotion controller and morphology-agnostic encoder/decoder design; what remains specific is robot metadata, controller tuning, rewards, and deployment configuration.  
4. The main bottleneck is still out-of-distribution embodiment transfer and the dependence on robot-specific low-level details.  
5. For your project, this paper is most valuable as a template for how to architect the boundary between shared policy and embodiment-specific realization.
