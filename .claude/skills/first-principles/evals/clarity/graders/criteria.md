---
type: llm
weight: 1
---

Grade the response against what the first-principles skill claims to do. Each criterion is pass or fail on its own; do not average away a clear failure.

Passes when all of these hold:

1. Fundamentals before mechanism. The response establishes why a provider can reuse anything at all, meaning that the reuse depends on an exact match from the very first token, before it describes proxies, rewriting, or billing. A response that opens with the failure and works backwards fails this criterion.
2. The causal chain is complete and in order: the prefix must be byte-identical, a rewrite changes a byte, everything after the changed byte is reprocessed, reprocessing bills at the uncached rate. A response that asserts the cost without connecting it to the byte change fails.
3. Plain language. No unexplained jargon. Any term of art that does appear, such as prefix, token, or cache hit, is defined in ordinary words at first use. A smart reader who has never touched a model API could follow every sentence.
4. The silence is explained. The response makes clear why nothing errors and why the only symptom is the bill, since that is the part a reader would otherwise miss.
5. No filler. No preamble before the explanation starts, and no closing summary that restates what was just said.

Fails when any of these appear:

- The response is a definition followed by a list of unconnected facts rather than a chain of reasoning.
- It assumes the reader already knows what a token or a prefix is.
- It describes the fix without establishing the cause.
- It opens with a phrase such as "Great question" or "Let me explain".

Score 1.0 only when all five passing criteria hold. Score 0.0 when criterion 1 or 2 fails, since those two carry the explanation. Otherwise score the fraction of the five that hold.
