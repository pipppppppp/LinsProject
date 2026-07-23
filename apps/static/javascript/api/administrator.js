// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************

const API = {
  dashboard: "/administrator/statistic",
  view: "/administrator/view",
  detail: "/administrator/detail",
  verify: "/administrator/verify",
  activate: "/administrator/activate",
  deactivate: "/administrator/deactivate",
  delete: "/administrator/delete",
};

const dashboardCard = {
  totalWorkshop: document.getElementById("total_workshop"),
  activeWorkshop: document.getElementById("active_workshop"),
  inactiveWorkshop: document.getElementById("inactive_workshop"),
  totalOwner: document.getElementById("total_owner"),
};

const tableBody = document.getElementById("table_workshop");

let selectedWorkshop = null;
let workshopTable = null;
let workshopDatas = [];
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// DASHBOARD SUMMARY | START
// **************************************************************

async function loadDashboard() {
  try {
    const response = await fetch(API.dashboard, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();

    if (result.status_code != 200) {
      swalError(result.message);
      return;
    }

    dashboardCard.totalWorkshop.textContent = result.data.total_workshop;

    dashboardCard.activeWorkshop.textContent = result.data.active_workshop;

    dashboardCard.inactiveWorkshop.textContent = result.data.inactive_workshop;

    dashboardCard.totalOwner.textContent = result.data.total_owner;
  } catch (error) {
    console.error(error);
    swalError("Failed to load dashboard summary.");
  }
}

// **************************************************************
// DASHBOARD SUMMARY | END
// **************************************************************

// **************************************************************
// READ WORKSHOP | START
// **************************************************************

async function loadWorkshop(status = "all") {
  try {
    const response = await fetch(`${API.view}?status=${status}`);

    const result = await response.json();

    if (result.status_code != 200) {
      return;
    }

    workshopDatas = result.data;

    renderWorkshopTable(workshopDatas);
  } catch (err) {
    console.error(err);
  }
}

// **************************************************************
// READ WORKSHOP | END
// **************************************************************

// **************************************************************
// RENDER TABLE | START
// **************************************************************

function renderWorkshopTable(datas) {
  tableBody.innerHTML = "";

  if (datas.length === 0) {
    tableBody.innerHTML = `
              <tr>
                  <td colspan="9" class="text-center">
                      No workshop available.
                  </td>
              </tr>
          `;

    return;
  }

  datas.forEach((data, index) => {
    tableBody.innerHTML += `
              <tr>
  
                  <td>
                      ${index + 1}
                  </td>
  
                  <td>
  
                        <img
                              src="${data.logo ? `/static/images/profiles/${data.logo}` : "/static/images/profiles/default-workshop.png"}"
                              class="workshop-logo">
  
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
  
                      ${generateStatusBadge(data.is_verified, data.workshop_status)}
  
                  </td>
  
                  <td>
  
                        <div>${data.created_at}</div>
        
                  </td>
  
                  <td class="text-center">
  
                      ${generateActionButton(data)}
  
                  </td>
  
              </tr>
          `;
  });
}

// **************************************************************
// RENDER TABLE | END
// **************************************************************

// **************************************************************
// STATUS BADGE | START
// **************************************************************

function generateStatusBadge(is_verified, is_active) {
  if (!Number(is_verified)) {
    return `
          <span class="badge rounded-pill bg-warning px-3 py-2">
              Pending Verification
          </span>
      `;
  }

  if (Number(is_active)) {
    return `
          <span class="badge rounded-pill bg-success px-3 py-2">
              Active
          </span>
      `;
  }

  return `
      <span class="badge rounded-pill bg-secondary px-3 py-2">
          Inactive
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
  let button = `
      <div class="action-group">
  `;

  // Belum diverifikasi
  if (!Number(data.is_verified)) {
    button += `
          <button
              class="btn btn-outline-success btn-sm"
              title="Verify Workshop"
              onclick="verifyWorkshop(${data.workshop_id})">

              <i class="bi bi-shield-check"></i>

          </button>
      `;
  }

  // Sudah diverifikasi tapi belum aktif
  else if (!Number(data.workshop_status)) {
    button += `
          <button
              class="btn btn-outline-primary btn-sm"
              title="Activate Workshop"
              onclick="activateWorkshop(${data.workshop_id})">

              <i class="bi bi-play-circle-fill"></i>

          </button>
      `;
  }

  // Sudah aktif
  else {
    button += `
          <button
              class="btn btn-outline-warning btn-sm"
              title="Deactivate Workshop"
              onclick="deactivateWorkshop(${data.workshop_id})">

              <i class="bi bi-pause-circle-fill"></i>

          </button>
      `;
  }

  // Tombol yang selalu ada
  button += `

      <button
          class="btn btn-outline-danger btn-sm"
          title="Delete Workshop"
          onclick="deleteWorkshop(${data.workshop_id})">

          <i class="bi bi-trash-fill"></i>

      </button>

      <button
          class="btn btn-outline-info btn-sm"
          title="Detail Workshop"
          onclick="detailWorkshop(${data.workshop_id})">

          <i class="bi bi-eye-fill"></i>

      </button>

  </div>
  `;

  return button;
}

// **************************************************************
// ACTION BUTTON | END
// **************************************************************

// **************************************************************
// VERIFY WORKSHOP | START
// **************************************************************

async function verifyWorkshop(workshop_id) {
  const confirm = await swalConfirm("Verify Workshop?", "This workshop will be activated.", "Verify");

  if (!confirm.isConfirmed) {
    return;
  }

  try {
    const response = await fetch(API.verify, {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        workshop_id: workshop_id,
      }),
    });

    const result = await response.json();

    if (result.status_code == 200) {
      await swalSuccess(result.message);
    } else {
      await swalError(result.message);
    }

    if (result.status_code == 200) {
      refreshAdministrator();
    }
  } catch (error) {
    console.error(error);
  }
}

// **************************************************************
// VERIFY WORKSHOP | END
// **************************************************************

// **************************************************************
// ACTIVATE WORKSHOP | START
// **************************************************************

async function activateWorkshop(workshop_id) {
  const confirm = await swalConfirm("Activate Workshop?", "", "Activate");

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

    if (result.status_code == 200) {
      await swalSuccess(result.message);
    } else {
      await swalError(result.message);
    }

    if (result.status_code == 200) {
      refreshAdministrator();
    }
  } catch (error) {
    console.error(error);
  }
}

// **************************************************************
// ACTIVATE WORKSHOP | END
// **************************************************************

// **************************************************************
// DEACTIVATE WORKSHOP | START
// **************************************************************

async function deactivateWorkshop(workshop_id) {
  const confirm = await swalConfirm("Deactivate Workshop?", "This workshop will be deactivated.", "Deactivate");

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

    if (result.status_code == 200) {
      await swalSuccess(result.message);
    } else {
      await swalError(result.message);
    }

    if (result.status_code == 200) {
      refreshAdministrator();
    }
  } catch (error) {
    console.error(error);

    swalError("Failed to deactivate workshop.");
  }
}

// **************************************************************
// DEACTIVATE WORKSHOP | END
// **************************************************************

// **************************************************************
// DETAIL WORKSHOP | START
// **************************************************************
async function detailWorkshop(workshopId) {
  try {
    const response = await fetch(`${API.detail}/${workshopId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();

    // alert(JSON.stringify(result));
    if (result.status_code != 200) {
      swalError(result.message);

      return;
    }

    const data = result.data;

    document.getElementById("detailWorkshopContent").innerHTML = `
          <div class="text-center mb-4">

              <img
                  src="${data.logo ? `/static/images/profiles/${data.logo}` : "/static/images/profiles/default.png"}"
                  class="detail-logo">

              <h4 class="mt-3">
                  ${data.workshop_name}
              </h4>

              ${generateStatusBadge(data.is_verified, data.workshop_status)}

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

    new bootstrap.Modal(document.getElementById("detailWorkshopModal")).show();
  } catch (error) {
    swalError(error.message);
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

    if (result.status_code == 200) {
      await swalSuccess(result.message);
    } else {
      await swalError(result.message);
    }

    if (result.status_code == 200) {
      refreshAdministrator();
    }
  } catch (error) {
    console.error(error);

    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Failed to delete workshop.",
    });
  }
}

// **************************************************************
// DELETE WORKSHOP | END
// **************************************************************

// **************************************************************
// REFRESH PAGE | START
// **************************************************************

async function refreshAdministrator() {
  await loadDashboard();
  const status = document.getElementById("filter_status").value;
  await loadWorkshop(status);
}

// **************************************************************
// REFRESH PAGE | END
// **************************************************************

// **************************************************************
// EVENT LISTENER | START
// **************************************************************
const filterStatus = document.getElementById("filter_status");

if (filterStatus) {
  filterStatus.addEventListener("change", async function () {
    await loadWorkshop(this.value);
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
      await refreshAdministrator();
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
  await refreshAdministrator();

  workshopTable = new simpleDatatables.DataTable("#administratorTable", {
    searchable: true,
    paging: true,
    perPage: 5,
    perPageSelect: [5, 10, 25, 50],
    fixedHeight: false,
  });
});

// **************************************************************
// PAGE INITIALIZATION | END
// **************************************************************
