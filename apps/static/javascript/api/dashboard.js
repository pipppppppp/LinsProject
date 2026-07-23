// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
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

  await loadPurchaseChart();

  await loadTopProducts();

  await loadTopServices();

  await loadLowStock();

  await loadRecentTransactions();
}
// **************************************************************
// LOAD DASHBOARD | END
// **************************************************************
// **************************************************************
// SUMMARY | START
// **************************************************************
// Variable Setup -------------------------------------------------
let summaryData = {};

// Load Data -------------------------------------------------
async function loadSummary() {
  const result = await getRequest("/dashboard/summary");

  summaryData = result.data;

  renderSummary();
}

// Render Data -------------------------------------------------
function renderSummary() {
  document.getElementById("total_payments").textContent = formatRupiah(summaryData.total_payments);

  document.getElementById("total_purchase").textContent = formatRupiah(summaryData.total_purchase);

  document.getElementById("total_transaction").textContent = summaryData.total_transaction;

  document.getElementById("total_customer").textContent = summaryData.total_customer;

  document.getElementById("total_product").textContent = summaryData.total_product;

  document.getElementById("total_service").textContent = summaryData.total_service;
}
// **************************************************************
// SUMMARY | END
// **************************************************************
// **************************************************************
// SALES CHART | START
// **************************************************************
// Variable Setup -------------------------------------------------
let salesChartData = [];

// Load Data -------------------------------------------------
async function loadSalesChart() {
  const body = {
    start_date: null,
    end_date: null,
  };

  const result = await postRequest("/dashboard/payment-chart", body);

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
    },

    series: [
      {
        name: "Penjualan",
        data: series,
      },
    ],

    xaxis: {
      categories: categories,
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
// SALES CHART | END
// **************************************************************
// **************************************************************
// PURCHASE CHART | START
// **************************************************************
// Variable Setup -------------------------------------------------
let purchaseChartData = [];

// Load Data -------------------------------------------------
async function loadPurchaseChart() {
  const body = {
    start_date: null,
    end_date: null,
  };

  const result = await postRequest("/dashboard/purchase-chart", body);

  purchaseChartData = result.data;

  renderPurchaseChart();
}

// Render Data -------------------------------------------------
function renderPurchaseChart() {
  const categories = purchaseChartData.map((item) => item.date);

  const series = purchaseChartData.map((item) => item.total);

  const options = {
    chart: {
      type: "bar",
      height: 350,
      toolbar: {
        show: false,
      },
    },

    series: [
      {
        name: "Pembelian",
        data: series,
      },
    ],

    xaxis: {
      categories: categories,
    },

    dataLabels: {
      enabled: false,
    },

    stroke: {
      curve: "smooth",
    },
  };

  document.getElementById("purchase_chart").innerHTML = "";

  const chart = new ApexCharts(document.querySelector("#purchase_chart"), options);

  chart.render();
}
// **************************************************************
// PURCHASE CHART | END
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

  const result = await postRequest("/dashboard/top-products", body);

  topProductsData = result.data;

  renderTopProducts();
}

// Render Data -------------------------------------------------
function renderTopProducts() {
  let html = "";

  topProductsData.forEach((product, index) => {
    html += `
      <tr>
        <td>${index + 1}</td>
        <td>${product.product_name}</td>
        <td>${product.total_sold}</td>
      </tr>
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

  const result = await postRequest("/dashboard/top-services", body);

  topServicesData = result.data;

  renderTopServices();
}

// Render Data -------------------------------------------------
function renderTopServices() {
  let html = "";

  topServicesData.forEach((service, index) => {
    html += `
      <tr>
        <td>${index + 1}</td>
        <td>${service.name}</td>
        <td>${service.total_service}</td>
      </tr>
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
  const result = await getRequest("/dashboard/low-stock");

  lowStockData = result.data;

  renderLowStock();
}

// Render Data -------------------------------------------------
function renderLowStock() {
  let html = "";

  lowStockData.forEach((product, index) => {
    html += `
      <tr>
        <td>${index + 1}</td>
        <td>${product.product_name}</td>
        <td>${product.stock}</td>
      </tr>
    `;
  });

  document.getElementById("low_stock_table").innerHTML = html;
}
// **************************************************************
// LOW STOCK | END
// **************************************************************

// **************************************************************
// RECENT TRANSACTION | START
// **************************************************************
// Variable Setup -------------------------------------------------
let recentTransactionData = [];

// Load Data -------------------------------------------------
async function loadRecentTransactions() {
  const result = await getRequest("/dashboard/recent-transactions");

  recentTransactionData = result.data;

  renderRecentTransactions();
}

// Render Data -------------------------------------------------
function renderRecentTransactions() {
  let html = "";

  recentTransactionData.forEach((transaction) => {
    html += `
      <tr>
        <td>${transaction.invoice}</td>
        <td>${transaction.customer_name}</td>
        <td>${formatRupiah(transaction.total)}</td>
      </tr>
    `;
  });

  document.getElementById("recent_transaction_table").innerHTML = html;
}
// **************************************************************
// RECENT TRANSACTION | END
// **************************************************************
