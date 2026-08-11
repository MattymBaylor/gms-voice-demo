# Embed codes — GMS voice agent demo

Two versions are live. Both are self-contained; nothing to install.

---

## 1. Realtime agent (recommended)

Grok speech-to-speech. Human prosody, no delay, and the visitor can talk over her.

**Direct link**

```
https://mattymbaylor.github.io/gms-voice-demo/realtime.html
```

**Embed**

```html
<iframe
  src="https://mattymbaylor.github.io/gms-voice-demo/realtime.html"
  title="Live AI voice agent demo"
  width="100%"
  height="720"
  style="border:0;max-width:560px;display:block;margin:0 auto;"
  allow="microphone"
  referrerpolicy="no-referrer-when-downgrade"
></iframe>
```

---

## 2. Original agent (GPT-4.1 + xAI voice)

Turn-based. Runs Matt's exact Retell script on the model it was tuned for.

**Direct link**

```
https://mattymbaylor.github.io/gms-voice-demo/
```

**Embed**

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

---

## Two things that will break an embed

**`allow="microphone"` is mandatory.** Leave it off and the browser blocks the mic inside the
iframe. The page looks fine, the button works, and the agent never hears a word — with no error
message. This is the single most common way an embed fails.

**The host page must be HTTPS.** Browsers refuse microphone access on plain HTTP, iframe or not.

---

## Optional: auto-resize

The original page posts its height to the parent as the view changes. Drop this beside the iframe:

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

Without it the fixed height is enough for the form and most of the call view.

---

## Switching the phone path back on

When Retell billing clears, edit `index.html`:

```js
var PHONE_ENABLED = false;   →   var PHONE_ENABLED = true;
```

That restores the phone field, the live "Call (xxx) xxx-xxxx now" button, and the browser
fallback. Nothing else changes. Re-run the photo inliner after editing.
