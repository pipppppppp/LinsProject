// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  await reloadTable(loadServices, renderTable);
}

// Form ID Setup
const form = {
  title: document.getElementById("modal_label"),
  id: document.getElementById("service_id"),
  name: document.getElementById("service_name"),
  fee: document.getElementById("service_fee"),
  description: document.getElementById("service_description"),
};
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************


// **************************************************************
// GET SERVICE | START
// **************************************************************
let servicesData = [];

async function loadServices() {
  const result = await getRequest("/service/view");

  servicesData = result.data;
}
// **************************************************************
// GET SERVICE | END
// **************************************************************


// **************************************************************
// RENDER DATA | START
// **************************************************************
function renderTable() {
  let html = "";

  servicesData.forEach((service, index) => {
    html += `
      <tr>
        <td>${index + 1}</td>
        <td>${service.name}</td>
        <td>${formatRupiah(service.service_fee)}</td>
        <td>${service.description ?? "-"}</td>
        <td>
          <div class="action-buttons">

            <button
              class="btn btn-outline-warning btn-sm btn-action btn-edit"
              data-bs-toggle="modal"
              data-bs-target="#service_modal"
              data-id="${service.id}"
              title="Edit">

              <i class="bi bi-pencil-fill"></i>
            </button>

            <button
              class="btn btn-outline-danger btn-sm btn-action btn-delete"
              data-id="${service.id}"
              title="Hapus">

              <i class="bi bi-trash-fill"></i>
            </button>

          </div>
        </td>
      </tr>
    `;
  });

  document.getElementById("service_table").innerHTML = html;
}
// **************************************************************
// RENDER DATA | END
// **************************************************************


// **************************************************************
// SAVE SERVICE | START
// **************************************************************
async function saveService() {

  const service = {
    id: form.id.value,
    name: formatTitle(form.name.value),
    service_fee: removeThousands(form.fee.value),
    description: form.description.value.trim(),
  };

  // VALIDATION ==================================================
  if (!validateService(service)) return;

  let result;

  try {
    swalLoading();

    if (!service.id) {
      result = await postRequest("/service/add", service);
    } else {
      result = await putRequest(`/service/edit/${service.id}`, service);
    }
  } finally {
    swalClose();
  }

  if (result.status_code === 201 || result.status_code === 200) {

    await swalSuccess(result.message);

    closeModal("service_modal");

    clearValue(
      form.id,
      form.name,
      form.fee,
      form.description
    );

    form.title.textContent = "Tambah Jasa";

    await reloadTable(loadServices, renderTable);

  } else {

    await swalError(result.message);

  }

}

document.querySelector(".btn-save").addEventListener("click", saveService);
// **************************************************************
// SAVE SERVICE | END
// **************************************************************


// **************************************************************
// UPDATE & DELETE SERVICE | START
// **************************************************************
document.getElementById("table1").addEventListener("click", handleTableClick);

async function handleTableClick(e) {

  const editBtn = e.target.closest(".btn-edit");
  const deleteBtn = e.target.closest(".btn-delete");

  if (editBtn) {

    const id = Number(editBtn.dataset.id);

    const service = servicesData.find(item => item.id === id);

    if (!service) return;

    form.title.textContent = "Ubah Jasa";

    form.id.value = service.id;
    form.name.value = service.name;
    form.fee.value = formatNumber(service.service_fee);
    form.description.value = service.description ?? "";

    return;
  }

  if (deleteBtn) {

    const id = Number(deleteBtn.dataset.id);

    const confirmDelete = await swalDelete();

    if (!confirmDelete.isConfirmed) return;

    let result;

    try {

      swalLoading();

      result = await deleteRequest(`/service/delete/${id}`);

    } finally {

      swalClose();

    }

    if (result.status_code === 200) {

      await swalSuccess(result.message);

      await reloadTable(loadServices, renderTable);

    } else {

      await swalError(result.message);

    }

  }

}
// **************************************************************
// UPDATE & DELETE SERVICE | END
// **************************************************************


// **************************************************************
// RESET FORM | START
// **************************************************************
function resetForm() {

  form.title.textContent = "Tambah Jasa";

  clearValue(
    form.id,
    form.name,
    form.fee,
    form.description
  );

}
// **************************************************************
// RESET FORM | END
// **************************************************************


// **************************************************************
// FORMAT INPUT | START
// **************************************************************
formatThousands(form.fee);
// **************************************************************
// FORMAT INPUT | END
// **************************************************************


// **************************************************************
// MODAL EVENT | START
// **************************************************************
document
  .getElementById("service_modal")
  .addEventListener("hidden.bs.modal", resetForm);
// **************************************************************
// MODAL EVENT | END
// **************************************************************