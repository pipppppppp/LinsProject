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
  // console.log(categoriesData);
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

  if (result.status_code === 200) {
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
    
    const result = await deleteRequest("/category/delete", {category_id: id,});
    console.log(result)
    swalClose();

    if (result.status_code === 200) {
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