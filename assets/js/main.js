// Header shadow on scroll, mobile menu, dropdown dismissal and TOC highlighting.
(function () {
  var header = document.querySelector("[data-header]");
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");
  var dropdowns = document.querySelectorAll("[data-dropdown]");

  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  function setMenu(open) {
    toggle.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("is-open", open);
    document.body.style.overflow = open ? "hidden" : "";
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    window.matchMedia("(min-width: 961px)").addEventListener("change", function (e) {
      if (e.matches) setMenu(false);
    });
  }

  // Only one dropdown open at a time; close on outside click or Escape.
  dropdowns.forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (!d.open) return;
      dropdowns.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });
  document.addEventListener("click", function (e) {
    dropdowns.forEach(function (d) { if (!d.contains(e.target)) d.open = false; });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    dropdowns.forEach(function (d) { d.open = false; });
    if (toggle && toggle.getAttribute("aria-expanded") === "true") { setMenu(false); toggle.focus(); }
  });

  // Highlight the current section in an on-page table of contents.
  var tocLinks = document.querySelectorAll(".toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    tocLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        tocLinks.forEach(function (a) { a.classList.remove("is-active"); });
        var a = byId[en.target.id];
        if (a) a.classList.add("is-active");
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }
})();
