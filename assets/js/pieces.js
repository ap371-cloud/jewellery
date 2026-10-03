/* The catalogue. This is the only place a product exists: the grid, the
   category chips, the search index, the detail dialog and the ItemList
   structured data are all generated from it. See README.md before editing.

   Plain object literals rather than a module, because ES modules are blocked
   over file:// and the site is meant to open by double-clicking index.html. */

window.JEWELLERY = {
  categories: [
    { id: "ring", label: "Rings" },
    { id: "earrings", label: "Earrings" },
    { id: "necklace", label: "Necklaces" },
    { id: "bangle", label: "Bangles" },
    { id: "bridal", label: "Bridal" },
    { id: "coin", label: "Coins" }
  ],

  // Single source of truth for the catalogue. Prices are whole rupees and
  // include GST, matching the footer note. `added` drives the newest-first sort.
  pieces: [
    {
      id: "solitaire", name: "Signature Solitaire", cat: "ring", added: 2026, flag: "new",
      metal: "18k Yellow Gold", detail: "1.24 ct", price: 148000, img: "assets/product-solitaire.jpg",
      blurb: "The one we are asked for most. A single round brilliant in six prongs, on a band thin enough to forget you are wearing it.",
      specs: [["Centre stone", "1.24 ct round brilliant, VS2 / F"],
              ["Certification", "GIA, IGI on request"],
              ["Metal", "18k yellow gold, 4.1 g"],
              ["Setting", "Six-prong, set by hand"],
              ["Sizing", "Free once within a year"]]
    },
    {
      id: "band", name: "Eternity Band", cat: "ring", added: 2026, flag: "new",
      metal: "Platinum 950", detail: "1.8 ct", price: 214000, img: "assets/product-band.jpg",
      blurb: "Sixteen stones set all the way round in platinum, so it reads the same whichever way your hand falls.",
      specs: [["Total weight", "1.8 ct across sixteen round stones"],
              ["Metal", "Platinum 950, 5.2 g"],
              ["Certification", "IGI on request"],
              ["Setting", "Shared bead, hand-finished"],
              ["Sizing", "Free within a year"]]
    },
    {
      id: "halo", name: "Ziya Halo", cat: "ring", added: 2025, flag: null,
      metal: "18k Rose Gold", detail: "0.62 ct", price: 78000, img: "assets/product-halo.jpg",
      blurb: "A whisper of rose gold with a thin circle of stones that widens the finger rather than covering it.",
      specs: [["Total weight", "0.62 ct across 24 stones"],
              ["Metal", "18k rose gold, 2.4 g"],
              ["Certification", "IGI on request"],
              ["Profile", "2.1 mm at the shoulder"]]
    },
    {
      id: "emerald", name: "Meera Emerald", cat: "ring", added: 2025, flag: null,
      metal: "18k Yellow Gold", detail: "1.05 ct emerald", price: 186000, img: "assets/product-emerald.jpg",
      blurb: "A single step-cut emerald flanked by two brilliants. The colour is checked in daylight before it is ever set.",
      specs: [["Centre stone", "1.05 ct step-cut emerald"],
              ["Side stones", "0.18 ct, two round brilliants"],
              ["Metal", "18k yellow gold, 5.6 g"],
              ["Certification", "GRS or IGI"],
              ["Setting", "Six-prong with a gallery rail"]]
    },
    {
      id: "hoops", name: "Ziya Hoops", cat: "earrings", added: 2024, flag: null,
      metal: "18k Yellow Gold", detail: "22 mm", price: 62500, img: "assets/product-hoops.jpg",
      blurb: "The everyday hoop, made thick enough to keep its shape and light enough to sleep in.",
      specs: [["Diameter", "22 mm on a 3.2 mm tube"],
              ["Metal", "18k yellow gold, 5.6 g pair"],
              ["Closure", "Hinged click with a safety catch"],
              ["Finish", "High polish, hand-burnished"]]
    },
    {
      id: "drops", name: "Noor Drops", cat: "earrings", added: 2025, flag: null,
      metal: "18k Rose Gold", detail: "1.42 ct", price: 78900, img: "assets/product-drops.jpg",
      blurb: "Two stones, one at the ear and one at the jaw. Light enough that you forget them by lunch.",
      specs: [["Total weight", "1.42 ct"],
              ["Metal", "18k rose gold, 6.1 g pair"],
              ["Certification", "GIA on request"],
              ["Drop length", "34 mm"],
              ["Closure", "Post and butterfly"]]
    },
    {
      id: "jhumka", name: "Chandni Jhumka", cat: "earrings", added: 2025, flag: null,
      metal: "22k Yellow Gold", detail: "9.4 g", price: 112000, img: "assets/product-jhumka.jpg",
      blurb: "A domed jhumka with a pearl drop, modelled on the pair our founder's mother wore to her own wedding.",
      specs: [["Metal", "22k yellow gold, 9.4 g pair"],
              ["Pearl", "Natural, 7 mm"],
              ["Fringe", "Four hand-linked chains"],
              ["Closure", "Post and butterfly"]]
    },
    {
      id: "studs", name: "Neelam Studs", cat: "earrings", added: 2024, flag: null,
      metal: "Platinum 950", detail: "1.1 ct sapphire", price: 135000, img: "assets/product-studs.jpg",
      blurb: "Two unheated sapphires on plain platinum posts. Nothing to hide behind.",
      specs: [["Stones", "Two cabochon sapphires, 1.1 ct total"],
              ["Metal", "Platinum 950, 3.2 g pair"],
              ["Certification", "IGI on request"],
              ["Fitting", "Screw posts with silicone-backed butterflies"]]
    },
    {
      id: "sitara", name: "Sitara Necklace", cat: "necklace", added: 2024, flag: null,
      metal: "18k Rose Gold", detail: "0.81 ct", price: 96400, img: "assets/product-necklace.jpg",
      blurb: "A single stone on a fine rose gold chain, sized to sit just below the collarbone.",
      specs: [["Total weight", "0.81 ct across five stones"],
              ["Metal", "18k rose gold, 7.8 g"],
              ["Chain", "42 cm with a 5 cm extender"],
              ["Clasp", "Spring ring"],
              ["Certification", "IGI on request"]]
    },
    {
      id: "rani", name: "Rani Haar", cat: "necklace", added: 2024, flag: null,
      metal: "22k Yellow Gold", detail: "22 g", price: 268000, img: "assets/product-rani.jpg",
      blurb: "Twenty-two grams of hand-linked gold that sits on the collarbone and stays there all day.",
      specs: [["Metal", "22k yellow gold, 22 g"],
              ["Length", "46 cm"],
              ["Links", "Hand-linked, 96 repeats"]]
    },
    {
      id: "choker", name: "Zaya Choker", cat: "necklace", added: 2026, flag: "new",
      metal: "18k Yellow Gold", detail: "1.9 ct", price: 142000, img: "assets/product-choker.jpg",
      blurb: "Stones set shoulder to shoulder all the way round. Meant to sit over a sari blouse, not under it.",
      specs: [["Total weight", "1.9 ct across 26 stones"],
              ["Metal", "18k yellow gold, 14.2 g"],
              ["Fitting", "Adjustable, 34 to 40 cm"],
              ["Certification", "GIA on request"]]
    },
    {
      id: "pendant", name: "Tidal Pendant", cat: "necklace", added: 2026, flag: null,
      metal: "18k Yellow Gold", detail: "0.9 ct lab-grown", price: 64000, img: "assets/product-pendant.jpg",
      blurb: "The lab-grown stone, stated plainly on the invoice and on the certificate. Same cut, a third of the price.",
      specs: [["Stone", "0.9 ct round, lab-grown, IGI certified"],
              ["Metal", "18k yellow gold, 1.8 g"],
              ["Chain", "45 cm, 1.1 mm cable"],
              ["Disclosure", "Lab-grown, declared on the invoice"]]
    },
    {
      id: "bangles", name: "Bangla Kada", cat: "bangle", added: 2025, flag: null,
      metal: "22k Yellow Gold", detail: "18 g", price: 235000, img: "assets/product-bangles.jpg",
      blurb: "Four wide textured bangles. They make a sound when you work, which is the point.",
      specs: [["Metal", "22k yellow gold, 18 g total"],
              ["Width", "9 mm each"],
              ["Closure", "Hook and eye"],
              ["Finish", "Rope texture, hand-cut"]]
    },
    {
      id: "bracelet", name: "Aane Tennis Bracelet", cat: "bangle", added: 2026, flag: "new",
      metal: "Platinum 950", detail: "4.2 ct", price: 410000, img: "assets/product-bracelet.jpg",
      blurb: "Twenty-two carats of stones in a single platinum line, with a clasp you cannot see from the front.",
      specs: [["Total weight", "4.2 ct across 44 stones"],
              ["Metal", "Platinum 950, 19.4 g"],
              ["Length", "17 cm with a 2 cm extender"],
              ["Certification", "IGI on request"],
              ["Clasp", "Hidden box, double safety"]]
    },
    {
      id: "sehra", name: "Sehra Bridal Set", cat: "bridal", added: 2026, flag: "new",
      metal: "22k Yellow Gold", detail: "32 g · 2.4 ct", price: 345000, was: 380000, img: "assets/product-bridal.jpg",
      blurb: "A maang tikka, a choker and a haar that weigh in at just under a tola. Assembled for you in ten working days.",
      specs: [["Metal", "22k yellow gold, 32 g"],
              ["Stones", "2.4 ct across 14 pieces"],
              ["Includes", "Maang tikka, choker, haar, earrings"],
              ["Hallmark", "BIS, Madhya Pradesh bureau"],
              ["Lead time", "Ten working days"]]
    },
    {
      id: "lehenga", name: "Dulhan Lehenga Set", cat: "bridal", added: 2025, flag: null,
      metal: "22k Yellow Gold", detail: "52 g", price: 590000, img: "assets/product-lehenga.jpg",
      blurb: "The full set, weighted to a lehenga rather than to a number on a page.",
      specs: [["Metal", "22k yellow gold, 52 g"],
              ["Includes", "Choker, haar, jhumka pair, tikka, bangles, ring"],
              ["Hallmark", "BIS, Madhya Pradesh bureau"],
              ["Lead time", "Four to five weeks"]]
    },
    {
      id: "coin", name: "Lakshmi Coin, 10 g", cat: "coin", added: 2025, flag: null,
      metal: "22K 999", detail: "10 g", price: 108500, img: "assets/product-coin.jpg",
      blurb: "Minted by a refinery on the bullion exchange. Comes in a sealed assay card, and we hand over the bill.",
      specs: [["Purity", "22K 999"],
              ["Weight", "10 g"],
              ["Minted by", "MMTC Ispat Limited"],
              ["Packing", "Sealed assay card"],
              ["Hallmark", "BIS registered"]]
    },
    {
      id: "silvercoin", name: "Silver Bullion, 100 g", cat: "coin", added: 2024, flag: null,
      metal: "Silver 999", detail: "100 g", price: 13400, img: "assets/product-silvercoin.jpg",
      blurb: "A plain 100 g bar for the people who buy silver and never wear it on their wrist.",
      specs: [["Purity", "999 fine"],
        ["Weight", "100 g"],
        ["Packing", "Heat-sealed with assay certificate"],
        ["Hallmark", "BIS registered"]]
    }
  ]
};
