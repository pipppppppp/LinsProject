// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
const API = {
  view: "/subscription-payment-history/view",
  detail: "/subscription-payment-history/detail",
};

const filterStatus = document.getElementById("filter_status");

const btnRefresh = document.getElementById("btn_refresh");

let paymentHistoryDatas = [];
let paymentHistoryTable = null;
let detailPaymentModal = null;
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// GET PAYMENT HISTORY | START
// **************************************************************
async function loadPaymentHistory(status = "all") {
  try {
    const response = await fetch(`${API.view}?status=${encodeURIComponent(status)}&_=${Date.now()}`, {
      method: "GET",
      cache: "no-store",
      headers: {
        Accept: "application/json",
      },
    });

    const result = await response.json();

    if (!response.ok || result.status_code !== 200) {
      paymentHistoryDatas = [];

      renderPaymentHistory(paymentHistoryDatas);

      return swalError(result.message);
    }

    paymentHistoryDatas = result.data ?? [];

    renderPaymentHistory(paymentHistoryDatas);
  } catch (error) {
    console.error("LOAD PAYMENT HISTORY ERROR:", error);

    paymentHistoryDatas = [];

    renderPaymentHistory(paymentHistoryDatas);

    swalError("Gagal memuat riwayat pembayaran.");
  }
}
// **************************************************************
// GET PAYMENT HISTORY | END
// **************************************************************

// **************************************************************
// RENDER PAYMENT HISTORY | START
// **************************************************************
function renderPaymentHistory(datas) {
  const tableBody = document.getElementById("table_subscription_payment_history");

  if (!tableBody) {
    return;
  }

  if (!Array.isArray(datas) || datas.length === 0) {
    tableBody.innerHTML = `
          <tr>
            <td
              colspan="9"
              class="text-center text-muted"
            >
              Data pembayaran tidak tersedia.
            </td>
          </tr>
        `;

    return;
  }

  const rows = datas
    .map((data, index) => {
      return `
            <tr>
              <td>${index + 1}</td>
    
              <td>
                <span class="fw-semibold">
                  ${data.order_id ?? "-"}
                </span>
              </td>
    
              <td>
                <div class="fw-semibold">
                  ${data.workshop_name ?? "-"}
                </div>
    
                <small class="text-muted">
                  ${data.owner_email ?? "-"}
                </small>
              </td>
    
              <td>
                ${data.owner_name ?? "-"}
              </td>
    
              <td class="fw-semibold">
                ${formatPaymentAmount(data.amount)}
              </td>
    
              <td>
                ${formatPaymentType(data.payment_type)}
              </td>
    
              <td>
                ${generatePaymentStatusBadge(data.transaction_status)}
              </td>
    
              <td>
                ${data.paid_at ?? "-"}
              </td>
    
              <td class="text-center">
                <button
                  type="button"
                  class="btn btn-info btn-sm"
                  title="Lihat Detail Pembayaran"
                  onclick="detailPayment(
                    ${data.payment_id}
                  )"
                >
                  <i class="bi bi-eye-fill"></i>
                </button>
              </td>
            </tr>
          `;
    })
    .join("");

  tableBody.innerHTML = rows;
}
// **************************************************************
// RENDER PAYMENT HISTORY | END
// **************************************************************

// **************************************************************
// REFRESH PAYMENT HISTORY | START
// **************************************************************
async function refreshPaymentHistory() {
  const status = filterStatus?.value ?? "all";

  if (paymentHistoryTable) {
    paymentHistoryTable.destroy();
    paymentHistoryTable = null;
  }

  await loadPaymentHistory(status);

  const table = document.getElementById("subscriptionPaymentHistoryTable");

  if (table && typeof simpleDatatables !== "undefined") {
    paymentHistoryTable = new simpleDatatables.DataTable("#subscriptionPaymentHistoryTable", {
      searchable: true,
      paging: true,
      perPage: 5,
      perPageSelect: [5, 10, 25, 50],
      fixedHeight: false,
    });
  }
}
// **************************************************************
// REFRESH PAYMENT HISTORY | END
// **************************************************************

// **************************************************************
// FORMAT PAYMENT AMOUNT | START
// **************************************************************
function formatPaymentAmount(amount) {
  return `Rp ${Number(amount || 0).toLocaleString("id-ID")}`;
}
// **************************************************************
// FORMAT PAYMENT AMOUNT | END
// **************************************************************

// **************************************************************
// FORMAT PAYMENT TYPE | START
// **************************************************************
function formatPaymentType(payment_type) {
  const paymentType = String(payment_type ?? "").toLowerCase();

  const paymentTypes = {
    bank_transfer: "Bank Transfer",
    credit_card: "Kartu Kredit",
    echannel: "Mandiri Bill",
    qris: "QRIS",
    gopay: "GoPay",
    shopeepay: "ShopeePay",
    cstore: "Gerai Retail",
  };

  return paymentTypes[paymentType] ?? payment_type ?? "-";
}
// **************************************************************
// FORMAT PAYMENT TYPE | END
// **************************************************************

// **************************************************************
// PAYMENT STATUS BADGE | START
// **************************************************************
function generatePaymentStatusBadge(status) {
  const transactionStatus = String(status ?? "").toLowerCase();

  if (transactionStatus === "settlement" || transactionStatus === "capture" || transactionStatus === "success") {
    return `
          <span class="badge bg-success">
            Berhasil
          </span>
        `;
  }

  if (transactionStatus === "pending") {
    return `
          <span class="badge bg-warning">
            Pending
          </span>
        `;
  }

  if (transactionStatus === "expire" || transactionStatus === "expired") {
    return `
          <span class="badge bg-secondary">
            Kedaluwarsa
          </span>
        `;
  }

  if (transactionStatus === "deny" || transactionStatus === "cancel" || transactionStatus === "failure") {
    return `
          <span class="badge bg-danger">
            Gagal
          </span>
        `;
  }

  return `
        <span class="badge bg-secondary">
          ${status ?? "-"}
        </span>
      `;
}
// **************************************************************
// PAYMENT STATUS BADGE | END
// **************************************************************

// **************************************************************
// DETAIL PAYMENT | START
// **************************************************************
async function detailPayment(payment_id) {
  try {
    const response = await fetch(`${API.detail}/${payment_id}?_=${Date.now()}`, {
      method: "GET",
      cache: "no-store",
      headers: {
        Accept: "application/json",
      },
    });

    const result = await response.json();

    if (!response.ok || result.status_code !== 200) {
      return swalError(result.message);
    }

    const data = result.data;

    const detailContent = document.getElementById("detailPaymentContent");

    const modalElement = document.getElementById("detailPaymentModal");

    if (!detailContent) {
      return swalError("Element detail pembayaran tidak ditemukan.");
    }

    if (!modalElement) {
      return swalError("Modal detail pembayaran tidak ditemukan.");
    }

    detailContent.innerHTML = `
          <div class="row g-4">
            <div class="col-md-6">
              <div class="card border h-100">
                <div class="card-body">
                  <h6 class="mb-3">
                    <i class="bi bi-shop me-2"></i>
                    Informasi Bengkel
                  </h6>
    
                  <table class="table table-borderless mb-0">
                    <tr>
                      <th>Nama Bengkel</th>
                      <td>
                        ${data.workshop_name ?? "-"}
                      </td>
                    </tr>
    
                    <tr>
                      <th>Email Bengkel</th>
                      <td>
                        ${data.workshop_email ?? "-"}
                      </td>
                    </tr>
    
                    <tr>
                      <th>Telepon</th>
                      <td>
                        ${data.workshop_phone ?? "-"}
                      </td>
                    </tr>
    
                    <tr>
                      <th>Owner</th>
                      <td>
                        ${data.owner_name ?? "-"}
                      </td>
                    </tr>
    
                    <tr>
                      <th>Email Owner</th>
                      <td>
                        ${data.owner_email ?? "-"}
                      </td>
                    </tr>
                  </table>
                </div>
              </div>
            </div>
    
            <div class="col-md-6">
              <div class="card border h-100">
                <div class="card-body">
                  <h6 class="mb-3">
                    <i class="bi bi-receipt me-2"></i>
                    Informasi Pembayaran
                  </h6>
    
                  <table class="table table-borderless mb-0">
                    <tr>
                      <th>Order ID</th>
                      <td>
                        ${data.order_id ?? "-"}
                      </td>
                    </tr>
    
                    <tr>
                      <th>Transaction ID</th>
                      <td class="text-break">
                        ${data.transaction_id ?? "-"}
                      </td>
                    </tr>
    
                    <tr>
                      <th>Nominal</th>
                      <td class="fw-semibold">
                        ${formatPaymentAmount(data.amount)}
                      </td>
                    </tr>
    
                    <tr>
                      <th>Metode</th>
                      <td>
                        ${formatPaymentType(data.payment_type)}
                      </td>
                    </tr>
    
                    <tr>
                      <th>Status</th>
                      <td>
                        ${generatePaymentStatusBadge(data.transaction_status)}
                      </td>
                    </tr>
    
                    <tr>
                      <th>Dibuat</th>
                      <td>
                        ${data.created_at ?? "-"}
                      </td>
                    </tr>
    
                    <tr>
                      <th>Dibayar</th>
                      <td>
                        ${data.paid_at ?? "-"}
                      </td>
                    </tr>
                  </table>
                </div>
              </div>
            </div>
          </div>
        `;

    if (!detailPaymentModal) {
      detailPaymentModal = new bootstrap.Modal(modalElement);
    }

    detailPaymentModal.show();
  } catch (error) {
    console.error("DETAIL PAYMENT ERROR:", error);

    swalError("Gagal memuat detail pembayaran.");
  }
}
// **************************************************************
// DETAIL PAYMENT | END
// **************************************************************

// **************************************************************
// EVENT LISTENER | START
// **************************************************************
if (filterStatus) {
  filterStatus.addEventListener("change", async function () {
    await refreshPaymentHistory();
  });
}

if (btnRefresh) {
  btnRefresh.addEventListener("click", async function () {
    btnRefresh.disabled = true;

    btnRefresh.innerHTML = `
            <span
              class="spinner-border
                     spinner-border-sm me-2"
            ></span>
            Memuat...
          `;

    try {
      await refreshPaymentHistory();
    } finally {
      btnRefresh.innerHTML = `
              <i class="bi bi-arrow-clockwise me-1"></i>
              Refresh
            `;

      btnRefresh.disabled = false;
    }
  });
}
// **************************************************************
// EVENT LISTENER | END
// **************************************************************

// **************************************************************
// PAGE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", async function () {
  await refreshPaymentHistory();
});
// **************************************************************
// PAGE INITIALIZATION | END
// **************************************************************