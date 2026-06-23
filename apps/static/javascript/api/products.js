// **************************************************************
// BASE INISIALIZATION | START 
// **************************************************************
document.addEventListener("DOMContentLoaded", init);
async function init() {
   await loadCategories();

   await loadProducts();

   renderTable();
}

// Form ID Setup
const form = {
   title: document.getElementById("modal_label"),
   id: document.getElementById("product_id"),
   name: document.getElementById("product_name"),
   category: document.getElementById("product_category"),
   stock: document.getElementById("product_stock"),
   purchase: document.getElementById("product_purchase"), // harga beli
   price: document.getElementById("product_price"), //harga jual
};
// **************************************************************
// BASE INISIALIZATION | END 
// **************************************************************


// **************************************************************
// GET PRODUCT | START 
// **************************************************************
// Variable Setup -------------------------------------------------
let productsData = [];
let categoriesData = [];

// Load Data -------------------------------------------------
async function loadProducts() {
   const response = await fetch("/product/view", {
      method: "GET",
      headers: {
         "Content-Type": "application/json",
      },
   });
   productsData = await response.json();
}

async function loadCategories() {
   const response = await fetch("/category/view", {
      method: "GET",
      headers: {
         "Content-Type": "application/json",
      },
   });
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
      option.value = category.ctg_id;
      option.textContent = category.ctg_name;

      select.appendChild(option);
   });
}

// Render Table -------------------------------------------------
function renderTable() {
   let html = "";

   productsData.forEach((product, index) => {
      html += `
            <tr>
                <td>${index+1}</td>
                <td>${product.product_name}</td>
                <td>${product.product_category}</td>
                <td>${product.product_stock}</td>
                <td>${product.product_purchase}</td>
                <td>${product.product_price}</td>
                <td>
                    <button
                        class="btn btn-warning btn-sm btn-edit" 
                        data-bs-toggle="modal" 
                        data-bs-target="#product_modal"
                        data-id="${product.product_id}"> Edit
                    </button>
                    <button
                        class="btn btn-danger btn-sm btn-delete"
                        data-id="${product.product_id}"> Hapus
                    </button>
                </td>
            </tr>
        `;
   });

   document.getElementById("product_table").innerHTML = html;
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
   const product_stock = form.stock.value;
   const product_price = form.price.value;
   const product_purchase = form.purchase.value;

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
            product_stock: product_stock,
            product_purchase: product_purchase,
            product_price: product_price,
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
            product_stock: product_stock,
            product_purchase: product_purchase,
            product_price: product_price,
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
document.getElementById("product_table").addEventListener("click", handleTableClick);
async function handleTableClick(e) {
   const id = Number(e.target.dataset.id);
   if (e.target.classList.contains("btn-edit")) {
      // proses edit
      const product = productsData.find((p) => p.product_id === id);

      form.title.textContent = "Ubah Produk";
      form.id.value = product.product_id;
      form.name.value = product.product_name;
      form.category.value = product.product_ctg_id;
      form.stock.value = product.product_stock;
      form.purchase.value = product.product_purchase;
      form.price.value = product.product_price;
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
