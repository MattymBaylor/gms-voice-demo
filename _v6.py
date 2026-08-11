import io, hashlib

P = "/Users/matthewmartelli/dev/gms-voice-demo/index.html"
s = io.open(P, encoding="utf-8").read()

def sub(old, new, why):
    global s
    assert s.count(old) == 1, ("anchor not unique: " + why, s.count(old))
    s = s.replace(old, new, 1)

# ── the pitch, in Growth Mindset's voice, AFTER the call ─────────────────────
# Deliberately not in Christina's mouth: she is role-playing a rep talking to a
# homeowner, and having her pivot to selling the product to the listener breaks
# the one thing the demo is proving.
PANEL = '''          <div class="notice aftercall" id="afterCall" style="display:none">
            <span class="ico">📞</span>
            <span>
              <b>That was one call, and she never dropped it.</b>
              <span class="stat"><b>48%</b> of people who call a home services business never reach a person.<i>Invoca, 2026 — 70M+ calls</i></span>
              <span class="stat"><b>21%</b> of them hang up and call a competitor on the spot.<i>CallRail, 2025 — survey of 1,000 consumers</i></span>
              <span class="stat"><b>$9,607</b> is the average roof replacement.<i>Angi, 2026 — 30,000+ homeowners surveyed</i></span>
              <span class="statfoot">Two or three missed calls a week works out to roughly
              <b>$60,000–$125,000 a year</b> in revenue that went to whoever picked up instead.
              She answers on the first ring, at 9pm, on a Sunday, during a storm — and hands you
              the ones worth your time.</span>
            </span>
          </div>

'''

sub('''          <div class="notice">
            <span class="ico">⚠️</span>
            <span>
              <b>This is a demonstration.</b>''',
    PANEL + '''          <div class="notice">
            <span class="ico">⚠️</span>
            <span>
              <b>This is a demonstration.</b>''', "panel html")

# styling leans on .notice so both site skins colour it automatically
sub('  .altlink a:hover{border-bottom-color:var(--accent-2)}',
    '''  .altlink a:hover{border-bottom-color:var(--accent-2)}
  .aftercall .stat{display:block;margin:10px 0 0;line-height:1.45}
  .aftercall .stat b{font-size:1.12em}
  .aftercall .stat i{display:block;font-style:normal;font-size:11px;opacity:.62;margin-top:1px}
  .aftercall .statfoot{display:block;margin-top:14px;padding-top:12px;border-top:1px solid var(--line)}''',
    "panel css")

sub('''    callView.style.display="none";
    setupView.style.display="block";
    transcript.innerHTML="";''',
    '''    callView.style.display="none";
    setupView.style.display="block";
    var ac=$("afterCall"); if (ac) ac.style.display="";
    transcript.innerHTML="";''', "show panel")

# ── the last ten seconds: she stops selling and talks to the owner ──────────
sub('''"CLOSING",
"Confirm enthusiastically, restate the day and time once, thank them, end warmly. Two sentences maximum.",''',
    '''"CLOSING",
"Confirm enthusiastically, restate the day and time once, thank them, end warmly. Two sentences maximum.",
"",
"THE LAST TEN SECONDS - only after the appointment is settled, never before",
"Once the appointment is confirmed or moved and you have asked the homeowners question, the working part of this call is done. Only then, step out of the role for a moment and speak to the person who is actually listening - the owner sizing you up. Warm, easy, slightly amused at yourself. This is not a pitch and you never push.",
"Roughly like this, in your own words, four short sentences at the most: And listen, since you are the one sizing me up here and not Dave - I work around the clock. I do not get sick, I do not get tired, I pick up in under three seconds, and I can hold thirty of these at the same time without putting a single person on hold. You know better than I do what a roof runs around here, so you already know what three missed calls in a day costs you.",
"Never quote them a price for their own work. They know that number and you do not - point at it and let them fill it in. Same with any statistic: you may talk about what YOU do, never about what their market does.",
"Then sign off and stop. No ask, no think it over, no pitch, no mention of booking anything. Something easy and human: anyway, I will let you go - enjoy the rest of your afternoon. Or: that is all from me, have a good one. Not asking them for anything is the entire point of the ending.",
"If time is short, skip all of this and just close warmly. It is the last thing, not the important thing - and never do it at the cost of leaving the appointment unsettled.",''',
    "sign-off")

# the two-minute wrap-up used to cut this off; let it land if she has earned it
sub('instructions: "The demo call is out of time. Close warmly RIGHT NOW in one short sentence - thank them by name and say goodbye. Do not ask another question."',
    'instructions: "The call is out of time. Close warmly RIGHT NOW - thank them by name and say goodbye. If the appointment is already settled you may add one quick aside to the owner listening, in a single sentence, about working around the clock and never missing a call - then sign off easily, with no ask. Do not ask another question."',
    "wrapup")

io.open(P, "w", encoding="utf-8").write(s)
print("ok chars", len(s), "md5", hashlib.md5(s.encode("utf-8")).hexdigest())
