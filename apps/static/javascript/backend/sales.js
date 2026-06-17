function addRow() {
  const tbody = document.getElementById("sales-items");

  let options = "";

  itemsData.forEach((item) => {
    options += `
            <option value="${item.id}">
                ${item.nama_barang}
            </option>
        `;
  });

  const row = `
        <tr>

            <td>
                <select class="form-control item_id">

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

function calculateRow(element) {
  const row = element.closest("tr");

  const qty = parseInt(row.querySelector(".qty").value || 0);

  const harga = parseInt(row.querySelector(".harga_jual").value || 0);

  const subtotal = qty * harga;

  row.querySelector(".subtotal").innerText = subtotal;

  calculateGrandTotal();
}

function calculateGrandTotal() {
  let total = 0;

  document.querySelectorAll(".subtotal").forEach((item) => {
    total += parseInt(item.innerText || 0);
  });

  document.getElementById("grand-total").innerText = total;
}

function removeRow(button) {
  button.closest("tr").remove();

  calculateGrandTotal();
}

async function saveSales() {
  // Ambil customer yang dipilih
  const customerId = document.getElementById("customer_id").value;

  // Validasi customer
  if (!customerId) {
    alert("Pilih customer terlebih dahulu");
    return;
  }

  // Ambil total penjualan
  const total = document.getElementById("grand-total").innerText;

  // Menyimpan semua detail barang yang dijual
  const details = [];

  // Mengambil data dari setiap baris barang
  document.querySelectorAll("#sales-items tr").forEach((row) => {
    details.push({
      item_id: row.querySelector(".item_id").value,

      qty: row.querySelector(".qty").value,

      harga_jual: row.querySelector(".harga_jual").value,

      subtotal: row.querySelector(".subtotal").innerText,
    });
  });

  // Menyiapkan data penjualan untuk dikirim ke backend
  const data = {
    customer_id: customerId,

    total: total,

    details: details,
  };

  try {
    // Mengirim data penjualan ke server
    const response = await fetch("/sales/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    // Mengambil response dari server
    const result = await response.json();

    // Menampilkan pesan jika transaksi gagal
    if (!response.ok) {
      alert(result.message);

      return;
    }

    // Menampilkan pesan jika transaksi berhasil
    alert(result.message);

    // Memuat ulang halaman
    location.reload();
  } catch (error) {
    console.error(error);

    alert("Terjadi kesalahan saat menyimpan data");
  }
}
