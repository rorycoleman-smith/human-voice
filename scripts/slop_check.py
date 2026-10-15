#!/usr/bin/env python3
"""Flag prose that reads as machine-generated. Plain Python 3, no dependencies.

Pattern numbers in the comments refer to references/patterns.md.

Two kinds of finding:
  flags  nearly always the tell; any flag fails the run (exit 1)
  hints  match innocent sentences too; a person reads each one and decides

Plus three density measures for whole articles: burstiness (variance in sentence
length), AI-phrase load, and lexical diversity. The density measures and the
burstiness, contraction and phrase-load thresholds are adapted from
`ai-slop-detection` in claude-blog (MIT, AgriciDaniel/claude-blog).

Usage:
  python3 slop_check.py draft.md             full report as JSON
  python3 slop_check.py --endings draft.md   last sentence of every paragraph
  cat draft.md | python3 slop_check.py       stdin works too
  echo "A Headline" | python3 slop_check.py  titles and one-liners

Exit codes: 0 = no flags, 1 = flagged.
"""
import argparse
import json
import re
import statistics
import sys

# ── Thresholds. Calibrate on two or three pieces of your own best writing so that
# good human copy passes comfortably, then leave them alone.
MIN_BURSTINESS = 6.0          # stdev of words per sentence; below this reads metronomic
MAX_AI_PHRASE_PER_1K = 1.0    # AI-phrase hits per 1,000 words; at post length, one hit fails
MIN_TTR = 0.40                # windowed type/token ratio; below this is repetitive
MIN_CONTRACTIONS_PER_1K = 6.0 # natural copy tends to run 15-45; stiff copy under 4
MIN_WORDS_FOR_CONTRACTIONS = 300  # the ratio is noise on short pieces
MAX_FRAGMENT_WORDS = 4        # pattern 21: a "fragment" is this many words or fewer
MIN_FRAGMENT_RUN = 3          # this many fragments in a row is a staccato run
LONG_COMPOUND_WORDS = 35      # pattern 29

# Pattern 7. Lower-case substrings.
AI_PHRASES = [
    "in today's fast-paced world", "in the ever-evolving", "in the realm of",
    "it's important to note", "it is important to note", "it's worth noting",
    "needless to say", "at the end of the day", "when it comes to",
    "delve into", "delving into", "a testament to", "navigating the",
    "in conclusion", "in summary", "to sum up", "rest assured",
    "the world of", "unlock the", "unleash the", "harness the power",
    "elevate your", "take your", "to the next level", "game-changer",
    "game changer", "tapestry", "symphony", "landscape of", "ever-changing",
    "look no further", "dive deep", "let's explore", "embark on", "robust",
    "seamless", "cutting-edge", "leverage", "in essence", "ultimately,",
    "moreover", "furthermore", "additionally,", "first and foremost",
    "paramount", "plethora", "myriad", "whether you're", "that being said",
]

# Pattern 17: negative parallelism. Zero tolerance.
NEG_PARALLELISM = [
    r"\bnot only\b[^.]*?\bbut\b",
    r"\bit'?s not just\b",
    r"\bnot just\b[^.]*?,\s*(?:it'?s|but)\b",
    r"\bisn'?t just\b[^.]*?,\s*(?:it'?s|but)\b",
    r"\bno\s+\w+,\s*no\s+\w+\b",   # clipped "no X, no Y"
    # the pivot split across a full stop: "aren't the ones that... They're the ones that"
    r"\b(?:isn'?t|aren'?t|won'?t be|wasn'?t|weren'?t)\b[^.!?]{0,90}\.\s+"
    r"(?:it'?s|they'?re|they'?ll be|it'?ll be|he'?s|she'?s)\b",
    # the comma splice: "did not defeat the technology, it defeated the rollout"
    r"\b(?:did|does|do|is|was|were|has|have)\s+not\s+[^.,!?]{0,60},\s*"
    r"(?:it|they|he|she)\s+\w+",
]

# Patterns 22 and 23: abstract and elevation reframes. HINT.
REFRAME_PATTERNS = [
    r"\bbecomes? (?:a|an|the)\b",
    r"\bturns? into\b",
    r"\bstops being\b",
    r"\bwhich is (?:where|how)\b",
    r"\bwearing a \w+ name\b",
    r"\bstarts to bite\b",
    r"\bthat'?s the (?:finding|problem|real|point|issue|question|answer|lesson|story)\b",
    r"\bthat'?s the \w+,? and it'?s a (?:bigger|worse|larger)\b",
    r"\bthe (?:real|bigger|actual) (?:problem|issue|question|finding|risk) (?:is|here)\b",
    r"\bhere'?s the (?:part|flaw|thing|bit|problem|catch)\b",
]

# Pattern 37: the announced count. Scoped to scaffolding nouns so that "Two of the
# flaws are being exploited" doesn't match. HINT.
ANNOUNCED_COUNT = re.compile(
    r"(?:^|[.!?]\s+|\n)(two|three|four|five|six)\s+(?:\w+\s+){0,2}"
    r"(notes?|checks?|things?|points?|reasons?|steps?|ways?|kinds?|types?|"
    r"options?|rules?|lessons?|takeaways?|questions?)\b",
    re.IGNORECASE)

# Pattern 45: anticipatory reassurance. FLAG.
REASSURANCE = [
    r"\bnone of (?:them|these|this|it) (?:needs?|requires?|takes?)\b",
    r"\b(?:tools?|software|kit|licence\w*|equipment) (?:you|they) don'?t (?:already )?have\b",
    r"\bcosts?\s+(?:you\s+)?nothing\b",
    r"\bat no cost\b",
    r"\bcosts? (?:an?|one) email\b",
    r"\bno special \w+ (?:needed|required)\b",
    r"\bwithout needing (?:a|an|any)\b",
]

# Pattern 18: the contrastive pivot. FLAG.
CONTRASTIVE_PIVOT = [
    r"\b(?:has|have|is|are|was|were)\s+more\s+to\s+do\s+with\b[^.!?]{0,60}\bthan\b",
    r"\bmore\s+(?:about|a|an|of\s+a)\b[^.!?]{0,50}\bthan\s+(?:about|a|an|of\s+a|it\s+is)\b",
    r"\bless\s+(?:about|a|an|of\s+a)\b[^.!?]{0,50}\bthan\b",
    r"\bnot\s+so\s+much\b[^.!?]{0,50}\bas\b",
    r"\b(?:easier|harder|simpler|cheaper|quicker|safer)\s+to\s+\w+\s+than\s+to\s+\w+",
    r"\bis\s+less\s+(?:a|an)\b[^.!?]{0,40}\bthan\s+(?:a|an)\b",
]

# Pattern 38: announced significance. FLAG. Plain sequencing ("The first question
# is which machines you have") is deliberately not matched.
ANNOUNCED_SIGNIFICANCE = [
    r"\bthe (?:one|bit|part|number|figure|question|line|point) (?:worth|that matters|that counts)\b",
    r"\bworth (?:your attention|noting|knowing|remembering|holding on to|sitting with)\b",
    r"\bthe (?:least|most) (?:useful|important|interesting|telling|revealing|striking)\b",
    r"\bis the (?:expensive|important|interesting|telling|useful|real) one\b",
    r"\bthe (?:real|actual|key|important|telling) (?:one|part|bit|number|figure|point|detail)\b",
    r"\bwhat (?:really )?matters (?:here|is|most)\b",
    r"\bthe (?:figure|number|finding|detail) (?:that should|you should|worth)\b",
    r"\bthe (?:conclusion|point|detail|part|thing|bit)\s+(?:the|that)\s+\w+\s+"
    r"(?:keeps? missing|misses|overlooks?|ignores?|never mentions?)\b",
]

# Pattern 39: announced plainness. FLAG.
ANNOUNCED_PLAINNESS = [
    r"\b(?:described|put|stated|said)\s+(?:plainly|simply|bluntly|another way)\b",
    r"\b(?:put|to put it)\s+(?:plainly|simply|bluntly)\b",
    r"\bin plain (?:terms|English)\b",
    r"\bthe (?:arrangement|position|situation|upshot|reality) (?:here )?is this\b",
    r"\bwhat this (?:really )?means is\b",
]

# Pattern 48: the rhetorical universal. FLAG. "Nobody senior has said..." (a
# reported finding) doesn't match.
RHETORICAL_UNIVERSAL = [
    r"\b(?:nobody|no one|no ?body)\s+(?:ever\s+)?(?:spends?|pays?|buys?|chooses?|"
    r"wants?|sets? out to|goes? looking for)\b",
    r"\b(?:people|nobody|no one|everybody|everyone)\s+(?:don'?t|doesn'?t|never)\s+"
    r"(?:spend|pay|buy|choose|bother)\b",
    r"\bthey can (?:manage|do|live|get by) without\b",
]

# Pattern 47: the strawman comparison. FLAG. Plain incapacity ("nobody can see
# which documents were uploaded") doesn't match.
STRAWMAN = [
    r"\b(?:nobody|no one)\s+(?:ever\s+)?(?:opens|reads|looks at|remembers|follows|"
    r"acts on|opens up|bothers with)\b",
    r"\bwill do more than\s+(?:a|an|any)\b",
    r"\bbeats?\s+(?:a|an|any)\s+\w+\s+(?:nobody|no one|that nobody)\b",
    r"\bmore use than\s+(?:a|an|any)\b",
]

# Pattern 40: article architecture. FLAG.
ARCHITECTURE = [
    r"\bsits? in (?:that|this) (?:post|article|piece)\b",
    r"\bwhat (?:it|this|that) (?:didn'?t|does not|doesn'?t|never) cover(?:ed)?\b",
    r"\brather than this one\b",
    r"\bwhat follows (?:here|is|below)\b",
    r"\b(?:on|in) this (?:list|section|article|piece)\b",
    r"\bthe rest of this (?:post|article|piece)\b",
    r"\bas (?:we|I) said (?:above|earlier in this)\b",
]

# Pattern 33: the genteel circumlocution. FLAG.
CIRCUMLOCUTION = [
    r"\b(?:a|an|the)\s+(?:conversation|discussion|exchange|chat)\s+"
    r"(?:they|he|she|you|nobody|no one)\s+(?:would rather not|doesn'?t want|does not want|"
    r"would prefer not)\b",
    r"\bavoids? (?:a|an|the) (?:conversation|discussion|exchange)\b",
]

# Pattern 34: the effort cliche. FLAG. Scoped to the effort-estimate shape so real
# scheduling ("rather than on Friday afternoon") doesn't match.
EFFORT_CLICHE = [
    r"\b(?:answerable|doable|done|fixed|sorted|solved|achievable|possible|handled)"
    r"\s+(?:in|within|over)\s+(?:an?|a single|one)\s+"
    r"(?:afternoon|morning|hour|day|weekend|evening|lunchtime)\b",
    r"\b(?:a|an|one)\s+(?:morning|afternoon|day|weekend)'?s?\s+work\b",
    r"\bby\s+monday\s+morning\b",
    r"\bin\s+(?:five|ten|fifteen|twenty)\s+minutes\b",
]

# Patterns 53 and 49: the teaser, and the verdict on the advice. FLAG.
TEASER = [
    # only where the phrase ends the sentence: "the risk you never check is your
    # backups" names its subject and is fine
    r"\bthe\s+(?:one|ones|thing|things|part|bit|mistake|risk|step)\s+"
    r"(?:you|nobody|no\s+one)\s+(?:(?:didn'?t|don'?t|never|won'?t|aren'?t|isn'?t|is)\s+)?"
    r"(?:expect|see|notice|talk|tell|mention|check|think|looking)\w*"
    r"(?:\s+(?:about|for|coming))?(?=\s*(?:[.?!:]|\n|$))",
    r"\b(?:you|nobody|no\s+one)\s+(?:didn'?t\s+see|never\s+saw|saw|never\s+see)\s+coming\b",
    r"\bwhat\s+(?:nobody|no\s+one|they)\s+(?:tells?|will\s+tell|won'?t\s+tell)\s+you\b",
    r"\bhiding\s+in\s+plain\s+sight\b",
    r"\b(?:that'?s|that\s+is|which\s+is|it'?s|this\s+is)\s+the\s+(?:right|correct|best|sensible|smart)\s+"
    r"(?:control|answer|call|approach|choice|move|reference|place\s+to\s+start|starting\s+point|option)"
    r"(?=\s*[.!?]|\s+(?:if|for|when|here)\b)",
]

# Patterns 53 and 54 in heading form, checked against each heading (and a one-line
# title) on its own, because headings otherwise run into the next sentence.
TEASER_HEADING = [
    # the slogan heading: two noun phrases balanced on ", and", no verb
    r"^(?:an?|the|one|your)\s+[\w'-]+(?:\s+[\w'-]+){0,2},\s+and\s+(?:an?|the|one|your)\s+[\w'-]+",
    r"^the\s+[\w-]+(?:\s+[\w-]+)?\s+(?:you|your\s+\w+|staff|people|they)\s+"
    r"(?:will|'ll|are\s+going\s+to)\s+(?:see|get|face|hear|meet|notice|need)$",
    r"(?:^|:\s*)(?:how\s+to\s+\w+\s+)?the\s+(?:one|ones|thing|things|part|bit|mistake|risk|step)\s+"
    r"(?:you|nobody|no\s+one)\s+(?:(?:didn'?t|don'?t|never|won'?t|aren'?t|isn'?t|is)\s+)?"
    r"(?:expect|see|notice|talk|tell|mention|check|think|looking)\w*(?:\s+(?:about|for|coming))?$",
]

# Pattern 25: the doubled quantifier. HINT ("if nothing runs, there's nothing to
# migrate" is a legitimate condition and result).
DOUBLED_QUANTIFIER = r"\b(nobody|no\s+one|every|everything|anything|nothing)\b[^.!?\n]{3,120}\b\1\b"

# Patterns 44 and 50: the reader guess and the benefit tail. FLAG.
READER_GUESS = [
    r"\byou'?ll\s+(?:probably|likely|almost\s+certainly|already)\s+(?:recognise|recognize|know|have|find|notice|be\s+familiar)\b",
    r"\byou\s+(?:probably|likely|almost\s+certainly)\s+(?:already\s+)?(?:know|have|use|recognise|recognize|run)\b",
    r"\bchances\s+are\s+(?:you|your)\b",
    r",\s+(?:and|which)\s+[^.!?\n]{0,70}?\b(?:will|would|can|should|could)\s+help\b[^.!?\n]*[.!]",
    r"\bwhich\s+gives\s+[^.!?\n]{0,40}?\bthe\s+(?:chance|opportunity)\s+to\b",
]

# Pattern 51: the epigram tail. HINT ("receive a valid token without ever handling
# the password" is literal and correct).
EPIGRAM_TAIL = [
    r"\bwithout ever \w+ing\b",
    r"\b(?:was|were|is|are) never (?:yours|ours|theirs|mine)\b",
    r"\bnever (?:was|were) (?:yours|ours|theirs)\b",
    r"\bnever so much as\b",
    r"\band nobody ever (?:sees|knows|asks|notices)\b",
]

# Pattern 24: the echoed noun. FLAG. The comma before "and" is required: that's the
# cadence construction rather than ordinary repetition.
ECHOED_NOUN = re.compile(
    r"\b(\w{5,})\b[^.!?]{0,80}?,\s+and\s+(?:it|that|this)[’']?s\s+"
    r"(?:a|an|the)\s+(?:\w+\s+){0,2}\1\b", re.IGNORECASE)

# Pattern 46: the invented objection. The quote itself is a HINT (did anyone say
# it?); the dismissal and the paired negation are FLAGS.
INVENTED_QUOTE = re.compile(
    r"[\"“]\s*(?:we|we'?re|we'?ve|our|i'?m|i'?ve|it'?s fine)\b[^\"”]{2,80}[\"”]",
    re.IGNORECASE)
DISMISSAL = [
    r"\b(?:is|isn'?t|are|aren'?t|was|wasn'?t)\s+not\s+an?\s+"
    r"(?:answer|strategy|plan|defence|defense|excuse|substitute)\b",
    r"\bisn'?t\s+an?\s+(?:answer|strategy|plan|defence|defense|excuse|substitute)\b",
    r"\band\s+(?:neither|nor)\s+(?:is|are|does|do|did|was|were|will)\b",
]

# Pattern 62: contractions.
CONTRACTION_RE = r"\b\w+'(?:s|t|ll|ve|re|d)\b"
UNCONTRACTED_RE = (r"\b(?:it is|that is|we are|you are|they are|do not|does not|did not|"
                   r"cannot|can not|will not|would not|should not|could not|we have|"
                   r"you have|there is|is not|are not|was not|were not|has not|have not|"
                   r"let us)\b")

CHATTY_RE = r"\b(?:you|we|they|i)'ve got\b|\bthere's loads of\b|\ba bit of a\b"  # 63, HINT
US_PERCENT_RE = r"\bpercent\b"  # 64. Doesn't match "percentage". Delete if you write US English.

PROPORTION = (r"(?:a (?:quarter|third|half|fifth)|two[- ]thirds|three[- ]quarters|"
              r"nine[- ]in[- ]ten|seven in ten|half)")
NUMBER_TWICE_RE = [  # 26, HINT
    PROPORTION + r"[^.]{0,40}?\d{1,3}\s*(?:%|per cent)",
    r"\d{1,3}\s*(?:%|per cent)[^.]{0,40}?" + PROPORTION,
]
SCARE_QUOTE_RE = r"[\"“][a-z]{2,12}[\"”]"                               # 32, HINT
CONTINUOUS_RE = r"\bwhat (?:they|you|we)(?:'re| are) \w+ing\b"                    # 28, HINT
DEFINE_BY_NEGATION_RE = r"\b(?:isn't|is not|aren't|are not) (?:what|the usual|the sort)\b"  # 19
LONG_COMPOUND_RE = r",\s+and (?:if|when|because|that's why)\b"                    # 29, HINT


def strip_markdown(md):
    md = re.sub(r"(?s)```.*?```", " ", md)
    md = re.sub(r"`[^`]*`", " ", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", md)
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"^#{1,6}\s*", "", md, flags=re.M)
    md = re.sub(r"[*_>#-]", " ", md)
    return re.sub(r"\s+", " ", md).strip()


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def windowed_ttr(words, window=200):
    if not words:
        return 0.0
    if len(words) <= window:
        return len(set(words)) / len(words)
    ratios = [len(set(words[i:i + window])) / window
              for i in range(0, len(words) - window + 1, window)]
    return statistics.mean(ratios)


def find_all(patterns, text, before=40, after=35):
    """Every match of every pattern, with a little surrounding context."""
    out = []
    for pat in patterns:
        for m in re.finditer(pat, text):
            out.append(text[max(0, m.start() - before):m.end() + after].strip())
    return out


def analyse(md):
    # Pattern 60. Count curly quotes, then straighten them: every pattern below is
    # written with straight apostrophes, so "doesn’t" would otherwise be invisible.
    curly = len(re.findall(r"[‘’“”]", md))
    md = (md.replace("‘", "'").replace("’", "'")
            .replace("“", '"').replace("”", '"'))
    prose = strip_markdown(md)
    low = prose.lower()
    sents = sentences(prose)
    lengths = [len(s.split()) for s in sents] or [0]
    words = re.findall(r"[a-zA-Z']+", low)
    word_count = len(words)
    long_form = word_count >= MIN_WORDS_FOR_CONTRACTIONS

    burstiness = statistics.pstdev(lengths) if len(lengths) > 1 else 0.0
    ttr = windowed_ttr(words)
    phrase_hits = {p: low.count(p) for p in AI_PHRASES if p in low}
    per_1k = sum(phrase_hits.values()) / word_count * 1000 if word_count else 0.0

    neg_par = sum(len(re.findall(p, low)) for p in NEG_PARALLELISM)
    em_dashes = len(re.findall(r"[—―]", md))
    contractions = len(re.findall(CONTRACTION_RE, low))
    uncontracted = len(re.findall(UNCONTRACTED_RE, low))
    contr_per_1k = contractions / word_count * 1000 if word_count else 0.0

    universals = find_all(RHETORICAL_UNIVERSAL, low, 30, 50)
    strawmen = find_all(STRAWMAN, low, 45, 25)
    architecture = find_all(ARCHITECTURE + CIRCUMLOCUTION, low)
    guesses = find_all(READER_GUESS, low, 35, 25)
    teasers = find_all(TEASER, low, 35, 20)
    effort = find_all(EFFORT_CLICHE, low, 45, 25)
    plainness = find_all(ANNOUNCED_PLAINNESS, low, 35, 40)
    significance = find_all(ANNOUNCED_SIGNIFICANCE, low, 35, 45)
    pivots = find_all(CONTRASTIVE_PIVOT, low, 40, 30)
    dismissals = find_all(DISMISSAL, low, 45, 25)
    reassurance = find_all(REASSURANCE, low, 40, 40)
    echoes = ECHOED_NOUN.findall(low)

    # Headings, and a lone one-liner such as a title, are checked on their own.
    lines = [re.sub(r"^#{1,6}\s*", "", ln).strip().lower().rstrip(".?!")
             for ln in md.splitlines() if ln.lstrip().startswith("#")]
    if "\n" not in md.strip() and len(md.split()) <= 20:
        lines.append(md.strip().lower().rstrip(".?!"))
    for line in lines:
        if any(re.search(p, line) for p in TEASER_HEADING) and line not in teasers:
            teasers.append(line)

    staccato_runs, run = [], []
    for s, n in zip(sents, lengths):
        if n <= MAX_FRAGMENT_WORDS:
            run.append(s)
            continue
        if len(run) >= MIN_FRAGMENT_RUN:
            staccato_runs.append(" ".join(run))
        run = []
    if len(run) >= MIN_FRAGMENT_RUN:
        staccato_runs.append(" ".join(run))

    us_percent = len(re.findall(US_PERCENT_RE, low))

    flags = []

    def flag(items, label, advice):
        if items:
            flags.append(f"{label} x{len(items)}: {advice} {items[:3]}")

    # The density measures only mean anything over a whole article.
    if long_form and burstiness < MIN_BURSTINESS:
        flags.append(f"low burstiness ({burstiness:.1f} < {MIN_BURSTINESS}): "
                     "sentence lengths too uniform")
    if long_form and per_1k > MAX_AI_PHRASE_PER_1K:
        flags.append(f"AI-phrase load {per_1k:.1f}/1k > {MAX_AI_PHRASE_PER_1K}: "
                     f"{sorted(phrase_hits)}")
    elif phrase_hits:
        flags.append(f"AI phrases (pattern 7): {sorted(phrase_hits)}")
    if long_form and ttr < MIN_TTR:
        flags.append(f"low lexical diversity (TTR {ttr:.2f} < {MIN_TTR})")
    if long_form and contr_per_1k < MIN_CONTRACTIONS_PER_1K:
        flags.append(f"too few contractions ({contr_per_1k:.1f}/1k < {MIN_CONTRACTIONS_PER_1K}, "
                     f"pattern 62): {uncontracted} uncontracted forms found")
    if neg_par:
        flags.append(f"negative parallelism x{neg_par} (pattern 17): state the point directly")
    if em_dashes:
        flags.append(f"em dashes x{em_dashes} (pattern 56): use a comma, colon, full stop or brackets")
    flag(pivots, "contrastive pivot (18)", "one abstract label swapped for another. Say what happens:")
    flag(echoes, "echoed noun (24)", "a noun restated for cadence:")
    flag(architecture, "article architecture or circumlocution (33, 40)",
         "describing the piece, or naming an abstract event instead of the action:")
    flag(effort, "effort cliche (34)", "a breezy unit of time standing in for an estimate:")
    flag(significance, "announced significance (38)", "ranking a fact instead of delivering it:")
    flag(plainness, "announced plainness (39)", "be plain rather than saying you're about to be:")
    flag(guesses, "reader guess or benefit tail (44, 50)",
         "guessing what the reader knows, or grading the advice. Say what to do:")
    flag(reassurance, "anticipatory reassurance (45)", "soothing an objection nobody raised:")
    flag(dismissals, "knocked-down objection (46)", "'X isn't an answer' / 'and neither is Y':")
    flag(strawmen, "strawman comparison (47)", "advice measured against a caricature:")
    flag(universals, "rhetorical universal (48)", "an absolute asserted as proof:")
    flag(teasers, "teaser, slogan heading or verdict (49, 53, 54)",
         "the line withholds its subject or grades the advice:")
    if staccato_runs:
        flags.append(f"staccato fragments x{len(staccato_runs)} (pattern 21): write the list "
                     f"inside a sentence. First: {staccato_runs[0][:80]!r}")
    if us_percent:
        flags.append(f"'percent' x{us_percent} (pattern 64): UK English is 'per cent' or %")

    return {
        "passed": not flags,
        "flags": flags,
        "hints": {k: v for k, v in {
            "reframe_candidates": find_all(REFRAME_PATTERNS, low, 45, 45),   # 22, 23
            "announced_counts": [" ".join(m) for m in ANNOUNCED_COUNT.findall(md)],  # 37
            "invented_quotes": [m.group(0) for m in INVENTED_QUOTE.finditer(md)],    # 46
            "epigram_tails": find_all(EPIGRAM_TAIL, low, 35, 40),            # 51
            "doubled_quantifiers": [low[max(0, m.start() - 20):m.end() + 20].strip()
                                    for m in re.finditer(DOUBLED_QUANTIFIER, low)],  # 25
            "number_stated_twice": [m.group(0) for p in NUMBER_TWICE_RE
                                    for m in re.finditer(p, low)],           # 26
            "scare_quoted_words": re.findall(SCARE_QUOTE_RE, prose),         # 32
            "present_continuous": re.findall(CONTINUOUS_RE, low),            # 28
            "define_by_negation": re.findall(DEFINE_BY_NEGATION_RE, low),    # 19
            "long_compound_sentences": [s[:100] for s, n in zip(sents, lengths)
                                        if n > LONG_COMPOUND_WORDS
                                        and re.search(LONG_COMPOUND_RE, s.lower())],  # 29
            "chatty_contractions": sorted(set(re.findall(CHATTY_RE, low))),  # 63
            "curly_quotes": curly,                                           # 60
        }.items() if v},
        "stats": {
            "word_count": word_count,
            "sentence_count": len(sents),
            "burstiness_stdev": round(burstiness, 2),
            "avg_sentence_len": round(statistics.mean(lengths), 1),
            "lexical_diversity_ttr": round(ttr, 3),
            "ai_phrase_hits_per_1k": round(per_1k, 2),
            "contractions_per_1k": round(contr_per_1k, 1),
            "uncontracted_forms": uncontracted,
        },
    }


def paragraph_endings(md):
    """The last sentence of every paragraph, to be read on its own (patterns 49-51)."""
    out = []
    for para in md.split("\n\n"):
        para = para.strip()
        if not para or para.startswith(("#", "|", ">", "```")):
            continue
        para = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", para)
        sents = sentences(para)
        if sents:
            out.append(sents[-1])
    return out


def main():
    ap = argparse.ArgumentParser(description="Flag prose that reads as AI-generated.")
    ap.add_argument("input", nargs="?", help="markdown or text file (default: stdin)")
    ap.add_argument("--endings", action="store_true",
                    help="print the last sentence of every paragraph and stop. Read each on "
                         "its own: does it state a fact, or assign an abstract quality?")
    args = ap.parse_args()
    md = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
    if args.endings:
        for i, s in enumerate(paragraph_endings(md), 1):
            print("%2d. %s" % (i, s))
        return 0
    report = analyse(md)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
