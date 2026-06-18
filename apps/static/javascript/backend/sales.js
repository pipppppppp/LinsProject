// ======================================================
// BARANG
// ======================================================

function addRow() {
  const tbody = document.getElementById("sales-items");

  let options = "";

  itemsData.forEach((item) => {
    options += `
            <option value="${item.id}"
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
                    class="form-control qty"
                    value="1"
                    oninput="calculateRow(this)">
            </td>

            <td>
                <input
                    type="number"
                    class="form-control harga_jual"
                    value="0"
                    oninput="calculateRow(this)">
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

function selectItem(element) {

    const row =
        element.closest("tr");

    const harga =
        parseInt(
            element.options[
                element.selectedIndex
            ]?.dataset.harga || 0
        );

    row.querySelector(
        ".harga_jual"
    ).value = harga;

    calculateRow(
        row.querySelector(
            ".harga_jual"
        )
    );
}

function calculateRow(element) {
  const row = element.closest("tr");

  const qty = parseInt(row.querySelector(".qty").value || 0);

  const harga = parseInt(row.querySelector(".harga_jual").value || 0);

  const subtotal = qty * harga;

  row.querySelector(".subtotal").innerText = subtotal;

  calculateGrandTotal();
}

// ======================================================
// JASA
// ======================================================
function addServiceRow() {

  const tbody =
      document.getElementById(
          "service-items"
      );

  let options = "";

  servicesData.forEach(service => {

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

  tbody.insertAdjacentHTML(
      "beforeend",
      row
  );
}

function calculateServiceRow(
  element
) {

  const row =
      element.closest("tr");

  const select =
      row.querySelector(
          ".service_id"
      );

  const qty =
      parseInt(
          row.querySelector(
              ".service_qty"
          ).value || 0
      );

  const harga =
      parseInt(
          select.options[
              select.selectedIndex
          ]?.dataset.harga || 0
      );

  row.querySelector(
      ".harga_jasa"
  ).value = harga;

  const subtotal =
      qty * harga;

  row.querySelector(
      ".service_subtotal"
  ).innerText = subtotal;

  calculateGrandTotal();
}

// ======================================================
// GRAND TOTAL
// ======================================================

function calculateGrandTotal() {

  let total = 0;

  document.querySelectorAll(
      ".subtotal"
  ).forEach(item => {

      total += parseInt(
          item.innerText || 0
      );
  });

  document.querySelectorAll(
      ".service_subtotal"
  ).forEach(item => {

      total += parseInt(
          item.innerText || 0
      );
  });

  document.getElementById(
      "grand-total"
  ).innerText = total;
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

  const customerId =
      document.getElementById(
          "customer_id"
      ).value;

  if (!customerId) {

      alert(
          "Pilih customer terlebih dahulu"
      );

      return;
  }

  const total =
      document.getElementById(
          "grand-total"
      ).innerText;

  const details = [];

  const service_details = [];

  // BARANG
  document.querySelectorAll(
      "#sales-items tr"
  ).forEach((row) => {

      details.push({

          item_id:
              row.querySelector(
                  ".item_id"
              ).value,

          qty:
              row.querySelector(
                  ".qty"
              ).value,

          harga_jual:
              row.querySelector(
                  ".harga_jual"
              ).value,

          subtotal:
              row.querySelector(
                  ".subtotal"
              ).innerText

      });

  });

  // JASA
  document.querySelectorAll(
      "#service-items tr"
  ).forEach((row) => {

      service_details.push({

          service_id:
              row.querySelector(
                  ".service_id"
              ).value,

          qty:
              row.querySelector(
                  ".service_qty"
              ).value,

          harga_jasa:
              row.querySelector(
                  ".harga_jasa"
              ).value,

          subtotal:
              row.querySelector(
                  ".service_subtotal"
              ).innerText

      });

  });

  const data = {

      customer_id:
          customerId,

      total:
          total,

      details:
          details,

      service_details:
          service_details

  };

  try {

      const response =
          await fetch(
              "/sales/add",
              {
                  method: "POST",
                  headers: {
                      "Content-Type":
                          "application/json"
                  },
                  body:
                      JSON.stringify(
                          data
                      )
              }
          );

      const result =
          await response.json();

      if (!response.ok) {

          alert(
              result.message
          );

          return;
      }

      alert(
          result.message
      );

      location.reload();

  } catch (error) {

      console.error(error);

      alert(
          "Terjadi kesalahan saat menyimpan data"
      );

  }
}
