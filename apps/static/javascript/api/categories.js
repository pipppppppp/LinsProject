// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);
async function init() {
  await loadCategories();
  renderTable();
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
  categoriesData = await getRequest("/category/view");
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
                    <button
                        class="btn btn-warning btn-sm btn-edit" 
                        data-bs-toggle="modal" 
                        data-bs-target="#category_modal"
                        data-id="${category.category_id}"> Edit
                    </button>
                    <button
                        class="btn btn-danger btn-sm btn-delete"
                        data-id="${category.category_id}"> Hapus
                    </button>
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

  swalLoading();

  let result;
  try {
    if (!category.category_id) {
      result = await postRequest("/category/add", category);
    } else {
      result = await putRequest(`/category/edit/${category.category_id}`, category);
    }
  } finally {
    swalClose();
  }

  if (result.status) {
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
document.getElementById("category_table").addEventListener("click", handleTableClick);
async function handleTableClick(e) {
  const id = Number(e.target.dataset.id);
  if (e.target.classList.contains("btn-edit")) {
    // proses edit
    const category = categoriesData.find((c) => c.category_id === id);

    form.title.textContent = "Ubah Kategori";
    form.id.value = category.category_id;
    form.name.value = category.category_name;
  } else if (e.target.classList.contains("btn-delete")) {
    // proses delete
    const confirmDelete = await swalDelete();

    if (!confirmDelete.isConfirmed) {
      return;
    }
    swalLoading();
    const result = await deleteRequest(`/category/delete/${id}`);

    swalClose();

    if (result.status) {
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
