// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************

const API = {
  view: "/workshop-management/view",
  detail: "/workshop-management/detail",
  activate: "/workshop-management/activate",
  deactivate: "/workshop-management/deactivate",
  delete: "/workshop-management/delete",
};

let workshopTable = null;
let workshopDatas = [];
let detailWorkshopModal = null;
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// READ WORKSHOP | START
// **************************************************************
async function loadWorkshop(status = "all") {
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
      workshopDatas = [];
      renderWorkshopTable(workshopDatas);

      return swalError(result.message);
    }

    workshopDatas = result.data ?? [];

    renderWorkshopTable(workshopDatas);
  } catch (error) {
    console.error("LOAD WORKSHOP ERROR:", error);

    swalError("Gagal memuat data bengkel.");
  }
}
// **************************************************************
// READ WORKSHOP | END
// **************************************************************

// **************************************************************
// RENDER TABLE | START
// **************************************************************
function renderWorkshopTable(datas) {
  const tableBody = document.getElementById("table_workshop");

  if (!tableBody) {
    return;
  }

  if (!Array.isArray(datas) || datas.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="9" class="text-center">
          Data bengkel tidak tersedia.
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
            <img
              src="${data.logo ? `/static/images/profiles/${data.logo}` : "/static/images/profiles/default-workshop.png"}"
              class="workshop-logo"
            >
          </td>

          <td class="workshop-name">
            ${data.workshop_name}
          </td>

          <td>
            <div class="owner-name">
              ${data.owner_name}
            </div>

            <div class="owner-role">
              Owner
            </div>
          </td>

          <td>${data.owner_email}</td>

          <td>${data.workshop_phone}</td>

          <td class="text-center">
            ${generateStatusBadge(data.workshop_status)}
          </td>

          <td>
            ${data.created_at}
          </td>

          <td class="text-center">
            ${generateActionButton(data)}
          </td>
        </tr>
      `;
    })
    .join("");

  tableBody.innerHTML = rows;
}
// **************************************************************
// RENDER TABLE | END
// **************************************************************

// **************************************************************
// REFRESH WORKSHOP | START
// **************************************************************
async function refreshWorkshop() {
  const status = document.getElementById("filter_status")?.value ?? "all";

  if (workshopTable) {
    workshopTable.destroy();
    workshopTable = null;
  }

  await loadWorkshop(status);

  const table = document.getElementById("workshopManagementTable");

  if (table && typeof simpleDatatables !== "undefined") {
    workshopTable = new simpleDatatables.DataTable("#workshopManagementTable", {
      searchable: true,
      paging: true,
      perPage: 5,
      perPageSelect: [5, 10, 25, 50],
      fixedHeight: false,
    });
  }
}
// **************************************************************
// REFRESH WORKSHOP | END
// **************************************************************

// **************************************************************
// STATUS BADGE | START
// **************************************************************
function generateStatusBadge(is_active) {
  if (Number(is_active)) {
    return `
      <span class="badge rounded-pill bg-success px-3 py-2">
        Aktif
      </span>
    `;
  }

  return `
    <span class="badge rounded-pill bg-secondary px-3 py-2">
      Tidak Aktif
    </span>
  `;
}
// **************************************************************
// STATUS BADGE | END
// **************************************************************

// **************************************************************
// ACTION BUTTON | START
// **************************************************************
function generateActionButton(data) {
  let statusButton = "";

  if (Number(data.workshop_status)) {
    statusButton = `
      <button
        type="button"
        class="btn btn-warning btn-sm"
        title="Nonaktifkan Bengkel"
        onclick="deactivateWorkshop(${data.workshop_id})"
      >
        <i class="bi bi-pause-circle-fill"></i>
      </button>
    `;
  } else {
    statusButton = `
      <button
        type="button"
        class="btn btn-success btn-sm"
        title="Aktifkan Bengkel"
        onclick="activateWorkshop(${data.workshop_id})"
      >
        <i class="bi bi-play-circle-fill"></i>
      </button>
    `;
  }

  return `
    <div
      class="d-flex justify-content-center align-items-center gap-1"
    >
      <button
        type="button"
        class="btn btn-info btn-sm"
        title="Lihat Detail"
        onclick="detailWorkshop(${data.workshop_id})"
      >
        <i class="bi bi-eye-fill"></i>
      </button>

      ${statusButton}

      <button
        type="button"
        class="btn btn-danger btn-sm"
        title="Hapus Bengkel"
        onclick="deleteWorkshop(${data.workshop_id})"
      >
        <i class="bi bi-trash-fill"></i>
      </button>
    </div>
  `;
}
// **************************************************************
// ACTION BUTTON | END
// **************************************************************

// **************************************************************
// ACTIVATE WORKSHOP | START
// **************************************************************
async function activateWorkshop(workshop_id) {
  const confirm = await swalConfirm("Aktifkan Bengkel?", "Bengkel akan diaktifkan kembali.", "Aktifkan");

  if (!confirm.isConfirmed) {
    return;
  }

  try {
    const response = await fetch(API.activate, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        workshop_id: workshop_id,
      }),
    });

    const result = await response.json();

    if (!response.ok || result.status_code !== 200) {
      return swalError(result.message);
    }

    await refreshWorkshop();

    await swalSuccess(result.message);
  } catch (error) {
    console.error("ACTIVATE WORKSHOP ERROR:", error);

    swalError("Gagal mengaktifkan bengkel.");
  }
}
// **************************************************************
// ACTIVATE WORKSHOP | END
// **************************************************************

// **************************************************************
// DEACTIVATE WORKSHOP | START
// **************************************************************
async function deactivateWorkshop(workshop_id) {
  const confirm = await swalConfirm("Nonaktifkan Bengkel?", "Bengkel akan dinonaktifkan.", "Nonaktifkan");

  if (!confirm.isConfirmed) {
    return;
  }

  try {
    const response = await fetch(API.deactivate, {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        workshop_id: workshop_id,
      }),
    });

    const result = await response.json();

    if (!response.ok || result.status_code !== 200) {
      return swalError(result.message);
    }

    await refreshWorkshop();
    await swalSuccess(result.message);
  } catch (error) {
    console.error("DEACTIVATE WORKSHOP ERROR:", error);
    swalError("Gagal menonaktifkan bengkel.");
  }
}
// **************************************************************
// DEACTIVATE WORKSHOP | END
// **************************************************************

// **************************************************************
// DETAIL WORKSHOP | START
// **************************************************************
async function detailWorkshop(workshop_id) {
  try {
    const response = await fetch(`${API.detail}/${workshop_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();

    if (result.status_code !== 200) {
      return swalError(result.message);
    }

    const data = result.data;
    const detailContent = document.getElementById("detailWorkshopContent");

    if (!detailContent) {
      return swalError("Element detail bengkel tidak ditemukan.");
    }

    detailContent.innerHTML = `
          <div class="text-center mb-4">
            <img
              src="${data.logo ? `/static/images/profiles/${data.logo}` : "/static/images/profiles/default-workshop.png"}"
              class="detail-logo"
              alt="Logo ${data.workshop_name}"
            >
    
            <h4 class="mt-3">
              ${data.workshop_name}
            </h4>
    
            ${generateStatusBadge(data.workshop_status)}
          </div>
    
          <table class="table table-borderless">
            <tr>
              <th>Owner</th>
              <td>${data.owner_name}</td>
            </tr>
    
            <tr>
              <th>Email</th>
              <td>${data.owner_email}</td>
            </tr>
    
            <tr>
              <th>Telepon</th>
              <td>${data.workshop_phone}</td>
            </tr>
    
            <tr>
              <th>Alamat</th>
              <td>${data.workshop_address}</td>
            </tr>
    
            <tr>
              <th>Dibuat</th>
              <td>${data.created_at}</td>
            </tr>
          </table>
        `;

    const modalElement = document.getElementById("detailWorkshopModal");

    if (!modalElement) {
      return swalError("Modal detail bengkel tidak ditemukan.");
    }

    if (!detailWorkshopModal) {
      detailWorkshopModal = new bootstrap.Modal(modalElement);
    }

    detailWorkshopModal.show();
  } catch (error) {
    console.error(error);
    swalError("Gagal memuat detail bengkel.");
  }
}
// **************************************************************
// DETAIL WORKSHOP | END
// **************************************************************

// **************************************************************
// DELETE WORKSHOP | START
// **************************************************************
async function deleteWorkshop(workshop_id) {
  const confirm = await swalDelete();

  if (!confirm.isConfirmed) {
    return;
  }

  try {
    const response = await fetch(API.delete, {
      method: "DELETE",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        workshop_id: workshop_id,
      }),
    });

    const result = await response.json();

    if (!response.ok || result.status_code !== 200) {
      return swalError(result.message);
    }

    await refreshWorkshop();
    await swalSuccess(result.message);
  } catch (error) {
    console.error("DELETE WORKSHOP ERROR:", error);
    swalError("Gagal menghapus bengkel.");
  }
}
// **************************************************************
// DELETE WORKSHOP | END
// **************************************************************

// **************************************************************
// EVENT LISTENER | START
// **************************************************************
const filterStatus = document.getElementById("filter_status");

if (filterStatus) {
  filterStatus.addEventListener("change", async function () {
    await refreshWorkshop();
  });
}

const btnRefresh = document.getElementById("btn_refresh");

if (btnRefresh) {
  btnRefresh.addEventListener("click", async function () {
    // Disable tombol
    btnRefresh.disabled = true;

    // Tampilkan loading
    btnRefresh.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2"></span>
                Refreshing...
            `;

    // Refresh data
    try {
      await refreshWorkshop();
    } finally {
      btnRefresh.innerHTML = `
                <i class="bi bi-arrow-clockwise"></i>
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
  await refreshWorkshop();
});
// **************************************************************
// PAGE INITIALIZATION | END
// **************************************************************
