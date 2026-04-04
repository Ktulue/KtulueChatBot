# Premises

> Office Hours — Builder Mode
> Date: 2026-04-04
> Phase: Premise Challenge

## Context
Tested four foundational assumptions before generating approaches. All four Builder-mode premise checks were run: right problem framing, what happens if we do nothing, existing tools that partially solve this, and scope honesty.

## Findings

### Premise 1: The API wiring is not the learning goal
You already know (or can quickly learn) how to call Claude's API. The real learning is in prompt engineering, personality tuning, guardrails, and context management.

**Result: AGREE**

### Premise 2: CLI first is the right sequencing
Building a web UI before the personality layer is dialed in means debugging two things at once. Terminal-first lets you iterate on the hard part (personality) without frontend noise.

**Result: AGREE**

### Premise 3: The bot needs curated knowledge about you, not RAG
At this scale (one person's info), a well-crafted system prompt with key facts beats building a retrieval pipeline. RAG is overkill until you have more content than fits in a context window.

**Result: AGREE**

### Premise 4: Scope is honest
The skateboard (CLI bot) is genuinely buildable in one session. The car (deployed web chatbot with streaming) is a multi-week arc, not a weekend project.

**Result: AGREE**

## Key Takeaways
- All premises confirmed — no fundamental misalignment between assumptions and intent
- The learning-first framing is load-bearing: it determines what to prioritize at each stage
- RAG is explicitly deferred — system prompt with curated facts is the right starting architecture
