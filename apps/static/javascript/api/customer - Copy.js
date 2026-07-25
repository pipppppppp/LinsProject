// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);
async function init() {
  await reloadTable(loadCustomers, renderTable);
}

// Form ID Setup
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
// Variable Setup -------------------------------------------------
let customersData = [];

// Load Data -------------------------------------------------
async function loadCustomers() {
  const result = await getRequest("/customer/view");

  customersData = result.data;
}
// **************************************************************
// GET CUSTOMER | END
// **************************************************************

// **************************************************************
// RENDER DATA | START
// **************************************************************
function renderTable() {
  let html = "";

  // true jika halaman kasir
  const isCashier = window.location.pathname.startsWith("/cashier");

  customersData.forEach((customer, index) => {
    let action = `
      <button
          class="btn btn-outline-info btn-sm btn-action btn-vehicle"
          data-id="${customer.id}"
          title="Data Kendaraan">

          <i class="bi bi-bicycle"></i>
      </button>
    `;

    if (!isCashier) {
      action = `
        <button
            class="btn btn-outline-warning btn-sm btn-action btn-edit"
            data-bs-toggle="modal"
            data-bs-target="#customer_modal"
            data-id="${customer.id}"
            title="Edit">
            <i class="bi bi-pencil-fill"></i>
        </button>

        <button
            class="btn btn-outline-danger btn-sm btn-action btn-delete"
            data-id="${customer.id}"
            title="Hapus">
            <i class="bi bi-trash-fill"></i>
        </button>

        ${action}
      `;
    }

    html += `
      <tr>
        <td>${index + 1}</td>
        <td>${customer.customer_name}</td>
        <td>${customer.customer_address}</td>
        <td>${customer.customer_phone}</td>
        <td>
          <div class="action-buttons">
            ${action}
          </div>
        </td>
      </tr>
    `;
  });

  document.getElementById("customer_table").innerHTML = html;
}
// **************************************************************
// RENDER DATA | END
// **************************************************************

// **************************************************************
// SAVE CUSTOMER | START
// **************************************************************
async function saveCustomer() {
  const customer = {
    id: form.id.value,
    customer_name: formatTitle(form.name.value),
    customer_address: form.address.value.trim(),
    customer_phone: formatPhone(form.phone.value),
  };

  // VALIDATION ==================================================
  if (!validateCustomer(customer)) return;

  let result;

  try {
    swalLoading();

    if (!customer.id) {
      result = await postRequest("/customer/add", customer);
    } else {
      result = await putRequest(`/customer/edit/${customer.id}`, customer);
    }
  } finally {
    swalClose();
  }

  if (result.status_code === 201 || result.status_code === 200) {
    await swalSuccess(result.message);

    closeModal("customer_modal");
    clearValue(form.id, form.name, form.address, form.phone);
    form.title.textContent = "Tambah Pelanggan";

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
// SAVE PRODUCT | END
// **************************************************************

// **************************************************************
// UPDATE & DELETE CUSTOMER | START
// **************************************************************
document.getElementById("table1").addEventListener("click", handleTableClick);
async function handleTableClick(e) {
  const editBtn = e.target.closest(".btn-edit");
  const deleteBtn = e.target.closest(".btn-delete");
  const vehicleBtn = e.target.closest(".btn-vehicle");

  if (editBtn) {
    const id = Number(editBtn.dataset.id);

    const customer = customersData.find((item) => item.id === id);
    if (!customer) return;

    form.title.textContent = "Ubah Pelanggan";
    form.id.value = customer.id;
    form.name.value = customer.customer_name;
    form.address.value = customer.customer_address;
    form.phone.value = customer.customer_phone;
    return;
  }

  if (deleteBtn) {
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

    if (result.status_code === 200) {
      await swalSuccess(result.message);
      await reloadTable(loadCustomers, renderTable);
    } else {
      await swalError(result.message);
    }
  }

  if (vehicleBtn) {
    const id = Number(vehicleBtn.dataset.id);

    window.location.href = `/vehicle/${id}`;
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
  form.title.textContent = "Tambah Pelanggan";

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
