// ====================date==================================
// BARANG
// ======================================================

function addRow() {
  const tbody = document.getElementById("sales-items");

  let options = "";

  itemsData.forEach((item) => {
    options += `
            <option
                value="${item.id}"
                data-harga="${item.harga_jual}">

                ${item.nama_barang}

            </option>
        `;
  });

  const row = `
        <tr>

            <td>

                <select
                    class="form-control item_id"
                    onchange="selectItem(this)">

                    <option value="">
                        Pilih Barang
                    </option>

                    ${options}

                </select>

            </td>

            <td>

                <input
                    type="number"
                    min="1"
                    class="form-control qty text-center"
                    value="1"
                    oninput="calculateRow(this)">

            </td>

            <td>

                <input
                    type="number"
                    class="form-control harga_jual"
                    readonly>

            </td>

            <td class="subtotal">
                0
            </td>

            <td>

                <button
                    class="btn btn-danger btn-sm"
                    onclick="removeRow(this)">

                    Hapus

                </button>

            </td>

        </tr>
    `;

  tbody.insertAdjacentHTML("beforeend", row);
}

function addItemToCart(item) {
  const rows = document.querySelectorAll("#sales-items tr");

  for (const row of rows) {
    const itemId = row.querySelector(".item_id")?.value;

    if (itemId == item.id) {
      const qtyInput = row.querySelector(".qty");

      qtyInput.value = parseInt(qtyInput.value) + 1;

      calculateRow(qtyInput);

      return;
    }
  }

  addRow();

  const lastRow = document.querySelector("#sales-items tr:last-child");

  const select = lastRow.querySelector(".item_id");

  select.value = item.id;

  selectItem(select);
}

function addServiceToCart(service) {
  const rows = document.querySelectorAll("#service-items tr");

  for (const row of rows) {
    const serviceId = row.querySelector(".service_id")?.value;

    if (serviceId == service.id) {
      const qtyInput = row.querySelector(".service_qty");

      qtyInput.value = parseInt(qtyInput.value) + 1;

      calculateServiceRow(qtyInput);

      return;
    }
  }

  addServiceRow();

  const lastRow = document.querySelector("#service-items tr:last-child");

  const select = lastRow.querySelector(".service_id");

  select.value = service.id;

  calculateServiceRow(select);
}

$(document).ready(function () {
  $('#customer_id').select2({
    placeholder: 'Pilih Member (Opsional)',
    allowClear: true,
    width: '100%'
  });
  $("#search-item").select2({
    placeholder: "Cari Barang",

    width: "100%",
    minimumInputLength: 1,
  });

  $("#search-item").on("change", function () {
    const itemId = $(this).val();

    if (!itemId) {
      return;
    }

    const item = itemsData.find((x) => x.id == itemId);

    if (!item) {
      return;
    }

    addItemToCart(item);

    $(this).val(null).trigger("change");
  });
});

$("#search-service").select2({

  placeholder:
      "Cari Jasa",

  width: "100%",

  minimumInputLength: 1

});

$("#search-service").on(
  "change",
  function () {

      const serviceId =
          $(this).val();

      if (!serviceId) {
          return;
      }

      const service =
          servicesData.find(
              x =>
              x.id == serviceId
          );

      if (!service) {
          return;
      }

      addServiceToCart(
          service
      );

      $(this)
          .val(null)
          .trigger("change");
  }
);

function selectItem(element) {
  const row = element.closest("tr");

  const harga = parseInt(
    element.options[element.selectedIndex]?.dataset.harga || 0
  );

  row.querySelector(".harga_jual").value = harga;

  calculateRow(row.querySelector(".harga_jual"));
}

function formatRupiah(number) {
  return new Intl.NumberFormat("id-ID").format(number);
}

function calculateRow(element) {
  const row = element.closest("tr");

  const qty = parseInt(row.querySelector(".qty").value || 0);

  const harga = parseInt(row.querySelector(".harga_jual").value || 0);

  const subtotal = qty * harga;

  row.querySelector(".subtotal").innerText = "Rp " + formatRupiah(subtotal);

  calculateGrandTotal();
}

// ======================================================
// JASA
// ======================================================
function addServiceRow() {
  const tbody = document.getElementById("service-items");

  let options = "";

  servicesData.forEach((service) => {
    options += `
          <option
              value="${service.id}"
              data-harga="${service.biaya_jasa}">

              ${service.nama_jasa}

          </option>
      `;
  });

  const row = `
      <tr>

          <td>

              <select
                  class="form-control service_id"
                  onchange="calculateServiceRow(this)">

                  <option value="">
                      Pilih Jasa
                  </option>

                  ${options}

              </select>

          </td>

          <td>

              <input
                  type="number"
                  class="form-control service_qty"
                  value="1"
                  oninput="calculateServiceRow(this)">

          </td>

          <td>

              <input
                  type="number"
                  class="form-control harga_jasa"
                  value="0"
                  readonly>

          </td>

          <td
              class="service_subtotal">

              0

          </td>

          <td>

              <button
                  class="btn btn-danger btn-sm"
                  onclick="removeRow(this)">

                  Hapus

              </button>

          </td>

      </tr>
  `;

  tbody.insertAdjacentHTML("beforeend", row);
}

function calculateServiceRow(element) {
  const row = element.closest("tr");

  const select = row.querySelector(".service_id");

  const qty = parseInt(row.querySelector(".service_qty").value || 0);

  const harga = parseInt(
    select.options[select.selectedIndex]?.dataset.harga || 0
  );

  row.querySelector(".harga_jasa").value = harga;

  const subtotal = qty * harga;

  row.querySelector(".service_subtotal").innerText =
    "Rp " + formatRupiah(subtotal);

  calculateGrandTotal();
}

// ======================================================
// GRAND TOTAL
// ======================================================

function calculateGrandTotal() {
  let total = 0;

  document.querySelectorAll(".subtotal").forEach((item) => {

    const value =
      item.innerText
        .replace("Rp", "")
        .replace(/\./g, "")
        .trim();

    total += parseInt(value || 0);

  });

  document.querySelectorAll(".service_subtotal").forEach((item) => {

    const value =
        item.innerText
            .replace("Rp", "")
            .replace(/\./g, "")
            .trim();
  
    total += parseInt(value || 0);
  
  });

  document.getElementById("grand-total").innerText =
    formatRupiah(total);

  hitungKembalian();
}

function hitungKembalian(){

  const total = parseInt(
      document.getElementById(
          "grand-total"
      ).innerText
      .replace(/\./g,"")
      .trim()
      || 0
  );

  const bayar = parseInt(
      document.getElementById(
          "bayar"
      ).value
      || 0
  );

  const kembalian =
      bayar - total;

  document.getElementById(
      "kembalian"
  ).value =
      "Rp " +
      formatRupiah(
          kembalian > 0
          ? kembalian
          : 0
      );
}

// ======================================================
// HAPUS BARIS
// ======================================================

function removeRow(button) {
  button.closest("tr").remove();

  calculateGrandTotal();
}

// ======================================================
// SIMPAN PENJUALAN
// ======================================================

async function saveSales() {
  const customerId = document.getElementById("customer_id").value;
  const tanggal = document.getElementById("tanggal").value;

  const total = parseInt(
    document.getElementById("grand-total")
        .innerText
        .replace("Rp", "")
        .replace(/\./g, "")
        .trim()
  );
  
  const bayar = parseInt(
      document.getElementById(
          "bayar"
      ).value || 0
  );

  if (bayar < total) {

      Swal.fire({
          icon: "warning",
          title: "Pembayaran Kurang",
          text:
              "Uang pembayaran lebih kecil dari total transaksi"
      });

      return;
  }
  const details = [];

  const service_details = [];

  // BARANG
  document.querySelectorAll("#sales-items tr").forEach((row) => {
    details.push({
      item_id: row.querySelector(".item_id").value,

      qty: row.querySelector(".qty").value,

      harga_jual: row.querySelector(".harga_jual").value,

      subtotal: parseInt(
        row.querySelector(".subtotal")
           .innerText
           .replace("Rp", "")
           .replace(/\./g, "")
           .trim()
    )
    });
  });

  // JASA
  document.querySelectorAll("#service-items tr").forEach((row) => {
    service_details.push({
      service_id: row.querySelector(".service_id").value,

      qty: row.querySelector(".service_qty").value,

      harga_jasa: row.querySelector(".harga_jasa").value,

      subtotal: parseInt(
        row.querySelector(".service_subtotal")
           .innerText
           .replace("Rp", "")
           .replace(/\./g, "")
           .trim()
    )
    });
  });

  const data = {
    customer_id: customerId,

    tanggal: tanggal,

    total: total,

    bayar:bayar,

    kembalian: bayar-total,

    details: details,

    service_details: service_details,
  };

  try {
    Swal.fire({
        title: "Menyimpan...",
        text: "Mohon tunggu",
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    const response = await fetch("/sales/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {

      Swal.fire({
          icon: "error",
          title: "Gagal",
          text: result.message
      });

      return;
    }
    Swal.fire({
      icon: "success",
      title: "Berhasil",
      text: result.message,
      confirmButtonText: "OK"
    }).then(() => {
      window.open(
        `/sales/invoice/${result.sale_id}`,
        "_blank"
      );
    });

  } catch (error) {
    console.error(error);

    Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Terjadi kesalahan saat menyimpan data"
    });
  }
}

// ======================================================
// BATALKAN PENJUALAN
// ======================================================

async function cancelSale(id){

  const confirm = await Swal.fire({

      title: "Batalkan Transaksi?",

      text: "Stok barang akan dikembalikan",

      icon: "warning",

      showCancelButton: true

  });

  if(!confirm.isConfirmed){
      return;
  }

  const response = await fetch(

      `/sales/cancel/${id}`,

      {
          method: "PUT"
      }

  );

  const result = await response.json();
  console.log(result);
  
  if(result.status){

      Swal.fire(
          "Berhasil",
          result.message,
          "success"
      ).then(()=>{

          location.reload();

      });

  }else{

      Swal.fire(
          "Gagal",
          result.message,
          "error"
      );

  } 
}
