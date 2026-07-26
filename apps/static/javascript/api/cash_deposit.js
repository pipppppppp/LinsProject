// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  formatThousands(form.totalDeposit);
  await reloadTable(loadCashDeposits, renderTable);
}

// Form ID Setup
const form = {
  totalSales: document.getElementById("total_sales"), //total penjualan
  totalDeposit: document.getElementById("total_deposit"),
  notes: document.getElementById("notes"),
};
// **************************************************************
// BASE INISIALIZATION | END
// **************************************************************

// **************************************************************
// GET CASH DEPOSIT | START
// **************************************************************
// Variable Setup -------------------------------------------------
let cashDepositsData = [];

// Load Data -------------------------------------------------

async function loadCashDeposits() {
  const result = await getRequest("/cash-deposit/view");

  console.log(result);

  cashDepositsData = result.data.history;

  form.totalSales.value = formatRupiah(result.data.today_sales);

  document.getElementById("today_sales").textContent = formatRupiah(result.data.today_sales);
  document.getElementById("today_deposit").textContent = formatRupiah(result.data.total_deposit);

  document.getElementById("remaining_deposit").textContent = formatRupiah(result.data.remaining);
  document.getElementById("deposit_count").textContent = `${cashDepositsData.length} kali setor`;

  let statusText = "Belum Setor";

  if (cashDepositsData.length > 0) {
    const latest = cashDepositsData[0];

    switch (latest.status) {
      case 0:
        statusText = "Menunggu";
        break;

      case 1:
        statusText = "Disetujui";
        break;

      case 2:
        statusText = "Ditolak";
        break;
    }
  }

  document.getElementById("deposit_status").textContent = statusText;
}
// **************************************************************
// GET CUSTOMER | END
// **************************************************************

// =============================================================
// STATUS BADGE
// =============================================================
function statusBadge(status) {
  if (status == 0) {
    return `<span class="badge bg-warning">Menunggu</span>`;
  }

  if (status == 1) {
    return `<span class="badge bg-success">Disetujui</span>`;
  }

  return `<span class="badge bg-danger">Ditolak</span>`;
}
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

        <td>${formatRupiah(item.total_deposit)}</td>

        <td>${item.notes ?? "-"}</td>

        <td>${statusBadge(item.status)}</td>

        <td>${item.verified_by ?? "-"}</td>

        <td>${item.verified_at ?? "-"}</td>

        <td>
            <button
                class="btn btn-outline-primary  px-3 btn-detail"
                data-id="${item.id}">
                <i class="bi bi-eye me-1"></i>
                Detail
            </button>
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
// SAVE CUSTOMER | START
// **************************************************************
async function saveCashDeposit() {
  const cashDeposit = {
    total_deposit: removeThousands(form.totalDeposit.value),
    notes: form.notes.value.trim(),
  };

  if (!validateCashDeposit(cashDeposit)) return;

  let result;

  try {
    swalLoading();

    result = await postRequest("/cash-deposit/add", cashDeposit);
  } finally {
    swalClose();
  }

  if (result.status_code === 201) {
    await swalSuccess(result.message);

    clearValue(form.totalDeposit, form.notes);

    await reloadTable(loadCashDeposits, renderTable);
  } else {
    await swalError(result.message);
  }
}

document.querySelector(".btn-save").addEventListener("click", saveCashDeposit);
// **************************************************************
// SAVE PRODUCT | END
// **************************************************************

// **************************************************************
// DELETE CUSTOMER | START
// **************************************************************
document.getElementById("table1").addEventListener("click", handleTableClick);

async function handleTableClick(e) {
  const detailBtn = e.target.closest(".btn-detail");

  if (detailBtn) {
    const id = Number(detailBtn.dataset.id);

    showDetail(id);

    return;
  }

  const deleteBtn = e.target.closest(".btn-delete");

  if (!deleteBtn) return;

  const id = Number(deleteBtn.dataset.id);

  const confirmDelete = await swalDelete();

  if (!confirmDelete.isConfirmed) return;

  let result;

  try {
    swalLoading();

    result = await deleteRequest(`/cash-deposit/delete/${id}`);
  } finally {
    swalClose();
  }

  if (result.status_code === 200) {
    await swalSuccess(result.message);

    await reloadTable(loadCashDeposits, renderTable);
  } else {
    await swalError(result.message);
  }
}
// **************************************************************
// DELETE CASH DEPOSIT | END
// **************************************************************

// **************************************************************
// DETAIL CASH DEPOSIT | END
// **************************************************************

function showDetail(id) {
  const data = cashDepositsData.find((item) => item.id == id);

  if (!data) return;

  document.getElementById("detail_modal_body").innerHTML = `
      <div class="row">

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
              <p>${data.verified_by ?? "-"}</p>
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
