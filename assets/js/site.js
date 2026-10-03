/* Page chrome for index.html: sticky header, mobile nav, the cursor light, the
   ticker strip, the testimonial carousel, the FAQ and the enquiry form.
   The catalogue lives in catalogue.js and the scroll reveal in reveal.js. */
(function () {
  "use strict";

  const reduced = window.reveal.reduced;

  /* The header goes opaque once you leave the hero. The back-to-top button
     waits until further down, otherwise it covers the sticky mobile CTA. */
  const HEADER_AT = 40;
  const TOPBTN_AT = 640;

  const header = document.getElementById("hdr");
  const topBtn = document.getElementById("top");

  function onScroll() {
    header.classList.toggle("solid", window.scrollY > HEADER_AT);
    topBtn.classList.toggle("on", window.scrollY > TOPBTN_AT);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  topBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
  });

  const burger = document.getElementById("burger");
  const nav = document.getElementById("nav");

  burger.addEventListener("click", () => {
    burger.classList.toggle("on");
    nav.classList.toggle("open");
  });

  nav.addEventListener("click", (e) => {
    if (e.target.tagName !== "A") return;
    burger.classList.remove("on");
    nav.classList.remove("open");
  });

  window.reveal.watch(document.querySelectorAll(".rv"));

  const glow = document.getElementById("glow");

  if (glow && !reduced) {
    // Lerp toward the pointer instead of pinning to it, so the light drags
    // behind the cursor rather than feeling glued on.
    const EASE = 0.09;
    let targetX = 0, targetY = 0;
    let glowX = 0, glowY = 0;

    window.addEventListener("mousemove", (e) => {
      targetX = e.clientX;
      targetY = e.clientY;
    }, { passive: true });

    (function follow() {
      glowX += (targetX - glowX) * EASE;
      glowY += (targetY - glowY) * EASE;
      glow.style.transform = "translate3d(" + glowX + "px," + glowY + "px,0)";
      requestAnimationFrame(follow);
    })();
  }

  const ticker = document.getElementById("st");
  const phrases = [
    "BIS Hallmarked Gold", "GIA & IGI Certified", "Fair Gold Exchange",
    "No-Cost EMI", "Lifetime Servicing", "Bespoke Commissions", "Made in Indore",
  ];
  // Duplicated once so the -50% translate loops seamlessly.
  ticker.innerHTML = phrases.concat(phrases)
    .map((p) => "<span>" + p + " &#9679;</span>").join("");

  const AUTOPLAY_MS = 5400;
  const track = document.getElementById("cx");
  const dots = document.getElementById("dots");
  const slideCount = track.children.length;
  let current = 0;
  let timer = null;

  for (let n = 0; n < slideCount; n++) {
    const dot = document.createElement("button");
    dot.className = "dot" + (n === 0 ? " on" : "");
    dot.setAttribute("aria-label", "Testimonial " + (n + 1));
    dot.addEventListener("click", () => {
      showSlide(n);
      restartTimer();
    });
    dots.appendChild(dot);
  }

  function showSlide(n) {
    current = (n + slideCount) % slideCount;
    track.style.transform = "translateX(-" + current * 100 + "%)";
    Array.from(dots.children).forEach((dot, k) => {
      dot.classList.toggle("on", k === current);
    });
  }

  function restartTimer() {
    clearInterval(timer);
    timer = setInterval(() => showSlide(current + 1), AUTOPLAY_MS);
  }

  document.getElementById("pv").addEventListener("click", () => {
    showSlide(current - 1);
    restartTimer();
  });
  document.getElementById("nx").addEventListener("click", () => {
    showSlide(current + 1);
    restartTimer();
  });
  if (!reduced) restartTimer();

  document.querySelectorAll(".qa").forEach((qa, i) => {
    const btn = qa.querySelector("button");
    const panel = qa.querySelector(".ans");

    panel.id = "ans" + (i + 1);
    btn.id = "q" + (i + 1);
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-controls", panel.id);

    btn.addEventListener("click", () => {
      const wasOpen = qa.classList.contains("open");

      document.querySelectorAll(".qa.open").forEach((other) => {
        other.classList.remove("open");
        other.querySelector(".ans").style.maxHeight = null;
        other.querySelector("button").setAttribute("aria-expanded", "false");
      });

      if (!wasOpen) {
        qa.classList.add("open");
        panel.style.maxHeight = panel.scrollHeight + "px";
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  const form = document.getElementById("form");
  const status = document.getElementById("msg");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const name = document.getElementById("nm").value.trim();
    const phone = document.getElementById("ph").value.trim();
    const email = document.getElementById("em").value.trim();

    if (!name) {
      status.textContent = "Please tell us your name.";
      return;
    }
    if (!/^[0-9+\-\s()]{8,15}$/.test(phone)) {
      status.textContent = "Please enter a valid phone number.";
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      status.textContent = "Please enter a valid email address.";
      return;
    }

    status.textContent = "Thank you, " + name + ". We will call you within one working day.";
    form.reset();
  });

  /* A missing photograph should not leave a torn image icon in the grid. */
  document.addEventListener("error", (e) => {
    if (e.target.tagName !== "IMG") return;
    const holder = e.target.closest(".art, .m-art");
    if (holder) holder.classList.add("noimg");
  }, true);
})();
