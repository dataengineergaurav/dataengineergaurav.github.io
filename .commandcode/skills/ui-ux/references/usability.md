# Usability

How to evaluate an interface, and what every interface owes the person using it. This file is the
checklist half of the skill: heuristics, states, feedback, errors, forms, and how to know whether
any of it worked.

---

## Heuristic evaluation

Ten heuristics, each as a question you can answer with evidence. Walk them in order; the first
four catch most real defects. One line of evidence per heuristic, and only report the ones that
actually fail — a heuristic marked "pass" with no evidence is a vibe.

| # | Heuristic | The question | Common failure |
|---|---|---|---|
| 1 | Visibility of system status | Does the user always know what the system is doing? | Silent saves, no in-flight state, a filter applied with nothing showing it |
| 2 | Match to the real world | Does the language come from the user's domain, not the schema? | `entity_id`, `status_code 3`, internal jargon |
| 3 | User control and freedom | Can they undo, back out, or escape without losing work? | No cancel on a long flow, no undo, modal with no escape |
| 4 | Consistency and standards | Same word, same control, same place — and the platform convention? | "Delete" here and "Remove" there for the same act |
| 5 | Error prevention | Is the error designed out, not just reported? | Free-text for a date, unvalidated destructive action |
| 6 | Recognition over recall | Is everything needed on screen? | Values from a prior step must be remembered |
| 7 | Flexibility and efficiency | Is there a fast path for the expert? | Forced wizards, no keyboard, no bulk action |
| 8 | Aesthetic and minimalist design | Is anything here not earning its place? | Competing primaries, decorative chrome, redundant copy |
| 9 | Error recovery | Does the message say what broke, why, and what next? | "Invalid input", "Something went wrong" |
| 10 | Help and documentation | Is help at the point of need? | Only a separate help centre, or none |

Heuristics find *candidate* problems, not confirmed ones. A heuristic finding says "this may be a
problem"; only watching someone attempt the task says it is.

---

## The nine states

A layout that only works in the first state is a sketch. Every interactive component exists in
all nine, and the missing ones are where the bugs and the support tickets live.

| State | What it must do | Failure mode to look for |
|---|---|---|
| **Idle** | Communicate what it is and that it is actionable | Looks disabled, or looks actionable but is not |
| **Hover** | Confirm the target under the pointer | Hover-only affordance (invisible on touch) |
| **Active** | Confirm the press registered | No press feedback, so people double-submit |
| **Focused** | Be unmistakably visible for keyboard users | `outline: none` with no replacement |
| **Loading** | Show progress and hold the layout | Spinner that shifts layout when content lands |
| **Empty** | Explain what belongs here and how to add it | Blank panel, or "No data" |
| **Error** | Say what broke, why, and the recovery | Red border with no text |
| **Disabled** | Explain why it is unavailable | Disabled with no reason, and no way to reach it |
| **Overflow** | Handle more content than expected | Truncation with no reveal, unbounded scroll, clipped text |

**Empty state is not one state.** First-run ("Nothing here yet — add your first source"), cleared
("All caught up"), no-results ("No matches for **xyz** — try a shorter term"), and error are four
different messages with four different actions. Using one for all four is a defect.

**Disabled with no reason is worse than enabled with a clear error.** A disabled control hides
the one thing the user must fix. Prefer enabled + validate, and only disable when the reason is
self-evident on screen.

---

## Feedback and system status

Every user action gets a result, and the result has to live where the user is looking.

- **Latency** drives the form: ≤100 ms nothing, ≤1 s a subtle state change, beyond that a
  progress indicator, beyond 10 s let them leave (see `human-behavior.md`).
- **Optimistic UI** for high-confidence, low-risk writes; give it a real rollback, and say so
  when it rolls back.
- **Place feedback adjacent to its cause**: field errors at the field, row errors in the row,
  page errors at the top of the page. A toast for a field error is a round trip.
- **Announce changes** the user did not trigger (live regions) — a silently updated count, a
  background sync, a validation that resolved. Otherwise the change effectively did not happen.
- **Never** show success before the write committed, and never show failure as success with a
  softer word.

**Toast vs banner vs inline**

| Pattern | Use | Do not use for |
|---|---|---|
| Inline | Field/row errors, contextual validation | Anything with no obvious anchor |
| Toast | Transient confirmation of an explicit, completed action | Errors that need a decision; anything long |
| Banner | Persistent, actionable state (outage, over-quota, mode) | Praise, or anything dismissible-and-forgotten |
| Notification centre | History and things that arrived while away | Real-time blocking decisions |

---

## Error prevention and recovery

Distinguish the two error types; they need different fixes.

- **Slips** — right intention, wrong execution (mis-typed, mis-tapped). Fix with constraints,
  bigger targets, forgiving parsing, and `autocomplete`; not with a warning.
- **Mistakes** — wrong intention from a wrong model. Fix with clearer language, a preview, or
  showing the consequence. Warnings do not help someone who is confidently wrong.

**Validation timing**

- Validate format on blur, not on every keystroke — mid-typing errors are noise.
- Validate cross-field and business rules on submit.
- Re-validate *live* only after a field has already failed once, and clear the error the moment
  it is fixed.
- Never stop the user from typing a valid prefix of a valid value. Do not reject `-`, `+971`, or
  an empty decimal mid-entry.

**Error copy** — three parts, in this order: what broke, why, and what to do next. Write it so it
survives being read alone in a screenshot.

- State the field and the requirement: "Phone must include the country code."
- Never blame: not "You entered an invalid value" but "We need a date after today."
- Put the fix in the message, next to the control that fixes it.
- One message per problem, at the problem.

**Recovery and reversibility**

- Preserve everything the user typed. A validation failure that clears the form is data loss.
- **Undo beats confirm.** Undo for reversible acts (delete → trash, move, edit, toggle).
  Confirm for irreversible, financial, legal, or bulk acts — and make the confirm name the thing
  and the count: "Delete 4 records?" not "Are you sure?".
- Prefer soft delete. If the data is gone, the confirm had better be unmissable.
- Never make a destructive control visually identical to a safe one — and not by colour alone.

---

## Forms

Forms are where usability is won or lost. The rules, roughly in order of payoff:

1. **Label every field, always visible.** A placeholder is not a label — it disappears on focus,
   fails contrast, and breaks screen readers. Placeholders show *format*, and only that.
2. **One column.** Multi-column forms break the vertical reading path and the tab order.
3. **Cut the field count.** Every optional field costs completions. Each field must earn its
   place against the cost of asking.
4. **Ask in the user's order and words**, not the database's.
5. **Mark the minority.** If most fields are required, mark the optional ones.
6. **Group with headings and proximity**, not borders.
7. **Use the right input type**: `type="email"`, `type="tel"`, `inputmode="numeric"`,
   `autocomplete` tokens. This is free usability on mobile.
8. **Show constraints before the error**, not after ("8+ characters" under the field).
9. **Default what you can infer**; never default something that commits the user to a choice.
10. **One primary action.** Secondary actions are visually secondary; cancel is always available.
11. **Never disable submit without a visible reason.** Disabling hides the fix.
12. **Preserve state** across validation, navigation, and back.
13. **Split into steps only when the steps are genuinely ordered and dependent**, and always show
    progress, allow back, and never lose earlier input.
14. **Review before commit** for bulk, financial, or irreversible submissions — show the values,
    not a summary of the form.

---

## Search, filtering, and no-results

- Offer search when the inventory is large or not visually enumerable; offer filtering when it is.
- Show **what is applied**, and give a one-click **clear all**.
- Show **how many** results, and **why** they matched when the match is non-obvious.
- No-results is a recovery screen, not a dead end: restate the query, suggest a broader term, and
  offer a way out.
- Empty results after filtering and empty data are different messages — do not conflate them.

---

## Onboarding

- Do not front-load. Teach at the moment of need, in context.
- Make it skippable, resumable, and re-findable.
- Coach marks and tooltips are fragile: they cover the thing they explain, break on resize, and
  are skipped. Prefer a real empty-state action or a checklist.
- Show progress; the goal-gradient effect does the work.
- End on a completed task with something visible to show for it (peak–end).

---

## Measurement

Heuristics are cheap and unreliable; testing is expensive and decisive. Use both, in that order.

| Method | Answers | Cost |
|---|---|---|
| Heuristic evaluation | "What might be wrong?" — candidates only | Low |
| Task-based usability test (5 users) | "Can anyone actually do it?" | Medium |
| Analytics / funnel | "Where do people leave?" | Low, after launch |
| Error-rate and support-ticket review | "What keeps breaking?" | Low |

Metrics worth naming: **task success rate**, **time on task**, **error rate**, and **SUS** for a
comparable satisfaction score. Percentages and completion counts are evidence; "feels nicer" is
not.

**The no-instruction test.** The cheapest usability test there is: hand the surface to someone
who has not seen it, name a task, and say nothing else. Note the first thing they do, where they
hesitate, and what they try that you did not anticipate. That is your primary finding.

**Severity for a usability finding** follows the same scale as `design`:

- **HIGH** — blocks the task, misleads, destroys work, or hides something the user needs.
- **MEDIUM** — the task is completable but costs real effort, error, or confidence.
- **LOW** — friction or polish with limited task impact.

Rank within severity by reach: a fix in a shared component outranks the same symptom in one leaf,
because it fixes every instance at once.
