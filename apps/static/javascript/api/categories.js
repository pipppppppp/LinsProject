// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);
async function init() {
  await reloadTable(loadCategories, renderTable);
}

// Form ID Setup
const form = {
  title: document.getElementById("modal_label"),
  id: document.getElementById("category_id"),
  name: document.getElementById("category_name"),
};
// **************************************************************
// BASE INISIALIZATION | END
// **************************************************************

// **************************************************************
// RENDER DATA TABLES | START
// **************************************************************
// Variable Setup -------------------------------------------------
let categoriesData = [];

// Get Data -------------------------------------------------
async function loadCategories() {
  const result = await getRequest("/category/view");
  categoriesData = result.data;
}

// Load Data -------------------------------------------------
function renderTable() {
  let html = "";

  categoriesData.forEach((category, index) => {
    html += `
            <tr>
                <td>${index + 1}</td>
                <td>${category.category_name}</td>
                <td>
                    <div class="action-buttons">
                      <button
                          class="btn btn-outline-warning btn-sm btn-action btn-edit"
                          data-bs-toggle="modal"
                          data-bs-target="#category_modal"
                          data-id="${category.category_id}"
                          title="Edit">
        
                          <i class="bi bi-pencil-fill"></i>
                      </button>
        
                      <button
                          class="btn btn-outline-danger btn-sm btn-action btn-delete"
                          data-id="${category.category_id}"
                          title="Hapus">
        
                          <i class="bi bi-trash-fill"></i>
                      </button>
                    </div>
                </td>
            </tr>
        `;
  });
  document.getElementById("category_table").innerHTML = html;
}
// **************************************************************
// RENDER DATA TABLES | END
// **************************************************************

// **************************************************************
// SAVE CATEGORY | START
// **************************************************************
async function saveCategory() {
  const category = {
    category_id: form.id.value,
    category_name: formatTitle(form.name.value),
  };

  // VALIDATION ==================================================
  if (!validateCategory(category)) return;

  let result;
  try {
    swalLoading();
    if (!category.category_id){
      result = await postRequest("/category/add", category);
    } else {
      result = await putRequest("/category/edit", category);
    }
  } finally {
    swalClose();
  }

  if (result.status_code === 201 || result.status_code === 200) {
    await swalSuccess(result.message);

    closeModal("category_modal");
    clearValue(form.id, form.name);

    form.title.textContent = "Tambah Kategori";

    await reloadTable(loadCategories, renderTable);
  } else {
    await swalError(result.message);
  }
}
document.querySelector(".btn-save").addEventListener("click", saveCategory);
// **************************************************************
// SAVE CATEGORY | END
// **************************************************************

// **************************************************************
// UPDATE & DELETE CATEGORY | START
// **************************************************************
document.getElementById("table1").addEventListener("click", handleTableClick);

async function handleTableClick(e) {
    const editBtn = e.target.closest(".btn-edit");
    const deleteBtn = e.target.closest(".btn-delete");

    if (editBtn) {
        const id = Number(editBtn.dataset.id);

        const category = categoriesData.find(
            item => item.category_id === id
        );

        if (!category) return;

        form.title.textContent = "Ubah Kategori";
        form.id.value = category.category_id;
        form.name.value = category.category_name;

        return;
    }

    if (deleteBtn) {
        const id = Number(deleteBtn.dataset.id);

        const confirmDelete = await swalDelete();

        if (!confirmDelete.isConfirmed) return;

        let result;

        try {
            swalLoading();

            result = await deleteRequest(
                "/category/delete",
                {
                    category_id: id
                }
            );
        } finally {
            swalClose();
        }

        if (result.status_code === 200 || result.status_code === 201) {
            await swalSuccess(result.message);

            await reloadTable(loadCategories, renderTable);
        } else {
            await swalError(result.message);
        }
    }
}
// **************************************************************
// UPDATE & DELETE CATEGORY | END
// **************************************************************

// **************************************************************
// RESET FORM | START
// **************************************************************
function resetForm() {
  form.title.textContent = "Tambah Kategori";

  clearValue(
      form.id,
      form.name
  );
}

document.getElementById("category_modal").addEventListener("hidden.bs.modal", resetForm);
// **************************************************************
// RESET FORM | END
// **************************************************************