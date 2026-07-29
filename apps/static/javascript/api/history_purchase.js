// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  const today = new Date().toISOString().split("T")[0];

  document.getElementById("start_date").value = today;
  document.getElementById("end_date").value = today;

  await loadSuppliers();

  await reloadTable(() => loadHistoryPurchase(today, today), renderTable);
  // Refresh button
  document.getElementById("btn_refresh")?.addEventListener("click", async () => {
    await reloadTable(loadHistoryPurchase, renderTable);
  });
}
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

let historyPurchaseData = [];

// ============================================================
// LOAD SUPPLIERS | START
// ============================================================
async function loadSuppliers() {
  const result = await getRequest("/supplier/view");

  if (!result) return;

  if (result.status_code !== 200) {
    return;
  }

  let html = `
      <option value="">Semua Supplier</option>
  `;

  result.data.forEach((supplier) => {
    html += `
        <option value="${supplier.id}">
            ${supplier.name}
        </option>
    `;
  });

  document.getElementById("supplier_id").innerHTML = html;
}
// ============================================================
// LOAD SUPPLIERS | END
// ============================================================

// **************************************************************
// GET HISTORY PURCHASE | START
// **************************************************************
async function loadHistoryPurchase(start_date = "", end_date = "", supplier_id = "") {
  let url = "/history-purchase/view";

  const params = [];

  if (start_date) {
    params.push(`start_date=${start_date}`);
  }

  if (end_date) {
    params.push(`end_date=${end_date}`);
  }

  if (supplier_id) {
    params.push(`supplier_id=${supplier_id}`);
  }

  if (params.length > 0) {
    url += "?" + params.join("&");
  }

  const result = await getRequest(url);

  if (!result) return;

  if (result.status_code !== 200) {
    return swalError(result.message);
  }

  historyPurchaseData = result.data.history;

  document.getElementById("total_purchase").textContent = result.data.total_purchase;

  document.getElementById("total_expense").textContent = formatRupiah(result.data.total_expense);

  document.getElementById("today_purchase").textContent = formatRupiah(result.data.today_purchase);

  document.getElementById("active_supplier").textContent = `${result.data.active_supplier} Supplier`;
}
// **************************************************************
// GET HISTORY PURCHASE | END
// **************************************************************

// **************************************************************
// RENDER TABLE | START
// **************************************************************
function renderTable() {
  let html = "";
  if (historyPurchaseData.length === 0) {
    document.getElementById("history_purchase_table").innerHTML = `
    <tr>
        <td colspan="8" class="text-center py-5">

            <i class="bi bi-receipt fs-1 text-secondary"></i>

            <h5 class="mt-3 mb-1">
                Belum Ada Riwayat Pembelian 
            </h5>

            <p class="text-muted mb-0">
                Riwayat transaksi pembelian akan muncul setelah melakukan pembelian barang.
            </p>

        </td>
    </tr>
    `;

    return;
  } else {
    historyPurchaseData.forEach((history, index) => {
      html += `
            <tr>

                <td class="text-center">
                    ${index + 1}
                </td>

                <td>
                    ${history.purchase_date}
                </td>

                <td>

                    <div class="d-flex align-items-center">

                        <div class="avatar avatar-md bg-primary me-3">

                            <span class="avatar-content fw-bold">
                                ${(history.supplier_name || "-").substring(0, 2).toUpperCase()}
                            </span>

                        </div>

                        <div>

                            <div class="fw-bold">
                                ${history.supplier_name ?? "-"}
                            </div>

                            <small class="text-muted">
                                Supplier
                            </small>

                        </div>

                    </div>

                </td>

                <td class="text-end">

                    <span class="fw-bold text-danger">

                        ${formatRupiah(history.total)}

                    </span>

                </td>

                <td class="text-center">

                    <button
                        class="btn btn-outline-primary rounded-pill btn-sm btn-detail"
                        data-id="${history.id}">

                        <i class="bi bi-eye-fill me-1"></i>

                        Detail

                    </button>

                </td>

            </tr>
        `;
    });
  }
  document.getElementById("history_purchase_table").innerHTML = html;
}
// **************************************************************
// RENDER TABLE | END
// **************************************************************

// **************************************************************
// DETAIL HISTORY PURCHASE | START
// **************************************************************
document.getElementById("table1").addEventListener("click", handleTableClick);

async function handleTableClick(e) {
  const detailBtn = e.target.closest(".btn-detail");

  if (!detailBtn) return;

  const id = Number(detailBtn.dataset.id);

  let result;

  try {
    swalLoading();

    result = await getRequest(`/history-purchase/detail/${id}`);
  } finally {
    swalClose();
  }

  if (result.status_code !== 200) {
    return swalError(result.message);
  }

  renderDetail(result.data);

  openModal("detail_modal");
}
// **************************************************************
// DETAIL HISTORY PURCHASE | END
// **************************************************************

// **************************************************************
// RENDER DETAIL | START
// **************************************************************
function renderDetail(data) {
  let productRows = "";

  data.products.forEach((item, index) => {
    productRows += `
          <tr>

              <td>${index + 1}</td>

              <td>${item.product_name}</td>

              <td class="text-center">
                  ${item.quantity}
              </td>

              <td class="text-end">
                  ${formatRupiah(item.unit_cost)}
              </td>

              <td class="text-end">
                  ${formatRupiah(item.subtotal)}
              </td>

          </tr>
      `;
  });

  document.getElementById("detail_modal_body").innerHTML = `

      <div class="row mb-4">

          <div class="col-md-4">

              <strong>Tanggal</strong><br>

              ${data.purchase_date}

          </div>

          <div class="col-md-4">

              <strong>Supplier</strong><br>

              ${data.supplier_name}

          </div>

          <div class="col-md-4">

              <strong>Total Pembelian</strong><br>

              <span class="fw-bold text-danger">

                  ${formatRupiah(data.total)}

              </span>

          </div>

      </div>

      <h6 class="mb-3">

          Daftar Produk

      </h6>

      <table class="table table-bordered">

          <thead>

              <tr>

                  <th width="5%">No</th>

                  <th>Produk</th>

                  <th width="10%" class="text-center">
                      Qty
                  </th>

                  <th width="20%" class="text-end">
                      Harga Beli
                  </th>

                  <th width="20%" class="text-end">
                      Subtotal
                  </th>

              </tr>

          </thead>

          <tbody>

              ${productRows}

          </tbody>

      </table>

  `;
}
// **************************************************************
// RENDER DETAIL | END
// **************************************************************

// **************************************************************
// FILTER HISTORY PURCHASE | START
// **************************************************************

document.getElementById("btn_filter").addEventListener("click", async () => {
  const start_date = document.getElementById("start_date").value;

  const end_date = document.getElementById("end_date").value;
  const supplier_id = document.getElementById("supplier_id").value;

  await reloadTable(() => loadHistoryPurchase(start_date, end_date, supplier_id), renderTable);
});

document.getElementById("btn_reset").addEventListener("click", async () => {
  const today = new Date().toISOString().split("T")[0];

  document.getElementById("start_date").value = today;
  document.getElementById("end_date").value = today;

  await reloadTable(() => loadHistoryPurchase(today, today), renderTable);
});
// **************************************************************
// FILTER HISTORY PURCHASE | END
// **************************************************************

// **************************************************************
// EXPORT EXCEL | START
// **************************************************************
async function exportHistorySalesExcel() {
  const report = {
    start_date: document.getElementById("start_date").value,
    end_date: document.getElementById("end_date").value,
  };

  const response = await fetch("/history-sales/excel", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(report),
  });

  if (!response.ok) {
    const error = await response.text();

    await swalError(error);

    return;
  }

  const blob = await response.blob();

  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");

  a.href = url;
  a.download = "history_sales_report.xlsx";

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
async function exportHistorySalesPDF() {
  const report = {
    start_date: document.getElementById("start_date").value,
    end_date: document.getElementById("end_date").value,
  };

  const response = await fetch("/history-sales/pdf", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(report),
  });

  if (!response.ok) {
    const error = await response.text();

    await swalError(error);

    return;
  }

  const blob = await response.blob();

  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");

  a.href = url;
  a.download = "history_sales_report.pdf";

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
// document.getElementById("btn-excel").addEventListener("click", exportHistorySalesExcel);

// document.getElementById("btn-pdf").addEventListener("click", exportHistorySalesPDF);
// **************************************************************
// EXPORT EVENT | END
// **************************************************************
