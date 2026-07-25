// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  updateDateTime();
  setInterval(updateDateTime, 1000);
  await loadDashboard();
}
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// LOAD DASHBOARD | START
// **************************************************************
async function loadDashboard() {
  await loadSummary();

  await loadSalesChart();

  await loadTopProducts();

  await loadTopServices();

  await loadRecentTransactions();

  await loadLowStock();

  await loadDepositSummary();

  await loadCashierProfile();
}
// **************************************************************
// LOAD DASHBOARD | END
// **************************************************************

// **************************************************************
// DATE TIME | START
// **************************************************************
function updateDateTime() {
  const now = new Date();

  document.getElementById("current_date").textContent = now.toLocaleDateString("id-ID", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  document.getElementById("current_time").textContent = now.toLocaleTimeString("id-ID", {
    hour: "2-digit",
    minute: "2-digit",
  });
}
// **************************************************************
// DATE TIME | END
// **************************************************************

// **************************************************************
// CASHIER PROFILE | START
// **************************************************************
let cashierData = {};

async function loadCashierProfile() {
  const result = await getRequest("/dashboard-cashier/profile");

  cashierData = result.data;

  renderCashierProfile();
  updateGreeting();
}

function renderCashierProfile() {
  document.getElementById("cashier_name").textContent = cashierData.username;

  document.getElementById("cashier_role").textContent = cashierData.role;
}
// **************************************************************
// CASHIER PROFILE | END
// **************************************************************

// **************************************************************
// SUMMARY | START
// **************************************************************
// Variable Setup -------------------------------------------------
let summaryData = {};

// Load Data -------------------------------------------------
async function loadSummary() {
  const result = await getRequest("/dashboard-cashier/summary");

  summaryData = result.data;

  renderSummary();
}

// Render Data -------------------------------------------------
function renderSummary() {
  total_sales.textContent = formatRupiah(summaryData.total_sales);

  total_transaction.textContent = summaryData.total_transaction;

  today_customer.textContent = summaryData.today_customer;

  deposit_status.textContent = summaryData.deposit_status;
}
// function renderSummary() {
//   document.getElementById("total_payments").textContent = formatRupiah(summaryData.total_payments);

//   document.getElementById("total_purchase").textContent = formatRupiah(summaryData.total_purchase);

//   document.getElementById("total_transaction").textContent = summaryData.total_transaction;

//   document.getElementById("total_customer").textContent = summaryData.total_customer;

//   document.getElementById("total_product").textContent = summaryData.total_product;

//   document.getElementById("total_service").textContent = summaryData.total_service;
// }
// **************************************************************
// SUMMARY | END
// **************************************************************

// **************************************************************
// PAYMENT CHART | START
// **************************************************************
// Variable Setup -------------------------------------------------
let salesChartData = [];

// Load Data -------------------------------------------------
async function loadSalesChart() {
  const body = {
    start_date: null,
    end_date: null,
  };

  const result = await postRequest("/dashboard-cashier/payment-chart", body);

  salesChartData = result.data;

  renderSalesChart();
}

// Render Data -------------------------------------------------
function renderSalesChart() {
  const categories = salesChartData.map((item) => item.date);

  const series = salesChartData.map((item) => item.total);

  const options = {
    chart: {
      type: "bar",
      height: 350,
      toolbar: {
        show: false,
      },
      animations: {
        enabled: true,
      },
    },

    plotOptions: {
      bar: {
        borderRadius: 6,
        columnWidth: "45%",
      },
    },

    grid: {
      borderColor: "#ececec",
      strokeDashArray: 4,
    },

    series: [
      {
        name: "Penjualan",
        data: series,
      },
    ],

    xaxis: {
      categories: categories,
      labels: {
        rotate: -45,
      },
    },

    yaxis: {
      labels: {
        formatter: function (value) {
          return formatRupiah(value);
        },
      },
    },

    tooltip: {
      y: {
        formatter: function (value) {
          return formatRupiah(value);
        },
      },
    },

    dataLabels: {
      enabled: false,
    },

    stroke: {
      curve: "smooth",
    },
  };

  document.getElementById("payment_chart").innerHTML = "";

  const chart = new ApexCharts(document.querySelector("#payment_chart"), options);

  chart.render();
}
// **************************************************************
// PAYMENT CHART | END
// **************************************************************

// **************************************************************
// TOP PRODUCT | START
// **************************************************************
// Variable Setup -------------------------------------------------
let topProductsData = [];

// Load Data -------------------------------------------------
async function loadTopProducts() {
  const body = {
    start_date: null,
    end_date: null,
  };

  const result = await postRequest("/dashboard-cashier/top-products", body);

  topProductsData = result.data;

  renderTopProducts();
}

// Render Data -------------------------------------------------
function renderTopProducts() {
  if (topProductsData.length === 0) {
    document.getElementById("top_product_table").innerHTML = `
      <div class="text-center py-4 text-muted">
        <i class="bi bi-box-seam fs-2 d-block mb-2"></i>
        Belum ada data produk.
      </div>
    `;
    return;
  }
  let html = "";

  topProductsData.forEach((product, index) => {
    html += `
      <div class="d-flex justify-content-between align-items-center py-3 ${index !== topProductsData.length - 1 ? "border-bottom" : ""}">

        <div class="d-flex align-items-center">
          <div>

            <div class="fw-semibold">
              ${product.product_name}
            </div>

            <small class="text-muted">
              Total Terjual
            </small>

          </div>

        </div>

        <span class="badge bg-primary rounded-pill px-3 py-2">

          ${product.total_sold}

        </span>

      </div>
    `;
  });

  document.getElementById("top_product_table").innerHTML = html;
}
// **************************************************************
// TOP PRODUCT | END
// **************************************************************

// **************************************************************
// TOP SERVICE | START
// **************************************************************
// Variable Setup -------------------------------------------------
let topServicesData = [];

// Load Data -------------------------------------------------
async function loadTopServices() {
  const body = {
    start_date: null,
    end_date: null,
  };

  const result = await postRequest("/dashboard-cashier/top-services", body);

  topServicesData = result.data;

  renderTopServices();
}

// Render Data -------------------------------------------------
function renderTopServices() {
  if (topServicesData.length === 0) {
    document.getElementById("top_service_table").innerHTML = `
      <div class="text-center py-4 text-muted">
        <i class="bi bi-tools fs-2 d-block mb-2"></i>
        Belum ada data jasa.
      </div>
    `;
    return;
  }
  let html = "";

  topServicesData.forEach((service, index) => {
    html += `
      <div class="d-flex justify-content-between align-items-center py-3 ${index !== topServicesData.length - 1 ? "border-bottom" : ""}">

        <div class="d-flex align-items-center">

          <div>

            <div class="fw-semibold">
              ${service.name}
            </div>

            <small class="text-muted">
              Total Digunakan
            </small>

          </div>

        </div>

        <span class="badge bg-success rounded-pill px-3 py-2">

          ${service.total_service}

        </span>

      </div>
    `;
  });

  document.getElementById("top_service_table").innerHTML = html;
}
// **************************************************************
// TOP SERVICE | END
// **************************************************************

// **************************************************************
// LOW STOCK | START
// **************************************************************
// Variable Setup -------------------------------------------------
let lowStockData = [];

// Load Data -------------------------------------------------
async function loadLowStock() {
  const result = await getRequest("/dashboard-cashier/low-stock");

  lowStockData = result.data;

  renderLowStock();
}

// Render Data -------------------------------------------------
function renderLowStock() {
  if (lowStockData.length === 0) {
    document.getElementById("low_stock_table").innerHTML = `
      <div class="text-center py-4 text-muted">
        <i class="bi bi-check-circle fs-2 d-block mb-2"></i>
        Tidak ada stok yang menipis.
      </div>
    `;
    return;
  }
  let html = "";

  lowStockData.forEach((item, index) => {
    html += `

      <div class="d-flex justify-content-between align-items-center py-3 ${index !== lowStockData.length - 1 ? "border-bottom" : ""}">

          <div>

              <div class="fw-semibold">

                  ${item.product_name}

              </div>

              <small class="text-muted">

                  Stok Barang

              </small>

          </div>

          <span class="badge bg-danger rounded-pill px-3 py-2">

              ${item.stock}

          </span>

      </div>

      `;
  });

  document.getElementById("low_stock_table").innerHTML = html;
}
// **************************************************************
// LOW STOCK | END
// **************************************************************

// **************************************************************
// DEPOSIT SUMMARY | START
// **************************************************************

// Variable Setup -------------------------------------------------
let depositSummaryData = {};

// Load Data -------------------------------------------------
async function loadDepositSummary() {
  const result = await getRequest("/dashboard-cashier/deposit-summary");

  depositSummaryData = result.data;

  renderDepositSummary();
}

// Render Data -------------------------------------------------
function renderSummary() {
  total_sales.textContent = formatRupiah(summaryData.total_sales);

  total_transaction.textContent = summaryData.total_transaction;

  today_customer.textContent = summaryData.today_customer;

  const status = document.getElementById("deposit_status");

  status.textContent = summaryData.deposit_status;

  // Reset class
  status.className = "font-extrabold mb-1";

  switch (summaryData.deposit_status) {
    case "Disetujui":
      status.classList.add("text-success");
      break;

    case "Menunggu":
      status.classList.add("text-warning");
      break;

    case "Ditolak":
      status.classList.add("text-danger");
      break;

    case "Belum Setor":
      status.classList.add("text-secondary");
      break;

    default:
      status.classList.add("text-dark");
  }
}

// **************************************************************
// DEPOSIT SUMMARY | END
// **************************************************************

// **************************************************************
// RECENT TRANSACTION | START
// **************************************************************
// Variable Setup -------------------------------------------------
let recentTransactionData = [];

// Load Data -------------------------------------------------
async function loadRecentTransactions() {
  const result = await getRequest("/dashboard-cashier/recent-transactions");

  recentTransactionData = result.data;

  renderRecentTransactions();
}

// Render Data -------------------------------------------------
function renderRecentTransactions() {
  if (recentTransactionData.length === 0) {
    document.getElementById("recent_transaction_table").innerHTML = `
      <div class="text-center py-4 text-muted">
        <i class="bi bi-receipt fs-2 d-block mb-2"></i>
        Belum ada transaksi.
      </div>
    `;
    return;
  }
  let html = "";

  recentTransactionData.forEach((trx, index) => {
    html += `
      <div class="d-flex justify-content-between align-items-center py-3 ${index !== recentTransactionData.length - 1 ? "border-bottom" : ""}">

        <div>

          <div class="fw-semibold">
            ${trx.invoice}
          </div>

          <small class="text-muted">
            ${trx.customer_name}
          </small>

        </div>

        <div class="text-end">

          <div class="fw-bold">
            ${formatRupiah(trx.total)}
          </div>

          <small class="text-muted">
            ${trx.payment_date}
          </small>

        </div>

      </div>
    `;
  });

  document.getElementById("recent_transaction_table").innerHTML = html;
}
// **************************************************************
// RECENT TRANSACTION | END
// **************************************************************

// **************************************************************
//  UPDATE GREETING | START
// **************************************************************
function updateGreeting() {
  const hour = new Date().getHours();

  let greeting = "";

  if (hour >= 5 && hour < 11) {
    greeting = "Selamat Pagi";
  } else if (hour >= 11 && hour < 15) {
    greeting = "Selamat Siang";
  } else if (hour >= 15 && hour < 18) {
    greeting = "Selamat Sore";
  } else {
    greeting = "Selamat Malam";
  }

  document.getElementById("greeting_text").textContent = `${greeting}, ${cashierData.username} 👋`;
}
// **************************************************************
// UPDATE GREETING | END
// **************************************************************
