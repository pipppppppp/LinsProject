// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  await loadSuppliers();
  await loadProducts();
  await loadPurchases();

  // Default tanggal hari ini
  form.purchaseDate.value = new Date().toISOString().split("T")[0];
  form.importDate.value = new Date().toISOString().split("T")[0];

  renderPurchaseTable();
  const table = document.querySelector("#table1");

  if (table) {
    new simpleDatatables.DataTable(table);
  }
}

// Form ID Setup
const form = {
  purchaseDate: document.getElementById("purchase_date"),
  supplierId: document.getElementById("supplier_id"),

  importSupplier: document.getElementById("import_supplier"),
  importDate: document.getElementById("import_purchase_date"),
  importFile: document.getElementById("import_file"),

  grandTotal: document.getElementById("grand_total"),
};
// **************************************************************
// BASE INISIALIZATION | END
// **************************************************************

// **************************************************************
// VARIABLE SETUP | START
// **************************************************************
let suppliersData = [];
let productsData = [];
let purchaseItems = [];
// **************************************************************
// VARIABLE SETUP | END
// **************************************************************

// **************************************************************
// LOAD SUPPLIER | START
// **************************************************************
async function loadSuppliers() {
  const result = await getRequest("/supplier/view");
  console.log(result);
  if (result.status_code !== 200) {
    await swalError(result.message);
    return;
  }

  suppliersData = result.data;

  let html = `
        <option value="">
            Pilih Supplier
        </option>
    `;

  suppliersData.forEach((supplier) => {
    html += `
            <option value="${supplier.id}">
                ${supplier.name}
            </option>
        `;
  });

  form.supplierId.innerHTML = html;
  form.importSupplier.innerHTML = html;
}
// **************************************************************
// LOAD SUPPLIER | END
// **************************************************************

// **************************************************************
// LOAD PRODUCT | START
// **************************************************************
async function loadProducts() {
  const result = await getRequest("/product/view");

  if (result.status_code !== 200) {
    await swalError(result.message);
    return;
  }

  productsData = result.data;
  //   console.log(productsData)
}
// **************************************************************
// LOAD PRODUCT | END
// **************************************************************

// **************************************************************
// PURCHASE ITEM | START
// **************************************************************
function addItem() {
  purchaseItems.push({
    product_id: "",
    quantity: 1,
    unit_cost: 0,
    subtotal: 0,
  });

  renderPurchaseTable();
}

function removeItem(index) {
  purchaseItems.splice(index, 1);

  renderPurchaseTable();
}

// **************************************************************
// PURCHASE TOTAL | START
// **************************************************************
function calculateTotal() {
  let total = 0;

  purchaseItems.forEach((item) => {
    item.subtotal = Number(item.quantity) * Number(item.unit_cost);

    total += item.subtotal;
  });

  form.grandTotal.value = formatRupiah(total);
}
// **************************************************************
// PURCHASE TOTAL | END
// **************************************************************
// **************************************************************
// PURCHASE ITEM | END
// **************************************************************

// **************************************************************
// RENDER TABLE | START
// **************************************************************
function renderPurchaseTable() {
  const table = document.getElementById("purchase_detail_table");

  if (purchaseItems.length === 0) {
    table.innerHTML = `
            <tr id="empty_row">
                <td colspan="5" class="text-center text-muted">
                    Belum ada barang.
                </td>
            </tr>
        `;

    calculateTotal();

    return;
  }

  let html = "";

  purchaseItems.forEach((item, index) => {
    item.subtotal = Number(item.quantity) * Number(item.unit_cost);

    let productOptions = `
            <option value="">
                Pilih Barang
            </option>
        `;

    productsData.forEach((product) => {
      productOptions += `
                <option
                    value="${product.id}"
                    ${item.product_id == product.id ? "selected" : ""}>

                    ${product.product_name}

                </option>
            `;
    });

    html += `
            <tr>

                <td>

                    <select
                        class="form-select product-select"
                        data-index="${index}">

                        ${productOptions}

                    </select>

                </td>

                <td>

                    <input
                        type="number"
                        class="form-control quantity-input"
                        data-index="${index}"
                        value="${item.quantity}"
                        min="1">

                </td>

                <td>

                    <input
                        type="text"
                        class="form-control purchase-input"
                        data-index="${index}"
                        value="${item.unit_cost == 0 ? "" : formatRupiah(item.unit_cost)}">

                </td>

                <td>

                    ${formatRupiah(item.subtotal)}

                </td>

                <td class="text-center">

                    <button
                        class="btn btn-outline-danger btn-sm btn-remove-item"
                        data-index="${index}">

                        <i class="bi bi-trash-fill"></i>

                    </button>

                </td>

            </tr>
        `;
  });

  table.innerHTML = html;

  calculateTotal();
}
// **************************************************************
// RENDER TABLE | END
// **************************************************************

// **************************************************************
// SAVE PURCHASE | START
// **************************************************************
async function savePurchase() {
  const purchase = {
    purchase_date: new Date(form.purchaseDate.value).getTime(),
    supplier_id: form.supplierId.value,
    purchase_details: purchaseItems,
  };

  // VALIDATION ==================================================
  if (!validatePurchase(purchase)) return;

  let result;

  try {
    swalLoading();

    result = await postRequest("/purchase/add", purchase);
  } finally {
    swalClose();
  }

  if (result.status_code === 201) {
    closeModal("purchase_modal");
    resetForm();
    await loadPurchases();
    await swalSuccess(result.message);
  } else {
    await swalError(result.message);
  }
}
// **************************************************************
// SAVE PURCHASE | END
// **************************************************************

// **************************************************************
// IMPORT PURCHASE | START
// **************************************************************
async function importPurchase() {
  const purchase = {
    supplier_id: form.importSupplier.value,
    purchase_date: form.importDate.value,
    file: form.importFile.files[0],
  };

  // VALIDATION ==================================================
  if (!validatePurchaseImport(purchase)) return;

  const formData = new FormData();

  formData.append("supplier_id", purchase.supplier_id);

  formData.append("purchase_date", new Date(form.importDate.value).getTime());

  formData.append("file", purchase.file);

  let result;

  try {
    swalLoading();

    result = await uploadRequest("/purchase/import", formData);
  } finally {
    swalClose();
  }

  if (result.status_code === 201) {
    closeModal("import_purchase_modal");

    clearValue(form.importSupplier, form.importDate, form.importFile);

    resetForm();

    await loadPurchases();

    await swalSuccess(result.message);
  } else {
    await swalError(result.message);
  }
}
// **************************************************************
// IMPORT PURCHASE | END
// **************************************************************

// **************************************************************
// LOAD PURCHASE | START
// **************************************************************
async function loadPurchases() {
  const result = await getRequest("/purchase/view");

  if (result.status_code !== 200) {
    await swalError(result.message);
    return;
  }

  let html = "";

  result.data.forEach((purchase, index) => {
    html += `
          <tr>

              <td>${index + 1}</td>

              <td>${purchase.purchase_date}</td>

              <td>${purchase.supplier_name}</td>

              <td>${purchase.total_item}</td>

              <td>${formatRupiah(purchase.total)}</td>

              <td>

                  <button
                      class="btn btn-outline-info btn-sm btn-detail"
                      data-id="${purchase.id}"
                      title="Detail Pembelian">
                  
                      <i class="bi bi-eye-fill me-2"></i>
                      Detail Pembelian
                  
                  </button>

              </td>

          </tr>
      `;
  });

  document.getElementById("purchase_table").innerHTML = html;
}
// **************************************************************
// LOAD PURCHASE | END
// **************************************************************

// **************************************************************
// LOAD PURCHASE DETAIL | START
// **************************************************************
async function loadPurchaseDetail(id) {
  const result = await getRequest(`/purchase/detail/${id}`);

  if (result.status_code !== 200) {
    await swalError(result.message);
    return;
  }

  const data = result.data;

  document.getElementById("detail_supplier").value = data.supplier_name;

  document.getElementById("detail_purchase_date").value = data.purchase_date;

  document.getElementById("detail_total").value = formatRupiah(data.total);

  let html = "";

  data.details.forEach((item, index) => {
    html += `
          <tr>

              <td>${index + 1}</td>

              <td>${item.product_name}</td>

              <td>${item.quantity}</td>

              <td>${formatRupiah(item.unit_cost)}</td>

              <td>${formatRupiah(item.subtotal)}</td>

          </tr>
      `;
  });

  document.getElementById("purchase_detail_body").innerHTML = html;

  openModal("purchase_detail_modal");
}
// **************************************************************
// LOAD PURCHASE DETAIL | END
// **************************************************************

// **************************************************************
// RESET FORM | START
// **************************************************************
function resetForm() {
  clearValue(form.purchaseDate, form.supplierId);

  clearValue(form.importSupplier, form.importDate, form.importFile);

  purchaseItems = [];

  form.grandTotal.value = formatRupiah(0);

  // Default tanggal hari ini
  form.purchaseDate.value = new Date().toISOString().split("T")[0];
  form.importDate.value = new Date().toISOString().split("T")[0];

  renderPurchaseTable();
}
// **************************************************************
// RESET FORM | END
// **************************************************************

// **************************************************************
// EVENT LISTENER | START
// **************************************************************

// Tambah Barang
document.getElementById("btn_add_item").addEventListener("click", addItem);

// Simpan Pembelian
document.getElementById("btn-save").addEventListener("click", savePurchase);

// Import Excel
document.getElementById("btn_import_purchase").addEventListener("click", importPurchase);

// Event Table
document.getElementById("purchase_detail_table").addEventListener("input", function (e) {
  const index = Number(e.target.dataset.index);

  if (e.target.classList.contains("quantity-input")) {
    purchaseItems[index].quantity = Number(e.target.value) || 1;
  }

  if (e.target.classList.contains("purchase-input")) {
    const number = unformatNumber(e.target.value);

    purchaseItems[index].unit_cost = Number(number);

    e.target.value = formatRupiah(number);
  }

  purchaseItems[index].subtotal = purchaseItems[index].quantity * purchaseItems[index].unit_cost;

  e.target.closest("tr").children[3].innerHTML = formatRupiah(purchaseItems[index].subtotal);

  calculateTotal();
});

document.getElementById("purchase_detail_table").addEventListener("change", function (e) {
  const index = Number(e.target.dataset.index);

  if (e.target.classList.contains("product-select")) {
    const product = productsData.find((item) => item.id == e.target.value);

    if (!product) return;

    purchaseItems[index].product_id = product.id;

    // Ambil harga beli dari Master Barang
    purchaseItems[index].unit_cost = Number(product.purchase_price);

    // Hitung subtotal
    purchaseItems[index].subtotal = purchaseItems[index].quantity * purchaseItems[index].unit_cost;

    renderPurchaseTable();
  }
});

// Hapus Item
document.getElementById("purchase_detail_table").addEventListener("click", function (e) {
  const btn = e.target.closest(".btn-remove-item");

  if (!btn) return;

  removeItem(Number(btn.dataset.index));
});

// Detail Pembelian
document.getElementById("purchase_table").addEventListener("click", function (e) {
  const btn = e.target.closest(".btn-detail");

  if (!btn) return;

  loadPurchaseDetail(btn.dataset.id);
});
// **************************************************************
// EVENT LISTENER | END
// **************************************************************
