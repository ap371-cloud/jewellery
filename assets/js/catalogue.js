/* The collection section: category chips, search, sort, paging, the detail
   dialog, and the matching ItemList structured data. Reads the products from
   window.JEWELLERY, which pieces.js defines. */
(function () {
  "use strict";

  const PIECES = window.JEWELLERY.pieces;
  const CATEGORIES = window.JEWELLERY.categories;

  const LABEL = {};
  CATEGORIES.forEach((c) => { LABEL[c.id] = c.label; });

  const BY_ID = {};
  PIECES.forEach((p) => { BY_ID[p.id] = p; });

  const PAGE = 6;

  const grid = document.getElementById("grid");
  const chipRow = document.getElementById("chips");
  const tally = document.getElementById("tally");
  const emptyNote = document.getElementById("empty");
  const moreWrap = document.getElementById("moreWrap");
  const moreBtn = document.getElementById("more");
  const resetBtn = document.getElementById("reset");
  const searchBox = document.getElementById("q");
  const sortBox = document.getElementById("sort");

  const modal = document.getElementById("modal");
  const sheet = modal.querySelector(".sheet");
  const closeBtn = document.getElementById("mClose");
  const art = document.getElementById("mArt");
  const img = document.getElementById("mImg");
  const catOut = document.getElementById("mCat");
  const nameOut = document.getElementById("mName");
  const priceOut = document.getElementById("mPrice");
  const blurbOut = document.getElementById("mBlurb");
  const specsOut = document.getElementById("mSpecs");
  const waOut = document.getElementById("mWa");
  const enquireBtn = document.getElementById("mEnquire");
  const enquiryBox = document.getElementById("ms");
  const booking = document.getElementById("book");

  const rupees = new Intl.NumberFormat("en-IN", {
    style: "currency", currency: "INR", maximumFractionDigits: 0
  });

  let activeCat = "all";
  let limit = PAGE;
  let openPiece = null;
  let lastFocus = null;

  const SORTS = {
    plow: (a, b) => a.price - b.price,
    phigh: (a, b) => b.price - a.price,
    new: (a, b) => b.added - a.added,
    name: (a, b) => a.name.localeCompare(b.name)
  };

  function money(amount) {
    return rupees.format(amount).replace("₹", "&#8377; ");
  }

  function priceTag(piece) {
    if (!piece.was) return money(piece.price);
    const off = Math.round((1 - piece.price / piece.was) * 100);
    return money(piece.price) +
      ' <span class="strike">' + money(piece.was) + "</span>" +
      '<span class="off">' + off + "% off</span>";
  }

  function cardHTML(piece) {
    const flag = piece.flag ? '<span class="tag-new">' + piece.flag + "</span>" : "";
    return '<article class="card rv">' + flag +
      '<button class="art" data-open="' + piece.id +
      '" aria-label="View details for ' + piece.name + '">' +
      '<img src="' + piece.img + '" alt="' + piece.name + " in " + piece.metal +
      '" loading="lazy" /></button>' +
      '<div class="info"><h3>' + piece.name + "</h3>" +
      '<p class="meta">' + piece.metal + " &middot; " + piece.detail + "</p>" +
      '<p class="price">' + priceTag(piece) + "</p>" +
      '<div class="acts">' +
      '<button class="lk" data-open="' + piece.id + '">Details</button>' +
      '<button class="lk" data-enquire="' + piece.id + '">Enquire</button>' +
      "</div></div></article>";
  }

  function matches(piece) {
    if (activeCat !== "all" && piece.cat !== activeCat) return false;
    const q = searchBox.value.trim().toLowerCase();
    if (!q) return true;
    return [piece.name, piece.metal, piece.detail, LABEL[piece.cat], piece.blurb]
      .join(" ").toLowerCase().includes(q);
  }

  function render() {
    const found = PIECES.filter(matches);
    const order = SORTS[sortBox.value];
    if (order) found.sort(order);

    const shown = found.slice(0, limit);
    grid.innerHTML = shown.map(cardHTML).join("");
    window.reveal.watch(grid.children);

    tally.textContent = found.length === PIECES.length
      ? "All " + found.length + " pieces"
      : "Showing " + Math.min(limit, found.length) + " of " + found.length +
        (found.length === 1 ? " piece" : " pieces");

    emptyNote.hidden = found.length !== 0;
    moreWrap.hidden = found.length <= limit;
  }

  function resetPaging() {
    limit = PAGE;
  }

  function markChip(chip) {
    Array.from(chipRow.children).forEach((c) => {
      const on = c === chip;
      c.classList.toggle("on", on);
      c.setAttribute("aria-pressed", on);
    });
  }

  function whatsappFor(piece) {
    return "https://wa.me/917314001200?text=" + encodeURIComponent(
      "Hi Jewellery, I'd like to know more about the " + piece.name +
      " (" + rupees.format(piece.price) + ")."
    );
  }

  function openDetails(id) {
    const piece = BY_ID[id];
    if (!piece) return;
    openPiece = piece;

    catOut.textContent = LABEL[piece.cat];
    nameOut.textContent = piece.name;
    priceOut.innerHTML = priceTag(piece);
    blurbOut.textContent = piece.blurb;
    specsOut.innerHTML = piece.specs
      .map((row) => "<div><dt>" + row[0] + "</dt><dd>" + row[1] + "</dd></div>").join("");
    art.classList.remove("noimg");
    img.alt = piece.name + " in " + piece.metal;
    img.src = piece.img;
    waOut.href = whatsappFor(piece);

    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.style.overflow = "hidden";
    closeBtn.focus();
  }

  function closeDetails() {
    modal.hidden = true;
    document.body.style.overflow = "";
    openPiece = null;
    if (lastFocus) lastFocus.focus();
  }

  /* An enquiry is a phone call, so the piece name goes into the message box
     before the visitor scrolls down to it. */
  function enquire(piece) {
    enquiryBox.value = "I would like to see the " + piece.name +
      " (" + rupees.format(piece.price) + ").";
    closeDetails();
    booking.scrollIntoView({ behavior: window.reveal.reduced ? "auto" : "smooth" });
    enquiryBox.focus({ preventScroll: true });
  }

  function buildChips() {
    [{ id: "all", label: "All" }].concat(CATEGORIES).forEach((cat) => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "chip" + (cat.id === activeCat ? " on" : "");
      chip.dataset.f = cat.id;
      chip.setAttribute("aria-pressed", cat.id === activeCat);
      chip.textContent = cat.label;
      chipRow.appendChild(chip);
    });
  }

  /* Emitted from the same array the grid renders, so the two cannot drift. */
  function publishStructuredData() {
    const pageUrl = location.href.split("#")[0];
    const data = {
      "@context": "https://schema.org",
      "@type": "ItemList",
      name: "Jewellery collection",
      numberOfItems: PIECES.length,
      itemListElement: PIECES.map((piece, i) => ({
        "@type": "ListItem",
        position: i + 1,
        item: {
          "@type": "Product",
          name: piece.name,
          sku: "JWL-" + piece.id,
          description: piece.blurb,
          image: new URL(piece.img, pageUrl).href,
          category: LABEL[piece.cat],
          material: piece.metal,
          offers: {
            "@type": "Offer",
            price: piece.price,
            priceCurrency: "INR",
            availability: "https://schema.org/InStock",
            url: pageUrl + "#collection"
          }
        }
      }))
    };
    document.getElementById("catalogueLd").textContent = JSON.stringify(data);
  }

  chipRow.addEventListener("click", (e) => {
    const chip = e.target.closest(".chip");
    if (!chip) return;
    activeCat = chip.dataset.f;
    markChip(chip);
    resetPaging();
    render();
  });

  searchBox.addEventListener("input", () => { resetPaging(); render(); });
  sortBox.addEventListener("change", render);

  moreBtn.addEventListener("click", () => {
    limit += PAGE;
    render();
  });

  resetBtn.addEventListener("click", () => {
    activeCat = "all";
    searchBox.value = "";
    markChip(chipRow.firstElementChild);
    resetPaging();
    render();
  });

  grid.addEventListener("click", (e) => {
    const ask = e.target.closest("[data-enquire]");
    if (ask) { enquire(BY_ID[ask.dataset.enquire]); return; }
    const view = e.target.closest("[data-open]");
    if (view) openDetails(view.dataset.open);
  });

  enquireBtn.addEventListener("click", () => {
    if (openPiece) enquire(openPiece);
  });

  closeBtn.addEventListener("click", closeDetails);
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeDetails();
  });

  /* Keeps Tab inside the dialog while it is open. */
  sheet.addEventListener("keydown", (e) => {
    if (e.key !== "Tab") return;
    const stops = sheet.querySelectorAll("button, a[href]");
    const first = stops[0];
    const last = stops[stops.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !modal.hidden) closeDetails();
  });

  buildChips();
  render();
  publishStructuredData();
})();
