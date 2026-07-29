// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  const today = new Date().toISOString().split("T")[0];

  document.getElementById("start_date").value = today;
  document.getElementById("end_date").value = today;

  await loadCashiers();

  await reloadTable(() => loadHistorySales(today, today), renderTable);
  // Refresh button
  document.getElementById("btn_refresh")?.addEventListener("click", async () => {
    await reloadTable(loadHistorySales, renderTable);
  });
}
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

let historySalesData = [];

// ============================================================
// LOAD CASHIERS | START
// ============================================================
async function loadCashiers() {
  const result = await getRequest("/cashier-management/view");

  if (!result) return;

  if (result.status_code !== 200) {
    return;
  }

  let html = `
      <option value="">Semua Kasir</option>
  `;

  result.data.forEach((cashier) => {
    html += `
          <option value="${cashier.id}">
              ${cashier.username}
          </option>
      `;
  });

  document.getElementById("cashier_id").innerHTML = html;
}
// ============================================================
// LOAD CASHIERS | END
// ============================================================

// **************************************************************
// GET HISTORY SALES | START
// **************************************************************
async function loadHistorySales(start_date = "", end_date = "", cashier_id = "") {
  let url = "/history-sales/view";

  const params = [];

  if (start_date) {
    params.push(`start_date=${start_date}`);
  }

  if (end_date) {
    params.push(`end_date=${end_date}`);
  }

  if (cashier_id) {
    params.push(`cashier_id=${cashier_id}`);
  }

  if (params.length > 0) {
    url += "?" + params.join("&");
  }

  const result = await getRequest(url);

  if (!result) return;

  if (result.status_code !== 200) {
    return swalError(result.message);
  }

  historySalesData = result.data.history;

  document.getElementById("today_transaction").textContent = result.data.today_transaction;

  document.getElementById("today_total").textContent = formatRupiah(result.data.today_total);

  document.getElementById("transaction_count").textContent = `${result.data.today_transaction} Transaksi`;

  document.getElementById("today_sales").textContent = formatRupiah(result.data.today_sales);

  const activeCashier = document.getElementById("active_cashier");

  if (activeCashier) {
    activeCashier.textContent = `${result.data.active_cashier} Orang`;
  }
}
// **************************************************************
// GET HISTORY SALES | END
// **************************************************************

// **************************************************************
// RENDER TABLE | START
// **************************************************************
function renderTable() {
  console.log("RENDER TABLE");
  console.log(historySalesData);
  let html = "";
  if (historySalesData.length === 0) {
    document.getElementById("history_sales_table").innerHTML = `
    <tr>
        <td colspan="8" class="text-center py-5">

            <i class="bi bi-receipt fs-1 text-secondary"></i>

            <h5 class="mt-3 mb-1">
                Belum Ada Riwayat Penjualan
            </h5>

            <p class="text-muted mb-0">
                Riwayat transaksi akan muncul setelah kasir melakukan penjualan.
            </p>

        </td>
    </tr>
    `;

    return;
  } else {
    historySalesData.forEach((history, index) => {
      const initial = history.customer_name
        .split(" ")
        .slice(0, 2)
        .map((n) => n[0])
        .join("")
        .toUpperCase();

      html += `
          <tr>
  
              <td class="text-center">
                  ${index + 1}
              </td>
  
              <td>
  
                  <span class="badge bg-primary">
  
                      ${history.invoice}
  
                  </span>
  
              </td>
  
              <td>
  
                  ${history.payment_date}
  
              </td>
  
              <td>
  
                <div class="d-flex align-items-center">

                    <div class="avatar avatar-md bg-primary me-3">
                
                        <span class="avatar-content fw-bold">
                            ${initial}
                        </span>
                
                    </div>
                
                    <div>
                
                        <div class="fw-bold">
                            ${history.customer_name}
                        </div>
                
                        <small class="text-muted">
                            Pelanggan
                        </small>
                
                    </div>
                
                </div>
  
              </td>
  
              <td>

                  <span class="badge bg-light-secondary text-secondary">

                      ${history.plate_number}

                  </span>

              </td>
  
              <td class="text-center">
  
              <span class="badge rounded-pill bg-success">

                  <i class="bi bi-person-check-fill me-1"></i>
              
                  ${history.cashier_name}
              
              </span>
  
              </td>
  
              <td class="text-end">

                  <span class="fw-bold text-success">

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
  
          </tr>
      `;
    });
  }
  document.getElementById("history_sales_table").innerHTML = html;
}
// **************************************************************
// RENDER TABLE | END
// **************************************************************

// **************************************************************
// DETAIL HISTORY SALES | START
// **************************************************************
document.getElementById("table1").addEventListener("click", handleTableClick);

async function handleTableClick(e) {
  const detailBtn = e.target.closest(".btn-detail");

  if (!detailBtn) return;

  const id = Number(detailBtn.dataset.id);

  let result;

  try {
    swalLoading();

    result = await getRequest(`/history-sales/detail/${id}`);
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
// DETAIL HISTORY SALES | END
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

              <td>${item.quantity}</td>

              <td>${formatRupiah(item.unit_price)}</td>

              <td>${formatRupiah(item.subtotal)}</td>

          </tr>
      `;
  });

  let serviceRows = "";

  data.services.forEach((item, index) => {
    serviceRows += `
          <tr>

              <td>${index + 1}</td>

              <td>${item.service_name}</td>

              <td>${item.quantity}</td>

              <td>${formatRupiah(item.service_price)}</td>

              <td>${formatRupiah(item.subtotal)}</td>

          </tr>
      `;
  });

  document.getElementById("detail_modal_body").innerHTML = `

      <div class="row mb-3">

          <div class="col-md-4">
              <strong>Invoice</strong><br>
              ${data.invoice}
          </div>

          <div class="col-md-4">
              <strong>Tanggal</strong><br>
              ${data.payment_date}
          </div>

          <div class="col-md-4">
              <strong>Kasir</strong><br>
              ${data.cashier_name}
          </div>

      </div>

      <div class="row mb-4">

          <div class="col-md-4">
              <strong>Customer</strong><br>
              ${data.customer_name}
          </div>

          <div class="col-md-4">
              <strong>No Polisi</strong><br>
              ${data.plate_number}
          </div>

          <div class="col-md-4">
              <strong>Total</strong><br>
              ${formatRupiah(data.total)}
          </div>

      </div>

      <h6>Produk</h6>

      <table class="table table-bordered">

          <thead>

              <tr>

                  <th>No</th>
                  <th>Produk</th>
                  <th>Qty</th>
                  <th>Harga</th>
                  <th>Subtotal</th>

              </tr>

          </thead>

          <tbody>

              ${productRows}

          </tbody>

      </table>

      <h6 class="mt-4">Jasa</h6>

      <table class="table table-bordered">

          <thead>

              <tr>

                  <th>No</th>
                  <th>Jasa</th>
                  <th>Qty</th>
                  <th>Harga</th>
                  <th>Subtotal</th>

              </tr>

          </thead>

          <tbody>

              ${serviceRows}

          </tbody>

      </table>

      <div class="row mt-4">

          <div class="col-md-4">

              <strong>Dibayar</strong><br>

              ${formatRupiah(data.paid)}

          </div>

          <div class="col-md-4">

              <strong>Kembalian</strong><br>

              ${formatRupiah(data.change)}

          </div>

      </div>

  `;
}
// **************************************************************
// RENDER DETAIL | END
// **************************************************************

// **************************************************************
// RENDER PRODUCT | START
// **************************************************************
function renderProducts(products) {
  let html = "";

  products.forEach((item, index) => {
    html += `
          <tr>

              <td>${index + 1}</td>

              <td>${item.product_name}</td>

              <td>${item.quantity}</td>

              <td>${formatRupiah(item.unit_price)}</td>

              <td>${formatRupiah(item.subtotal)}</td>

          </tr>
      `;
  });

  document.getElementById("product_detail_table").innerHTML = html;
}
// **************************************************************
// RENDER PRODUCT | END
// **************************************************************

// **************************************************************
// RENDER SERVICE | START
// **************************************************************
function renderServices(services) {
  let html = "";

  services.forEach((item, index) => {
    html += `
          <tr>

              <td>${index + 1}</td>

              <td>${item.service_name}</td>

              <td>${item.quantity}</td>

              <td>${formatRupiah(item.service_price)}</td>

              <td>${formatRupiah(item.subtotal)}</td>

          </tr>
      `;
  });

  document.getElementById("service_detail_table").innerHTML = html;
}
// **************************************************************
// RENDER SERVICE | END
// **************************************************************

// **************************************************************
// FILTER HISTORY SALES | START
// **************************************************************

document.getElementById("btn_filter").addEventListener("click", async () => {
  const start_date = document.getElementById("start_date").value;

  const end_date = document.getElementById("end_date").value;
  const cashier_id = document.getElementById("cashier_id")?.value ?? "";

  await reloadTable(() => loadHistorySales(start_date, end_date, cashier_id), renderTable);
});

document.getElementById("btn_reset").addEventListener("click", async () => {
  document.getElementById("start_date").value = "";
  document.getElementById("end_date").value = "";

  const cashier_id = document.getElementById("cashier_id")?.value ?? "";

  await reloadTable(() => loadHistorySales("", "", cashier_id), renderTable);
});
// **************************************************************
// FILTER HISTORY SALES | END
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
