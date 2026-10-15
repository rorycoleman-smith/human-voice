# AI writing patterns

Each entry is a tell, what to watch for, and the fix. ✗ is the flagged line, ✓ the rewrite.
The examples come from real drafts, mostly business and IT writing, but the patterns are
topic-neutral. "(checker)" means `scripts/slop_check.py` looks for it; everything else needs
a person.

---

## A. Vocabulary and inflation

### 1. Significance inflation
Watch for: stands/serves as, testament, pivotal moment, underscores, evolving landscape,
focal point, indelible mark. Fix: state the plain fact.

### 2. Name-dropping
Watch for: "cited in [list of outlets]", "leading expert", "active social media presence".
Fix: one specific reference, or cut the claim.

### 3. Tacked-on -ing analysis
Watch for: "...symbolising", "reflecting", "showcasing", "highlighting", "fostering", and any
"-ing" clause bolted on to inflate a sentence ("...always aiming for wider business goals").
Fix: cut it, or make it its own plain sentence.

### 4. Promotional language
Watch for: boasts, vibrant, rich (figurative), nestled, in the heart of, groundbreaking,
stunning. Fix: neutral description.

### 5. Vague attributions
Watch for: "Experts argue", "Industry reports suggest", "Observers have noted". Fix: name the
source and date, or cut the claim.

### 6. Formulaic sections
Watch for: "Despite challenges... continues to thrive", "Challenges and Legacy", "Future
Outlook". Fix: specific facts about the actual challenges.

### 7. AI vocabulary (checker)
Cut or replace: actually, additionally, align with, crucial, delve, enhance, fostering,
garner, highlight (verb), intricate, key (adjective), landscape (abstract), leverage, pivotal,
robust, seamless, showcase, tapestry, testament, underscore, unlock, vibrant, moreover,
furthermore, "in today's fast-paced world", "it's important to note", "when it comes to",
"navigating the", "in conclusion", "whether you're", "that being said". Fix: the plain word.
"also" not "additionally", "is" not "serves as".

### 8. Copula avoidance
Watch for: serves as, stands as, marks, represents, boasts, features, offers, where "is" or
"has" would do. Fix: use "is", "are", "has".

### 9. Filler phrases
"In order to" → "To". "Due to the fact that" → "Because". "At this point in time" → "Now".
"Has the ability to" → "Can". "It is important to note that" → delete.

### 10. Hedging, in both directions
Over-hedged: "could potentially possibly be argued that it might". One hedge is enough.

Under-hedged is a tell too. ✗ `A 40-person business has nobody whose job it is to notice`
asserts something usually but not always true. ✓ `In a 40-person business, nobody is usually
responsible for spotting it.` Hedge once, honestly.

And don't defend an awkward phrase because it's "an idiom". If it reads badly, rewrite it.

### 11. Soft adverbs
Watch for: quietly, seamlessly, effortlessly, gently, simply, smoothly, used to add a false
sense of ease. ✗ `servers age quietly until they don't` ✓ `servers tick along fine until
they don't`.

### 12. Abstract nouns as verbs
"to solution", "to action", "to leverage", "to ideate". Fix: use, do, act on.

### 13. Stacked superlatives
"the most advanced, comprehensive and powerful solution". Pick one you can support.

### 14. Hyphenated-pair overuse
cross-functional, data-driven, decision-making, high-quality, real-time, end-to-end applied
with robotic consistency. Drop the ones the sentence doesn't need.

### 15. Generic positive conclusions
"The future looks bright", "Exciting times ahead", "a step in the right direction". Fix: a
specific fact, plan or next step.

### 16. Chatbot residue
"I hope this helps!", "Let me know if...", "Great question!", "You're absolutely right",
"As of my last update", "While specific details are limited". Delete. Find a real source or
cut the claim.

---

## B. Sentence shapes

### 17. Negative parallelism, every form (checker)
The single most recognisable AI move. Watch for:
- "It's not just X, it's Y", "Not only X but Y"
- the trailing form, "X, not just Y"
- setup and reveal: "Most businesses don't have X. What they lack is Y"
- the reframe: "It's not a cost, it's the thing that opens doors"
- clipped pairs: "no guessing, no wasted motion", "no obligation, no hard sell" (even
  familiar sign-offs count)
- **split over a full stop**, which evades most filters:
  ✗ `The businesses that will be fine aren't the ones that patched fastest. They're the ones that could answer it without going to look.`
  ✓ `What decides how this goes is whether somebody can already say what's on the network. Patching speed comes second.`
- the comma splice: ✗ `The attack did not defeat the technology, it defeated the rollout.`

Fix: state the point directly. "No obligation, no hard sell" → "There's no obligation and no
hard sell." Don't swap one formula for another ("The hard part is...", see 36).

### 18. The contrastive pivot (checker)
Negative parallelism with the "not" swapped for a comparative, so most filters miss it. Both
halves are abstract labels and nothing that happened gets reported.
- ✗ `Most haven't told their employer, and the reason has more to do with fear than defiance.`
- ✓ `Most haven't mentioned it to their employer, and 64 per cent worry the tool makes them look replaceable.`
- ✗ `You lose visibility and control rather than money.`
- ✓ `The business pays nothing for the tool, so nothing about it appears where you'd look.`

Watch for "more to do with X than Y", "less about X than Y", "not so much X as Y", "easier to
X than to Y". A plain "rather than" naming two real things is fine ("a purchasing decision
rather than a helpdesk ticket").

### 19. Defining a thing by what it isn't (checker, hint)
✗ `it isn't what most business owners expect` ✓ `it may surprise business owners`. Say what
it is.

### 20. Rule of three
Watch for ideas forced into threes, three items starting with the same word ("a X, a Y, a Z"),
and three-beat rhythms with a punchline third beat ("Your team keeps the day to day. You keep
continuity. Everyone sleeps."). Fix: use the true number, or break the rhythm by joining two
beats or cutting one.

Not a ban on three things. ✓ `It recognises that unauthorised AI use is here to stay, that
policy has fallen behind, and that the priority should be reducing risk.` Three, because the
source said three.

### 21. Staccato fragments (checker)
The most common tell left after everything else passes.
- ✗ `...for finance work. Payroll. Management accounts. Supplier details. Client billing.`
- ✓ `...for finance work, including payroll, management accounts, supplier details and client billing.`

Prefer fewer, fuller sentences. If a rewrite has more sentences than the draft and says the
same thing, it's probably worse.

### 22. The abstract reframe (checker, hint)
"X becomes Y" where both halves are categories, not events. It's the same pivot as 17 with
no negation in it.
- ✗ `...which is where a productivity tweak becomes a data protection decision.`
- ✓ `Both have to read company mail to be useful, which means reading personal data about your clients and staff.`

Also: "X turns into Y", "X stops being Y", relabelling for effect ("that's shadow IT wearing a
friendlier name"), "which is where/how" bolted on for a closing beat, idiom enders ("starts to
bite", "and that's the point"), and mirrored conditionals ("Come in clear and it multiplies
your clarity. Come in vague and it multiplies that just as quickly."). Test: what happens in
the world? If both halves are abstractions, the sentence carries no information.

### 23. The elevation reframe (checker, hint)
A plain fact re-announced as the real discovery.
- ✗ `If you don't know what's on the network, that's the finding, and it's a bigger one than either vulnerability.`
- ✓ `If you can't answer that today, the inventory comes before the patching, because nobody can patch a machine they haven't listed.`

Watch for "that's the real problem", "the bigger issue is", "here's the part that...". Fix by
stating the consequence: what the reader does, and why.

### 24. The echoed noun (checker)
A noun restated in a trailing clause for cadence.
- ✗ `...which is a real decision for someone on an ordinary salary, and it's a decision they make again every month.`
- ✓ `...which is roughly £240 a year that nobody reimburses.`

The echo was reaching for "recurring". Turn the restatement into the fact it gestured at.

### 25. The doubled quantifier (checker, hint)
One sweeping word used twice for cadence: "nobody revokes what nobody approved", "every
application on every machine".
- ✗ `A machine that nobody manages won't appear in the inventory, and nobody would be alerted to anything installed on it.`
- ✓ `Ask for the list of machines it manages and compare it with the laptops you know you have. A machine missing from that list won't show up in the inventory or trigger an alert.`

A plain condition and result can keep it: "if nothing runs over a phone line, there's nothing
to migrate".

### 26. The same number twice (checker, hint)
✗ `Almost a quarter of staff, 22%, have used...` ✓ `Twenty-two per cent of staff have
used...` Pick one. Spell it out at the start of a sentence, numerals elsewhere.

### 27. Passive voice and subjectless fragments
✗ `No configuration file needed.` `Most incidents are contained.` ✓ `You don't need a config
file.` `We contain most incidents before you hear about them.` Name the actor.

### 28. Present continuous for habits (checker, hint)
✗ `ask people what they're using` ✓ `ask people what they use`.

### 29. Long compound sentences (checker, hint)
A clause chain joined by ", and if", ", and when", ", and because" where the second half is a
new idea. Split it at the join.

### 30. Garbled and false ranges
"from X to Y" where X and Y aren't on a scale. Chained ranges: ✗ `went from 50 to 100 a year
to more than 650` ✓ `once managed 50 to 100 a year, and now manages more than 650`.

### 31. Broken idioms and wrong words
"costs more than it looks like", "a considerate eye" for "a careful eye". Correct them.

### 32. Gesturing instead of naming (checker, hint)
Abstractions, scare quotes and vague pronouns where the noun belongs.
- ✗ `The "why" tells you which tool is missing` ✓ `Their answers will show which tool is missing`
- ✗ `the privacy of what they're pasting in` ✓ `the privacy of the information they paste in`
- ✗ `it's usually uncomfortable reading` ✓ `the results are often uncomfortable`

If a word is in scare quotes, the real noun is almost always available.

### 33. The genteel circumlocution (checker)
An abstract event named in place of the action. ✗ `paying the £20 themselves avoids a
conversation they'd rather not start` means "so they don't have to tell anyone". Say that.

### 34. Writerly flourishes and time clichés (checker)
- Time clichés with no real timing: "on Monday morning", "overnight", "by Friday"
- Effort clichés standing in for an estimate nobody made: ✗ `answerable in an afternoon`,
  `a reply drafted before lunch`
- Personified abstractions: ✗ `No policy survives that` ✓ `No policy can overcome that`
- Laboured spatial metaphors: ✗ `sits underneath the headline one` ✓ `is buried beneath the headline`

Real scheduling stays: "worth raising today rather than on Friday afternoon" about when to
reboot a server is fine.

---

## C. Announcing instead of saying

The sentence describes the shape of the paragraph, or ranks its content, instead of
delivering it. Test every one by deleting it. If nothing is lost, it was scaffolding.

### 35. Signposting and throat-clearing
"Let's dive in", "Here's what you need to know", "Without further ado", "When it comes to...",
"In today's world...", "Say, for example, ...". Start with the substance.

### 36. Authority tropes
"At its core", "The real question is", "Fundamentally", "The heart of the matter", "The hard
part is", "The real difference is". Drop the ceremony and say the point.

### 37. The announced count (checker, hint)
- ✗ `Three checks, and none of them needs a tool you don't have.`
- ✗ `Two practical notes. The DNS role often runs on the same server...`
- ✓ Delete it and start with the first note.

A count is fine when it's the news ("Two of the flaws are already being exploited") or the
reader needs it to act. The test: does the number tell them about the world or about your
prose?

### 38. Announced significance (checker)
Ranking a fact instead of delivering it.
- ✗ `The one worth your attention is quieter.`
- ✗ `It's the least useful figure in the study.`
- ✗ `The second decision is the expensive one.`
- ✗ `worth noting`, `worth knowing`, `what matters here`, `This is the piece that gets missed`
- ✓ State the fact and let the reader rank it.

Vague impact verbs are a cousin: "makes a dent in", "moves the needle", "goes a long way
towards". Say what changes. Plain sequencing stays: "The first question is which machines you
have, and the second is which patch each one needs."

### 39. Announced plainness (checker)
✗ `So the arrangement, described plainly, is this.` Saying you're about to be plain isn't
being plain. Watch for "put simply", "in plain terms", "the reality is this", "what this
really means is". Whatever follows is usually an epigram (see 51).

### 40. Article architecture (checker)
Describing the piece rather than saying anything: ✗ `the security case sits in that post
rather than this one`, "what follows", "on this list", "the rest of this article". Linking to
another piece is fine if you say what's behind the link. Check whether the paragraph is
redundant before rewriting it; cutting is often the fix.

### 41. Headers that repeat themselves
A heading followed by a one-sentence paragraph restating it. Delete the sentence.

---

## D. Talking at the reader

### 42. "You" for a third party
"You" is the reader. When reporting what a regulator, vendor or study said, second person is
inaccurate and reads like a sales pitch dressed as news.
- ✗ `It doesn't tell you to ban anything` ✓ `It doesn't call for a ban`
- ✗ `pretending you can remove it` ✓ `pretending the problem can be eliminated`

"If you have a security team" is fine, because there the reader is the subject.

### 43. The imputed motive
Guessing the reader's feelings to make a point feel relatable.
- ✗ `A line you keep because moving it feels like a hassle is getting more expensive.`
- ✓ `The wholesale price still goes up on dates the network operator has already published.`

Siblings: "people who were perfectly happy with the old ones", "you can stop thinking about
this". State the fact and leave the reader's feelings to them.

### 44. The reader guess (checker)
- ✗ `...TeamViewer and LogMeIn, and you'll probably recognise some of them.`
- ✓ `...TeamViewer and LogMeIn. Ask your provider about any you don't recognise.`

Watch for "you'll probably", "you probably already", "chances are you". Replace with what the
reader should do, or cut.

### 45. Anticipatory reassurance (checker)
Soothing an objection nobody raised. It reads as selling.
- ✗ `and it costs nothing` · `it costs an email` · `closes a route at no cost` · `none of them needs a tool you don't have`
- ✓ `That's still the control we'd put first.` · `closes a route they never needed`

State the real cost or say nothing. "It costs money and the price rises each year, so it buys
time without solving the problem" persuades harder, because a reader told a true cost believes
the rest. It clusters around calls to action.

### 46. The invented objection, knocked down (checker)
Words put in the reader's mouth so they can be dismissed.
- ✗ `"We finished our Windows 11 migration" is not an answer this month, and neither is "we're still on 10".`
- ✓ `Which patch a machine needs depends on the version it runs, so a finished migration changes the answer rather than removing the question.`

Three parts: the invented first-person quote, the dismissal ("isn't an answer", "isn't a
strategy"), and the paired negation ("and neither is..."). It often reaches the headline
first. If the reader has a real objection, answer it plainly in an FAQ. Real quotes from real
people stay.

### 47. The strawman comparison (checker)
Measuring advice against a caricature nobody proposed.
- ✗ `An hour on what belongs in these tools will do more than a policy document nobody opens.`
- ✓ `Enough to cover which information can go into these tools, and what to do when something has gone in that shouldn't have.`

The signature is the sneering relative clause: "nobody opens", "nobody reads", "that no one
follows". The caricature turns up when the recommendation hasn't been specified, so specifying
it removes the need.

### 48. The rhetorical universal (checker)
An absolute asserted as proof: ✗ `Nobody spends £240 a year of their own money on software they
can manage without.` It's a debating move, usually not even true. Give the fact and let the
reader conclude. A reported finding ("nobody senior has said what good use looks like") stays.

---

## E. Sentence and paragraph endings

Closing beats are where the instinct for a satisfying ending is strongest, so most surviving
tells are here. Read the last sentence of every paragraph on its own.

### 49. The verdict tail (checker, partly)
A fact followed by a wry, unevidenced verdict.
- ✗ `Around 150,000 premises came off copper in under two months, and the lines left behind are increasingly the ones nobody has got round to.`
- ✓ `By September those figures were 1.5 million and 350,000, so at least 150,000 premises came off copper in seven months.`

Nobody had measured which lines were left, so the clause was invented colour. And the
flourish was covering a wrong figure: February to September is seven months. **A sentence
reaching for a knowing ending is a sentence to check the numbers in.**

The same move graded at the advice: ✗ `For one IT team and one approved tool, that's the right
control.` (usually followed by "Most smaller businesses don't work like that", which is
negative parallelism across a paragraph break). State when it applies as a fact. Treat any
"that's the right X" ending as a tell by default.

### 50. The benefit tail (checker)
An instruction followed by a clause grading it.
- ✗ `...close it and report it, and a screenshot of the prompt will help your team recognise it.`
- ✓ `...close it and report it. Include a screenshot of the prompt when you brief your team.`
- ✗ `...needs administrator rights, which gives a member of staff the chance to stop it.`
- ✓ `...needs administrator rights, so a member of staff who refuses that prompt stops the attack there.`

Sweep every ", and..." and ", which..." ending.

### 51. The epigram and the abstract closing beat (checker, hint)
- ✗ `There's nobody to ask for an export, because the relationship was never yours.`
- ✓ `The contract is between that person and the vendor, so the business has no standing to ask for a copy.`
- ✗ `...and the business is collecting the benefit without ever seeing an invoice.`
- ✓ `The business pays nothing towards it and holds no contract with the supplier.`

The test: does the clause state a fact or assign an abstract quality? An image ("seeing an
invoice") standing in for the fact ("paying") is the tell. The same construction can be
literal and correct ("receive a valid token without ever handling the password"), which is why
a person has to judge.

### 52. The balanced date pair
✗ `The campaigns ran in July, and the research came out on 29 September.` Two events balanced
on ", and" as a sentence of their own, for rhythm. Fold each date into the claim it dates:
"phishing emails, first seen in July, that...".

---

## F. Titles and headings

### 53. The teaser (checker)
A line that withholds its subject so the reader has to click.
- ✗ `How to Spot the One You Didn't Expect` ✓ `How Small Businesses Can Spot Unexpected Remote Access`
- ✗ `## The prompt your staff will see` ✓ `## An administrator prompt after clicking an email link`
- ✗ `## Where to start` ✓ `## Writing the list and asking your provider`

Watch for "the one nobody talks about", "what nobody tells you", "the attack nobody saw
coming", "hiding in plain sight". A phrase that goes on to name its subject is fine: "the risk
you never check is your backups".

### 54. The slogan heading (checker)
Two noun phrases balanced on ", and" with no verb, reading like a tagline.
✗ `## An expected-tools list, and an alert for anything else` ✓ `## Listing which remote tools
belong on each machine`. A heading says what the section does.

### 55. Title case
✗ `## Strategic Negotiations And Global Partnerships` ✓ `## Strategic negotiations and global
partnerships` (if your house style is sentence case).

---

## G. Formatting

### 56. Em dashes (checker)
Banned. Comma, colon, full stop or brackets instead. Rewrite the sentence if needed.

### 57. Bullets
Last resort. Watch for bullets used to avoid writing sentences, and every section ending in a
list. Use them only for genuinely parallel, discrete items.

### 58. Bold
Only for something genuinely critical. Never bolded labels at the start of bullets
("**Speed:** it's fast"), which should become prose.

### 59. Emojis
Remove them from headings and bullets.

### 60. Curly quotes
Use straight quotes if that's your house style; mixed quote styles are a paste-from-chatbot tell.

### 61. Eyebrow labels on graphics
The small uppercase category label above a title on a social graphic or slide ("PHISHING AND
REMOTE ACCESS") is the visual version of announced significance. Let the title stand alone.

---

## H. Register

### 62. Contractions by default (checker)
Uncontracted verbs are one of the biggest tells in body copy. it's, that's, we're, you're,
don't, can't, won't, there's, who'll. "That's not" and "it's not" often read more naturally
than "isn't". Leave quotes and formal names alone.

### 63. Chatty contractions (checker, hint)
Contractions aren't a licence for a colloquial register. "you've got", "there's loads of", "a
bit of a" may be too casual for professional copy. Ordinary contractions stay. (A style
choice, so adjust to your voice.)

### 64. Spelling convention (checker for "percent")
Pick one and enforce it everywhere. UK defaults:

| US | UK |
|---|---|
| -ize (organize, recognize) | -ise (organise, recognise) |
| -or (behavior, color) | -our (behaviour, colour) |
| toward | towards |
| advisor | adviser |
| program (non-software) | programme |
| practice (verb) | practise |
| license (noun) | licence |
| April 16, 2026 | 16 April 2026 |
| percent | per cent, or % |

---

## I. Across the whole piece

None of these show up sentence by sentence. Do this read on every draft before anyone else
sees it.

- **Synonym cycling.** One thing called RMM tool, remote access tool, remote management tool
  and remote tooling. Pick the clearest term and keep it.
- **One word carrying the post.** "legitimate" five times, "genuine" three. Count content
  words before shipping.
- **Echoes inside a sentence.** "its own system... its own agent", "flag either... flag both".
- **Repeated openings.** We / We / We / Our down the page.
- **Mirrored twin sentences.** "X is on A, used by B and behind MFA. Y is on C, used by D and
  also behind MFA." Merge them.
- **A closing section restating an earlier one.** Cut it.
- **A motif repeated too often** ("we start with the business, not the technology" three
  times on one page). Keep the point once.
- **The same skeleton across pieces.** Two posts written in one sitting both closed on "the
  ones who do well aren't X, they're Y". Each passed alone; a day apart on the same feed they
  read as generated. When you write two pieces together, compare their endings.
- **Uniform rhythm.** Every sentence the same length and structure (the checker measures this
  as "burstiness").

## Adding voice

Removing tells is half the job. Sterile, voiceless writing is as obvious as slop. Signs: every
sentence the same length, no opinions, no acknowledgement of uncertainty, reads like a press
release. Have a view, vary the rhythm, admit what's complicated, and be specific about why
something matters rather than saying that it does.
