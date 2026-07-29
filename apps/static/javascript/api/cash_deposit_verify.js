// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  document.getElementById("filter_date").value = new Date().toISOString().split("T")[0];

  document.querySelector(".btn-search").addEventListener("click", async () => {
    await reloadTable(loadCashDeposits, renderTable);
  });

  await reloadTable(loadCashDeposits, renderTable);
}

// Variable Setup -------------------------------------------------
let cashDepositsData = [];
// **************************************************************
// BASE INISIALIZATION | END
// **************************************************************

// **************************************************************
// GET CASH DEPOSIT | START
// **************************************************************
async function loadCashDeposits() {
  const date = document.getElementById("filter_date").value;
  console.log("Date:", date);
  const status = document.getElementById("status").value;
  console.log("STATUS :", status);
  const result = await getRequest(`/cash-deposit/view?date=${date}&status=${status}`);
  if (!result) {
    return;
  }
  cashDepositsData = result.data.history;
}

// **************************************************************
// GET CASH DEPOSIT | END
// **************************************************************

// **************************************************************
// STATUS BADGE | START
// **************************************************************
function statusBadge(status) {
  if (status == 0) {
    return `<span class="badge bg-warning">Pending</span>`;
  }

  if (status == 1) {
    return `<span class="badge bg-success">Approved</span>`;
  }

  return `<span class="badge bg-danger">Rejected</span>`;
}
// **************************************************************
// STATUS BADGE | END
// **************************************************************

// **************************************************************
// RENDER DATA | START
// **************************************************************
function renderTable() {
  let html = "";

  cashDepositsData.forEach((item, index) => {
    html += `
      <tr>

        <td>${index + 1}</td>

        <td>${item.deposit_date}</td>

        <td>${item.cashier_name}</td>

        <td>${formatRupiah(item.total_sales)}</td>

        <td>${formatRupiah(item.total_deposit)}</td>

        <td>${formatRupiah(item.difference)}</td>

        <td>${statusBadge(item.status)}</td>

        <td>

          <button
            class="btn btn-outline-primary btn-detail"
            data-id="${item.id}">

            <i class="bi bi-eye me-1"></i>

            Detail

          </button>

          ${
            item.status == 0
              ? `
                <button
                  class="btn btn-success btn-approve"
                  data-id="${item.id}">

                  <i class="bi bi-check-lg"></i>

                </button>

                <button
                  class="btn btn-danger btn-reject"
                  data-id="${item.id}">

                  <i class="bi bi-x-lg"></i>

                </button>
              `
              : ""
          }

        </td>

      </tr>
    `;
  });

  document.getElementById("cash_deposit_table").innerHTML = html;
}
// **************************************************************
// RENDER DATA | END
// **************************************************************

// **************************************************************
// TABLE EVENT | START
// **************************************************************
document.getElementById("table1").addEventListener("click", handleTableClick);

async function handleTableClick(e) {
  const detailBtn = e.target.closest(".btn-detail");

  if (detailBtn) {
    const id = Number(detailBtn.dataset.id);

    showDetail(id);

    return;
  }

  const approveBtn = e.target.closest(".btn-approve");

  if (approveBtn) {
    const id = Number(approveBtn.dataset.id);

    await verifyCashDeposit(id, 1);

    return;
  }

  const rejectBtn = e.target.closest(".btn-reject");

  if (rejectBtn) {
    const id = Number(rejectBtn.dataset.id);

    await verifyCashDeposit(id, 2);

    return;
  }
}
// **************************************************************
// TABLE EVENT | END
// **************************************************************

// **************************************************************
// VERIFY CASH DEPOSIT | START
// **************************************************************
async function verifyCashDeposit(id, status) {
  const confirm = await Swal.fire({
    title: "Konfirmasi",
    text: status == 1 ? "Setujui setor kas ini?" : "Tolak setor kas ini?",
    icon: "question",
    showCancelButton: true,
    confirmButtonText: "Ya",
    cancelButtonText: "Batal",
  });

  if (!confirm.isConfirmed) return;

  let result;

  try {
    swalLoading();

    result = await putRequest("/cash-deposit/verify", {
      deposit_id: id,
      status: status,
    });
  } finally {
    swalClose();
  }
  if (!result) {
    return;
  }

  if (result.status_code === 200) {
    await swalSuccess("Berhasil", result.message);

    await reloadTable(loadCashDeposits, renderTable);
  } else {
    await swalError("Gagal", result.message);
  }
}
// **************************************************************
// VERIFY CASH DEPOSIT | END
// **************************************************************

// **************************************************************
// DETAIL CASH DEPOSIT | START
// **************************************************************
function showDetail(id) {
  const data = cashDepositsData.find((item) => item.id == id);

  if (!data) return;

  document.getElementById("detail_modal_body").innerHTML = `
          <div class="row">
    
              <div class="col-md-6 mb-3">
                  <label class="fw-bold">Kasir</label>
                  <p>${data.cashier_name}</p>
              </div>
    
              <div class="col-md-6 mb-3">
                  <label class="fw-bold">Tanggal Setor</label>
                  <p>${data.deposit_date}</p>
              </div>
    
              <div class="col-md-6 mb-3">
                  <label class="fw-bold">Status</label>
                  <p>${statusBadge(data.status)}</p>
              </div>
    
              <div class="col-md-6 mb-3">
                  <label class="fw-bold">Total Penjualan</label>
                  <p>${formatRupiah(data.total_sales)}</p>
              </div>
    
              <div class="col-md-6 mb-3">
                  <label class="fw-bold">Nominal Setor</label>
                  <p>${formatRupiah(data.total_deposit)}</p>
              </div>
    
              <div class="col-md-6 mb-3">
                  <label class="fw-bold">Selisih</label>
                  <p>${formatRupiah(data.difference)}</p>
              </div>
    
              <div class="col-md-6 mb-3">
                  <label class="fw-bold">Diverifikasi Oleh</label>
                  <p>${data.verified_by_name ?? "-"}</p>
              </div>
    
              <div class="col-md-6 mb-3">
                  <label class="fw-bold">Diverifikasi Pada</label>
                  <p>${data.verified_at ?? "-"}</p>
              </div>
    
              <div class="col-12">
                  <label class="fw-bold">Catatan</label>
                  <p>${data.notes ?? "-"}</p>
              </div>
    
          </div>
      `;

  new bootstrap.Modal(document.getElementById("detail_modal")).show();
}
// **************************************************************
// DETAIL CASH DEPOSIT | END
// **************************************************************
