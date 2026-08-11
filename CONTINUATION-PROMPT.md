Handoff 003 · 2026-08-11 · Build the conversational voice agent demo (companion to the sales one) [Sonnet]

## What you're building

A second browser voice-agent demo, sibling to the appointment-confirmation one that is already live.
That one **sells**. This one **talks**. A visitor enters their name and a few things about
themselves, and gets a warm, genuinely enjoyable open-ended conversation.

Matt's demand signal: prospects keep asking for conversational agents, not just sales bots. One
person asked whether he could build an agent based on her grandmother who passed away.

## What already exists — reuse it, don't rebuild it

Everything below is live and working. Read `realtime.html` in the repo first; it is the template.

**Repo:** `MattymBaylor/gms-voice-demo`, GitHub Pages, `main` branch, root.
Working copy on Matt's Mac at `/tmp/gms-demo`. Deploy from the Mac with `gh` — the Cowork cloud
container's git proxy blocks non-authorized repos.

| Page | URL |
|---|---|
| Sales agent (GPT-4.1 → xAI TTS) | https://mattymbaylor.github.io/gms-voice-demo/ |
| Sales agent, embeddable | same URL + `?embed=1` |
| **Sales agent, realtime — the template** | https://mattymbaylor.github.io/gms-voice-demo/realtime.html |

| n8n workflow | ID | Webhook |
|---|---|---|
| Realtime Token Minter | `zAX2ZFQ2njcnwrAO` | `/webhook/gms-demo-token` |
| Browser Agent (GPT-4.1 + TTS) | `PkGnNOTIc7su1hhR` | `/webhook/gms-demo-chat` |
| Phone path (Retell, currently 402) | `QBIsO13ss2GQHMk1` | `/webhook/gms-voice-demo` |

The realtime architecture, already proven end to end:

```
browser → POST /webhook/gms-demo-token   (n8n mints a 10-min xAI client secret)
       → wss://api.x.ai/v1/realtime?model=grok-voice-latest
          auth via subprotocol:  ["xai-client-secret." + token]
       → session.update { instructions, voice, turn_detection: server_vad }
       → mic PCM16 @16k up, audio PCM16 @24k down, played through a
         300-3400Hz telephone band-pass + pink-noise room bed
```

## Hard-won gotchas — these cost hours, do not rediscover them

1. **The ephemeral token is single-use per WebSocket connection.** Mint a fresh one for every
   call. A second connect on the same token returns 401.
2. **Browsers cannot set WebSocket headers.** Auth must go through the `Sec-WebSocket-Protocol`
   subprotocol form, not `Authorization`. Verified working.
3. **Grok follows instructions less literally than GPT-4.1.** Vague rules get improvised around.
   Give it the *exact words* you want ("you MUST say 'let me connect you with our team'") or it
   invents its own. This took the behavioural suite from 2/4 to 3/3.
4. **`AGENT_PHOTO` is an inlined base64 data URI, not a filename.** After editing any HTML file,
   re-run the inliner or the photo silently reverts to a broken `christina.jpg` reference.
5. **GitHub Pages sends `cache-control: max-age=600`**, which overrides any `<meta>` cache tag.
   Use `?v=N` while iterating. Not a problem for first-time visitors.
6. **xAI TTS needs `with_timestamps: true`** to return base64 JSON. Otherwise you get raw bytes,
   and this n8n stores binary on the filesystem, so you receive the literal string
   `"filesystem-v2"` instead of audio. (Only relevant to the non-realtime page.)
7. **n8n's `updateNodeParameters` merges.** Use `setNodeParameter` on `/options` to replace.

## The build

Create `talk.html` from `realtime.html`. The engine is identical — only the intake form and the
`instructions()` block change.

**Intake:** first name, then two or three things that give the conversation somewhere to go —
a hobby or interest, where they grew up, what they do. Keep it to four fields. The whole point is
that she knows *something* real about them and can be genuinely curious.

**Her character:** warm, curious, funny, a great listener. She asks follow-up questions about what
they actually said rather than steering anywhere. No selling, no appointment, no handoff triggers —
delete all of that. The one-or-two-sentence rule and the filler-word guidance should stay; they are
what made the sales agent sound human.

**Voice:** `ara` works well. `eve`, `luna`, `celeste`, `iris` and `carina` are also available and
were sampled — pick per persona.

## On the grandmother request — worth thinking about before building

Matt should decide this, not you. A memorial voice agent is a real product with real demand, and
it can be done with care — but it is meaningfully different from a demo, and getting it wrong
hurts someone who is grieving. Raise these with him rather than deciding unilaterally:

- Whose consent covers the likeness and the voice, and can that be evidenced?
- Is it framed as remembrance, or as the person still being present? Those land very differently.
- What happens when someone uses it heavily, or at 3am on a bad night?

None of that blocks the general conversational agent — build that first. It is the same engine
and Matt has broad demand for it.

## Working agreements

- Recommendation first, one alternative at most. No preamble, no pep talk.
- Copy-paste-ready complete blocks, never fragments.
- Verify before claiming. Every claim in this handoff was tested against the live endpoints.
- Reversible and inside the repo → just do it, then report.

## State at handoff

Finished and verified live: realtime page (3/3 behavioural tests), sales page, embed mode,
hands-free mic, Aria voice, phone-line audio, Christina's photo, fictional-company disclaimer,
client name scrubbed from every surface.

Not started: `talk.html`.

Assumption made without asking: the realtime page was deployed as a *separate* file rather than
replacing the live sales demo, so nothing Matt had already approved was put at risk. He has not
yet chosen which of the two becomes the primary Upwork link.

Still blocked on Matt: Retell billing (phone path stays off until then — flip `PHONE_ENABLED`
to `true` in `index.html` and it returns), and whether to brand the embed with the
growthmindset.ai logo.
