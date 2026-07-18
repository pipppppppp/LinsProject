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
      Swal.fire({
        icon: "error",
        title: result.error,
        text: result.message,
      });

      return;
    }

    dashboardCard.totalWorkshop.textContent = result.data.total_workshop;

    dashboardCard.activeWorkshop.textContent = result.data.active_workshop;

    dashboardCard.inactiveWorkshop.textContent = result.data.inactive_workshop;

    dashboardCard.totalOwner.textContent = result.data.total_owner;
  } catch (error) {
    console.error(error);

    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Failed to load dashboard summary.",
    });
  }
}

// **************************************************************
// DASHBOARD SUMMARY | END
// **************************************************************

// **************************************************************
// READ WORKSHOP | START
// **************************************************************

async function loadWorkshop() {
  try {
    const response = await fetch(API.view, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();

    if (result.status_code != 200) {
      Swal.fire({
        icon: "error",
        title: result.error,
        text: result.message,
      });

      return;
    }

    renderWorkshopTable(result.data);
  } catch (error) {
    console.error(error);

    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Failed to load workshop data.",
    });
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
                              src="${data.logo ? `/static/images/profiles/${data.logo}` : "/static/images/profiles/default.png"}"
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
  
                      ${generateStatusBadge(data.workshop_status)}
  
                  </td>
  
                  <td>
  
                        <div>${data.created_at.date}</div>

                        <small class="text-muted">
                            ${data.created_at.time}
                        </small>
        
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

function generateStatusBadge(status) {
  return Number(status) === 1
    ? `<span class="badge rounded-pill bg-success px-3 py-2">Active</span>`
    : `<span class="badge rounded-pill bg-danger px-3 py-2">Inactive</span>`;
}

// **************************************************************
// STATUS BADGE | END
// **************************************************************

// **************************************************************
// ACTION BUTTON | START
// **************************************************************

function generateActionButton(data) {
  let button = "";

  if (parseInt(data.workshop_status) === 0) {
    button += `
            <div class="action-group">

                <button
                    class="btn btn-outline-success btn-sm"
                    title="Verify Workshop"
                    onclick="verifyWorkshop(${data.workshop_id})">

                    <i class="bi bi-patch-check-fill"></i>

                </button>

                <button
                    class="btn btn-outline-primary btn-sm"
                    title="Activate Workshop"
                    onclick="activateWorkshop(${data.workshop_id})">

                    <i class="bi bi-check-circle-fill"></i>

                </button>

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
  } else {
    button += `
            <div class="d-flex justify-content-center align-items-center gap-2">

                <button
                    class="btn btn-outline-warning btn-sm"
                    title="Deactivate Workshop"
                    onclick="deactivateWorkshop(${data.workshop_id})">

                    <i class="bi bi-slash-circle-fill"></i>

                </button>

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
  }

  return button;
}

// **************************************************************
// ACTION BUTTON | END
// **************************************************************

// **************************************************************
// VERIFY WORKSHOP | START
// **************************************************************

async function verifyWorkshop(workshop_id) {
  const confirm = await Swal.fire({
    title: "Verify Workshop?",
    text: "This workshop will be activated.",
    icon: "question",

    showCancelButton: true,

    confirmButtonText: "Verify",
    cancelButtonText: "Cancel",
  });

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

    Swal.fire({
      icon: result.status_code == 200 ? "success" : "error",
      title: result.error,
      text: result.message,
    });

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
  const confirm = await Swal.fire({
    title: "Activate Workshop?",
    icon: "question",

    showCancelButton: true,

    confirmButtonText: "Activate",
  });

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

    Swal.fire({
      icon: result.status_code == 200 ? "success" : "error",
      title: result.error,
      text: result.message,
    });

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
  const confirm = await Swal.fire({
    title: "Deactivate Workshop?",
    text: "This workshop will be deactivated.",
    icon: "warning",

    showCancelButton: true,

    confirmButtonText: "Deactivate",
    cancelButtonText: "Cancel",
  });

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

    Swal.fire({
      icon: result.status_code == 200 ? "success" : "error",
      title: result.error,
      text: result.message,
    });

    if (result.status_code == 200) {
      refreshAdministrator();
    }
  } catch (error) {
    console.error(error);

    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Failed to deactivate workshop.",
    });
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

          Swal.fire({
              icon: "error",
              title: result.error,
              text: result.message,
          });

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
                  <td>${data.created_at.date_time}</td>
              </tr>

          </table>
      `;

      new bootstrap.Modal(
          document.getElementById("detailWorkshopModal")
      ).show();

  } catch (error) {

      Swal.fire({
          icon: "error",
          title: "Error",
          text: error.message,
      });

  }

}
// **************************************************************
// DETAIL WORKSHOP | END
// **************************************************************

// **************************************************************
// DELETE WORKSHOP | START
// **************************************************************

async function deleteWorkshop(workshop_id) {
  const confirm = await Swal.fire({
    title: "Delete Workshop?",
    text: "Deleted data cannot be restored.",
    icon: "warning",

    showCancelButton: true,

    confirmButtonText: "Delete",
    cancelButtonText: "Cancel",

    confirmButtonColor: "#dc3545",
  });

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

    Swal.fire({
      icon: result.status_code == 200 ? "success" : "error",
      title: result.error,
      text: result.message,
    });

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

  await loadWorkshop();
}

// **************************************************************
// REFRESH PAGE | END
// **************************************************************

// **************************************************************
// EVENT LISTENER | START
// **************************************************************

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
// EVENT LISTENER | END
// **************************************************************

// **************************************************************
// PAGE INITIALIZATION | START
// **************************************************************

document.addEventListener("DOMContentLoaded", async function () {
  await refreshAdministrator();
});

// **************************************************************
// PAGE INITIALIZATION | END
// **************************************************************
