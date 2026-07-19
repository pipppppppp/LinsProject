// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);
async function init() {
  await loadCustomers();
  renderTable();
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
// GET SPPLIER | START
// **************************************************************
// Variable Setup -------------------------------------------------
let customersData = [];

// Load Data -------------------------------------------------
async function loadCustomers() {
  customersData = await getRequest("/customer/view");
}
// **************************************************************
// GET CUSTOMER | END
// **************************************************************

// **************************************************************
// RENDER DATA | START
// **************************************************************
function renderTable() {
  let html = "";

  customersData.forEach((customer, index) => {
    html += `
            <tr>
                <td>${index + 1}</td>
                <td>${customer.customer_name}</td>
                <td>${customer.customer_address}</td>
                <td>${customer.customer_phone}</td>
                <td>
                    <button
                        class="btn btn-warning btn-sm btn-edit"
                        data-bs-toggle="modal"
                        data-bs-target="#customer_modal"
                        data-id="${customer.customer_id}">
                        Edit
                    </button>

                    <button
                        class="btn btn-danger btn-sm btn-delete"
                        data-id="${customer.customer_id}">
                        Hapus
                    </button>
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
    customer_id: form.id.value,
    customer_name: formatTitle(form.name.value),
    customer_address: form.address.value.trim(),
    customer_phone: formatPhone(form.phone.value),
  };

  // VALIDATION ==================================================
  if (!validateCustomer(customer)) return;

  swalLoading();

  let result;

  try {
    swalLoading();

    if (!customer.customer_id) {
      result = await postRequest("/customer/add", customer);
    } else {
      result = await putRequest(`/customer/edit/${customer.customer_id}`, customer);
    }
  } finally {
    swalClose();
  }

  if (result.status) {
    await swalSuccess(result.message);

    closeModal("customer_modal");
    clearValue(form.id, form.name, form.address, form.phone);
    await reloadTable(loadCustomers, renderTable);
  } else {
    await swalError(result.message);
  }
}
document.querySelector(".btn-save").addEventListener("click", saveCustomer);
// **************************************************************
// SAVE PRODUCT | END
// **************************************************************

// **************************************************************
// UPDATE & DELETE CUSTOMER | START
// **************************************************************
document.getElementById("customer_table").addEventListener("click", handleTableClick);
async function handleTableClick(e) {
  const id = Number(e.target.dataset.id);
  if (e.target.classList.contains("btn-edit")) {
    // proses edit
    const customer = customersData.find((s) => s.customer_id === id);

    form.title.textContent = "Ubah Customer";
    form.id.value = customer.customer_id;
    form.name.value = customer.customer_name;
    form.address.value = customer.customer_address;
    form.phone.value = customer.customer_phone;
  } else if (e.target.classList.contains("btn-delete")) {
    // proses delete
    const confirmDelete = await swalDelete();
    if (!confirmDelete.isConfirmed) {
      return;
    }
    swalLoading();
    const result = await deleteRequest(`/customer/delete/${id}`);
    swalClose();

    if (result.status) {
      await swalSuccess(result.message);

      await reloadTable(loadCustomers, renderTable);
    } else {
      await swalError(result.message);
    }
  }
}
// **************************************************************
// UPDATE & DELETE CUSTOMER | END
// **************************************************************
