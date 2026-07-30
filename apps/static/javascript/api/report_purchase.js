// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  setDefaultDate();
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
// DEFAULT DATE | START
// **************************************************************
function setDefaultDate() {
  const today = new Date();

  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");

  const currentDate = `${year}-${month}-${day}`;

  form.start_date.value = currentDate;
  form.end_date.value = currentDate;
}
// **************************************************************
// DEFAULT DATE | END
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

  renderSummary(summary.data || {});

  // Chart
  const chart = await getRequest(`/report-purchase/chart?${params.toString()}`);

  chartData = chart.data?.chart || [];

  // Top Products
  const products = await getRequest(`/report-purchase/top-products?${params.toString()}`);

  topProductsData = products.data?.top_products || [];

  // Top Suppliers
  const suppliers = await getRequest(`/report-purchase/top-suppliers?${params.toString()}`);

  topSuppliersData = suppliers.data?.top_suppliers || [];

  // Table
  const table = await getRequest(`/report-purchase/table?${params.toString()}`);
  if (table.status_code !== 200) {
    throw new Error(table.message || "Gagal mengambil tabel laporan pembelian.");
  }

  reportData = table.data?.report || [];
  reportData = table.data?.report || [];

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
function renderSummary(data = {}) {
  document.getElementById("total_purchase").textContent = formatRupiah(data.total_purchase || 0);

  document.getElementById("total_transaction").textContent = data.total_transaction || 0;

  document.getElementById("total_supplier").textContent = data.active_supplier || 0;

  document.getElementById("total_item").textContent = data.total_item || 0;
}
// **************************************************************
// RENDER SUMMARY | END
// **************************************************************

// **************************************************************
// RENDER PURCHASE CHART | START
// **************************************************************
let purchaseChart = null;

function renderPurchaseChart() {
  const chartElement = document.querySelector("#purchase_chart");

  if (!chartElement) {
    return;
  }

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
        data: chartData.map((item) => item.total_purchase || 0),
      },
    ],

    xaxis: {
      categories: chartData.map((item) => item.date || "-"),
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

  purchaseChart = new ApexCharts(chartElement, options);

  purchaseChart.render();
}
// **************************************************************
// RENDER PURCHASE CHART | END
// **************************************************************

// **************************************************************
// RENDER TOP PRODUCTS | START
// **************************************************************
function renderTopProducts() {
  let html = "";

  if (!Array.isArray(topProductsData) || topProductsData.length === 0) {
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
              ${index + 1}. ${product.product_name || "-"}
            </h6>

            <small class="text-muted">
              Jumlah pembelian produk
            </small>
          </div>

          <span class="badge bg-light-primary text-primary">
            ${product.total_quantity || 0} Item
          </span>
        </div>
      `;
    });
  }

  const topProductsElement = document.getElementById("top_products");

  if (!topProductsElement) {
    return;
  }

  topProductsElement.innerHTML = html;
}
// **************************************************************
// RENDER TOP PRODUCTS | END
// ****************************************************************************************************************************

// **************************************************************
// RENDER TOP SUPPLIERS | START
// **************************************************************
function renderTopSuppliers() {
  let html = "";

  if (!Array.isArray(topSuppliersData) || topSuppliersData.length === 0) {
    html = `
      <div class="text-center text-muted py-4">
        Tidak ada data supplier.
      </div>
    `;
  } else {
    topSuppliersData.forEach((supplier, index) => {
      html += `
        <div class="d-flex justify-content-between align-items-center border-bottom py-3">
          <div>
            <h6 class="mb-1">
              ${index + 1}. ${supplier.name || "-"}
            </h6>

            <small class="text-muted">
              Total nilai pembelian
            </small>
          </div>

          <span class="badge bg-light-success text-success">
            ${formatRupiah(supplier.total_purchase || 0)}
          </span>
        </div>
      `;
    });
  }

  const topSuppliersElement = document.getElementById("top_suppliers");

  if (!topSuppliersElement) {
    return;
  }

  topSuppliersElement.innerHTML = html;
}
// **************************************************************
// RENDER TOP SUPPLIERS | END
// **************************************************************
// **************************************************************
// RENDER TABLE | START
// **************************************************************
function renderTable() {
  let html = "";

  if (!Array.isArray(reportData) || reportData.length === 0) {
    html = `
      <tr>
        <td colspan="6" class="text-center text-muted py-4">
          Tidak ada data laporan pembelian.
        </td>
      </tr>
    `;
  } else {
    reportData.forEach((report, index) => {
      html += `
        <tr>
          <td class="text-center fw-bold">
            ${index + 1}
          </td>

          <td>
            ${report.invoice || "-"}
          </td>

          <td>
            ${report.purchase_date || "-"}
          </td>

          <td>
            ${report.name || "-"}
          </td>

          <td class="text-center">
            ${report.total_item || 0}
          </td>

          <td class="text-end fw-semibold">
            ${formatRupiah(report.total || 0)}
          </td>
        </tr>
      `;
    });
  }

  const tableBody = document.getElementById("table_report_purchase_body");

  if (!tableBody) {
    return;
  }

  tableBody.innerHTML = html;
}
// **************************************************************
// RENDER TABLE | END
// ************************************************************** **************************************************************

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
  form.supplier_id.value = "";

  setDefaultDate();

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
// LOAD SUPPLIERS | START
// **************************************************************
async function loadSuppliers() {
  const result = await getRequest("/supplier/view");

  const suppliers = Array.isArray(result.data) ? result.data : [];

  let html = `
    <option value="">
      Semua Supplier
    </option>
  `;

  suppliers.forEach((supplier) => {
    html += `
      <option value="${supplier.id}">
        ${supplier.name || "-"}
      </option>
    `;
  });

  form.supplier_id.innerHTML = html;
}
// **************************************************************
// LOAD SUPPLIERS | END
// **************************************************************
