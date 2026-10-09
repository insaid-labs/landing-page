(() => {
  "use strict";
  const en = document.documentElement.lang === "en";
  const select = (query, root = document) => root.querySelector(query);
  const all = (query, root = document) => [...root.querySelectorAll(query)];
  const menuButton = select(".menu-toggle");
  const mobileNav = select("#mobile-nav");
  const closeMenu = () => {
    if (!menuButton || !mobileNav) return;
    mobileNav.hidden = true;
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", en ? "Open menu" : "Abrir menú");
  };
  menuButton?.addEventListener("click", () => {
    const opening = menuButton.getAttribute("aria-expanded") !== "true";
    mobileNav.hidden = !opening;
    menuButton.setAttribute("aria-expanded", String(opening));
    menuButton.setAttribute("aria-label", opening ? (en ? "Close menu" : "Cerrar menú") : (en ? "Open menu" : "Abrir menú"));
  });
  all("#mobile-nav a").forEach(link => link.addEventListener("click", closeMenu));
  document.addEventListener("click", event => {
    if (!event.target.closest(".header-inner")) closeMenu();
    all(".language-switch[open]").forEach(switcher => {
      if (!switcher.contains(event.target)) switcher.removeAttribute("open");
    });
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") {
      if (menuButton?.getAttribute("aria-expanded") === "true") {
        closeMenu();
        menuButton.focus();
      }
      all(".language-switch[open]").forEach(switcher => {
        switcher.removeAttribute("open");
        select("summary", switcher)?.focus();
      });
    }
  });
  window.matchMedia("(min-width: 701px)").addEventListener("change", event => {
    if (event.matches) closeMenu();
  });

  select(".back-top")?.addEventListener("click", event => {
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" });
  });

  const dialogs = all("dialog");
  let returnFocus = null;
  const openDialog = (dialog, trigger) => {
    if (!dialog || typeof dialog.showModal !== "function") {
      window.location.hash = "contacto";
      return;
    }
    const previous = dialogs.find(item => item.open);
    const originalTrigger = previous ? returnFocus : trigger;
    dialogs.forEach(item => { if (item.open) item.close(); });
    returnFocus = originalTrigger;
    closeMenu();
    dialog.showModal();
    dialog.scrollTop = 0;
    document.body.classList.add("modal-open");
  };
  all("[data-contact], [data-service]").forEach(trigger => {
    trigger.addEventListener("click", event => {
      event.preventDefault();
      const context = select("#service-context");
      const service = trigger.dataset.service;
      if (context) {
        context.hidden = !service;
        context.textContent = service ? `${en ? "Let’s talk about" : "Conversemos sobre"}: ${service}` : "";
      }
      openDialog(select("#contact-modal"), trigger);
    });
  });
  all("[data-project]").forEach(trigger => {
    trigger.addEventListener("click", () => openDialog(select(`#project-${trigger.dataset.project}`), trigger));
  });
  dialogs.forEach(dialog => {
    all("[data-close]", dialog).forEach(button => button.addEventListener("click", () => dialog.close()));
    dialog.addEventListener("click", event => {
      if (event.target !== dialog) return;
      const bounds = dialog.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
    });
    dialog.addEventListener("close", () => {
      if (!dialogs.some(item => item.open)) {
        document.body.classList.remove("modal-open");
        if (returnFocus?.isConnected) returnFocus.focus({ preventScroll: true });
      }
    });
  });

  const filters = all("[data-filter]");
  const projects = all(".project-card");
  filters.forEach(button => {
    button.addEventListener("click", () => {
      filters.forEach(filter => filter.setAttribute("aria-pressed", String(filter === button)));
      let visible = 0;
      projects.forEach(project => {
        const matches = button.dataset.filter === "all" || project.dataset.category === button.dataset.filter;
        project.hidden = !matches;
        if (matches) visible++;
      });
      const status = select("#filter-status");
      if (status) status.textContent = en ? `${visible} projects shown` : `${visible} proyectos visibles`;
    });
  });

  // Deep links must reveal their case study even when another filter is active.
  all("a[href^=\"#case-\"]").forEach(link => {
    link.addEventListener("click", () => {
      const target = document.getElementById(link.getAttribute("href").slice(1));
      if (target?.hidden) filters.find(button => button.dataset.filter === "all")?.click();
    });
  });

  // Distinct service scopes stay usable without JavaScript through native details.
  all(".service-detail").forEach(item => {
    item.addEventListener("toggle", () => {
      if (item.open) all(".service-detail").forEach(other => {
        if (other !== item) other.open = false;
      });
    });
  });

  // Remote photo references are optional. Offline, show a deliberate monogram,
  // never a broken image or a misleading generated likeness.
  all("[data-stock-photo]").forEach(image => {
    const showFallback = () => {
      image.closest(".photo-reference")?.classList.add("photo-unavailable");
    };
    const showPhoto = () => {
      image.closest(".photo-reference")?.classList.remove("photo-unavailable");
    };
    image.addEventListener("error", showFallback);
    image.addEventListener("load", showPhoto);
    if (image.complete && image.naturalWidth === 0) showFallback();
  });

  // External photography and brand favicon have intentional local fallbacks.
  // Use the direct image CDN, not a download endpoint. Failure stays explicit.
  all("[data-hero-photo]").forEach(image => {
    const frame = image.closest(".photo-hero");
    const fail = () => frame?.classList.add("hero-photo-unavailable");
    const ready = () => frame?.classList.remove("hero-photo-unavailable");
    image.addEventListener("error", fail);
    image.addEventListener("load", ready);
    if (image.complete && image.naturalWidth === 0) fail();
  });
  all("[data-official-brand]").forEach(image => {
    const frame = image.closest("[data-brand-logo]");
    const fail = () => frame?.classList.add("brand-logo-unavailable");
    const ready = () => frame?.classList.remove("brand-logo-unavailable");
    image.addEventListener("error", fail);
    image.addEventListener("load", ready);
    if (image.complete && image.naturalWidth === 0) fail();
  });

  // Canonical technology assets fail to a readable label, never a handmade substitute.
  all("[data-stack-asset]").forEach(image => {
    const label = image.closest("a");
    const fail = () => label?.classList.add("stack-asset-unavailable");
    const ready = () => label?.classList.remove("stack-asset-unavailable");
    image.addEventListener("error", fail);
    image.addEventListener("load", ready);
    if (image.complete && image.naturalWidth === 0) fail();
  });

  // Native details remain usable even without JavaScript.
  all(".faq-item").forEach(item => {
    item.addEventListener("toggle", () => {
      if (item.open) all(".faq-item").forEach(other => { if (other !== item) other.open = false; });
    });
  });

  // Content is visible by default; only enhance when the observer is supported.
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    document.documentElement.classList.add("js-ready");
    const reveals = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          reveals.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px 25px 0px" });
    all(".reveal").forEach(element => reveals.observe(element));
  }
  if ("IntersectionObserver" in window) {
    const sections = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          all(".desktop-nav a").forEach(link => {
            const active = link.hash === `#${entry.target.id}`;
            link.classList.toggle("active", active);
            if (active) link.setAttribute("aria-current", "location");
            else link.removeAttribute("aria-current");
          });
        }
      });
    }, { rootMargin: "-15% 0px -60% 0px" });
    ["servicios", "proyectos", "equipo"].forEach(id => {
      const element = document.getElementById(id);
      if (element) sections.observe(element);
    });
  }
})();
