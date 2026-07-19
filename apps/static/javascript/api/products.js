// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  await loadCategories();
  await reloadTable(loadProducts, renderTable);
}

// Form ID Setup
const form = {
  title: document.getElementById("modal_label"),
  id: document.getElementById("product_id"),
  category: document.getElementById("product_category"),
  name: document.getElementById("product_name"),
  stock: document.getElementById("product_stock"),
  purchase: document.getElementById("product_purchase"),
  price: document.getElementById("product_price"),
};

// Variable Setup
let productsData = [];
let categoriesData = [];
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// GET PRODUCT | START
// **************************************************************

// Load Product -------------------------------------------------
async function loadProducts() {
  const result = await getRequest("/product/view");
  
  productsData = result.data;
}

// Load Category -------------------------------------------------
async function loadCategories() {
  const result = await getRequest("/category/view");
  categoriesData = result.data;

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
  const select = form.category;

  select.innerHTML = `
     <option value="">Pilih Kategori</option>
   `;

  categoriesData.forEach((category) => {
    select.innerHTML += `
       <option value="${category.category_id}">
         ${category.category_name}
       </option>
     `;
  });
}

// Render Table -------------------------------------------------
function renderTable() {

  const table = document.getElementById("product_table");
  
  let html = "";

  productsData.forEach((product, index) => {
    html += `
      <tr>
        <td>${index + 1}</td>
        <td>${product.product_name}</td>
        <td>${product.category}</td>
        <td>${formatNumber(product.stock)}</td>
        <td>${formatRupiah(product.purchase_price)}</td>
        <td>${formatRupiah(product.selling_price)}</td>
        <td>
          <button
            class="btn btn-warning btn-sm btn-edit"
            data-bs-toggle="modal"
            data-bs-target="#product_modal"
            data-id="${product.id}">
            Edit
          </button>

          <button
            class="btn btn-danger btn-sm btn-delete"
            data-id="${product.id}">
            Hapus
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
  const product = {
    id: form.id.value,
    category_id: form.category.value,
    product_name: formatTitle(form.name.value),
    stock: form.stock.value,
    purchase: form.purchase.value,
    price: form.price.value,
  };

  // VALIDATION ==================================================
  if (!validateProduct(product)) return;

  let result;

  try {
    swalLoading();

    if (!product.id) {
      result = await postRequest("/product/add", product);
    } else {
      result = await putRequest("/product/edit", product);
    }
  } finally {
    swalClose();
  }

  if (result.status_code === 200) {
    await swalSuccess(result.message);

    closeModal("product_modal");

    clearValue(form.id, form.category, form.name, form.stock, form.purchase, form.price);

    form.title.textContent = "Tambah Barang";

    await reloadTable(loadProducts, renderTable);
  } else {
    await swalError(result.message);
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
    // Edit Product ========================================

    const product = productsData.find((item) => item.id === id);

    if (!product) return;

    form.title.textContent = "Ubah Barang";

    form.id.value = product.id;
    form.category.value = product.category_id;
    form.name.value = product.product_name;
    form.stock.value = product.stock;
    form.purchase.value = product.purchase_price;
    form.price.value = product.selling_price;
  } else if (e.target.classList.contains("btn-delete")) {
    // Delete Product ========================================
    const confirmDelete = await swalDelete();

    if (!confirmDelete.isConfirmed) {
      return;
    }

    let result;

    try {
      swalLoading();

      result = await deleteRequest("/product/delete", {
        product_id: id,
      });
    } finally {
      swalClose();
    }

    if (result.status_code === 200) {
      await swalSuccess(result.message);

      await reloadTable(loadProducts, renderTable);
    } else {
      await swalError(result.message);
    }
  }
}
// **************************************************************
// UPDATE & DELETE PRODUCT | END
// **************************************************************

// **************************************************************
// RESET FORM | START
// **************************************************************
function resetForm() {
  form.title.textContent = "Tambah Barang";

  clearValue(form.id, form.name, form.stock, form.purchase, form.price);

  form.category.value = "";
}
// **************************************************************
// RESET FORM | END
// **************************************************************

// **************************************************************
// MODAL EVENT | START
// **************************************************************
document.getElementById("product_modal").addEventListener("hidden.bs.modal", resetForm);
// **************************************************************
// MODAL EVENT | END
// **************************************************************
