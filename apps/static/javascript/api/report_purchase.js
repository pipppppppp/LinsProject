// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  await loadSuppliers();
  await reloadTable(loadReport, renderTable);
}

// Form ID Setup
const form = {
  start_date: document.getElementById("start_date"),
  end_date: document.getElementById("end_date"),
  supplier_id: document.getElementById("supplier_id"),
};
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// GET REPORT | START
// **************************************************************

// Variable Setup -------------------------------------------------
let reportData = [];
let chartData = [];
let topProductsData = [];
let topSuppliersData = [];

// Load Data -------------------------------------------------
async function loadReport() {
  const params = new URLSearchParams({
    start_date: form.start_date.value,
    end_date: form.end_date.value,
    supplier_id: form.supplier_id.value,
  });

  // Summary
  const summary = await getRequest(`/report-purchase/summary?${params.toString()}`);

  renderSummary(summary.data);

  // Chart
  const chart = await getRequest(`/report-purchase/chart?${params.toString()}`);

  chartData = chart.data.chart;

  // Top Products
  const products = await getRequest(`/report-purchase/top-products?${params.toString()}`);

  topProductsData = products.data.top_products;

  // Top Services
  const suppliers = await getRequest(`/report-purchase/top-suppliers?${params.toString()}`);

  topSuppliersData = suppliers.data.top_suppliers;

  // Table
  const table = await getRequest(`/report-purchase/table?${params.toString()}`);

  reportData = table.data.report;

  renderPurchaseChart();
  renderTopProducts();
  renderTopSuppliers();
}
// **************************************************************
// GET REPORT | END
// ************************************************************** **************************************************************

// **************************************************************
// RENDER SUMMARY | START
// **************************************************************
function renderSummary(data) {
  document.getElementById("total_purchase").textContent = formatRupiah(data.total_sales);

  document.getElementById("total_transaction").textContent = data.total_transaction;

  document.getElementById("total_supplier").textContent = data.total_transaction;


  document.getElementById("total_item").textContent = formatRupiah(data.average_transaction);

//   document.getElementById("active_cashier").textContent = data.active_cashier;
}
// **************************************************************
// RENDER SUMMARY | END
// **************************************************************

// **************************************************************
// RENDER SALES CHART | START
// **************************************************************
let purchaseChart = null;

function renderPurchaseChart() {
  const options = {
    chart: {
      type: "area",
      height: 350,
      toolbar: {
        show: false,
      },
    },

    dataLabels: {
      enabled: false,
    },

    stroke: {
      curve: "smooth",
      width: 3,
    },

    series: [
      {
        name: "Pembelian",
        data: chartData.map((item) => item.total),
      },
    ],

    xaxis: {
      categories: chartData.map((item) => item.date),
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
  };

  if (purchaseChart) {
    purchaseChart.destroy();
  }

  purchaseChart = new ApexCharts(document.querySelector("#purchase_chart"), options);

  purchaseChart.render();
}
// **************************************************************
// RENDER SALES CHART | END
// **************************************************************

// **************************************************************
// RENDER TOP PRODUCTS | START
// **************************************************************
function renderTopProducts() {
  let html = "";

  if (topProductsData.length === 0) {
    html = `
      <div class="text-center text-muted py-4">
        Tidak ada data produk.
      </div>
    `;
  } else {
    topProductsData.forEach((product, index) => {
      html += `
        <div class="d-flex justify-content-between align-items-center border-bottom py-3">

          <div>

            <h6 class="mb-1">
              ${index + 1}. ${product.product_name}
            </h6>

            <small class="text-muted">
              ${product.total_quantity} Terjual
            </small>

          </div>

          <span class="badge bg-light-primary text-primary">
            ${formatRupiah(product.total_sales)}
          </span>

        </div>
      `;
    });
  }

  document.getElementById("top_products").innerHTML = html;
}
// **************************************************************
// RENDER TOP PRODUCTS | END
// **************************************************************

// **************************************************************
// RENDER TOP SERVICES | START
// **************************************************************
function renderTopSuppliers() {
  let html = "";

  if (topSuppliersData.length === 0) {
    html = `
      <div class="text-center text-muted py-4">
        Tidak ada data Supplier.
      </div>
    `;
  } else {
    topSuppliersData.forEach((service, index) => {
      html += `
        <div class="d-flex justify-content-between align-items-center border-bottom py-3">

          <div>

            <h6 class="mb-1">
              ${index + 1}. ${service.service_name}
            </h6>

            <small class="text-muted">
              ${service.total_quantity} Digunakan
            </small>

          </div>

          <span class="badge bg-light-success text-success">
            ${formatRupiah(service.total_sales)}
          </span>

        </div>
      `;
    });
  }

  document.getElementById("top_suppliers").innerHTML = html;
}
// **************************************************************
// RENDER TOP SERVICES | END
// **************************************************************

// **************************************************************
// RENDER TABLE | START
// **************************************************************
function renderTable() {
  let html = "";

  reportData.forEach((report, index) => {
    html += `
      <tr>

        <td class="text-center fw-bold">
          ${index + 1}
        </td>

        <td>
          ${report.purchase_date}
        </td>

        <td>
          ${report.customer_name}
        </td>

        <td>
          ${report.plate_number}
        </td>

        <td>
          ${report.cashier_name}
        </td>

        <td class="text-end fw-semibold">
          ${formatRupiah(report.total)}
        </td>

      </tr>
    `;
  });

  document.getElementById("table_report_purchase").innerHTML = html;
}
// **************************************************************
// RENDER TABLE | END
// **************************************************************

// **************************************************************
// FILTER REPORT | START
// **************************************************************
async function filterReport() {
  await reloadTable(loadReport, renderTable);
}

const btnFilter = document.getElementById("btn_filter");

if (btnFilter) {
  btnFilter.addEventListener("click", filterReport);
}
// **************************************************************
// FILTER REPORT | END
// **************************************************************

// **************************************************************
// RESET FILTER | START
// **************************************************************
async function resetFilter() {
  form.start_date.value = "";
  form.end_date.value = "";
  form.supplier_id.value = "";

  await reloadTable(loadReport, renderTable);
}

const btnReset = document.getElementById("btn_reset");

if (btnReset) {
  btnReset.addEventListener("click", resetFilter);
}
// **************************************************************
// RESET FILTER | END
// **************************************************************

// **************************************************************
// EXPORT EXCEL | START
// **************************************************************
async function exportExcel(event) {
  event.preventDefault();
  console.log("Export Excel diklik");
  const body = {
    start_date: form.start_date.value,
    end_date: form.end_date.value,
    supplier_id: form.supplier_id.value,
  };

  try {
    swalLoading();

    const response = await fetch("/report-purchase/export/excel", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error("Gagal mengunduh laporan.");
    }

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "report_purchase.xlsx";

    document.body.appendChild(link);
    link.click();
    link.remove();

    window.URL.revokeObjectURL(url);

    swalClose();
    await swalSuccess("Laporan Excel berhasil diunduh.");
  } catch (error) {
    swalClose();
    await swalError(error.message);
  }
}
const btnExportExcel = document.getElementById("btn_export_excel");

if (btnExportExcel) {
  btnExportExcel.addEventListener("click", exportExcel);
}
// **************************************************************
// EXPORT EXCEL | END
// **************************************************************

// **************************************************************
// EXPORT PDF | START
// **************************************************************
async function exportPdf(event) {
  event.preventDefault();

  const body = {
    start_date: form.start_date.value,
    end_date: form.end_date.value,
    supplier_id: form.supplier_id.value,
  };

  try {
    swalLoading();

    const response = await fetch("/report-purchase/export/pdf", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error("Gagal mengunduh laporan.");
    }

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "report_purchase.pdf";

    document.body.appendChild(link);
    link.click();
    link.remove();

    window.URL.revokeObjectURL(url);

    swalClose();
    await swalSuccess("Laporan PDF berhasil diunduh.");
  } catch (error) {
    swalClose();
    await swalError(error.message);
  }
}
const btnExportPdf = document.getElementById("btn_export_pdf");

if (btnExportPdf) {
  btnExportPdf.addEventListener("click", exportPdf);
}
// **************************************************************
// EXPORT PDF | END
// **************************************************************

// **************************************************************
// LOAD CASHIERS | START
// **************************************************************
async function loadSuppliers() {
  const result = await getRequest("/supplier/view");

  const cashiers = result.data;

  let html = `
    <option value="">
      Semua Kasir
    </option>
  `;

  cashiers.forEach((cashier) => {
    html += `
      <option value="${cashier.id}">
        ${cashier.username}
      </option>
    `;
  });

  form.supplier_id.innerHTML = html;
}
// **************************************************************
// LOAD CASHIERS | END
// **************************************************************
