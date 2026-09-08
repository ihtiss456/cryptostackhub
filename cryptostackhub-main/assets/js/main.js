/* CRYPTOSTACKHUB — front-end interactions */
(function () {
  "use strict";

  /* ---------- mobile nav ---------- */
  const burger = document.querySelector(".burger");
  const nav = document.querySelector(".main-nav");
  const header = document.querySelector(".site-header");
  if (burger && nav) {
    burger.setAttribute("aria-expanded", "false");
    burger.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("open");
      burger.setAttribute("aria-expanded", isOpen);
      burger.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
      if (isOpen && header) header.classList.remove("header-hidden");
    });
    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        nav.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
        burger.setAttribute("aria-label", "Open navigation menu");
      });
    });
  }

  /* ---------- hide header on down, reveal on up ---------- */
  if (header) {
    let lastScrollY = window.scrollY;
    let scrollTicking = false;
    const updateHeaderVisibility = () => {
      const currentScrollY = window.scrollY;
      const delta = currentScrollY - lastScrollY;
      const menuOpen = nav && nav.classList.contains("open");

      if (currentScrollY <= 24 || delta < -4 || menuOpen) {
        header.classList.remove("header-hidden");
      } else if (delta > 4) {
        header.classList.add("header-hidden");
      }

      lastScrollY = currentScrollY;
      scrollTicking = false;
    };
    document.addEventListener("scroll", () => {
      if (!scrollTicking) {
        window.requestAnimationFrame(updateHeaderVisibility);
        scrollTicking = true;
      }
    }, { passive: true });
  }

  /* ---------- current section navigation ---------- */
  const currentPath = window.location.pathname.replace(/\/index\.html$/, "/");
  document.querySelectorAll(".main-nav a:not(.nav-cta)").forEach((link) => {
    const linkPath = new URL(link.href, window.location.origin).pathname;
    if (linkPath !== "/" && currentPath.startsWith(linkPath)) link.classList.add("active");
  });

  /* ---------- reading progress ---------- */
  const bar = document.querySelector(".progress");
  if (bar) {
    const onScroll = () => {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
    };
    document.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------- reveal on scroll ---------- */
  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
    { threshold: 0.12 }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  /* ---------- TOC active highlight ---------- */
  const tocLinks = document.querySelectorAll(".toc-box a");
  if (tocLinks.length) {
    const heads = Array.from(document.querySelectorAll(".prose h2[id]"));
    const spy = () => {
      let current = heads[0];
      heads.forEach((h) => { if (h.getBoundingClientRect().top < 140) current = h; });
      tocLinks.forEach((a) => a.classList.toggle("active", current && a.getAttribute("href") === "#" + current.id));
    };
    document.addEventListener("scroll", spy, { passive: true });
    spy();
  }

  /* ---------- share buttons ---------- */
  document.querySelectorAll("[data-share]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const url = window.location.href;
      const title = document.title;
      const kind = btn.getAttribute("data-share");
      if (kind === "copy") {
        try { await navigator.clipboard.writeText(url); btn.innerHTML = "&#10003;"; setTimeout(() => (btn.innerHTML = "&#128279;"), 1400); } catch (e) {}
      } else if (kind === "x") {
        window.open("https://twitter.com/intent/tweet?text=" + encodeURIComponent(title) + "&url=" + encodeURIComponent(url), "_blank", "width=560,height=440");
      } else if (kind === "native" && navigator.share) {
        navigator.share({ title, url }).catch(() => {});
      }
    });
  });

  /* ---------- newsletter (demo handler) ---------- */
  document.querySelectorAll(".news-form").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const input = form.querySelector("input");
      if (input && input.value.includes("@")) {
        form.innerHTML = '<p style="color:var(--accent);font-weight:600;margin:0">You are on the list. Welcome aboard.</p>';
      } else if (input) { input.focus(); }
    });
  });

  /* ---------- live search ---------- */
  const searchInput = document.querySelector("#search-input");
  if (searchInput) {
    const resultsBox = document.querySelector("#search-results");
    const countBox = document.querySelector("#search-count");
    let index = [];
    fetch("/assets/search-index.json")
      .then((r) => r.json())
      .then((data) => { index = data; run(); })
      .catch(() => { if (countBox) countBox.textContent = "Search index unavailable when opened as a local file — serve the site over HTTP (Replit does this automatically)."; });

    const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

    function run() {
      const q = (searchInput.value || "").trim().toLowerCase();
      const hits = !q ? index.slice(0, 12)
        : index.filter((it) =>
            (it.title + " " + it.description + " " + it.category + " " + (it.keywords || "")).toLowerCase().includes(q)
          );
      if (countBox) countBox.textContent = q ? hits.length + " result" + (hits.length === 1 ? "" : "s") + ' for "' + q + '"' : "Browse all " + index.length + " guides";
      resultsBox.innerHTML = hits.length
        ? hits.map((it) =>
            '<a class="result-item" href="' + it.url + '">' +
            '<span class="chip ' + it.catClass + '">' + esc(it.category) + "</span>" +
            "<h3>" + esc(it.title) + "</h3><p>" + esc(it.description) + "</p></a>"
          ).join("")
        : '<div class="no-result">No matches. Try “staking”, “solidity”, “capital gains” or “NFT”.</div>';
    }
    searchInput.addEventListener("input", run);
    const params = new URLSearchParams(window.location.search);
    if (params.get("q")) { searchInput.value = params.get("q"); }
  }

  /* ---------- contact / write / advertise forms (demo) ---------- */
  document.querySelectorAll("[data-demo-form]").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      form.innerHTML = '<p style="color:var(--accent);font-weight:600">Thank you — your message has been noted. Wire this form to your email service (e.g. Formspree) to receive submissions.</p>';
    });
  });
})();
