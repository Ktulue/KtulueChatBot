# Web Layer Manual Test Log

**Date started:** 2026-04-06
**Branch under test:** `feat/web-layer` (PR #4)
**QA branch:** `feat/web-layer-qa` (this branch)
**Tester:** Josh (Ktulue)

## How to use this document

Run through the checklist below in order. For each item:
- Tick the box if it works as expected
- Add a note under the item if anything is off (visual glitch, unexpected behavior, console error, etc.)
- If you find a bug, log it in the "Findings" section at the bottom

When testing is complete, this document gets committed to `feat/web-layer-qa`. Any code fixes that come out of testing should be made on `feat/web-layer` directly (so they ship in PR #4), and this branch can pull them in via `git merge feat/web-layer` to keep the testing log up to date with the latest code.

## Setup

- [ ] Pull latest `feat/web-layer-qa` branch and confirm `pytest -v` shows 44 passing
- [ ] Confirm `.env` contains a valid `ANTHROPIC_API_KEY`
- [ ] Run `uvicorn web.app:app --reload` in a terminal at `F:/GDriveClone/Claude_Code/KtulueChatBot`

Expected startup log lines:
```
INFO ktulue.web: Building system prompt...
INFO ktulue.web: System prompt ready.
INFO ktulue.web: Anthropic client ready.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

- [ ] Server started cleanly without errors

## Visual / Layout (chrome desktop)

- [ ] Open `http://localhost:8000` in a browser
- [ ] Page loads with no broken images, missing fonts, or 404s in the browser console (F12 → Network tab)
- [ ] Header shows: logo, "KTULUEBOT" heading, "Chat with The Water Father" tagline
- [ ] Header colors look right — green accent matching ktulue.com landing page
- [ ] Background is dark, matching the landing page
- [ ] Geizer font is rendering for the heading (not falling back to a default serif)
- [ ] Initial bot greeting message appears in the message area (left-aligned bot bubble)
- [ ] Input field and Send button are visible at the bottom
- [ ] Footer disclosure text reads exactly: *"Conversations are logged for quality, tuning, and diagnostic purposes only."* — and is italicized

## First message (happy path)

- [ ] Type "Hi! Who are you?" and press Enter
- [ ] Your message appears immediately on the right (user bubble)
- [ ] Typing indicator (three pulsing dots) appears in a bot bubble on the left
- [ ] Within ~1-2 seconds, the typing indicator disappears
- [ ] Bot response streams in word-by-word
- [ ] When the response is complete, the input becomes usable again
- [ ] The response sounds like Josh (first person, in character — not "I am an AI")

## Multi-turn conversation

- [ ] Send a follow-up like "What do you stream?"
- [ ] Bot's answer is contextually aware (knows it just introduced itself)
- [ ] Send a third message and confirm conversation continues coherently

## Per-tab session isolation

- [ ] Open `http://localhost:8000` in a SECOND browser tab
- [ ] Second tab starts fresh — only the greeting message, no conversation history from tab 1
- [ ] Send a different message in tab 2 and confirm it doesn't affect tab 1
- [ ] Switch back to tab 1 and confirm its history is still there

## Refresh resets session

- [ ] In tab 1, refresh the page (F5)
- [ ] Conversation resets to just the greeting
- [ ] A new session ID is generated (this is correct — sessionStorage is per-tab AND per-page-load)

## Server logs (terminal where uvicorn is running)

- [ ] Each user message produces a log line: `INFO ktulue.web: [<session-id>] user: <text>`
- [ ] Each bot response produces a log line: `INFO ktulue.web: [<session-id>] bot: <text>`
- [ ] Different tabs show different session IDs in the logs

## Error handling

- [ ] In the input, type an extremely long message (e.g. paste a wall of text) — should it be accepted or rejected?
- [ ] Try sending an empty message — Send button should not fire (the form has a `required` attribute)
- [ ] Open browser DevTools (F12 → Console) — should be no JavaScript errors during normal use

### Testing the friendly error path (optional / advanced)

To force an error and verify the friendly bubble appears:

1. Stop the server (Ctrl+C)
2. Edit `.env` and temporarily set `ANTHROPIC_API_KEY=invalid_key_for_testing`
3. Restart `uvicorn web.app:app --reload`
4. Send a message in the browser
5. Confirm the bot returns a friendly in-character error bubble (not an exception or 500)
6. Confirm the terminal shows an ERROR log line with traceback
7. **IMPORTANT:** Restore the real API key in `.env` afterward

- [ ] Friendly error bubble appears
- [ ] Server log shows ERROR with full traceback and session ID
- [ ] Real API key restored

## Mobile / responsive (optional)

- [ ] Open Chrome DevTools (F12) → Toggle device toolbar (Ctrl+Shift+M)
- [ ] Try a few device sizes (iPhone, iPad, etc.)
- [ ] Layout adapts cleanly — no horizontal scrolling, no clipped content

## Browser compatibility (optional)

- [ ] Test in a second browser (Firefox or Edge)
- [ ] Streaming still works
- [ ] No console errors

## Shutdown

- [ ] Press Ctrl+C in the terminal
- [ ] Server shuts down cleanly (no hung processes, no traceback noise)

---

## Findings

Log any issues you find here. For each one, note:
- **What happened** (what you saw)
- **What you expected** (what should have happened)
- **Steps to reproduce** (so it can be fixed and re-tested)
- **Severity:** Critical (broken) / Important (visible defect) / Minor (polish)

### Example format

> **Finding 1: [short title]**
> - **What:** [description]
> - **Expected:** [description]
> - **Repro:** [steps]
> - **Severity:** [Critical / Important / Minor]
> - **Status:** [Open / Fixed in <commit> / Won't fix]

### Findings log

_(none yet)_

---

## Sign-off

- [ ] All checklist items pass OR all findings are resolved or accepted
- [ ] Ready to merge PR #4

**Tested by:** _________
**Date completed:** _________
