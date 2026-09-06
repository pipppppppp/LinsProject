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

  // Refresh button
  document.getElementById("btn_refresh")?.addEventListener("click", async () => {
    await reloadTable(loadPurchases, renderPurchaseTable);
  });
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
// DATATABLE | START
// **************************************************************

function destroyPurchaseDataTable() {
  if (purchaseDataTable) {
    purchaseDataTable.destroy();

    purchaseDataTable = null;
  }
}

// **************************************************************
// DATATABLE | END
// **************************************************************

// **************************************************************
// VARIABLE SETUP | START
// **************************************************************
let suppliersData = [];
let productsData = [];
let purchaseItems = [];
let isSupplierSearchMode = false;
let purchaseDataTable = null;
// **************************************************************
// VARIABLE SETUP | END
// **************************************************************

// **************************************************************
// LOAD SUPPLIER | START
// **************************************************************
async function loadSuppliers() {
  const result = await getRequest("/supplier/view");
  if (!result) {
    return;
  }
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
  if (!result) {
    return;
  }
  if (result.status_code !== 200) {
    await swalError(result.message);
    return;
  }

  productsData = result.data;
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

  if (!validatePurchase(purchase)) {
    return;
  }

  let result;

  try {
    swalLoading();

    result = await postRequest("/purchase/add", purchase);
  } finally {
    swalClose();
  }

  if (!result) {
    return;
  }

  if (result.status_code === 201 || result.status_code === 200) {
    closeModal("purchase_modal");

    resetForm();

    await loadPurchases();

    await swalSuccess("Berhasil", result.message);
  } else {
    await swalError("Gagal", result.message);
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
  if (!result) {
    return;
  }

  if (result.status_code === 201 || result.status_code === 200) {
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
  destroyPurchaseDataTable();

  const result = await getRequest("/purchase/view");

  if (!result) {
    return;
  }
  if (result.status_code !== 200) {
    await swalError(result.message);
    return;
  }

  let html = "";

  result.data.forEach((purchase, index) => {
    html += `
          <tr>

              <td>${index + 1}</td>

              <td>
                  <div class="fw-semibold">
                      <i class="bi bi-calendar-event me-2 text-primary"></i>
                      ${purchase.purchase_date}
                  </div>
              </td>

              <td>
                  <div class="fw-semibold">
                      <i class="bi bi-building me-2 text-secondary"></i>
                      ${purchase.supplier_name}
                  </div>
              </td>

              <td>
                  <span class="badge bg-light-primary text-primary">
                      ${purchase.total_item} Barang
                  </span>
              </td>

              <td>
                  <div class="fw-bold text-success">
                      ${formatRupiah(purchase.total)}
                  </div>
              </td>

              <td class="text-center">

                  <button
                      class="btn btn-outline-primary btn-sm btn-detail"
                      data-id="${purchase.id}">

                      <i class="bi bi-eye-fill me-1"></i>

                      Detail

                  </button>

              </td>

          </tr>
      `;
  });

  document.getElementById("purchase_table").innerHTML = html;
  document.getElementById("purchase_count").textContent = `${result.data.length} Pembelian`;
  purchaseDataTable = new simpleDatatables.DataTable("#table1");
}
// **************************************************************
// LOAD PURCHASE | END
// **************************************************************

// **************************************************************
// LOAD PURCHASE DETAIL | START
// **************************************************************
async function loadPurchaseDetail(id) {
  const result = await getRequest(`/purchase/detail/${id}`);

  if (!result) {
    return;
  }

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
// SEARCH SUPPLIER BY PRODUCT | START
// **************************************************************

async function searchSupplierByProduct() {
  const input = document.getElementById("search_product_supplier");

  const keyword = input.value.trim();

  if (keyword === "") {
    await swalError("Silakan masukkan nama barang terlebih dahulu.");

    return;
  }

  const result = await getRequest(`/purchase/search-supplier/${encodeURIComponent(keyword)}`);

  if (!result) {
    return;
  }

  if (result.status_code !== 200) {
    await swalError(result.message);

    return;
  }

  isSupplierSearchMode = true;

  closeModal("search_supplier_modal");

  renderSupplierSearchTable(result.data);
}

// **************************************************************
// RENDER SEARCH RESULT | START
// **************************************************************

// function renderSupplierSearchResult(data) {
//   const table = document.getElementById("search_supplier_table");

//   let html = "";

//   let rowNumber = 1;

//   // Tidak ada supplier
//   if (data.length === 0) {
//     table.innerHTML = `
//       <tr>
//         <td
//           colspan="5"
//           class="text-center text-muted py-4"
//         >

//           <i class="bi bi-search fs-4 d-block mb-2"></i>

//           Barang tidak ditemukan.

//         </td>
//       </tr>
//     `;

//     return;
//   }

//   data.forEach((product) => {
//     // Barang ditemukan tetapi belum pernah dibeli
//     if (!product.suppliers || product.suppliers.length === 0) {
//       html += `
//         <tr>

//           <td>
//             ${rowNumber++}
//           </td>

//           <td>
//             <div class="fw-semibold">
//               <i class="bi bi-box-seam me-2 text-primary"></i>
//               ${product.product_name}
//             </div>
//           </td>

//           <td colspan="3">
//             <span class="text-muted">
//               Belum terdapat riwayat supplier.
//             </span>
//           </td>

//         </tr>
//       `;

//       return;
//     }

//     // Tampilkan supplier
//     product.suppliers.forEach((supplier) => {
//       html += `
//         <tr>

//           <td>
//             ${rowNumber++}
//           </td>

//           <td>
//             <div class="fw-semibold">
//               <i class="bi bi-box-seam me-2 text-primary"></i>
//               ${product.product_name}
//             </div>
//           </td>

//           <td>
//             <div class="fw-semibold">
//               <i class="bi bi-building me-2 text-secondary"></i>
//               ${supplier.supplier_name}
//             </div>
//           </td>

//           <td>
//             <div class="fw-semibold">
//               <i class="bi bi-calendar-event me-2 text-primary"></i>
//               ${supplier.purchase_date}
//             </div>
//           </td>

//           <td>
//             <div class="fw-bold text-success">
//               ${formatRupiah(supplier.unit_cost)}
//             </div>
//           </td>

//         </tr>
//       `;
//     });
//   });

//   table.innerHTML = html;
// }

// **************************************************************
// RENDER SEARCH RESULT | END
// **************************************************************

// **************************************************************
// SEARCH SUPPLIER BY PRODUCT | END
// **************************************************************

// **************************************************************
// RENDER SUPPLIER SEARCH TABLE | START
// **************************************************************

function renderSupplierSearchTable(data) {
  // Hancurkan DataTable lama
  destroyPurchaseDataTable();

  const title = document.getElementById("purchase_table_title");

  const subtitle = document.getElementById("purchase_table_subtitle");

  const table = document.getElementById("purchase_table");

  const tableHead = document.querySelector("#table1 thead tr");
  // Ubah Header
  title.textContent = "Supplier Berdasarkan Barang";

  subtitle.textContent = "Menampilkan supplier berdasarkan riwayat pembelian barang.";

  // Ubah kolom tabel
  tableHead.innerHTML = `
    <th width="60">No</th>
    <th>Barang</th>
    <th>Supplier</th>
    <th width="170">Tanggal Pembelian</th>
    <th width="100">Qty</th>
    <th width="160">Harga Beli</th>
  `;

  let html = "";

  let rowNumber = 1;

  // Tidak ada data
  if (!data || data.length === 0) {
    table.innerHTML = `
      <tr>
  
        <td
          colspan="5"
          class="text-center text-muted py-4"
        >
  
          <i
            class="bi bi-search fs-4 d-block mb-2"
          ></i>
  
          Barang tidak ditemukan.
  
        </td>
  
      </tr>
    `;

    renderSupplierSearchToolbar();

    purchaseDataTable = new simpleDatatables.DataTable("#table1");

    return;
  }

  // Gabungkan seluruh riwayat pembelian dari semua barang
  const rows = [];

  data.forEach((product) => {
    if (!product.suppliers || product.suppliers.length === 0) {
      return;
    }

    product.suppliers.forEach((supplier) => {
      rows.push({
        product_name: product.product_name,
        supplier_name: supplier.supplier_name,
        purchase_date: supplier.purchase_date,
        quantity: supplier.quantity,
        unit_cost: supplier.unit_cost,
      });
    });
  });

  // Urutkan semua data berdasarkan tanggal terbaru
  rows.sort((a, b) => {
    const [dayA, monthA, yearA] = a.purchase_date.split("-");
    const [dayB, monthB, yearB] = b.purchase_date.split("-");

    const dateA = new Date(yearA, monthA - 1, dayA);
    const dateB = new Date(yearB, monthB - 1, dayB);

    return dateB - dateA;
  });

  // Render seluruh hasil
  rows.forEach((row) => {
    html += `
    <tr>

      <td>
        ${rowNumber++}
      </td>

      <td>
        <div class="fw-semibold">
          <i class="bi bi-box-seam me-2 text-primary"></i>
          ${row.product_name}
        </div>
      </td>

      <td>
        <div class="fw-semibold">
          <i class="bi bi-building me-2 text-secondary"></i>
          ${row.supplier_name}
        </div>
      </td>

      <td>
        <div class="fw-semibold">
          <i class="bi bi-calendar-event me-2 text-primary"></i>
          ${row.purchase_date}
        </div>
      </td>

      <td>
        <span class="badge bg-light-primary text-primary">
          ${row.quantity} Barang
        </span>
      </td>

      <td>
        <div class="fw-bold text-success">
          ${formatRupiah(row.unit_cost)}
        </div>
      </td>

    </tr>
  `;
  });

  table.innerHTML = html;

  // Ubah toolbar
  renderSupplierSearchToolbar();

  // Inisialisasi kembali DataTable
  purchaseDataTable = new simpleDatatables.DataTable("#table1");
}

// **************************************************************
// RENDER SUPPLIER SEARCH TABLE | END
// **************************************************************

// **************************************************************
// SUPPLIER SEARCH TOOLBAR | START
// **************************************************************

function renderSupplierSearchToolbar() {
  const button = document.getElementById("btn_search_supplier_modal");

  button.innerHTML = `
    <i class="bi bi-arrow-left me-1"></i>
    Kembali
  `;

  button.classList.remove("btn-light-primary");
  button.classList.add("btn-light-secondary");

  button.removeAttribute("data-bs-toggle");
  button.removeAttribute("data-bs-target");

  button.onclick = returnPurchaseHistory;
}

// **************************************************************
// SUPPLIER SEARCH TOOLBAR | END
// **************************************************************

// **************************************************************
// RETURN PURCHASE HISTORY | START
// **************************************************************

async function returnPurchaseHistory() {
  isSupplierSearchMode = false;

  // Hancurkan DataTable mode pencarian terlebih dahulu
  destroyPurchaseDataTable();

  const title = document.getElementById("purchase_table_title");
  const subtitle = document.getElementById("purchase_table_subtitle");
  const tableHead = document.querySelector("#table1 thead tr");

  title.textContent = "Data Pembelian";

  subtitle.textContent = "Daftar seluruh transaksi pembelian barang.";

  tableHead.innerHTML = `
    <th width="60">No</th>
    <th width="180">Tanggal</th>
    <th>Supplier</th>
    <th width="130">Total Item</th>
    <th width="180">Total Pembelian</th>
    <th width="150" class="text-center">Aksi</th>
  `;

  const button = document.getElementById("btn_search_supplier_modal");

  button.innerHTML = `
    <i class="bi bi-search me-1"></i>
    Cari Supplier
  `;

  button.classList.remove("btn-light-secondary");
  button.classList.add("btn-light-primary");

  button.setAttribute("data-bs-toggle", "modal");
  button.setAttribute("data-bs-target", "#search_supplier_modal");

  button.onclick = null;

  await loadPurchases();
}
// **************************************************************
// RETURN PURCHASE HISTORY | END
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

// Cari Supplier Berdasarkan Barang
document.getElementById("btn_search_product_supplier").addEventListener("click", searchSupplierByProduct);

// Enter pada Input Search
document.getElementById("search_product_supplier").addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();

    searchSupplierByProduct();
  }
});

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
document.getElementById("table1").addEventListener("click", function (e) {
  const btn = e.target.closest(".btn-detail");

  if (!btn) return;

  loadPurchaseDetail(btn.dataset.id);
});

// **************************************************************
// EVENT LISTENER | END
// **************************************************************
