# Human voice

A Claude skill for writing that doesn't read as AI-generated, plus a small checker script.

Most "humaniser" prompts stop at banned words and em dashes. This one goes further: about
half the catalogue comes from a human editor going through drafts line by line after they'd
already passed those filters, and writing down each thing that still gave them away.

## What's in it

- `SKILL.md`: the process and the hard rules. Claude reads this first.
- `references/patterns.md`: 64 patterns, each with what to watch for and a before/after.
  Worth reading yourself too. It works as a checklist without Claude.
- `scripts/slop_check.py`: a Python 3 checker with no dependencies. It flags the patterns that
  can be caught mechanically and prints the last sentence of each paragraph for a manual read.

## Installing it

**Claude.ai or the desktop app:** download `human-voice-skill.zip` from the
[latest release](https://github.com/rorycoleman-smith/human-voice/releases/latest), then go to
Settings > Capabilities > Skills, upload it, and switch it on. Claude will use it whenever you
ask it to write or edit something.

**Claude Code:**

```bash
git clone https://github.com/rorycoleman-smith/human-voice ~/.claude/skills/human-voice
```

**Anything else (ChatGPT, Gemini, a custom GPT):** paste `SKILL.md` and `references/patterns.md`
into the instructions. The script won't run there, but the rules still work.

## Using it

Ask Claude to write as normal, or paste a draft and say "humanise this". To check a draft
yourself:

```bash
python3 scripts/slop_check.py my-post.md
python3 scripts/slop_check.py --endings my-post.md
```

The spelling defaults are UK English. If you write in US English, change the table in
`patterns.md` (pattern 64) and delete the `percent` check in the script.

The best habit it teaches: when you spot one tell in a draft, assume there are more of the
same kind and go looking, rather than fixing that one line.

## Licence

MIT. See `LICENSE`, which also carries the notices for the two MIT projects this builds on.
