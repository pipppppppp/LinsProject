// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  renderAdministratorHeader();

  await loadDashboardSummary();
}

const API = {
  summary: "/dashboard-administrator/summary",
};

const dashboardCard = {
  totalWorkshop: document.getElementById("total_workshop"),

  activeWorkshop: document.getElementById("active_workshop"),

  inactiveWorkshop: document.getElementById("inactive_workshop"),

  totalRevenue: document.getElementById("total_revenue"),
};

const administratorHeader = {
  greeting: document.getElementById("administrator_greeting"),

  date: document.getElementById("administrator_date"),
};
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// GET DASHBOARD SUMMARY | START
// **************************************************************
async function loadDashboardSummary() {
  try {
    const response = await fetch(`${API.summary}?_=${Date.now()}`, {
      method: "GET",
      cache: "no-store",
      headers: {
        Accept: "application/json",
      },
    });

    const result = await response.json();

    if (!response.ok || result.status_code !== 200) {
      return swalError(result.message ?? "Gagal memuat dashboard administrator.");
    }

    renderDashboardSummary(result.data);
  } catch (error) {
    console.error("DASHBOARD ADMINISTRATOR ERROR:", error);

    swalError("Gagal memuat dashboard administrator.");
  }
}
// **************************************************************
// GET DASHBOARD SUMMARY | END
// **************************************************************

// **************************************************************
// RENDER DASHBOARD SUMMARY | START
// **************************************************************
function renderDashboardSummary(data) {
  if (!data) {
    return;
  }

  if (dashboardCard.totalWorkshop) {
    dashboardCard.totalWorkshop.textContent = data.total_workshop ?? 0;
  }

  if (dashboardCard.activeWorkshop) {
    dashboardCard.activeWorkshop.textContent = data.active_workshop ?? 0;
  }

  if (dashboardCard.inactiveWorkshop) {
    dashboardCard.inactiveWorkshop.textContent = data.inactive_workshop ?? 0;
  }

  if (dashboardCard.totalRevenue) {
    dashboardCard.totalRevenue.textContent = formatDashboardCurrency(data.total_revenue);
  }
}
// **************************************************************
// RENDER DASHBOARD SUMMARY | END
// **************************************************************

// **************************************************************
// FORMAT CURRENCY | START
// **************************************************************
function formatDashboardCurrency(amount) {
  return `Rp ${Number(amount || 0).toLocaleString("id-ID")}`;
}
// **************************************************************
// FORMAT CURRENCY | END
// **************************************************************

// **************************************************************
// ADMINISTRATOR HEADER | START
// **************************************************************
function renderAdministratorHeader() {
  const currentDate = new Date();

  if (administratorHeader.greeting) {
    administratorHeader.greeting.textContent = generateGreeting(currentDate.getHours());
  }

  if (administratorHeader.date) {
    administratorHeader.date.textContent = currentDate.toLocaleDateString("id-ID", {
      weekday: "long",
      day: "2-digit",
      month: "long",
      year: "numeric",
    });
  }
}
// **************************************************************
// ADMINISTRATOR HEADER | END
// **************************************************************

// **************************************************************
// GREETING | START
// **************************************************************
function generateGreeting(hour) {
  if (hour >= 4 && hour < 11) {
    return "Selamat Pagi, Administrator!";
  }

  if (hour >= 11 && hour < 15) {
    return "Selamat Siang, Administrator!";
  }

  if (hour >= 15 && hour < 18) {
    return "Selamat Sore, Administrator!";
  }

  return "Selamat Malam, Administrator!";
}
// **************************************************************
// GREETING | END
// **************************************************************
