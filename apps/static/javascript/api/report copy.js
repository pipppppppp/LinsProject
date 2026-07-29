// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  const today = new Date().toISOString().split("T")[0];

  document.getElementById("start_date").value = today;
  document.getElementById("end_date").value = today;
  
  await loadSuppliers();
}

// Form Setup ----------------------------------------------------
const form = {
  start_date: document.getElementById("start_date"),
  end_date: document.getElementById("end_date"),
  supplier_id: document.getElementById("supplier_id"),
  total_purchase: document.getElementById("total_purchase"),
  total_expense: document.getElementById("total_expense"),
};
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// VARIABLE SETUP | START
// **************************************************************
let suppliersData = [];
let purchaseReportData = [];
let purchaseSummary = {};
// **************************************************************
// VARIABLE SETUP | END
// **************************************************************

// **************************************************************
// LOAD SUPPLIER | START
// **************************************************************
async function loadSuppliers() {
  const result = await getRequest("/supplier/view");

  suppliersData = result.data;

  renderSupplier();
}
// **************************************************************
// LOAD SUPPLIER | END
// **************************************************************

// **************************************************************
// RENDER SUPPLIER | START
// **************************************************************
function renderSupplier() {
  let html = `
        <option value="">
            Semua Supplier
        </option>
    `;

  suppliersData.forEach((supplier) => {
    html += `
            <option value="${supplier.id}">
                ${supplier.name}
            </option>
        `;
  });

  form.supplier_id.innerHTML = html;
}
// **************************************************************
// RENDER SUPPLIER | END
// **************************************************************

// **************************************************************
// SEARCH PURCHASE REPORT | START
// **************************************************************
async function searchPurchaseReport() {
  const report = {
    start_date: new Date(form.start_date.value).getTime(),
    end_date: new Date(form.end_date.value).getTime(),
    supplier_id: form.supplier_id.value,
  };

  // VALIDATION ==================================================
  if (!validatePurchaseReport(report)) return;

  let result;

  try {
    swalLoading();

    result = await postRequest("/report/purchase/view", report);
  } finally {
    swalClose();
  }
  if (!result) {
    await swalError("Gagal mengambil data laporan.");
    return;
  }
  if (result.status_code === 200) {
    purchaseReportData = result.data.data;
    purchaseSummary = result.data.summary;

    renderSummary();
    renderTable();
  } else {
    await swalError(result.message);
  }
}
// **************************************************************
// SEARCH PURCHASE REPORT | END
// **************************************************************

// **************************************************************
// RENDER SUMMARY | START
// **************************************************************
function renderSummary() {
  form.total_purchase.textContent = purchaseSummary.total_purchase ?? 0;

  form.total_expense.textContent = formatRupiah(String(purchaseSummary.total_expense ?? 0));
}
// **************************************************************
// RENDER SUMMARY | END
// **************************************************************

// **************************************************************
// RENDER TABLE | START
// **************************************************************
function renderTable() {
  let html = "";

  purchaseReportData.forEach((purchase, index) => {
    
    html += `
              <tr>
  
                  <td>${index + 1}</td>
  
                  <td>
                      ${purchase.purchase_date}
                  </td>
  
                  <td>
                      ${purchase.supplier_name}
                  </td>
  
                  <td>
                      ${formatRupiah(String(purchase.total))}
                  </td>
  
              </tr>
          `;
  });

  document.getElementById("purchase_report_table").innerHTML = html;
}
// **************************************************************
// RENDER TABLE | END
// **************************************************************

// **************************************************************
// SEARCH BUTTON | START
// **************************************************************
document.getElementById("btn-search").addEventListener("click", searchPurchaseReport);
// **************************************************************
// SEARCH BUTTON | END
// **************************************************************

// **************************************************************
// EXPORT EXCEL | START
// **************************************************************
async function exportPurchaseExcel() {
  const report = {
    start_date: new Date(form.start_date.value).getTime(),
    end_date: new Date(form.end_date.value).getTime(),
    supplier_id: form.supplier_id.value,
  };

  // VALIDATION ==================================================
  if (!validatePurchaseReport(report)) return;

  const response = await fetch("/report/purchase/export/excel", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(report),
  });

  if (!response.ok) {
    // await swalError("Gagal export Excel.");
    const error = await response.text();

    await swalError(error);
    return;
  }

  const blob = await response.blob();

  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");

  a.href = url;
  a.download = "purchase_report.xlsx";

  document.body.appendChild(a);

  a.click();

  a.remove();

  window.URL.revokeObjectURL(url);
}
// **************************************************************
// EXPORT EXCEL | END
// **************************************************************

// **************************************************************
// EXPORT PDF | START
// **************************************************************
async function exportPurchasePDF() {
  const report = {
    start_date: new Date(form.start_date.value).getTime(),
    end_date: new Date(form.end_date.value).getTime(),
    supplier_id: form.supplier_id.value,
  };

  // VALIDATION ==================================================
  if (!validatePurchaseReport(report)) return;

  const response = await fetch("/report/purchase/export/pdf", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(report),
  });

  if (!response.ok) {
    // await swalError("Gagal export PDF.");
    const error = await response.text();

    await swalError(error);
    return;
  }

  const blob = await response.blob();

  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");

  a.href = url;
  a.download = "purchase_report.pdf";

  document.body.appendChild(a);

  a.click();

  a.remove();

  window.URL.revokeObjectURL(url);
}
// **************************************************************
// EXPORT PDF | END
// **************************************************************

// **************************************************************
// EXPORT EVENT | START
// **************************************************************
document.getElementById("btn-excel").addEventListener("click", exportPurchaseExcel);

document.getElementById("btn-pdf").addEventListener("click", exportPurchasePDF);
// **************************************************************
// EXPORT EVENT | END
// **************************************************************