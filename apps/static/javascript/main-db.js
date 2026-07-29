function slideToggle(t, e, o) {
  0 === t.clientHeight ? j(t, e, o, !0) : j(t, e, o);
}
function slideUp(t, e, o) {
  j(t, e, o);
}
function slideDown(t, e, o) {
  j(t, e, o, !0);
}
function j(t, e, o, i) {
  void 0 === e && (e = 400), void 0 === i && (i = !1), (t.style.overflow = "hidden"), i && (t.style.display = "block");
  var p,
    l = window.getComputedStyle(t),
    n = parseFloat(l.getPropertyValue("height")),
    a = parseFloat(l.getPropertyValue("padding-top")),
    s = parseFloat(l.getPropertyValue("padding-bottom")),
    r = parseFloat(l.getPropertyValue("margin-top")),
    d = parseFloat(l.getPropertyValue("margin-bottom")),
    g = n / e,
    y = a / e,
    m = s / e,
    u = r / e,
    h = d / e;
  window.requestAnimationFrame(function l(x) {
    void 0 === p && (p = x);
    var f = x - p;
    i
      ? ((t.style.height = g * f + "px"),
        (t.style.paddingTop = y * f + "px"),
        (t.style.paddingBottom = m * f + "px"),
        (t.style.marginTop = u * f + "px"),
        (t.style.marginBottom = h * f + "px"))
      : ((t.style.height = n - g * f + "px"),
        (t.style.paddingTop = a - y * f + "px"),
        (t.style.paddingBottom = s - m * f + "px"),
        (t.style.marginTop = r - u * f + "px"),
        (t.style.marginBottom = d - h * f + "px")),
      f >= e
        ? ((t.style.height = ""),
          (t.style.paddingTop = ""),
          (t.style.paddingBottom = ""),
          (t.style.marginTop = ""),
          (t.style.marginBottom = ""),
          (t.style.overflow = ""),
          i || (t.style.display = "none"),
          "function" == typeof o && o())
        : window.requestAnimationFrame(l);
  });
}

let sidebarItems = document.querySelectorAll(".sidebar-item.has-sub");
for (var i = 0; i < sidebarItems.length; i++) {
  let sidebarItem = sidebarItems[i];
  sidebarItems[i].querySelector(".sidebar-link").addEventListener("click", function (e) {
    e.preventDefault();

    let submenu = sidebarItem.querySelector(".submenu");
    if (submenu.classList.contains("active")) submenu.style.display = "block";

    if (submenu.style.display == "none") submenu.classList.add("active");
    else submenu.classList.remove("active");
    slideToggle(submenu, 300);
  });
}

// **************************************************************
// MAIN DASHBOARD INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", initMainDashboard);

async function initMainDashboard() {
  setupResponsiveSidebar();

  setupSidebarButtons();

  setupPerfectScrollbar();

  scrollToActiveSidebar();

  await loadWorkshopStatusBanner();
}
// **************************************************************
// MAIN DASHBOARD INITIALIZATION | END
// **************************************************************

// **************************************************************
// RESPONSIVE SIDEBAR | START
// **************************************************************
function setupResponsiveSidebar() {
  const sidebar = document.getElementById("sidebar");

  if (!sidebar) {
    return;
  }

  function updateSidebar() {
    if (window.innerWidth < 1200) {
      sidebar.classList.remove("active");
    } else {
      sidebar.classList.add("active");
    }
  }

  updateSidebar();

  window.addEventListener("resize", updateSidebar);
}
// **************************************************************
// RESPONSIVE SIDEBAR | END
// **************************************************************

// **************************************************************
// SIDEBAR BUTTONS | START
// **************************************************************
function setupSidebarButtons() {
  const sidebar = document.getElementById("sidebar");

  const burgerButton = document.querySelector(".burger-btn");

  const sidebarHideButton = document.querySelector(".sidebar-hide");

  if (!sidebar) {
    return;
  }

  burgerButton?.addEventListener("click", () => {
    sidebar.classList.toggle("active");
  });

  sidebarHideButton?.addEventListener("click", () => {
    sidebar.classList.toggle("active");
  });
}
// **************************************************************
// SIDEBAR BUTTONS | END
// **************************************************************

// **************************************************************
// PERFECT SCROLLBAR | START
// **************************************************************
function setupPerfectScrollbar() {
  const container = document.querySelector(".sidebar-wrapper");

  if (typeof PerfectScrollbar !== "function" || !container) {
    return;
  }

  new PerfectScrollbar(container, {
    wheelPropagation: false,
  });
}
// **************************************************************
// PERFECT SCROLLBAR | END
// **************************************************************

// **************************************************************
// ACTIVE SIDEBAR SCROLL | START
// **************************************************************
function scrollToActiveSidebar() {
  const targetElement = document.querySelector(".sidebar-item.active");

  if (!targetElement) {
    return;
  }

  targetElement.scrollIntoView({
    behavior: "smooth",
    block: "nearest",
  });
}
// **************************************************************
// ACTIVE SIDEBAR SCROLL | END
// **************************************************************

// **************************************************************
// LOAD WORKSHOP STATUS | START
// **************************************************************
async function loadWorkshopStatusBanner() {
  const administratorPage = document.querySelector(".workshop-management-page, .dashboard-administrator-page");

  if (administratorPage) {
    return;
  }

  const statusUrl = document.body.dataset.workshopStatusUrl;

  if (!statusUrl) {
    return;
  }

  try {
    const response = await fetch(statusUrl, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    const result = await response.json();

    if (!response.ok || result.status_code !== 200 || !result.data) {
      return;
    }

    renderWorkshopStatusBanner(result.data);
  } catch (error) {
    console.error("WORKSHOP STATUS ERROR:", error);
  }
}
// **************************************************************
// LOAD WORKSHOP STATUS | END
// **************************************************************

// **************************************************************
// RENDER WORKSHOP STATUS | START
// **************************************************************
function renderWorkshopStatusBanner(workshop) {
  const oldBanner = document.getElementById("workshop_status_banner");

  if (oldBanner) {
    oldBanner.remove();
  }

  const operationalStatus = String(workshop.operational_status || "").toLowerCase();

  // Tidak perlu menampilkan banner
  // jika bengkel dan langganan aktif
  if (operationalStatus === "active" || operationalStatus === "") {
    return;
  }

  const statusConfig = {
    inactive: {
      alertClass: "alert-secondary",
      icon: "bi-slash-circle",
      title: "Bengkel Tidak Aktif",
      message: "Bengkel sedang dinonaktifkan oleh administrator.",
    },

    unsubscribed: {
      alertClass: "alert-warning",
      icon: "bi-exclamation-triangle",
      title: "Belum Berlangganan",
      message: "Fitur tambah, ubah, hapus, dan transaksi sedang dibatasi.",
    },

    expired: {
      alertClass: "alert-danger",
      icon: "bi-calendar-x",
      title: "Langganan Kedaluwarsa",
      message: "Perpanjang langganan agar fitur transaksi dapat digunakan kembali.",
    },
  };

  const config = statusConfig[operationalStatus];

  if (!config) {
    return;
  }

  const banner = document.createElement("div");

  banner.id = "workshop_status_banner";

  banner.className = `
    alert
    ${config.alertClass}
    border-0
    shadow-sm
    d-flex
    align-items-center
    gap-3
    mb-4
  `;

  banner.innerHTML = `
    <i class="bi ${config.icon} fs-3"></i>

    <div>
      <div class="fw-bold">
        ${config.title}
      </div>

      <div>
        ${config.message}
      </div>
    </div>
  `;

  const mainElement = document.getElementById("main");

  if (!mainElement) {
    return;
  }

  const pageHeading = mainElement.querySelector(".page-heading");

  if (pageHeading) {
    pageHeading.insertAdjacentElement("beforebegin", banner);

    return;
  }

  mainElement.prepend(banner);
}

// beforebegin → banner sebelum .page-heading
// afterbegin  → banner di dalam, paling awal .page-heading
// beforeend   → banner di dalam, paling akhir .page-heading
// afterend    → banner setelah .page-heading

// **************************************************************
// RENDER WORKSHOP STATUS | END
// **************************************************************
