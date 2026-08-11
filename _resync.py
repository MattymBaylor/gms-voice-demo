import io, hashlib

DEV = "/Users/matthewmartelli/dev/"
new = io.open(DEV + "gms-voice-demo/index.html", encoding="utf-8").read()

ANCHOR = "  .altlink a:hover{border-bottom-color:var(--accent-2)}"
FOLLOW = new[new.index(ANCHOR) + len(ANCHOR):][:300]
assert new.count(ANCHOR) == 1 and new.count(FOLLOW) == 1

for path, sid in [(DEV + "gms-website-3.0-perplexity/public/demo-appointment/index.html", "gms-site-skin"),
                  (DEV + "mattmartelli-site/public/appointment-demo/index.html", "mm-site-skin")]:
    s = io.open(path, encoding="utf-8").read()
    p = s.index(ANCHOR) + len(ANCHOR)
    block = s[p:s.index(FOLLOW, p)]
    assert ('id="%s"' % sid) in block and "body.embed" in block and block.count("<style") == 1

    out = new.replace(ANCHOR, ANCHOR + block, 1)
    check = out.replace(block, "", 1)
    assert check == new, "rebuild drifted from upstream: " + sid

    io.open(path, "w", encoding="utf-8").write(out)
    print(sid, "OK | block", len(block), "| file", len(out),
          "| minus-block md5", hashlib.md5(check.encode("utf-8")).hexdigest())

print("upstream md5", hashlib.md5(new.encode("utf-8")).hexdigest())
