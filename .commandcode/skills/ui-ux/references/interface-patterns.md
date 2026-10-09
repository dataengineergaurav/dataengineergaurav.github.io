# Interface Patterns

A pattern is a claim: *for this job, this shape is conventional, learnable, and hard to get
wrong.* Use this file to pick the right claim, and to recognise a pattern used past the point
where it holds. Every entry names when the pattern is right, when it is wrong, and how it fails.

Visual treatment of these patterns belongs to `design`; this file is about which one to reach for
and what happens when you reach for the wrong one.

---

## Job to pattern

Pick the row for the job, then the pattern. If two patterns are plausible, prefer the one with
the lower cost of being wrong.

| Job | Leading pattern | Wrong choice to avoid |
|---|---|---|
| **Monitor** | Status board, feed, timeline, alert list with live priority | A settings page pretending to be a dashboard |
| **Operate** | Command bar, canvas, inspector, side panel, direct manipulation | Multi-step wizard for a repeatable action |
| **Compare** | Table, matrix, split view, ranked list | Cards that hide the deciding attribute |
| **Configure** | Grouped settings by task or object, with summary and preview | One flat list of every option, alphabetically |
| **Learn** | Article flow, progressive sections, readable measure | Carousel that hides content behind motion |
| **Decide** | Focused pitch, proof, risk reduction, one dominant action | Equal weight for five competing CTAs |
| **Explore** | Search, filters, gallery, clusters, reversible discovery | Pagination that destroys the exploration state |

---

## Navigation

**Signals that must always be present** — users should be able to answer three questions at any
point: *Where am I? What is here? What can I do?* Missing any one produces the "lost" feeling
that gets misdiagnosed as "bad design".

- Mark the **current location** persistently (selected nav item, active tab, breadcrumb tail).
- Names come from the user's words, not the org chart or the schema.
- Keep depth to **three levels** where possible; beyond that, users lose the path and search
  becomes the only way to work.

**Choosing the container**

| Pattern | Right for | Fails when |
|---|---|---|
| Top nav | Few (≤7) top-level destinations, low depth | Depth grows — it cannot hold it |
| Side nav | Many destinations, deep hierarchy, expert users | The content is a single task flow, not a workspace |
| Tabs | Sibling views of *one* object | The views are actually different objects |
| Breadcrumbs | Deep hierarchy, not for the primary navigation | Used as the only way back |
| Drawer / hamburger | Secondary nav on narrow screens | Used on desktop because it looks tidy — it lowers discovery |
| Bottom tab bar | 3–5 primary destinations on touch | More than 5, or it fills with actions instead of destinations |
| Command palette | Expert, keyboard-first, many actions | New users — it is invisible without a visible entry point |

**Narrow screens lose navigation first.** When the header collapses, the destinations must
reappear somewhere reachable — a disclosure, a drawer, a tab bar. Deleting the links and keeping
only the primary CTA is the most common responsive defect there is.

**Hub-and-spoke vs hierarchy** — if people bounce between siblings more than they descend, they
want a hub, not a tree. Watch the back-button usage; heavy back usage from siblings means the
level above should be the destination.

---

## Search and filtering

- **Search** when the inventory is large, growing, or not visually enumerable. **Browse** when it
  is small and the categories are the user's own mental model.
- Combine facet + query only when both are needed; a query box that can also be a filter is a
  common source of silent mis-filtering.
- Always show **applied filters as removable chips** and provide **clear all**.
- Autocomplete must never be the only path to a valid value — it is an accelerator, not a gate.
- Show the **result count**; a filtered empty result and an empty dataset are different screens.

**Failure modes**: filters applied with no visible state; search that silently searches a subset;
no-results that blames the user; sorting that resets when the query changes.

---

## Lists, tables, and data

- **Scan lanes** — right-align numbers, left-align text, decimal-align quantities. Alignment is
  what makes a column comparable at a glance.
- **Column priority** — decide which 3–4 columns answer the question at a glance; the rest belong
  in a detail view or a progressive reveal.
- **Density** is a feature: operators want compact rows, first-time readers want air. Offer both
  where the audience is mixed.
- **Sticky headers** for anything longer than a screen; **sticky first column** for wide tables.
- **Alignment to the decision**: if the table supports a decision, the deciding column should be
  the easiest to scan — often sorted or visually weighted, not buried in the middle.

**Responsive tables** — never amputate columns silently. Rank columns and: hide the low-priority
ones behind a detail view, switch to a card/definition list, or scroll horizontally with a pinned
identity column. Losing a column without a way to recover it is data loss.

**Pagination vs load-more vs infinite scroll**

| Pattern | Right for | Failure |
|---|---|---|
| Pagination | Known sets, positional work ("page 3 of 12"), reachable footer | Resets state; painful on mobile |
| Load more | Bounded exploration, footer matters | Hidden cost — the button is often missed |
| Infinite scroll | Feeds, discovery, no footer dependency | Makes the footer and anything after the list unreachable |

If the page has a footer, a legal notice, or a CTA at the bottom, infinite scroll and a long list
are in conflict. Surface the footer another way or choose a bounded pattern.

---

## Selection and controls

| Control | Right for | Wrong when |
|---|---|---|
| Radio | One of a small set, all visible, compare-first | More than ~5 options — use select |
| Checkbox | Zero-to-many, independent, submitted together | One option (use a toggle) |
| Toggle / switch | Binary setting that takes effect **immediately** | Used inside a form that needs a Save — it lies about when it applies |
| Segmented control | 2–5 mutually exclusive views, quick switching | Options that are not peers |
| Select / dropdown | Many options, limited space, one choice | Used to hide 3 options that would have fit |
| Combobox / autocomplete | Long lists, free text plus suggestions | As the only way to enter a valid value |
| Stepper / slider | A range where precision is not needed | Precise values — use a text field |
| Multi-select | Bulk operations on a visible set | Without showing the current selection |

**Toggle labelling** — because a toggle is immediate, its label is a statement of fact
("Send weekly summary"), not an instruction ("Enable"). An "Enable" toggle next to a Save button
is ambiguous in both directions.

**Selection must be visible and reviewable.** Any pattern that lets the user accumulate choices
(a multi-select, a cart, a bulk action) must show the accumulated set and allow removal before
commit.

---

## Overlays

Choose by *how much work* and *how much interruption*, not by how important it feels.

| Pattern | Right for | Fails when |
|---|---|---|
| Inline (expand, popover) | Small edits, contextual detail, keeps context | Content overflows a constrained anchor |
| Drawer / side panel | Editing an object while keeping the list visible | It is really a full task — use a page |
| Modal dialog | Short, focused, binary decision; destructive confirms | It holds a form with many fields or steps |
| Full page / route | Anything the user will spend real time in | It is a 2-field prompt |
| Bottom sheet (touch) | Actions and choices on handheld | Desktop, where it is unfamiliar |

**Modal rules that are not optional**: move focus in on open, trap it, return it to the trigger on
close, close on Escape, and make the background `inert`. Never stack modals. Never open one
unbidden on load.

**The most common overlay mistake** is using a modal for complex work. A form with many fields,
validation, and a submit step belongs on a page with a URL — it can be linked, refreshed, and
bookmarked, and it does not trap the user in a state they cannot leave.

---

## Destructive and irreversible actions

Match the guard to the blast radius.

| Blast radius | Guard |
|---|---|
| Reversible, single item | **Undo** (toast with undo, soft delete). No dialogue. |
| Reversible, but surprising | Undo, plus a clear statement of what happened |
| Irreversible, single item | Confirm naming the item |
| Irreversible, many items | Confirm naming the **count** and the consequence; offer export first |
| Account / data / financial / legal | Typing the name to confirm, or re-authentication |

- Prefer **soft delete** with a retention window wherever the domain allows it. Undo beats a
  dialogue because it does not interrupt and it does not get click-through'd.
- A confirm dialogue that always appears is trained away; people click through it. Reserve it so
  that its appearance means something.
- Never distinguish a destructive action from a safe one by **colour alone** — colour-blind users
  and grey-scale screens lose the distinction.
- Put the destructive action where it is **deliberately less reachable** than the safe one, and
  never where a mis-tap reaches it.

---

## Notifications and attention

Attention is the scarcest resource; spending it is a design decision.

- **Interrupt** (modal, blocking) — only for a decision that must happen now.
- **Alert** (banner, badge) — state that is persistent and actionable.
- **Inform** (toast, inline confirmation) — completed actions, transient.
- **Record** (notification centre, log) — anything that happened while away.
- Never use a toast for something requiring a decision; it disappears before the decision is made.
- Never let a notification be the only place a state is visible — it must be visible on the
  surface it belongs to.
- Respect frequency: every interruption has a cost, and the second unnecessary one teaches people
  to ignore all of them.

---

## Empty, loading, and error states

Covered mechanically in `usability.md`; here is the pattern choice.

- **First run** — teach the space and give the first action. Not "No data".
- **Cleared / all done** — celebrate the completion, then offer the next thing (peak–end).
- **No results** — restate the query, broaden it, offer a way out.
- **Partial** — some data, some missing. Show what exists and mark what is absent, rather than
  hiding the whole set.
- **Loading** — skeleton matching the final layout when the shape is known; progress with a
  determinate bar when duration is known; never a spinner that resolves into a layout shift.

---

## Onboarding and progressive disclosure

- **Progressive disclosure** is the default for complexity: show the common path, reveal the rest
  on request. It fails when the hidden thing is needed to complete the visible thing.
- Prefer a **real first action** over a tour. A working example teaches more than a pointer.
- Make skippable, resumable, and re-findable. An onboarding that cannot be re-entered is a
  one-shot that fails the second user.
- Never gate the product behind onboarding. Let people in, teach in context.

---

## Settings and configuration

- **Group by task or object**, never alphabetically. Alphabetical order is a lookup structure for
  people who already know the name — the opposite of what settings need.
- Show the **current value** in the summary; do not make people open a section to see the state.
- **Defaults matter more than options.** The default is the product for most users.
- **Preview** anything whose effect is not self-evident.
- Be explicit about the **save model**: immediate effect, or explicit Save. Never mix the two on
  one screen. Immediate-effect settings need immediate, visible confirmation.
- Provide **reset to default** and **search within settings** once the count passes ~20.

---

## Wizards and multi-step flows

Split only when steps are **ordered and dependent**. Otherwise, one form.

- Show step count and current position.
- Allow going back without losing input.
- Persist a draft; never lose completed steps on refresh or navigation.
- Validate per step, but validate cross-step dependencies before the final commit.
- The final step is a review of real values, not a summary of the form.
- Never make step 1 depend on information the user will only learn at step 4.

---

## Responsive and adaptive

- **Adapt, never amputate.** Hiding a feature on small screens is a bug, not a responsive design.
- Detect the **input mode**, not just the width: `hover: hover` and `pointer: fine` gate hover
  affordances and precision gestures (drag, hover menus). Never gate *functionality* behind hover.
- **Thumb zone**: primary actions in the bottom quarter on touch; destructive actions deliberately
  out of easy reach.
- **Priority+**: collapse the lowest-priority items behind a "more" disclosure, and keep the
  highest-priority ones visible — the opposite of the common "hide everything" collapse.
- Reflow at 320 px and 200 % zoom is the floor, not a nice-to-have (`usability.md`).
- Form inputs need ≥16 px text on small screens or iOS Safari zooms the viewport on focus.

---

## Anti-pattern reference

Name these when you find them. Each one is a HIGH or MEDIUM finding, not a style preference.

| Anti-pattern | Why it fails |
|---|---|
| Carousel (auto-advancing) | Content past slide 1 is effectively unseen; motion ignores reduced-motion |
| Infinite scroll above a footer | Makes everything below the list unreachable |
| Placeholder used as a label | Disappears on focus, fails contrast, invisible to screen readers |
| Disabled submit with no reason | Hides the single thing the user must fix |
| Mystery-meat icon nav | No label, no meaning without a legend |
| Hover-only affordance | Invisible on touch; unreachable by keyboard |
| Modal holding a long form | Traps the user in a state with no URL, no back, no refresh |
| Confirmation on every action | Trains click-through, so the confirm that matters is ignored |
| Reset button on a form | Destroys work, is never wanted, and sits next to submit |
| Destructive control styled like a safe one | Mis-clicks with irreversible consequences |
| Meaning by colour alone | Invisible to colour-blind users and in grey-scale |
| Paginating a 10-item list | Adds a click and a state to something that fits |
| Silent background mutation | Change blindness means the update effectively did not happen |
| "Click here" / "Learn more" links | Nothing to scan, nothing for a screen reader to announce |
| `outline: none` with no replacement | Removes the keyboard user's only position indicator |
