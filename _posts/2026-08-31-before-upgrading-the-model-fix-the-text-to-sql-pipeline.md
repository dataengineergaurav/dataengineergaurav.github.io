---
layout: post
title: "Before Upgrading the Model, Fix the Text-to-SQL Pipeline"
date: 2026-08-31
topic: Analytics Delivery
summary: "A controlled study of modular in-context-learning text-to-SQL systems suggests that execution-feedback refinement should be tested before model upgrades. The practical lesson is not to copy a benchmark stack wholesale, but to evaluate models and pipeline modules as one governed system under accuracy"
description: "A production-focused interpretation of Jiayan Lin and co-authors\u2019 accuracy\u2013cost analysis of text-to-SQL pipelines, including deployment limits and a concrete framework for choosing between refinement, pipeline enrichment, candidate selection, and a stronger model."
---

# Before Upgrading the Model, Fix the Text-to-SQL Pipeline

When a text-to-SQL system produces disappointing answers, upgrading the language model is an obvious response. It is also an incomplete one.

A text-to-SQL product is not just a model. It is a pipeline that may retrieve examples, filter a schema, generate one or more queries, select a candidate, execute SQL, and attempt a correction. Each module can change accuracy, token consumption, latency, operational complexity, and failure modes.

In their preprint *Are These Modules Worth Their Cost?*, Jiayan Lin and co-authors examine that pipeline as a modular system rather than treating it as a single model call [1]. Their central finding is useful for analytics leaders: under their controlled evaluation, execution-feedback refinement was the only tested paradigm that improved execution accuracy across all four primary model backbones while maintaining consistently low incremental cost.

That does **not** establish a universally safe production architecture. It does provide a stronger starting hypothesis than “buy the best model available.”

## What the study actually tested

Lin et al. decomposed an in-context-learning text-to-SQL pipeline into five modules:

1. **Example retrieval** for selecting demonstrations.
2. **Schema linking** for narrowing the available tables and columns.
3. **Generation strategy**, including direct, chain-of-thought-enhanced, and decomposition-based generation.
4. **Candidate selection** over multiple generated queries.
5. **Refinement** after an initial query has been produced.

The authors implemented 17 paradigm-level configurations. For most experiments, they changed one module at a time while holding the other modules at trivial settings. Candidate selection used a matched five-candidate baseline so that the selector’s effect could be separated from the effect of generating more candidates.

The main analysis used 1,534 examples from the BIRD development set across four primary backbones. BIRD was introduced as a database-grounded text-to-SQL benchmark containing realistic database content and external knowledge requirements [2]. Lin et al. also transferred selected pipeline configurations to Spider, a primary cross-domain semantic-parsing benchmark [3], and validated their tiered guideline on five additional backbones [1].

The paper measured execution accuracy, input and output tokens, API cost, and incremental cost per execution-accuracy percentage point. Accuracy differences were evaluated with paired McNemar tests. This matters because a higher end-to-end score alone cannot reveal whether an expensive module contributed meaningful incremental value.

## The strongest first experiment: failure-gated refinement

The paper’s most consistent result concerns **R1, execution-feedback refinement**.

This mechanism first executes the generated SQL. It asks the model to rewrite the query only if execution returns an error or no rows. Lin et al. report gains of 1.83 to 4.89 execution-accuracy percentage points across the four primary backbones, with incremental cost below $0.30 per percentage point in every case [1]. Because the additional model call is failure-gated rather than mandatory, its average token overhead remained close to the baseline.

The contrast with other refinement methods is instructive. The paper reports that prompt-only self-correction was not significantly beneficial on one reasoning backbone and was more expensive where it did help. Agentic refinement improved results across the four primary backbones, but its incremental cost per accuracy point was substantially higher than failure-gated execution feedback [1].

The production lesson is narrower than “self-correction works.” It is this:

> Test whether a cheap, externally observed database signal can trigger a targeted repair before adding unconditional review or multi-agent loops.

Execution supplies information that was not available when the SQL was generated. A second prompt without new evidence may simply reproduce the original model’s blind spots.

## Why the other modules require backbone-specific evidence

Lin et al. found that the remaining module families were more dependent on model capability or reasoning behaviour.

### Schema linking may compensate for a weaker backbone

On GPT-4o-mini, several schema-linking approaches produced meaningful gains. Those gains generally declined on stronger backbones, and some linking configurations reduced accuracy on particular models [1]. Filtering a schema can remove distracting context, but it can also remove a table or column required for the correct query.

Production teams should therefore measure **schema-link recall**, not merely the reduction in prompt size. A cheaper prompt is not an improvement if the required join key disappears before generation.

### External reasoning scaffolds can duplicate model behaviour

The paper reports that chain-of-thought-enhanced generation improved execution accuracy by 4.24 percentage points on GPT-4o-mini and 2.87 points on Gemini-2.5-Flash, but reduced accuracy on DeepSeek-V4-Flash [1]. Follow-up tests on two additional reasoning backbones found no consistent benefit from chain-of-thought or decomposition over direct generation.

Lin et al. appropriately describe this as suggestive rather than universal because reasoning style, capability, and model family are confounded. For deployment decisions, the implication is straightforward: do not assume that asking a reasoning model to emit another explicit reasoning scaffold will improve SQL. It can increase output tokens without adding new information.

### Candidate selection is limited by its candidate pool

All three tested selectors improved over the matched five-candidate baseline, according to the paper. Yet a gap remained between selected accuracy and oracle candidate recall—the fraction of questions for which at least one of the five candidates was correct [1].

A selector cannot choose a correct query that was never generated. Multi-candidate selection also pays for five generations before selection begins. Lin et al. therefore excluded it from their cost-efficient tiers.

In production, candidate selection belongs behind a specific diagnosis: use it when candidate diversity is adequate but ranking is weak. If candidate recall is poor, invest first in schema context, generation, or refinement.

## A concrete decision framework

The paper proposes three tiers: a single-pass baseline; baseline plus execution-feedback refinement; and a richer stack combining refinement, masked-question example retrieval, pseudo-SQL-guided schema linking, and a generation strategy conditioned on whether the backbone is reasoning-capable [1].

A production decision can adapt those tiers into five gates.

### Gate 1: Establish a lean, governed baseline

Start with one model call, the full permitted schema, direct generation, and one SQL candidate. Record:

- execution success and task correctness;
- cost per question;
- input and output tokens;
- median and tail latency;
- errors by database, query pattern, and business domain;
- rejected, modified, and executed SQL.

Use a representative internal evaluation set. Public benchmarks can support comparison, but they do not represent an organisation’s schema naming, permissions, data quality, dialect, or question distribution.

### Gate 2: Add failure-gated execution feedback

Test the paper’s R1 pattern next. Compare it with the lean baseline using paired questions and the same model version.

Promote it only if the accuracy gain survives your acceptance thresholds for cost, latency, and safety. Separately measure valid business questions that legitimately return zero rows: the paper’s trigger treats an empty result as a reason to attempt rewriting, so an overly broad implementation could alter a correct query.

### Gate 3: Diagnose the remaining error class

Add modules according to observed failures:

- **Missing or confused schema elements:** test schema linking, while tracking required-element recall.
- **Poor structural transfer across recurring question types:** test example retrieval.
- **Weak planning on a non-reasoning backbone:** test chain-of-thought-enhanced generation against direct generation.
- **Correct SQL often appears among candidates but is not selected:** test candidate selection.
- **Complex errors survive simple feedback:** evaluate more expensive refinement, with an explicit budget.

This prevents pipeline stacking from becoming an architectural reflex.

### Gate 4: Compare complete systems, not model prices

Construct a cost–quality frontier whose unit is a **backbone plus pipeline configuration**. Lin et al. report that their Gemini-2.5-Flash stack achieved higher BIRD execution accuracy at lower total API cost than their lean GPT-5.4 configuration [1]. On Spider, the selected DeepSeek-V4-Flash and Gemini-2.5-Flash stacks also exceeded the lean GPT-5.4 baseline at lower reported costs [1].

These are results from the authors’ benchmark setup and recorded API prices, not durable vendor rankings. Prices, models, prompts, and workloads change. The durable method is to compare complete deployable configurations under one workload and budget.

### Gate 5: Require a production-readiness review

A benchmark-correct query is not necessarily safe to run. Lin et al. recommend least-privilege access, read-only execution where possible, SQL validation, sandboxing, human oversight, and audit logs [1].

The operational gate should also cover query timeouts, row and scan limits, approved SQL constructs, sensitive-column policies, tenant isolation, dialect compatibility, and deterministic rollback to the last valid query. These controls should sit outside the model so that a prompt or generated query cannot bypass them.

## Where the evidence stops

The paper is a controlled benchmark study, not a production reliability study. Its primary metric compares predicted and reference-query execution results. It does not establish semantic correctness for ambiguous business questions, protection against malicious prompts, performance on changing schemas, or acceptable warehouse load.

Its costs are also workload- and price-specific. The authors calculated API spending from token prices recorded on May 2, 2026 [1]. Network latency, database execution cost, observability, retries, engineering maintenance, and incident response are outside that accounting.

Finally, the single-module protocol is valuable for attribution but cannot predict every interaction in a larger stack. Lin et al. tested selected generation–refinement and generation–retrieval combinations and found that composition varied by backbone [1]. Every extra module should therefore retain its own telemetry and an ablation path.

## The leadership decision

The paper supports a disciplined ordering of investment:

1. Measure a lean baseline.
2. Test failure-gated execution feedback.
3. Add modules only for diagnosed error classes.
4. Compare the resulting system with a model upgrade on accuracy, cost, latency, and risk.
5. Deploy only behind database-enforced controls.

The strongest model may still be the correct choice when maximum accuracy dominates cost. But Lin et al.’s results show why model capability and pipeline design should be budgeted together. For many analytics teams, the next improvement may be a better-controlled feedback path—not a larger model.

## References

1. Jiayan Lin, Yujia Liu, Zijin Hong, Zheng Yuan, Yilin Xiao, Hao Chen, Qinggang Zhang, Xiao Huang, and Feiran Huang. “Are These Modules Worth Their Cost? A Paradigm-Level Accuracy-Cost Analysis of In-context Learning Text-to-SQL.” arXiv:2608.28432v1, 2026. https://arxiv.org/abs/2608.28432v1
2. Jinyang Li et al. “Can LLM Already Serve as a Database Interface? A Big Bench for Large-Scale Database Grounded Text-to-SQLs.” *Advances in Neural Information Processing Systems*, 2023. https://arxiv.org/abs/2305.03111
3. Tao Yu et al. “Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task.” *Proceedings of EMNLP*, 2018. https://aclanthology.org/D18-1425/

<figure class="article-diagram" style="margin:2.5rem 0;padding:1.5rem;background:#f5f0e5;border:1px solid rgba(24,55,42,0.12);border-radius:8px">
<div class="diagram-shell"><svg viewBox="0 0 900 620" role="img" aria-labelledby="sql-flow-title sql-flow-desc" xmlns="http://www.w3.org/2000/svg"><title id="sql-flow-title">A cost-aware path for configuring a text-to-SQL pipeline</title><desc id="sql-flow-desc">Flowchart beginning with a lean direct-generation baseline, adding failure-gated execution-feedback refinement, diagnosing residual errors, choosing backbone-conditioned retrieval, linking, and generation, treating candidate selection as an accuracy-first option, and ending at a production control gate.</desc><style>@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;600&amp;family=Geist+Mono:wght@400;600&amp;display=swap');.bg{fill:#f5f0e5}.panel{fill:#ebe3d3;stroke:#18372a;stroke-width:1.5}.node{fill:#f5f0e5;stroke:#18372a;stroke-width:1.5}.focus{fill:#efb34e;stroke:#18372a;stroke-width:2}.title{font-family:Georgia,serif;font-size:25px;fill:#18372a}.name{font-family:Geist,Avenir,sans-serif;font-size:12px;font-weight:600;fill:#18372a}.sub{font-family:'Geist Mono',monospace;font-size:9px;fill:#51665b}.focus-sub{font-family:'Geist Mono',monospace;font-size:9px;fill:#18372a}.edge{fill:none;stroke:#2e5aa8;stroke-width:2}.edge-muted{fill:none;stroke:#51665b;stroke-width:1.5;stroke-dasharray:5 4}.label{font-family:'Geist Mono',monospace;font-size:9px;fill:#2e5aa8}.small{font-family:'Geist Mono',monospace;font-size:8px;fill:#51665b}</style><rect class="bg" width="900" height="620"/><text class="title" x="40" y="48">Configure the pipeline before upgrading the model</text><text class="sub" x="40" y="72">DECISION FLOW · EVIDENCE DISTILLED FROM LIN ET AL.</text><path class="edge" d="M210 152 V176 Q210 184 218 184 H442 Q450 184 450 192 V216"/><path class="edge" d="M450 288 V320"/><path class="edge" d="M450 384 V408 Q450 416 442 416 H258 Q250 416 250 424 V448"/><path class="edge" d="M450 384 V408 Q450 416 458 416 H642 Q650 416 650 424 V448"/><path class="edge-muted" d="M690 152 V320 Q690 328 682 328 H584"/><path class="edge" d="M250 520 V544 Q250 552 258 552 H442"/><path class="edge" d="M650 520 V544 Q650 552 642 552 H458"/><text class="label" x="466" y="310">residual errors</text><text class="label" x="292" y="406">non-reasoning</text><text class="label" x="574" y="406">reasoning</text><text class="small" x="702" y="238">only when pool</text><text class="small" x="702" y="250">recall is adequate</text><polygon class="node" points="40,96 380,96 380,152 368,164 40,164"/><text class="name" x="60" y="120">Tier 1 · Lean baseline</text><text class="sub" x="60" y="140">FULL SCHEMA · DIRECT GENERATION · N=1</text><polygon class="node" points="520,96 860,96 860,152 848,164 520,164"/><text class="name" x="540" y="120">Candidate selection</text><text class="sub" x="540" y="140">N=5 POOL · RECALL-BOUND · EXTRA SAMPLING</text><polygon class="focus" points="270,216 630,216 630,276 618,288 270,288"/><text class="name" x="290" y="242">Tier 2 · Execution-feedback refinement</text><text class="focus-sub" x="290" y="263">EXECUTE → REWRITE ONLY ON ERROR OR EMPTY RESULT</text><polygon class="panel" points="316,320 584,320 584,372 572,384 316,384"/><text class="name" x="336" y="344">Classify the backbone</text><text class="sub" x="336" y="364">REASONING BEHAVIOUR CHANGES GENERATION CHOICE</text><polygon class="node" points="80,448 420,448 420,508 408,520 80,520"/><text class="name" x="100" y="474">Tier 3 · Retrieval + linking + G2</text><text class="sub" x="100" y="495">E2 MASKED RETRIEVAL · S2 PSEUDO-SQL LINKING</text><polygon class="node" points="480,448 820,448 820,508 808,520 480,520"/><text class="name" x="500" y="474">Tier 3 · Retrieval + linking + G1</text><text class="sub" x="500" y="495">E2 MASKED RETRIEVAL · S2 LINKING · DIRECT GEN</text><polygon class="focus" points="280,544 620,544 620,596 608,608 280,608"/><text class="name" x="300" y="568">Production control gate</text><text class="focus-sub" x="300" y="588">VALIDATE · READ ONLY · LIMIT · AUDIT · OBSERVE</text></svg></div>
<figcaption style="font:400 0.82rem Geist,sans-serif;color:#51665b;margin-top:0.9rem;text-align:center">A cost-aware path for configuring a text-to-SQL pipeline — A decision flow derived from Lin and co-authors’ tiered guideline. Teams begin with direct single-pass generation, add execution-feedback refinement, diagnose residual errors, and condition richer pipeline modules on the backbone and candidate-pool evidence before passing a production control gate.</figcaption>
</figure>


*Diagram: [A cost-aware path for configuring a text-to-SQL pipeline](/assets/diagrams/2026-08-31-before-upgrading-the-model-fix-the-text-to-sql-pipeline.html) — standalone HTML/SVG*

