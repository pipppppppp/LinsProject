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
   const response = await fetch("/category/view", {
      method: "GET",
      headers: {
         "Content-Type": "application/json",
      },
   });
   categoriesData = await response.json();
}

// Load Data -------------------------------------------------
function renderTable() {
   let html = "";

   categoriesData.forEach((category, index) => {
      html += `
            <tr>
                <td>${index + 1}</td>
                <td>${category.ctg_name}</td>
                <td>
                    <button
                        class="btn btn-warning btn-sm btn-edit" 
                        data-bs-toggle="modal" 
                        data-bs-target="#category_modal"
                        data-id="${category.ctg_id}"> Edit
                    </button>
                    <button
                        class="btn btn-danger btn-sm btn-delete"
                        data-id="${category.ctg_id}"> Hapus
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
   const category_id = form.id.value;
   const category = form.name.value;

   let response;
   if (!category_id) {
      response = await fetch("/category/add", {
         method: "POST",
         headers: {
            "Content-Type": "application/json",
         },
         body: JSON.stringify({
            category: category,
         }),
      });
   } else {
      response = await fetch(`/category/edit/${category_id}`, {
         method: "PUT",
         headers: {
            "Content-Type": "application/json",
         },
         body: JSON.stringify({
            category: category,
         }),
      });
   }

   const result = await response.json();
   if (result.status) {
      alert(result.message);
      location.reload();
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
      const category = categoriesData.find((p) => p.ctg_id === id);

      form.title.textContent = "Ubah Kategori";
      form.id.value = category.ctg_id;
      form.name.value = category.ctg_name;
   } else if (e.target.classList.contains("btn-delete")) {
      // proses delete
      if (!confirm("Yakin hapus data?")) {
         return;
      }

      const response = await fetch(`/category/delete/${id}`, {
         method: "DELETE",
      });

      const result = await response.json();

      if (result.status) {
         location.reload();
      } else {
         alert(result.message);
      }
   }
}
// **************************************************************
// UPDATE & DELETE CATEGORY | END
// **************************************************************
