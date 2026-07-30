// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  await loadCategories();
  await reloadTable(loadProducts, renderTable);

  // Refresh button
  document.getElementById("btn_refresh")?.addEventListener("click", async () => {
    await reloadTable(loadProducts, renderTable);
  });
}

// Form ID Setup
const form = {
  title: document.getElementById("modal_label"),
  id: document.getElementById("product_id"),
  category: document.getElementById("product_category"),
  barcode: document.getElementById("product_barcode"),
  name: document.getElementById("product_name"),
  stock: document.getElementById("product_stock"),
  minimum_stock: document.getElementById("product_minimum_stock"),
  purchase: document.getElementById("product_purchase"),
  price: document.getElementById("product_price"),
};

// Formatter Setup -----------------------------------------------
formatThousands(form.purchase);
formatThousands(form.price);

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

  if (!result || result.status_code !== 200) {
    productsData = [];

    document.getElementById("product_count").textContent = "0 Produk";

    return;
  }

  productsData = result.data ?? [];

  document.getElementById("product_count").textContent = `${productsData.length} Produk`;
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
  let html = "";

  productsData.forEach((product, index) => {
    let status = "";

    if (product.stock === 0) {
      status = `<span class="badge bg-danger">Habis</span>`;
    } else if (product.stock <= product.minimum_stock) {
      status = `<span class="badge bg-warning text-dark">Menipis</span>`;
    } else {
      status = `<span class="badge bg-success">Aman</span>`;
    }

    html += `
      <tr>

        <td>${index + 1}</td>
        <td>
          ${
            product.barcode
              ? `<span class="badge bg-light-primary text-primary">
                  ${product.barcode}
                </span>`
              : "-"
          }
        </td>
        <td class="fw-semibold">
            <i class="bi bi-box-seam text-primary me-2"></i>
              ${product.product_name}
        </td>

        <td>
          <span class="badge bg-light-primary text-primary px-3 py-2">
            ${product.category}
          </span>
        </td>

        <td>

            <div class="fw-bold">
                ${formatNumber(product.stock)}
            </div>

            <small class="text-muted">
                Min : ${formatNumber(product.minimum_stock)}
            </small>

        </td>

        <td>

            <div class="text-danger fw-semibold">
                <i class="bi bi-arrow-down-circle me-1"></i>
                ${formatRupiah(product.purchase_price)}
            </div>

            <div class="text-success fw-semibold">
                <i class="bi bi-arrow-up-circle me-1"></i>
                ${formatRupiah(product.selling_price)}
            </div>

        </td>
        <td>
          ${status}
        </td>

        <td class="text-center">

          <div class="d-flex justify-content-center gap-2">

            <button
              class="btn btn-warning btn-sm btn-edit"
              data-bs-toggle="modal"
              data-bs-target="#product_modal"
              data-id="${product.id}"
              title="Ubah">

              <i class="bi bi-pencil-fill"></i>

            </button>

            <button
              class="btn btn-danger btn-sm btn-delete"
              data-id="${product.id}"
              title="Hapus">

              <i class="bi bi-trash-fill"></i>

            </button>

          </div>

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
    barcode: form.barcode.value.trim(),
    product_name: formatTitle(form.name.value),
    stock: form.stock.value,
    minimum_stock: form.minimum_stock.value,
    purchase: removeThousands(form.purchase.value),
    price: removeThousands(form.price.value),
  };

  // VALIDATION ==================================================
  if (!validateProduct(product)) return;

  // FORMAT DATA ==================================================
  product.stock = Number(product.stock);
  product.minimum_stock = Number(product.minimum_stock);
  product.purchase = Number(product.purchase);
  product.price = Number(product.price);
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

  if (!result) {
    return;
  }

  if (result.status_code === 201 || result.status_code === 200) {
    await swalSuccess("Berhasil", result.message);

    closeModal("product_modal");

    clearValue(form.id, form.category, form.barcode, form.name, form.stock, form.minimum_stock, form.purchase, form.price);

    form.title.textContent = "Tambah Barang";

    await reloadTable(loadProducts, renderTable);
  } else {
    await swalError("Gagal", result.message);
  }
}
document.querySelector(".btn-save").addEventListener("click", saveProduct);
// **************************************************************
// SAVE PRODUCT | END
// **************************************************************

// **************************************************************
// UPDATE & DELETE PRODUCT | START
// **************************************************************
document.getElementById("table1").addEventListener("click", handleTableClick);

async function handleTableClick(e) {
  const editBtn = e.target.closest(".btn-edit");
  const deleteBtn = e.target.closest(".btn-delete");

  if (editBtn) {
    const id = Number(editBtn.dataset.id);

    const product = productsData.find((item) => item.id === id);

    if (!product) return;

    form.title.textContent = "Ubah Barang";

    form.id.value = product.id;
    form.category.value = product.category_id;
    form.barcode.value = product.barcode ?? "";
    form.name.value = product.product_name;
    form.stock.value = product.stock;
    form.minimum_stock.value = product.minimum_stock;
    form.purchase.value = formatNumber(product.purchase_price);
    form.price.value = formatNumber(product.selling_price);

    return;
  }

  if (deleteBtn) {
    const id = Number(deleteBtn.dataset.id);

    const confirmDelete = await swalDelete();

    if (!confirmDelete.isConfirmed) return;

    let result;

    try {
      swalLoading();

      result = await deleteRequest("/product/delete", {
        product_id: id,
      });
    } finally {
      swalClose();
    }
    if (!result) {
      return;
    }

    if (result.status_code === 200 || result.status_code === 201) {
      await swalSuccess("Berhasil", result.message);

      await reloadTable(loadProducts, renderTable);
    } else {
      await swalError("Gagal", result.message);
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

  clearValue(form.id, form.barcode, form.name, form.stock, form.minimum_stock, form.purchase, form.price);

  form.minimum_stock.value = 5;
  form.category.value = "";
}
// **************************************************************
// RESET FORM | END
// **************************************************************

// **************************************************************
// MODAL EVENT | START
// **************************************************************
const productModal = document.getElementById("product_modal");
const productForm = productModal.querySelector("form");

// Mencegah form submit otomatis ketika scanner mengirim Enter
productForm.addEventListener("submit", function (event) {
  event.preventDefault();
});

// Setelah barcode di-scan, pindahkan fokus ke nama barang
form.barcode.addEventListener("keydown", function (event) {
  if (event.key !== "Enter") return;

  event.preventDefault();

  form.name.focus();
});

// Reset form ketika modal ditutup
productModal.addEventListener("hidden.bs.modal", resetForm);
// **************************************************************
// MODAL EVENT | END
// **************************************************************
