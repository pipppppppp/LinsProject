// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  await reloadTable(loadCashiers, renderTable);
}

// Form ID Setup
const form = {
  title: document.getElementById("modal_label"),
  id: document.getElementById("cashier_id"),
  owner_name: document.getElementById("owner_name"),
  username: document.getElementById("username"),
  email: document.getElementById("email"),
  password: document.getElementById("password"),
  role: document.getElementById("role"),
  is_active: document.getElementById("is_active"),
};
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// GET CASHIER | START
// **************************************************************
// Variable Setup -------------------------------------------------
let cashiersData = [];

// Load Data -------------------------------------------------
async function loadCashiers() {
  const result = await getRequest("/cashier-management/view");

  if (!result) {
    return;
  }

  if (result.status_code !== 200) {
    await swalError("Gagal", result.message);

    return;
  }

  cashiersData = result.data;
}
// **************************************************************
// GET CASHIER | END
// **************************************************************

// **************************************************************
// RENDER DATA | START
// **************************************************************
function renderTable() {
  let html = "";

  cashiersData.forEach((cashier, index) => {
    const statusBadge =
      Number(cashier.is_active) === 1 ? `<span class="badge bg-success">Aktif</span>` : `<span class="badge bg-danger">Nonaktif</span>`;

    const statusButton =
      Number(cashier.is_active) === 1
        ? `
          <button
            class="btn btn-secondary btn-sm btn-status"
            data-id="${cashier.id}"
            data-status="0"
            title="Nonaktifkan Kasir">
            <i class="bi bi-pause-circle-fill"></i>
          </button>
        `
        : `
          <button
            class="btn btn-success btn-sm btn-status"
            data-id="${cashier.id}"
            data-status="1"
            title="Aktifkan Kasir">
            <i class="bi bi-play-circle-fill"></i>
          </button>
        `;

    html += `
      <tr>
        <td>${index + 1}</td>
        <td>${cashier.owner_name}</td>
        <td>${cashier.username}</td>
        <td>${cashier.email}</td>

        <td class="text-center">
          ${statusBadge}
        </td>

        <td class="text-center">
          <div class="d-inline-flex gap-2">

            <button
              class="btn btn-warning btn-sm btn-edit"
              data-id="${cashier.id}"
              title="Ubah Kasir">
              <i class="bi bi-pencil-square"></i>
            </button>

            ${statusButton}

          </div>
        </td>
      </tr>
    `;
  });

  document.getElementById("cashier_table").innerHTML = html;

  renderSummary();
}
// **************************************************************
// RENDER DATA | END
// **************************************************************

// **************************************************************
// SAVE CASHIER | START
// **************************************************************
async function saveCashier() {
  const cashier = {
    id: form.id.value,
    owner_name: formatTitle(form.owner_name.value),
    username: form.username.value.trim(),
    email: form.email.value.trim().toLowerCase(),
    password: form.password.value,
    role: form.role.value,
    is_active: form.is_active.value,
  };

  // VALIDATION ==================================================
  if (!validateCashier(cashier)) return;

  let result;

  try {
    swalLoading();

    if (!cashier.id) {
      result = await postRequest("/cashier-management/add", cashier);
    } else {
      result = await putRequest(`/cashier-management/edit/${cashier.id}`, cashier);
    }
  } finally {
    swalClose();
  }

  if (!result) {
    return;
  }

  if (result.status_code === 201 || result.status_code === 200) {
    closeModal("cashier_modal");

    clearValue(form.id, form.owner_name, form.username, form.email, form.password, form.role, form.is_active);

    form.title.textContent = "Tambah Kasir";

    await reloadTable(loadCashiers, renderTable);

    await swalSuccess("Berhasil", result.message);
  } else {
    await swalError("Gagal", result.message);
  }
}

document.querySelector(".btn-save").addEventListener("click", saveCashier);
// **************************************************************
// SAVE CASHIER | END
// **************************************************************

// **************************************************************
// UPDATE & ACTIVE NONACTIVE CASHIER | START
// **************************************************************
// **************************************************************
// UPDATE & ACTIVE NONACTIVE CASHIER | START
// **************************************************************
document.getElementById("table1").addEventListener("click", handleTableClick);

async function handleTableClick(e) {
  const editBtn = e.target.closest(".btn-edit");
  const statusBtn = e.target.closest(".btn-status");

  // EDIT ==================================================
  if (editBtn) {
    const id = Number(editBtn.dataset.id);

    const cashier = cashiersData.find((item) => item.id === id);

    if (!cashier) return;

    form.title.textContent = "Ubah Kasir";

    form.id.value = cashier.id;
    form.owner_name.value = cashier.owner_name;
    form.username.value = cashier.username;
    form.email.value = cashier.email;
    form.password.value = "";
    form.role.value = cashier.role;
    form.is_active.value = cashier.is_active;

    const modal = new bootstrap.Modal(document.getElementById("cashier_modal"));

    modal.show();

    return;
  }

  // ACTIVE / NONACTIVE =====================================
  if (statusBtn) {
    const id = Number(statusBtn.dataset.id);
    const newStatus = Number(statusBtn.dataset.status);

    const cashier = cashiersData.find((item) => item.id === id);

    if (!cashier) return;

    const actionText = newStatus === 1 ? "Aktifkan" : "Nonaktifkan";

    const confirm = await swalConfirm(
      `${actionText} Kasir?`,
      newStatus === 1 ? "Akun kasir akan diaktifkan kembali." : "Akun kasir akan dinonaktifkan.",
      actionText
    );

    if (!confirm.isConfirmed) return;

    let result;

    try {
      swalLoading();

      const data = {
        id: cashier.id,
        owner_name: cashier.owner_name,
        username: cashier.username,
        email: cashier.email,
        password: "",
        role: cashier.role,
        is_active: newStatus,
      };

      result = await putRequest(`/cashier-management/edit/${cashier.id}`, data);
    } finally {
      swalClose();
    }

    if (!result) return;

    if (result.status_code === 200) {
      await reloadTable(loadCashiers, renderTable);

      await swalSuccess("Berhasil", newStatus === 1 ? "Kasir berhasil diaktifkan." : "Kasir berhasil dinonaktifkan.");
    } else {
      await swalError("Gagal", result.message);
    }

    return;
  }
}
// **************************************************************
// UPDATE & ACTIVE NONACTIVE CASHIER | END
// **************************************************************
// **************************************************************
// UPDATE & ACTIVE NONACTIVE CASHIER | END
// **************************************************************

// **************************************************************
// RESET FORM | START
// **************************************************************
function resetForm() {
  form.title.textContent = "Tambah Kasir";

  clearValue(form.id, form.owner_name, form.username, form.email, form.password);

  form.role.value = "2";
  form.is_active.value = "1";
}
// **************************************************************
// RESET FORM | END
// **************************************************************

// **************************************************************
// MODAL EVENT | START
// **************************************************************
document.getElementById("cashier_modal").addEventListener("hidden.bs.modal", resetForm);
// **************************************************************
// MODAL EVENT | END
// **************************************************************

// **************************************************************
// RENDER SUMMARY | START
// **************************************************************
function renderSummary() {
  // Total Kasir
  const totalCashier = cashiersData.length;

  // Total Kasir Aktif
  const activeCashier = cashiersData.filter((cashier) => Number(cashier.is_active) === 1).length;

  // Total Kasir Nonaktif
  const inactiveCashier = cashiersData.filter((cashier) => Number(cashier.is_active) === 0).length;

  // Render Summary Card
  document.getElementById("total_cashier").textContent = totalCashier;
  document.getElementById("active_cashier").textContent = activeCashier;
  document.getElementById("inactive_cashier").textContent = inactiveCashier;
}
// **************************************************************
// RENDER SUMMARY | END
// **************************************************************
