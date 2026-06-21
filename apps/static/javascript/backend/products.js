// **************************************************************
// RENDERING DOCUMENT | START 
// **************************************************************
document.addEventListener("DOMContentLoaded", init);
async function init() {
   await loadCategories();

   await loadProducts();

   renderTable();
}
// **************************************************************
// RENDERING DOCUMENT | END 
// **************************************************************


// **************************************************************
// GET PRODUCT | START 
// **************************************************************
// Initialization -------------------------------------------------
let productsData = [];
let categoriesData = [];
const form = {
   title: document.getElementById("modal_label"),
   id: document.getElementById("product_id"),
   name: document.getElementById("product_name"),
   category: document.getElementById("product_category"),
};

// Load Data -------------------------------------------------
async function loadProducts() {
   const response = await fetch("/product/view");
   productsData = await response.json();
}

async function loadCategories() {
   const response = await fetch("/category/view");
   categoriesData = await response.json();

   renderCategoryOptions();
}
// **************************************************************
// GET PRODUCT | END 
// **************************************************************


// **************************************************************
// RENDER DATA | START 
// **************************************************************
// Render Category -------------------------------------------------
function renderCategoryOptions() {
   const select = document.getElementById("product_category");
   select.innerHTML = "";

   const defaultOption = document.createElement("option");
   defaultOption.textContent = "Pilih...";
   defaultOption.selected = true;
   select.appendChild(defaultOption);

   categoriesData.forEach((category) => {
      const option = document.createElement("option");
      option.value = category.id;
      option.textContent = category.category;

      select.appendChild(option);
   });
}

// Render Table -------------------------------------------------
function renderTable() {
   let html = "";

   productsData.forEach((product) => {
      html += `
            <tr>
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.category}</td>
                <td>
                    <button
                        class="btn btn-warning btn-sm btn-edit" 
                        data-bs-toggle="modal" 
                        data-bs-target="product_modal"
                        data-id="${product.id}"> Edit
                    </button>
                    <button
                        class="btn btn-danger btn-sm btn-delete"
                        data-id="${product.id}"> Hapus
                    </button>
                </td>
            </tr>
        `;
   });

   document.getElementById("productTable").innerHTML = html;
}
// **************************************************************
// RENDER DATA | END 
// **************************************************************


// **************************************************************
// SAVE PRODUCT | START 
// **************************************************************
async function saveProduct() {
   const product_id = form.id.value;
   const product_name = form.name.value;
   const product_category = form.category.value;

   let response;
   if (!product_id) {
      response = await fetch("/product/add", {
         method: "POST",
         headers: {
            "Content-Type": "application/json",
         },
         body: JSON.stringify({
            product_name: product_name,
            product_category: product_category,
         }),
      });
   } else {
      response = await fetch(`/product/edit/${product_id}`, {
         method: "PUT",
         headers: {
            "Content-Type": "application/json",
         },
         body: JSON.stringify({
            product_name: product_name,
            product_category: product_category,
         }),
      });
   }
   const result = await response.json();

   if (result.status) {
      alert(result.message);
      location.reload();
   }
}
document.querySelector(".btn-save").addEventListener("click", saveProduct);
// **************************************************************
// SAVE PRODUCT | END 
// **************************************************************


// **************************************************************
// UPDATE & DELETE PRODUCT | START 
// **************************************************************
document.getElementById("productTable").addEventListener("click", handleTableClick);

async function handleTableClick(e) {
   const id = Number(e.target.dataset.id);
   if (e.target.classList.contains("btn-edit")) {
      // proses edit
      const product = productsData.find((p) => p.id === id);

      form.title.textContent = "Ubah Produk";
      form.id.value = product.id;
      form.name.value = product.name;
      form.category.value = product.category;
   } else if (e.target.classList.contains("btn-delete")) {
      // proses delete
      if (!confirm("Yakin hapus data?")) {
         return;
      }

      const response = await fetch(`/product/delete/${id}`, {
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
// UPDATE & DELETE PRODUCT | END 
// **************************************************************
