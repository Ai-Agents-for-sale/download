// Zero Work AI — mini-site behaviour. Two small jobs, no cookies, no tracking.
(function () {
  // 1. The store that matches the visitor's phone goes first.
  try {
    var ua = navigator.userAgent || "";
    var android = /Android/i.test(ua);
    var ios = /iPhone|iPad|iPod/i.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    if (android) {
      document.querySelectorAll(".stores").forEach(function (box) {
        var gp = box.querySelector("[data-store='android']");
        if (gp) box.insertBefore(gp, box.firstChild);
      });
    }
    void ios;
  } catch (e) {}

  // 2. The lead form → site-lead edge function → Monday leads board.
  var ENDPOINT = "https://jjbxsivcjhpuobpohpoz.supabase.co/functions/v1/site-lead";
  // Public anon key — the same one shipped inside the app; not a secret.
  var ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpqYnhzaXZjamhwdW9icG9ocG96Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIxMTYzNTUsImV4cCI6MjA5NzY5MjM1NX0.CRtQPXuDTiG8LhSiBiv8zpFh-Pi6rboN7AiBGppKPfA";
  var started = Date.now();

  function israeliPhone(raw) {
    var d = String(raw || "").replace(/\D/g, "");
    if (d.indexOf("00972") === 0) d = d.slice(5);
    else if (d.indexOf("972") === 0) d = d.slice(3);
    if (d.charAt(0) !== "0") d = "0" + d;
    return /^0(5\d{8}|7\d{8}|[2-4689]\d{7})$/.test(d) ? d : "";
  }

  function setError(form, name, msg) {
    var input = form.querySelector("[name='" + name + "']");
    var err = form.querySelector("#" + form.id + "-" + name + "-error");
    if (!input || !err) return;
    if (msg) {
      input.setAttribute("aria-invalid", "true");
      err.textContent = msg;
      err.hidden = false;
    } else {
      input.removeAttribute("aria-invalid");
      err.textContent = "";
      err.hidden = true;
    }
  }

  document.querySelectorAll("form.lead-form").forEach(function (form) {
    var status = form.querySelector(".form-status");
    var button = form.querySelector("button[type='submit']");

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var name = form.elements.name.value.trim();
      var phoneRaw = form.elements.phone.value.trim();
      var phone = israeliPhone(phoneRaw);
      var bad = null;

      setError(form, "name", name.length < 2 ? "נא לכתוב שם מלא." : "");
      if (name.length < 2) bad = bad || form.elements.name;
      setError(form, "phone", !phone ? "נא לכתוב מספר טלפון ישראלי, למשל 050-1234567." : "");
      if (!phone) bad = bad || form.elements.phone;
      if (bad) { bad.focus(); return; }

      status.hidden = true;
      button.disabled = true;
      button.textContent = "שולחים…";

      var payload = {
        name: name,
        phone: phone,
        business: form.elements.business.value.trim(),
        message: form.elements.message.value.trim(),
        marketing_consent: !!form.elements.marketing_consent.checked,
        website: form.elements.website.value,
        elapsed_ms: Date.now() - started,
        page: location.pathname
      };

      fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", "apikey": ANON, "Authorization": "Bearer " + ANON },
        body: JSON.stringify(payload)
      })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok && j.ok, j: j }; }); })
        .then(function (res) {
          if (res.ok) {
            form.reset();
            status.className = "form-status ok";
            status.textContent = "תודה! קיבלנו את הפרטים, ונחזור אליכם בימים א׳–ה׳.";
          } else if (res.j && res.j.error === "phone") {
            setError(form, "phone", "נא לכתוב מספר טלפון ישראלי, למשל 050-1234567.");
            form.elements.phone.focus();
            return;
          } else {
            throw new Error("failed");
          }
        })
        .catch(function () {
          status.className = "form-status err";
          status.textContent = "לא הצלחנו לשלוח כרגע. אפשר להתקשר או לשלוח וואטסאפ ל-050-9257065.";
        })
        .then(function () {
          status.hidden = false;
          button.disabled = false;
          button.textContent = "שליחה";
          status.focus();
        });
    });
  });
})();
