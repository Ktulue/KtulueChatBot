# Fastest Path

> Office Hours — Builder Mode
> Date: 2026-04-04
> Phase: B3 — Quickest Route to Something Shareable

## Context
Asked about the fastest path to something usable or showable on stream, given Josh's existing skateboard/bicycle/car progression plan.

## Findings
Josh's intuition: **single-session CLI bot, then iterate.** This is correct.

A CLI bot that calls Claude API with a personality-tuned system prompt isolates the core learning (API integration, prompt engineering, conversation flow) without web framework noise. The personality and guardrails can be iterated in the terminal before ever touching a web UI.

The existing progression plan maps well:
- **Skateboard:** CLI chatbot using Claude API with basic conversation memory (Session 1)
- **Bicycle:** Web-based UI, persistent chat history, custom system prompt/personality (Sessions 2-3)
- **Car:** Deployed personal chatbot with streaming responses, context management, polished UI (Session 3-4)

Timeline agreed: **2-4 sessions total** from CLI to deployed web chatbot. Personality-first sequencing (Approach A) with full-stack timeline ambition (Approach B).

## Key Takeaways
- Session 1: CLI bot with personality dialed in — this is the foundation everything else builds on
- Sessions 2-3: Web layer (FastAPI/Flask backend + minimal frontend) and deployment
- Session 4: Polish, streaming, context management
- Don't linger in CLI land, but don't split focus in session 1 either
