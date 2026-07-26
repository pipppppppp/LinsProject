// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);
async function init() {
  await reloadTable(loadVehicles, renderTable);
  // Refresh button
  document.getElementById("btn_refresh")?.addEventListener("click", async () => {
    await reloadTable(loadVehicles, renderTable);
  });
}

// Form ID Setup
const form = {
  title: document.getElementById("modal_label"),
  id: document.getElementById("vehicle_id"),
  customer_id: document.getElementById("customer_id"),
  plate_number: document.getElementById("plate_number"),
  vehicle_brand: document.getElementById("vehicle_brand"),
  vehicle_type: document.getElementById("vehicle_type"),
  vehicle_year: document.getElementById("vehicle_year"),
  vehicle_color: document.getElementById("vehicle_color"),
};
// **************************************************************
// BASE INISIALIZATION | END
// **************************************************************

// **************************************************************
// GET CUSTOMER | START
// **************************************************************
// Variable Setup -------------------------------------------------
let vehiclesData = [];

// Load Data -------------------------------------------------
async function loadVehicles() {
  const customerId = form.customer_id.value;

  const result = await getRequest(`/vehicle/view/${customerId}`);
  console.log(result);

  if (!result) {
    vehiclesData = [];
    return;
  }

  const customer = result.data.customer;

  document.getElementById("customer_name").textContent = customer.customer_name;

  // Avatar Inisial
  const initial = customer.customer_name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((word) => word.charAt(0).toUpperCase())
    .join("");

  document.getElementById("customer_initial").textContent = initial;
  
  document.getElementById("customer_phone").textContent = customer.customer_phone;

  document.getElementById("customer_address").textContent = customer.customer_address;

  vehiclesData = result.data.vehicles ?? [];
  document.getElementById("vehicle_count").textContent = `${vehiclesData.length} Kendaraan`;
}
// **************************************************************
// GET CUSTOMER | END
// **************************************************************

// **************************************************************
// RENDER DATA | START
// **************************************************************
function renderTable() {
  let html = "";

  vehiclesData.forEach((vehicle, index) => {
    html += `
      <tr>
          <td>${index + 1}</td>
          <td>${vehicle.plate_number}</td>
          <td>${vehicle.vehicle_brand}</td>
          <td>${vehicle.vehicle_type}</td>
          <td>${vehicle.vehicle_year}</td>
          <td>${vehicle.vehicle_color}</td>
          <td class="text-center">
              <div class="d-flex justify-content-center gap-2">
                  <button
                      class="btn btn-warning btn-sm btn-edit"
                      data-bs-toggle="modal"
                      data-bs-target="#vehicle_modal"
                      data-id="${vehicle.id}"
                      title="Ubah">
                      <i class="bi bi-pencil-fill"></i>
                  </button>
      
                  <button
                      class="btn btn-danger btn-sm btn-delete"
                      data-id="${vehicle.id}"
                      title="Hapus">
                      <i class="bi bi-trash-fill"></i>
                  </button>
      
              </div>
          </td>
      </tr>
      `;
  });

  document.getElementById("vehicle_table").innerHTML = html;
}
// **************************************************************
// RENDER DATA | END
// **************************************************************

// **************************************************************
// SAVE CUSTOMER | START
// **************************************************************
async function saveVehicle() {
  const vehicle = {
    id: form.id.value,
    customer_id: form.customer_id.value,
    plate_number: form.plate_number.value.trim().toUpperCase(),
    vehicle_brand: formatTitle(form.vehicle_brand.value),
    vehicle_type: formatTitle(form.vehicle_type.value),
    vehicle_year: form.vehicle_year.value,
    vehicle_color: formatTitle(form.vehicle_color.value),
  };

  // VALIDATION ==================================================
  if (!validateVehicle(vehicle)) return;

  let result;

  try {
    swalLoading();

    if (!vehicle.id) {
      result = await postRequest("/vehicle/add", vehicle);
    } else {
      result = await putRequest(`/vehicle/edit/${vehicle.id}`, vehicle);
    }
  } finally {
    swalClose();
  }

  if (result.status_code === 201 || result.status_code === 200) {
    await swalSuccess(result.message);

    closeModal("vehicle_modal");
    clearValue(form.id, form.plate_number, form.vehicle_brand, form.vehicle_type, form.vehicle_year, form.vehicle_color);
    form.title.textContent = "Tambah Kendaraan";

    await reloadTable(loadVehicles, renderTable);
  } else {
    await swalError(result.message);
  }
}
document.querySelector(".btn-save").addEventListener("click", saveVehicle);
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

  if (editBtn) {
    const id = editBtn.dataset.id;

    const vehicle = vehiclesData.find((item) => item.id == id);
    if (!vehicle) return;

    form.title.textContent = "Ubah Data Kendaraan";
    form.id.value = vehicle.id;
    form.customer_id.value = vehicle.customer_id;
    form.plate_number.value = vehicle.plate_number;
    form.vehicle_brand.value = vehicle.vehicle_brand;
    form.vehicle_type.value = vehicle.vehicle_type;
    form.vehicle_year.value = vehicle.vehicle_year;
    form.vehicle_color.value = vehicle.vehicle_color;
    return;
  }

  if (deleteBtn) {
    const id = Number(deleteBtn.dataset.id);

    const confirmDelete = await swalDelete();
    if (!confirmDelete.isConfirmed) return;

    let result;

    try {
      swalLoading();
      result = await deleteRequest(`/vehicle/delete/${id}`);
    } finally {
      swalClose();
    }

    if (result.status_code === 200) {
      await swalSuccess(result.message);
      await reloadTable(loadVehicles, renderTable);
    } else {
      await swalError(result.message);
    }
  }
}
// **************************************************************
// UPDATE & DELETE CUSTOMER | END
// **************************************************************

// **************************************************************
// RESET FORM | START
// **************************************************************
function resetForm() {
  form.title.textContent = "Tambah Kendaraan";

  clearValue(form.id, form.plate_number, form.vehicle_brand, form.vehicle_type, form.vehicle_year, form.vehicle_color);
}
// **************************************************************
// RESET FORM | END
// **************************************************************

// **************************************************************
// MODAL EVENT | START
// **************************************************************
document.getElementById("vehicle_modal").addEventListener("hidden.bs.modal", resetForm);
// **************************************************************
// MODAL EVENT | END
// **************************************************************
