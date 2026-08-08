// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  await reloadTable(loadCustomers, renderTable);

  // Refresh Button ----------------------------------------------
  document.getElementById("btn_refresh")?.addEventListener("click", async () => {
    await reloadTable(loadCustomers, renderTable);
  });
}

// Page Role Setup -----------------------------------------------
const isCashierPage = window.location.pathname.startsWith("/cashier");

// Form ID Setup -------------------------------------------------
const form = {
  title: document.getElementById("modal_label"),
  id: document.getElementById("customer_id"),
  name: document.getElementById("customer_name"),
  address: document.getElementById("customer_address"),
  phone: document.getElementById("customer_phone"),
};
// **************************************************************
// BASE INISIALIZATION | END
// **************************************************************

// **************************************************************
// GET CUSTOMER | START
// **************************************************************
// Variable Setup ------------------------------------------------
let customersData = [];

// Load Data -----------------------------------------------------
async function loadCustomers() {
  const result = await getRequest("/customer/view");

  if (!result) return;

  if (result.status_code !== 200) {
    customersData = [];

    await swalError(result.message);

    return;
  }

  customersData = result.data.customer || [];

  renderSummary(result.data);
}
// **************************************************************
// GET CUSTOMER | END
// **************************************************************

// **************************************************************
// RENDER SUMMARY | START
// **************************************************************
function renderSummary(data) {
  const totalCustomer = document.getElementById("total_customer");
  const totalVehicle = document.getElementById("total_vehicle");
  const customerCount = document.getElementById("customer_count");

  if (totalCustomer) {
    totalCustomer.textContent = data.total_customer || 0;
  }

  if (totalVehicle) {
    totalVehicle.textContent = data.total_vehicle || 0;
  }

  if (customerCount) {
    customerCount.textContent = `${data.total_customer || 0} Pelanggan`;
  }
}
// **************************************************************
// RENDER SUMMARY | END
// **************************************************************

// **************************************************************
// RENDER DATA | START
// **************************************************************
function renderTable() {
  let html = "";

  customersData.forEach((customer, index) => {
    const customerName = customer.customer_name || "-";
    const totalVehicle = Number(customer.total_vehicle || 0);

    const customerInitial = customerName
      .split(" ")
      .filter(Boolean)
      .map((name) => name[0])
      .join("")
      .substring(0, 2)
      .toUpperCase();

    // Kasir hanya mendapatkan tombol kendaraan.
    let action = `
      <button
        type="button"
        class="btn btn-primary btn-sm btn-vehicle"
        style="width: 34px; height: 34px"
        data-id="${customer.id}"
        title="Data Kendaraan"
      >
        <i class="bi bi-bicycle fs-6"></i>
      </button>
    `;

    // Owner dapat edit, hapus, dan melihat kendaraan.
    if (!isCashierPage) {
      action = `
        <button
          type="button"
          class="btn btn-warning btn-sm btn-edit"
          style="width: 34px; height: 34px"
          data-bs-toggle="modal"
          data-bs-target="#customer_modal"
          data-id="${customer.id}"
          title="Edit Pelanggan"
        >
          <i class="bi bi-pencil-square"></i>
        </button>

        <button
          type="button"
          class="btn btn-danger btn-sm btn-delete"
          style="width: 34px; height: 34px"
          data-id="${customer.id}"
          title="Hapus Pelanggan"
        >
          <i class="bi bi-trash"></i>
        </button>

        <button
          type="button"
          class="btn btn-primary btn-sm btn-vehicle"
          style="width: 34px; height: 34px"
          data-id="${customer.id}"
          title="Data Kendaraan"
        >
          <i class="bi bi-bicycle fs-6"></i>
        </button>
      `;
    }

    html += `
      <tr>
        <td class="text-center fw-bold">
          ${index + 1}
        </td>

        <td>
          <div class="d-flex align-items-center">
            <div class="avatar avatar-md bg-primary me-3">
              <span class="avatar-content">
                ${customerInitial}
              </span>
            </div>

            <div>
              <h6 class="mb-0">
                ${customerName}
              </h6>

              <small class="text-muted">
                ${customer.customer_address || "-"}
              </small>
            </div>
          </div>
        </td>

        <td>
          <div>
            <i class="bi bi-telephone-fill me-1"></i>

            ${customer.customer_phone || "-"}
          </div>
        </td>

        <td class="text-center">
          <span
            class="badge ${totalVehicle > 0 ? "bg-light-primary text-primary" : "bg-light-secondary text-secondary"}"
          >
            ${totalVehicle} Unit
          </span>
        </td>

        <td class="text-center">
          <div class="d-flex justify-content-center align-items-center gap-1">
            ${action}
          </div>
        </td>
      </tr>
    `;
  });

  const customerTable = document.getElementById("customer_table");

  if (!customerTable) return;

  customerTable.innerHTML = html;
}
// **************************************************************
// RENDER DATA | END
// **************************************************************

// **************************************************************
// SAVE CUSTOMER | START
// **************************************************************
async function saveCustomer() {
  if (!form.id || !form.name || !form.address || !form.phone) {
    await swalError("Form pelanggan tidak ditemukan.");

    return;
  }

  const customer = {
    id: form.id.value,
    customer_name: formatTitle(form.name.value),
    customer_address: form.address.value.trim(),
    customer_phone: formatPhone(form.phone.value),
  };

  // Validation --------------------------------------------------
  if (!validateCustomer(customer)) return;

  let result;

  try {
    swalLoading();

    // Kasir selalu menambahkan customer baru.
    if (isCashierPage) {
      result = await postRequest("/customer/add", customer);
    } else if (!customer.id) {
      result = await postRequest("/customer/add", customer);
    } else {
      result = await putRequest(`/customer/edit/${customer.id}`, customer);
    }
  } finally {
    swalClose();
  }

  if (!result) return;

  if (result.status_code === 201 || result.status_code === 200) {
    await swalSuccess(result.message);

    closeModal("customer_modal");

    clearValue(form.id, form.name, form.address, form.phone);

    if (form.title) {
      form.title.textContent = "Tambah Pelanggan";
    }

    await reloadTable(loadCustomers, renderTable);
  } else {
    await swalError(result.message);
  }
}

const btnSave = document.querySelector(".btn-save");

if (btnSave) {
  btnSave.addEventListener("click", saveCustomer);
}
// **************************************************************
// SAVE CUSTOMER | END
// **************************************************************

// **************************************************************
// UPDATE & DELETE CUSTOMER | START
// **************************************************************
const table = document.getElementById("table1");

if (table) {
  table.addEventListener("click", handleTableClick);
}

async function handleTableClick(event) {
  const editBtn = event.target.closest(".btn-edit");
  const deleteBtn = event.target.closest(".btn-delete");
  const vehicleBtn = event.target.closest(".btn-vehicle");

  // Edit Customer -----------------------------------------------
  if (editBtn && !isCashierPage) {
    const id = Number(editBtn.dataset.id);

    const customer = customersData.find((item) => Number(item.id) === id);

    if (!customer) return;

    if (form.title) {
      form.title.textContent = "Ubah Pelanggan";
    }

    form.id.value = customer.id;
    form.name.value = customer.customer_name || "";
    form.address.value = customer.customer_address || "";
    form.phone.value = customer.customer_phone || "";

    return;
  }

  // Delete Customer ---------------------------------------------
  if (deleteBtn && !isCashierPage) {
    const id = Number(deleteBtn.dataset.id);

    const confirmDelete = await swalDelete();

    if (!confirmDelete.isConfirmed) return;

    let result;

    try {
      swalLoading();

      result = await deleteRequest(`/customer/delete/${id}`);
    } finally {
      swalClose();
    }

    if (!result) return;

    if (result.status_code === 200) {
      await swalSuccess(result.message);

      await reloadTable(loadCustomers, renderTable);
    } else {
      await swalError(result.message);
    }

    return;
  }

  // Customer Vehicle --------------------------------------------
  if (vehicleBtn) {
    const id = Number(vehicleBtn.dataset.id);

    const isCashier = window.location.pathname.startsWith("/cashier");

    if (isCashier) {
      window.location.href = `/cashier/customer/vehicle/${id}`;
    } else {
      window.location.href = `/vehicle/${id}`;
    }

    return;
  }
}
// **************************************************************
// UPDATE & DELETE CUSTOMER | END
// **************************************************************

// **************************************************************
// RESET FORM | START
// **************************************************************
function resetForm() {
  if (form.title) {
    form.title.textContent = "Tambah Pelanggan";
  }

  if (!form.id || !form.name || !form.address || !form.phone) {
    return;
  }

  clearValue(form.id, form.name, form.address, form.phone);
}
// **************************************************************
// RESET FORM | END
// **************************************************************

// **************************************************************
// MODAL EVENT | START
// **************************************************************
const modal = document.getElementById("customer_modal");

if (modal) {
  modal.addEventListener("hidden.bs.modal", resetForm);
}
// **************************************************************
// MODAL EVENT | END
// **************************************************************
