// Accordion navigation - collapses sibling sections when one is expanded
// Compatible with Material for MkDocs navigation.instant feature
(function () {
  function initAccordion() {
    const nav = document.querySelector(".md-nav--primary");
    if (!nav || nav.dataset.accordionInit) return;
    nav.dataset.accordionInit = "true";

    nav.addEventListener("click", function (e) {
      const toggle = e.target.closest(".md-nav__item--nested > .md-nav__link");
      if (!toggle) return;

      const parent = toggle.closest(".md-nav__item--nested");
      const siblings = parent.parentElement.querySelectorAll(":scope > .md-nav__item--nested");

      siblings.forEach(function (sibling) {
        if (sibling !== parent) {
          const input = sibling.querySelector(":scope > input");
          if (input) input.checked = false;
        }
      });
    });
  }

  // Initialize on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAccordion);
  } else {
    initAccordion();
  }

  // Re-initialize after instant navigation (Material for MkDocs)
  document.addEventListener("DOMContentSwitch", initAccordion);
})();
