// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  checkoutModal = new bootstrap.Modal(document.getElementById("checkoutModal"));

  await loadCustomer();
  renderCart();

  calculateTotal();
}

// Form =========================================================
const form = {
  barcode: document.getElementById("barcode"),

  customer: document.getElementById("customer_id"),

  vehicle: document.getElementById("vehicle_id"),

  total: document.getElementById("grand_total"),

  payment: document.getElementById("payment"),

  change: document.getElementById("change"),
};
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// FORMAT INPUT | START
// **************************************************************
formatThousands(form.payment);
// **************************************************************
// FORMAT INPUT | END
// **************************************************************

// **************************************************************
// GLOBAL VARIABLE | START
// **************************************************************
let searchData = [];
let cart = [];
let checkoutModal = null;
let currentPaymentId = null;
// **************************************************************
// GLOBAL VARIABLE | END
// **************************************************************

// **************************************************************
// CALCULATE TOTAL | START
// **************************************************************
function calculateTotal() {
  let total = 0;

  cart.forEach((item) => {
    total += Number(item.subtotal);
  });

  form.total.innerHTML = "Rp " + formatNumber(total);

  calculateChange();
}
// **************************************************************
// CALCULATE TOTAL | END
// **************************************************************

// **************************************************************
// CALCULATE CHANGE | START
// **************************************************************
function calculateChange() {
  const total = cart.reduce((sum, item) => {
    return sum + Number(item.subtotal);
  }, 0);

  const payment = Number(unformatNumber(form.payment.value || "0"));

  if (payment <= 0) {
    form.change.innerHTML = "Rp 0";
    return;
  }

  if (payment < total) {
    form.change.innerHTML = "Rp 0";
    return;
  }

  const change = payment - total;

  form.change.innerHTML = "Rp " + formatNumber(change);
}
// **************************************************************
// CALCULATE CHANGE | END
// **************************************************************

// **************************************************************
// PAYMENT EVENT | START
// **************************************************************
form.payment.addEventListener("input", function () {
  formatNumber(this);

  calculateChange();
});
// **************************************************************
// PAYMENT EVENT | END
// **************************************************************

// **************************************************************
// RESET CART | START
// **************************************************************
document.getElementById("btn_reset").addEventListener("click", resetCart);

function resetCart() {
  cart = [];

  $("#customer_id").val(null).trigger("change");

  form.vehicle.innerHTML = `<option value="">Pilih Kendaraan</option>`;
  form.payment.value = "";

  form.total.value = "0";
  form.change.value = "0";

  renderCart();
}
// **************************************************************
// RESET CART | END
// **************************************************************

// **************************************************************
// SEARCH ITEM | START
// **************************************************************
form.barcode.addEventListener("keyup", function (e) {
  if (e.key === "Enter") {
    searchItem();
  }
});

async function searchItem() {
  const keyword = form.barcode.value.trim();

  if (keyword == "") return;

  const response = await getRequest(`/cashier/search?keyword=${encodeURIComponent(keyword)}`);

  searchData = response.data || [];

  // Barcode ditemukan (langsung add ke cart)
  if (searchData.length === 1 && keyword === searchData[0].barcode) {
    const item = searchData[0];
    addToCart(item);

    // Bersihkan hasil pencarian
    clearSearchResult();
    return;
  }

  renderSearchTable();
}
// **************************************************************
// SEARCH ITEM | END
// **************************************************************

// **************************************************************
// RENDER SEARCH TABLE | START
// **************************************************************
function renderSearchTable() {
  const tbody = document.getElementById("search_table");

  tbody.innerHTML = "";

  if (searchData.length == 0) {
    tbody.innerHTML = `
              <tr>
                  <td colspan="4" class="text-center">
                      Data tidak ditemukan
                  </td>
              </tr>
          `;

    return;
  }

  searchData.forEach((item, index) => {
    tbody.innerHTML += `
  
              <tr>
  
                  <td>${index + 1}</td>
  
                  <td>${item.name}</td>
  
                  <td>
                      Rp ${formatNumber(item.price)}
                  </td>
  
                  <td>
  
                      <button
                          class="btn btn-success btn-sm"
                          onclick="addToCart(searchData[${index}])">
  
                          <i class="bi bi-plus-circle"></i>
  
                      </button>
  
                  </td>
  
              </tr>
  
          `;
  });
}
// **************************************************************
// RENDER SEARCH TABLE | END
// **************************************************************

// **************************************************************
// CLEAR SEARCH TABLE | START
// **************************************************************
function clearSearchResult() {
  searchData = [];
  renderSearchTable();
}
// **************************************************************
// CLEAR SEARCH TABLE | END
// **************************************************************

// **************************************************************
// ADD CART | START
// **************************************************************
function addToCart(item) {
  const exist = cart.find((x) => x.id == item.id && x.type == item.type);

  if (exist) {
    exist.quantity++;
    exist.subtotal = exist.quantity * exist.price;
  } else {
    cart.push({
      id: item.id,
      type: item.type,
      name: item.name,
      quantity: 1,
      price: Number(item.price),
      subtotal: Number(item.price),
    });
  }
  renderCart();
  calculateTotal();

  form.barcode.value = "";
  form.barcode.focus();
}
// **************************************************************
// ADD CART | END
// **************************************************************

// **************************************************************
// LOAD CUSTOMER | START
// **************************************************************
async function loadCustomer() {
  const response = await getRequest("/customer/view");

  const customers = response.data?.customer || [];

  // Option kosong untuk Select2 placeholder
  form.customer.innerHTML = "";

  const empty = new Option("Pilih Pelanggan", "");
  empty.disabled = true;
  empty.selected = true;

  form.customer.add(empty);

  customers.forEach((customer) => {
    form.customer.add(new Option(customer.customer_name, customer.id));
  });

  if ($("#customer_id").hasClass("select2-hidden-accessible")) {
    $("#customer_id").select2("destroy");
  }
  
  $("#customer_id").select2({
    width: "100%",
  });

  $("#customer_id").on("change", function () {
    loadVehicle(this.value);
  });
}
// **************************************************************
// LOAD CUSTOMER | END
// **************************************************************

// **************************************************************
// LOAD VEHICLE | START
// **************************************************************
// async function loadVehicle(customer_id) {
//   console.log(customer_id);

//   form.vehicle.innerHTML = `<option value="">Pilih Kendaraan</option>`;

//   if (!customer_id) return;
//   console.log("Request:", `/vehicle/view/${customer_id}`);

//   const result = await getRequest(`/vehicle/view/${customer_id}`);
//   console.log(result);
//   const vehicles = result.data?.vehicles || [];
//   console.log("vehicles =", vehicles);
//   console.log("vehicle select =", form.vehicle);

//   vehicles.forEach((vehicle) => {
//     form.vehicle.innerHTML += `
//       <option value="${vehicle.id}">
//         ${vehicle.plate_number} - ${vehicle.vehicle_brand} ${vehicle.vehicle_type}
//       </option>
//     `;
//   });
// }
async function loadVehicle(customer_id) {
  form.vehicle.innerHTML = "";

  form.vehicle.add(new Option("Pilih Kendaraan", ""));

  if (!customer_id) return;

  const result = await getRequest(`/vehicle/view/${customer_id}`);

  const vehicles = result.data?.vehicles || [];

  vehicles.forEach((vehicle) => {
    form.vehicle.add(new Option(`${vehicle.plate_number} - ${vehicle.vehicle_brand} ${vehicle.vehicle_type}`, vehicle.id));
  });

  form.vehicle.selectedIndex = 0;
}
// **************************************************************
// LOAD VEHICLE | END
// **************************************************************

// **************************************************************
// RENDER CART | START
// **************************************************************
function renderCart() {
  const tbody = document.getElementById("cart_table");
  tbody.innerHTML = "";
  if (cart.length == 0) {
    tbody.innerHTML = `
    <tr>
        <td colspan="6" class="text-center py-4">

            <i class="bi bi-cart-x fs-2 text-muted d-block mb-2"></i>

            <h6 class="mb-1">
                Keranjang masih kosong
            </h6>

            <small class="text-muted">
                Cari barang atau jasa untuk memulai transaksi.
            </small>

        </td>
    </tr>
    `;

    calculateTotal();
    return;
  }

  cart.forEach((item, index) => {
    tbody.innerHTML += `
  
          <tr>
  
              <td>${index + 1}</td>
  
              <td>${item.name}</td>
  
              <td>
  
                  <div class="btn-group">
  
                      <button
                          class="btn btn-sm btn-danger"
                          onclick="decreaseQty(${index})">
  
                          <i class="bi bi-dash"></i>
  
                      </button>
  
                      <button
                          class="btn btn-sm btn-light"
                          disabled>
  
                          ${item.quantity}
  
                      </button>
  
                      <button
                          class="btn btn-sm btn-success"
                          onclick="increaseQty(${index})">
  
                          <i class="bi bi-plus"></i>
  
                      </button>
  
                  </div>
  
              </td>
  
              <td>
                  Rp ${formatNumber(item.price)}
              </td>
  
              <td>
                  Rp ${formatNumber(item.subtotal)}
              </td>
  
              <td>
  
                  <button
                      class="btn btn-danger btn-sm"
                      onclick="removeCart(${index})">
  
                      <i class="bi bi-trash-fill"></i>
  
                  </button>
  
              </td>
  
          </tr>
  
          `;
  });

  calculateTotal();
}
// **************************************************************
// RENDER CART | END
// **************************************************************

// **************************************************************
// INCREASE QTY | START
// **************************************************************
function increaseQty(index) {
  cart[index].quantity++;

  cart[index].subtotal = cart[index].quantity * cart[index].price;

  renderCart();
}
// **************************************************************
// INCREASE QTY | END
// **************************************************************

// **************************************************************
// DECREASE QTY | START
// **************************************************************
function decreaseQty(index) {
  cart[index].quantity--;

  if (cart[index].quantity <= 0) {
    cart.splice(index, 1);
  } else {
    cart[index].subtotal = cart[index].quantity * cart[index].price;
  }

  renderCart();
}
// **************************************************************
// DECREASE QTY | END
// **************************************************************

// **************************************************************
// REMOVE CART | START
// **************************************************************
function removeCart(index) {
  cart.splice(index, 1);

  renderCart();
}
// **************************************************************
// REMOVE CART | END
// **************************************************************

// **************************************************************
// CHECKOUT | START
// **************************************************************
document.getElementById("btn_checkout").addEventListener("click", checkout);

async function checkout() {
  if (cart.length == 0) {
    swalWarning("Keranjang masih kosong.");

    return;
  }

  const total = cart.reduce((sum, item) => {
    return sum + item.subtotal;
  }, 0);

  const payment = Number(unformatNumber(form.payment.value || "0"));

  if (payment < total) {
    swalWarning("Nominal pembayaran kurang.");
    return;
  }

  const MAX_PAYMENT_MULTIPLIER = 20;

  if (payment > total * MAX_PAYMENT_MULTIPLIER) {
    swalWarning(`Nominal pembayaran terlalu besar. Maksimal Rp ${formatNumber(total * MAX_PAYMENT_MULTIPLIER)}`);
    form.payment.focus();
    return;
  }

  const data = {
    customer_id: form.customer.value || null,

    vehicle_id: form.vehicle.value || null,

    payment: Number(unformatNumber(form.payment.value)),

    product_details: cart
      .filter((x) => x.type == "product")
      .map((item) => ({
        product_id: item.id,
        quantity: item.quantity,
      })),

    service_details: cart
      .filter((x) => x.type == "service")
      .map((item) => ({
        service_id: item.id,
        quantity: item.quantity,
      })),
  };

  const response = await postRequest("/cashier/checkout", data);

  if (response.status_code === 200) {
    showCheckoutModal(response.message);
  } else {
    swalWarning(response.message);
  }
}
// **************************************************************
// CHECKOUT | END
// **************************************************************

// **************************************************************
// CHECKOUT MODAL | START
// **************************************************************

function showCheckoutModal(data) {
  currentPaymentId = data.payment_id;

  document.getElementById("modal_total").innerHTML = "Rp " + formatNumber(data.total);

  document.getElementById("modal_paid").innerHTML = "Rp " + formatNumber(data.paid);

  document.getElementById("modal_change").innerHTML = "Rp " + formatNumber(data.change);

  checkoutModal.show();
}

document.getElementById("btn_modal_done").addEventListener("click", function () {
  checkoutModal.hide();

  resetCart();

  document.getElementById("search_table").innerHTML = "";
});

document.getElementById("btn_modal_print").addEventListener("click", function () {
  window.open(`/cashier/receipt/${currentPaymentId}`, "_blank");
  checkoutModal.hide();
  resetCart();
});

// **************************************************************
// CHECKOUT MODAL | END
// **************************************************************
