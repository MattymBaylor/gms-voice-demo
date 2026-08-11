# GMS Voice Agent Demo

Live AI voice agent demo — a prospect fills in an appointment and talks to Christina, an
appointment-confirmation agent, right in the browser.

**Live page:** https://mattymbaylor.github.io/gms-voice-demo/

---

## Embedding it in another site

The same page runs in a stripped-down widget mode. It switches automatically when it detects
it's inside an iframe, or you can force it with `?embed=1`.

### Copy-paste embed

```html
<iframe
  src="https://mattymbaylor.github.io/gms-voice-demo/?embed=1"
  title="Live AI voice agent demo"
  width="100%"
  height="680"
  style="border:0;max-width:560px;display:block;margin:0 auto;"
  allow="microphone"
  referrerpolicy="no-referrer-when-downgrade"
></iframe>
```

**`allow="microphone"` is required.** Without it the browser blocks mic access inside the
iframe and the agent will never hear anything. This is the single most common way an embed
breaks.

The host page must also be served over **HTTPS**. Browsers refuse microphone access on
plain HTTP, iframe or not.

### Auto-resizing (optional)

The widget posts its height to the parent window whenever it changes, so the iframe can grow
when the call view opens. Drop this next to the iframe:

```html
<script>
  window.addEventListener("message", function (e) {
    if (e.data && e.data.gmsVoiceDemoHeight) {
      var f = document.querySelector('iframe[src*="gms-voice-demo"]');
      if (f) f.style.height = e.data.gmsVoiceDemoHeight + "px";
    }
  });
</script>
```

Without it, the fixed `height="680"` is enough for the form and most of the call view.

### Widget mode drops

The header, the left-hand pitch column, and the footer. What remains is the card: the
appointment form, the call button, and the live transcript. The background goes transparent
so it inherits the host page.

---

## How it works

```
Browser (mic + speech-to-text)
  → n8n webhook  /webhook/gms-demo-chat
  → GPT-4.1 with Christina's prompt, appointment details injected as live variables
  → xAI TTS (voice "ara")
  → browser plays it through a telephone band-pass with a room-tone bed
```

A phone-call path also exists (`/webhook/gms-voice-demo` → Retell), currently switched off.

## Configuration

All at the top of the `<script>` block in `index.html`:

| Flag | Purpose |
|---|---|
| `PHONE_ENABLED` | `true` restores the "Call me now" phone path. Off while telephony billing is down. |
| `TELEPHONE_FX` | Band-limits her voice to 300–3400 Hz and adds the call-center room tone. |
| `AGENT_PHOTO` | Base64 data URI of Christina's photo, inlined so it can't fall out of sync. |

## Editing note

`AGENT_PHOTO` holds an inlined data URI, not a filename. After editing `index.html`, re-run the
inliner or the photo reverts to a plain `christina.jpg` reference.
