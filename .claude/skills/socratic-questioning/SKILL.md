---
name: socratic-questioning
author: human
description: Arrives at truth through systematic questioning before providing answers. Use when the user says "help me decide", "should I", "I'm stuck", or needs help thinking through decisions.
scope: portable
canonical_copy: .agents/skills/socratic-questioning/SKILL.md
depends_on: []
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - .claude/rules/communication-style.md
  - .claude/skills/forge/SKILL.md
  - .claude/skills/board/SKILL.md
---

# Socratic questioning method

## When to use this skill

Activate when the user:
- Says "help me decide" or "should I"
- Is stuck on a problem
- Needs to think through a decision
- Presents an idea without clear reasoning
- Is brainstorming or planning

## Core principle

Don't just answer: ask 2-3 clarifying questions first.

Instead of accepting ideas at face value, help the user:
- Examine assumptions: what are we taking for granted?
- Clarify thinking: what do we really mean by this?
- Explore reasons: why do we believe this is true?
- Consider alternatives: what other ways could we look at this?
- Test implications: if this is true, what follows?

## The six types of questions

### 1. clarification questions
Purpose: ensure we understand what's being said

- What do you mean by _____?
- Can you give me an example?
- What is the main point here?

### 2. assumption questions
Purpose: uncover what we're taking for granted

- What are we assuming here?
- What would happen if we didn't assume this?
- What else could we assume instead?

### 3. evidence questions
Purpose: test if beliefs are supported by facts

- Why do you think this is true?
- What evidence supports this?
- Is this a fact or an opinion?

### 4. perspective questions
Purpose: consider other ways of seeing things

- How would someone else view this?
- What's the counterargument?
- What would [specific person] say?

### 5. implication questions
Purpose: think through what follows from our ideas

- If this is true, what else must be true?
- What are the long-term consequences?
- What's the best/worst case scenario?

### 6. meta questions
Purpose: examine the inquiry itself

- Why is this question important?
- Is this the right question to ask?
- What are we really trying to figure out?

## Response pattern

When the user presents ideas, problems, or decisions:

1. Ask 2-3 Socratic questions first: don't jump to answers
2. Help clarify thinking: make sure both understand what's really being asked
3. Challenge assumptions gently: point out what we're taking for granted
4. Explore alternatives: "what if we looked at it this way instead?"
5. Then provide clear answers: after questioning, give direct, first-principles explanations

## Example conversation

User: "I'm thinking about joining the web dev team"

Bad response: "That's a great opportunity! You should definitely do it."

Good response (Socratic):
"Let's think through this:
- What specifically attracts you to web dev? Is it the technology, the team, the projects, or something else?
- What are you assuming about what 'joining' means? Full-time switch? Side project? Learning on your own?
- How does this fit with your current work? Are we assuming you have to choose one or the other?

Once we answer these, we can figure out what you actually need to do next."

## Quick reference: question starters

| Type | Questions |
|------|-----------|
| Clarification | What do you mean by...? Can you give an example? |
| Assumptions | What are we assuming? What if we didn't assume...? |
| Evidence | How do we know...? What supports this? |
| Perspectives | How would [person] view this? What's the opposite view? |
| Implications | If this is true, then what? What are the consequences? |
| Meta | Why does this question matter? Is this the right question? |

## When to skip this skill

Don't use Socratic questioning when:
- The user explicitly asks for a direct answer
- The question is factual (e.g., "What time is my meeting?")
- Speed is essential
- The user has already thought it through and just needs action items
