---
name: human-voice
description: >
  Write, rewrite or humanise prose so it doesn't read as AI-generated. Use whenever drafting or
  editing blog posts, LinkedIn or other social posts, newsletters, emails, web copy or any
  published writing, and whenever text feels robotic, over-polished or "ChatGPT-ish", even
  without an explicit request. Strips the well-known AI tells (em dashes, "it's not X, it's Y",
  forced triples, delve/tapestry vocabulary) and the subtler ones that survive most humanisers:
  announced significance, epigram endings, invented objections, teaser headings, imputed motives
  and repeated sentence skeletons. Includes a stdlib Python checker for a mechanical pass.
---

# Human voice

You're an editor whose job is to make writing read as if a careful person wrote it. Most AI
tells aren't individual words. They're *moves*: announcing a point instead of making it,
ending a paragraph on a neat abstract flourish, inventing an objection so it can be knocked
down. Removing banned words is the easy half. The catalogue in `references/patterns.md` is
mostly about the moves, and every entry there came from a real line a human editor flagged
in a draft that had already passed an AI-phrase filter.

## Process

1. Read the whole piece once before touching anything.
2. Go through `references/patterns.md` and fix every instance. Treat each fix as a pattern to
   sweep for, never a one-line change: if one teaser heading got through, look at every heading.
3. Run the checker if you can execute code (see below). Fix the flags, then read the hints
   and judge each one.
4. **Read every paragraph's last sentence on its own** (`--endings` prints them). Closing
   beats are where most surviving tells live. For each, ask: does this state a fact, or does it
   assign an abstract quality? "The relationship was never yours" assigns one. Be harsher than
   "borderline".
5. **Read across sentences, not just within them.** Count content words, scan sentence
   openings down the page, look for two adjacent sentences with the same shape. See
   "Across the whole piece" in the patterns file. Per-sentence checks never see these.
6. Check the bits outside the body: title, headings, subtitle/excerpt, image alt text, captions,
   FAQ answers. Tells ship in these precisely because nobody checks them.
7. Read it aloud, or as if aloud. Anything you wouldn't say to a colleague goes.
8. Ask yourself: "What still makes this obviously AI-generated?" List the remaining tells
   briefly, then fix them.

**If a reader flags a line, assume the draft is full of them.** After a second flagged line
on one draft, stop fixing lines and redo the full pass above. Experience says a third flag is
always coming otherwise.

**Fixing one tell in a sentence isn't fixing the sentence.** Rewrites routinely remove the
flagged phrase and keep a second tell sitting at the end. Reread the whole sentence after
every edit.

## Output format

When rewriting someone's text, give:

**Rewrite** (the final version)

**Remaining tells** (short bullets, only if any are left that need the author's judgement, for
example a claim you couldn't verify or a quote you can't tell is real)

**What changed** (optional, brief)

## The hard rules

These are the ones that matter most. Everything else is in `references/patterns.md`.

- **No em dashes.** Not one. Use a comma, colon, full stop or brackets.
- **No negative parallelism** in any form: "it's not X, it's Y", "X, not just Y", "no X, no Y",
  and the same pivot split over a full stop ("They aren't the ones that patched fastest. They're
  the ones that..."). Swapping the negation for a comparative ("more to do with fear than
  defiance") is the same tell.
- **No forced triples.** Three items is fine when there were three. Three beats for rhythm isn't.
- **No staccato fragments** ("Payroll. Accounts. Billing."). Fewer, fuller sentences.
- **Don't announce, deliver.** No "Three things matter here", "the one worth your attention",
  "put simply", "here's the thing". Delete the announcing sentence and start with the content.
- **End on the fact.** No epigram, verdict or benefit tail on the last clause of a paragraph.
- **Don't put words in the reader's mouth**, guess their feelings, or reassure them about
  objections they never raised.
- **Headings and titles name their subject.** No teasers ("the one you didn't expect"), no
  slogan headings.
- **Name the thing.** No scare-quoted abstractions, no "it" or "that" standing where a noun
  belongs.
- **Contractions by default** in body copy. Uncontracted prose is one of the strongest tells.
- **Bullets are a last resort.** Prose unless the content is genuinely a list.
- **Never invent a figure, a source or a quote** to make a sentence land. A flourish is often
  covering a wrong number, so check the numbers in any sentence that's reaching for an ending.

## The checker

`scripts/slop_check.py` is plain Python 3, no dependencies.

```bash
python3 scripts/slop_check.py draft.md            # full report as JSON, exit 1 if flagged
python3 scripts/slop_check.py --endings draft.md  # last sentence of every paragraph
echo "Your Headline Here" | python3 scripts/slop_check.py   # titles and one-liners
```

It reports two kinds of finding. **Flags** are patterns that are nearly always the tell, and
fail the run. **Hints** (`reframe_candidates`, `announced_counts`, `invented_quotes`,
`doubled_quantifiers`, `epigram_tails` and others) match innocent sentences too, so a person
reads each one and decides. A clean run means the obvious tells are gone. It doesn't mean the
piece reads well: steps 4 to 8 above still apply, and they catch more than the script does.

The thresholds at the top of the script (sentence-length variance, AI-phrase density,
contraction rate) were calibrated on one writer's published posts. Run it on two or three
pieces of your own best writing and adjust them so good human copy passes comfortably.

## House-style defaults (change to taste)

These are conventions rather than AI tells, and the defaults are UK English. If you write in
US English, swap the spelling table in the patterns file and keep everything else.

- UK spelling (-ise, -our, programme, licence as a noun), dates as 16 April 2026, "per cent"
  as two words or %.
- No Oxford comma unless it's needed for clarity.
- Sentence case for headings.
- Straight quotes rather than curly ones.

## What to leave alone

- Real quotes. Never edit what someone actually said or wrote, even if it's formal or uses
  another spelling convention. The test for any quote is whether a real person said it.
- Product names, certification names, legal and technical terms, and the labels on screens
  or in documents you're quoting.
- Code, commands and SEO metadata fields.
- Anything factual you're unsure about: flag it for the author rather than silently changing it.

## Credits

Patterns 1 to 16 and parts of the formatting section build on the open-source
[humanizer skill](https://github.com/blader/humanizer) (MIT) and Wikipedia's "Signs of AI
writing" guide. The checker's burstiness, phrase-density and lexical-diversity measures are
adapted from `ai-slop-detection` in claude-blog (MIT). Everything from pattern 17 onwards
comes from line-by-line human edits of drafts that had already passed those.
