// Zero Work AI — mini-site behaviour. No cookies, no tracking. The head script has already set
// html.js plus html.motion or html.motion-none before first paint.
(function () {
  var html = document.documentElement;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var motionOn = function () { return html.classList.contains("motion") && !html.classList.contains("motion-paused"); };
  var svgs = function () { return document.querySelectorAll("svg.smil"); };

  // ── 1. accessibility menu (our own; no third-party plugin) ──
  // Motion on/off lives here — WCAG 2.2.2: every ambient loop can be stopped.
  var live = document.getElementById("a11y-live");
  var say = function (msg) { if (live) { live.textContent = ""; setTimeout(function () { live.textContent = msg; }, 60); } };
  var store = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };
  var prefs = {}; try { prefs = JSON.parse(localStorage.getItem("zw-a11y") || "{}") || {}; } catch (e) {}
  function btn(k) { return document.querySelector("[data-a11y='" + k + "']"); }
  function pressed(k, on) { var b = btn(k); if (b) b.setAttribute("aria-pressed", on ? "true" : "false"); }

  function setMotion(on, save) {
    html.classList.toggle("motion-paused", !on && html.classList.contains("motion"));
    if (on) { html.classList.remove("motion-none", "motion-paused"); html.classList.add("motion"); }
    svgs().forEach(function (s) { try { on ? s.unpauseAnimations() : s.pauseAnimations(); } catch (e) {} });
    pressed("motion", !on);
    if (save) store("zw-motion", on ? "on" : "off");
  }
  if (!html.classList.contains("motion")) {
    svgs().forEach(function (s) { try { s.pauseAnimations(); s.setCurrentTime(0); } catch (e) {} });
    setMotion(false, false);
  } else { setMotion(true, false); }

  function applyPrefs() {
    html.classList.toggle("a11y-contrast", !!prefs.contrast); pressed("contrast", !!prefs.contrast);
    html.classList.toggle("a11y-links", !!prefs.links); pressed("links", !!prefs.links);
    html.classList.toggle("a11y-font", !!prefs.font); pressed("font", !!prefs.font);
    html.classList.remove("a11y-text-1", "a11y-text-2"); if (prefs.text) html.classList.add("a11y-text-" + prefs.text);
    store("zw-a11y", JSON.stringify(prefs));
  }
  applyPrefs();

  var menuBtn = document.querySelector(".a11y-btn"), panel = document.getElementById("a11y-panel");
  function openMenu(open) {
    if (!panel) return;
    panel.hidden = !open; menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) { var first = panel.querySelector("[data-a11y]"); if (first) first.focus(); } else { menuBtn.focus(); }
  }
  if (menuBtn && panel) {
    menuBtn.addEventListener("click", function () { openMenu(panel.hidden); });
    panel.querySelector(".a11y-close").addEventListener("click", function () { openMenu(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) openMenu(false); });
    document.addEventListener("click", function (e) { if (!panel.hidden && !e.target.closest(".a11y")) { panel.hidden = true; menuBtn.setAttribute("aria-expanded", "false"); } });
    panel.addEventListener("click", function (e) {
      var b = e.target.closest("[data-a11y]"); if (!b) return;
      var k = b.getAttribute("data-a11y");
      if (k === "motion") { var stop = b.getAttribute("aria-pressed") !== "true"; setMotion(!stop, true); say(stop ? "האנימציות נעצרו" : "האנימציות הופעלו"); return; }
      if (k === "text-up") { prefs.text = Math.min(2, (prefs.text || 0) + 1); applyPrefs(); say(prefs.text === 2 ? "הטקסט בגודל המקסימלי" : "הטקסט הוגדל"); return; }
      if (k === "text-down") { prefs.text = Math.max(0, (prefs.text || 0) - 1); applyPrefs(); say(prefs.text ? "הטקסט הוקטן" : "הטקסט בגודל הרגיל"); return; }
      if (k === "reset") { prefs = {}; applyPrefs(); setMotion(!reduce, true); try { localStorage.removeItem("zw-motion"); } catch (e2) {} say("כל ההגדרות אופסו"); return; }
      prefs[k] = !prefs[k]; applyPrefs();
      say(b.textContent.trim() + (prefs[k] ? " הופעל" : " כובה"));
    });
  }

  // ── 2. header glass after scrolling ──
  var header = document.querySelector(".site-header");
  var onScroll = function () { if (header) header.classList.toggle("scrolled", window.scrollY > 8); };
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // ── 3. scroll reveals + count-up ──
  var revealAll = function () { document.querySelectorAll(".rv").forEach(function (el) { el.classList.add("in"); }); };
  function countUp(el) {
    var to = parseInt(el.getAttribute("data-to"), 10), suffix = el.getAttribute("data-suffix") || "";
    if (!to || !motionOn()) return;
    var t0 = null, dur = 1300;
    function step(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / dur); var e = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(to * e) + (k === 1 ? suffix : ""); if (k < 1) requestAnimationFrame(step); }
    el.textContent = "0"; requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        en.target.querySelectorAll("[data-to]").forEach(countUp);
        io.unobserve(en.target);
      });
    }, { threshold: 0.14, rootMargin: "0px 0px -6% 0px" });
    document.querySelectorAll(".rv").forEach(function (el) { io.observe(el); });
    // Safety net: whatever the observer missed (very tall viewports, crawlers that render) shows after 3s.
    setTimeout(revealAll, 3000);

    // ── 4. the phone follows the step in the middle of the screen ──
    var phone = document.querySelector(".story .phone");
    var steps = document.querySelectorAll(".story-step");
    if (phone && steps.length) {
      var so = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          steps.forEach(function (s) { s.classList.toggle("on", s === en.target); });
          phone.setAttribute("data-step", en.target.getAttribute("data-step"));
        });
      }, { rootMargin: "-45% 0px -45% 0px" });
      steps.forEach(function (s) { so.observe(s); });
    }
  } else { revealAll(); document.querySelectorAll(".story-step").forEach(function (s) { s.classList.add("on"); }); }

  // ── 5. light that follows the pointer on feature tiles ──
  document.querySelectorAll(".tile").forEach(function (t) {
    t.addEventListener("pointermove", function (ev) {
      var r = t.getBoundingClientRect();
      t.style.setProperty("--mx", (ev.clientX - r.left) + "px");
      t.style.setProperty("--my", (ev.clientY - r.top) + "px");
    });
  });

  // ── 6. the store that matches the visitor's phone goes first ──
  try {
    if (/Android/i.test(navigator.userAgent || "")) {
      document.querySelectorAll(".stores, .foot-stores").forEach(function (box) {
        var gp = box.querySelector("[data-store='android']"); if (gp) box.insertBefore(gp, box.firstChild);
      });
    }
  } catch (e) {}

  // ── 7. the lead form → site-lead edge function → Monday leads board ──
  var ENDPOINT = "https://jjbxsivcjhpuobpohpoz.supabase.co/functions/v1/site-lead";
  // Public anon key — the same one shipped inside the app; not a secret.
  var ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpqYnhzaXZjamhwdW9icG9ocG96Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIxMTYzNTUsImV4cCI6MjA5NzY5MjM1NX0.CRtQPXuDTiG8LhSiBiv8zpFh-Pi6rboN7AiBGppKPfA";
  var started = Date.now();
  function israeliPhone(raw) {
    var d = String(raw || "").replace(/\D/g, "");
    if (d.indexOf("00972") === 0) d = d.slice(5); else if (d.indexOf("972") === 0) d = d.slice(3);
    if (d.charAt(0) !== "0") d = "0" + d;
    return /^0(5\d{8}|7\d{8}|[2-4689]\d{7})$/.test(d) ? d : "";
  }
  function setError(form, name, msg) {
    var input = form.querySelector("[name='" + name + "']"), err = form.querySelector("#" + form.id + "-" + name + "-error");
    if (!input || !err) return;
    if (msg) { input.setAttribute("aria-invalid", "true"); err.textContent = msg; err.hidden = false; }
    else { input.removeAttribute("aria-invalid"); err.textContent = ""; err.hidden = true; }
  }
  document.querySelectorAll("form.lead-form").forEach(function (form) {
    var status = form.querySelector(".form-status"), button = form.querySelector("button[type='submit']");
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var name = form.elements.name.value.trim(), phone = israeliPhone(form.elements.phone.value.trim()), bad = null;
      setError(form, "name", name.length < 2 ? "נא לכתוב שם מלא." : ""); if (name.length < 2) bad = bad || form.elements.name;
      setError(form, "phone", !phone ? "נא לכתוב מספר טלפון ישראלי, למשל 050-1234567." : ""); if (!phone) bad = bad || form.elements.phone;
      if (bad) { bad.focus(); return; }
      status.hidden = true; button.disabled = true; button.textContent = "שולחים…";
      var payload = { name: name, phone: phone, business: form.elements.business.value.trim(), message: form.elements.message.value.trim(),
        marketing_consent: !!form.elements.marketing_consent.checked, website: form.elements.website.value, elapsed_ms: Date.now() - started, page: location.pathname };
      fetch(ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", "apikey": ANON, "Authorization": "Bearer " + ANON }, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok && j.ok, j: j }; }); })
        .then(function (res) {
          if (res.ok) { form.reset(); status.className = "form-status ok"; status.textContent = "תודה! קיבלנו את הפרטים, ונחזור אליכם בימים א׳–ה׳."; }
          else if (res.j && res.j.error === "phone") { setError(form, "phone", "נא לכתוב מספר טלפון ישראלי, למשל 050-1234567."); form.elements.phone.focus(); return "skip"; }
          else throw new Error("failed");
        })
        .catch(function () { status.className = "form-status err"; status.textContent = "לא הצלחנו לשלוח כרגע. אפשר להתקשר או לשלוח וואטסאפ ל-050-9257065."; })
        .then(function (r) { button.disabled = false; button.textContent = "שליחה"; if (r === "skip") return; status.hidden = false; status.focus(); });
    });
  });
})();
