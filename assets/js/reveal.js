/* Scroll reveal, shared by the static markup in index.html and by the cards
   the catalogue renders later. Exposed on window so both can use it without
   either depending on the other's load order. */
(function () {
  "use strict";

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let observer = null;

  if ("IntersectionObserver" in window && !reduced) {
    observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.style.transitionDelay = (entry.target.dataset.d || 0) + "ms";
        entry.target.classList.add("in");
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.14, rootMargin: "0px 0px -7% 0px" });
  }

  /* Nodes are revealed in reading order, four at a time, so a row of cards
     fades up as a wave instead of all at once. */
  function watch(nodes, offset) {
    const list = Array.from(nodes);
    if (!observer) {
      list.forEach((el) => el.classList.add("in"));
      return;
    }
    list.forEach((el, i) => {
      el.dataset.d = ((offset || 0) + i) % 4 * 100;
      observer.observe(el);
    });
  }

  window.reveal = { watch: watch, reduced: reduced };
})();
