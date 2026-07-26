// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  await reloadTable(loadSuppliers, renderTable);

  // Refresh button
  document.getElementById("btn_refresh")?.addEventListener("click", async () => {
    await reloadTable(loadSuppliers, renderTable);
  });
}

// Form ID Setup
const form = {
  title: document.getElementById("modal_label"),
  id: document.getElementById("supplier_id"),
  name: document.getElementById("supplier_name"),
  address: document.getElementById("supplier_address"),
  phone: document.getElementById("supplier_phone"),
};
// **************************************************************
// BASE INISIALIZATION | END
// **************************************************************

// **************************************************************
// GET SUPPLIER | START
// **************************************************************
// Variable Setup -------------------------------------------------
let suppliersData = [];

// Load Data -------------------------------------------------
async function loadSuppliers() {
  const result = await getRequest("/supplier/view");

  suppliersData = result.data;

  document.getElementById("supplier_count").textContent = `${suppliersData.length} Supplier`;

}
// **************************************************************
// GET SUPPLIER | END
// **************************************************************

// **************************************************************
// RENDER DATA | START
// **************************************************************
function renderTable() {
  let html = "";

  suppliersData.forEach((supplier, index) => {
    html += `
      <tr>
          <td>${index + 1}</td>

          <td>
              <div class="d-flex align-items-center">

                  <div class="avatar avatar-md bg-primary me-3">
                      <span class="avatar-content">
                          <i class="bi bi-building"></i>
                      </span>
                  </div>

                  <div>
                      <div class="fw-semibold">
                          ${supplier.name}
                      </div>

                      <small class="text-muted">
                          <i class="bi bi-telephone me-1"></i>
                          ${supplier.phone}
                      </small>
                  </div>

              </div>
          </td>

          <td>${supplier.address}</td>

          <td class="text-center">
              <div class="d-flex justify-content-center gap-2">

                  <button
                      class="btn btn-warning btn-sm btn-edit"
                      data-bs-toggle="modal"
                      data-bs-target="#supplier_modal"
                      data-id="${supplier.id}"
                      title="Ubah">

                      <i class="bi bi-pencil-fill"></i>

                  </button>

                  <button
                      class="btn btn-danger btn-sm btn-delete"
                      data-id="${supplier.id}"
                      title="Hapus">

                      <i class="bi bi-trash-fill"></i>

                  </button>

              </div>
          </td>
      </tr>
    `;
  });

  document.getElementById("supplier_table").innerHTML = html;
}
// **************************************************************
// RENDER DATA | END
// **************************************************************

// **************************************************************
// SAVE SUPPLIER | START
// **************************************************************
async function saveSupplier() {
  const supplier = {
    id: form.id.value,
    name: formatTitle(form.name.value),
    address: form.address.value.trim(),
    phone: formatPhone(form.phone.value),
  };

  // VALIDATION ==================================================
  if (!validateSupplier(supplier)) return;

  let result;

  try {
    swalLoading();

    if (!supplier.id) {
      result = await postRequest("/supplier/add", supplier);
    } else {
      result = await putRequest(`/supplier/edit/${supplier.id}`, supplier);
    }
  } finally {
    swalClose();
  }

  if (result.status_code === 201 || result.status_code === 200) {
    await swalSuccess(result.message);

    closeModal("supplier_modal");
    clearValue(form.id, form.name, form.address, form.phone);
    form.title.textContent = "Tambah Supplier";

    await reloadTable(loadSuppliers, renderTable);
  } else {
    await swalError(result.message);
  }
}

document.querySelector(".btn-save").addEventListener("click", saveSupplier);
// **************************************************************
// SAVE SUPPLIER | END
// **************************************************************

// **************************************************************
// UPDATE & DELETE SUPPLIER | START
// **************************************************************
document.getElementById("table1").addEventListener("click", handleTableClick);

async function handleTableClick(e) {
  const editBtn = e.target.closest(".btn-edit");
  const deleteBtn = e.target.closest(".btn-delete");

  if (editBtn) {
    const id = Number(editBtn.dataset.id);

    const supplier = suppliersData.find((item) => item.id === id);
    if (!supplier) return;

    form.title.textContent = "Ubah Supplier";
    form.id.value = supplier.id;
    form.name.value = supplier.name;
    form.address.value = supplier.address;
    form.phone.value = supplier.phone;

    return;
  }

  if (deleteBtn) {
    const id = Number(deleteBtn.dataset.id);

    const confirmDelete = await swalDelete();
    if (!confirmDelete.isConfirmed) return;

    let result;

    try {
      swalLoading();
      result = await deleteRequest(`/supplier/delete/${id}`);
    } finally {
      swalClose();
    }

    if (result.status_code === 200) {
      await swalSuccess(result.message);
      await reloadTable(loadSuppliers, renderTable);
    } else {
      await swalError(result.message);
    }
  }
}
// **************************************************************
// UPDATE & DELETE SUPPLIER | END
// **************************************************************

// **************************************************************
// RESET FORM | START
// **************************************************************
function resetForm() {
  form.title.textContent = "Tambah Supplier";

  clearValue(form.id, form.name, form.address, form.phone);
}
// **************************************************************
// RESET FORM | END
// **************************************************************

// **************************************************************
// MODAL EVENT | START
// **************************************************************
document.getElementById("supplier_modal").addEventListener("hidden.bs.modal", resetForm);
// **************************************************************
// MODAL EVENT | END
// **************************************************************
