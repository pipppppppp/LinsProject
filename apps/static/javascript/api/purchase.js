function addRow() {

    const tbody = document.getElementById(
        "purchase-items"
    );

    let options = "";

    itemsData.forEach(item => {
    
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
                    class="form-control harga_beli"
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

    tbody.insertAdjacentHTML(
        "beforeend",
        row
    );

}

function calculateRow(element){

    const row = element.closest("tr");

    const qty = parseInt(
        row.querySelector(".qty").value || 0
    );

    const harga = parseInt(
        row.querySelector(".harga_beli").value || 0
    );

    const subtotal = qty * harga;

    row.querySelector(".subtotal").innerText = subtotal;

    calculateGrandTotal();

}

function calculateGrandTotal(){

    let total = 0;

    document.querySelectorAll(".subtotal")
        .forEach(item => {

            total += parseInt(
                item.innerText || 0
            );

        });

    document.getElementById(
        "grand-total"
    ).innerText = total;

}

function removeRow(button){

    button.closest("tr").remove();

    calculateGrandTotal();

}

// IMPORT FILE EXCEL
async function importExcel() {

    const file =
        document.getElementById(
            "excel-file"
        ).files[0];
    
    const supplierId =
        document.getElementById(
            "supplier_id"
        ).value;
    
    const tanggal =
        document.getElementById(
            "tanggal"
        ).value;
    
    if (!supplierId) {

        Swal.fire({
        
            icon: 'warning',
    
            title: 'Supplier Belum Dipilih',
    
            text: 'Silakan pilih supplier terlebih dahulu'
        
        });
        
        return;
    }
        
    if (!tanggal) {
        
        Swal.fire({
        
            icon: 'warning',
        
            title: 'Tanggal Belum Dipilih',
        
            text: 'Silakan pilih tanggal transaksi'
        
        });
        
        return;
    }

    if (!file) {

        alert(
            "Pilih file excel dulu"
        );

        return;
    }

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    Swal.fire({

        title: 'Memproses File...',
    
        allowOutsideClick: false,
    
        didOpen: () => {
    
            Swal.showLoading();
    
        }
    
    });
    
    const response =
        await fetch(
            "/purchase/import",
            {
                method: "POST",
                body: formData
            }
        );
    
    Swal.close();

    const result =
        await response.json();

        if (!result.status) {

            Swal.fire({
                icon: 'error',
                title: 'Import Gagal',
                text: result.message
            });
        
            return;
        }
        
        renderImportedData(
            result.data
        );
        
        document.getElementById(
            "excel-file"
        ).value = "";
        
        Swal.fire({
        
            icon: 'success',
        
            title: 'Import Excel Berhasil',
        
            html: `
                <b>${result.data.length}</b>
                barang berhasil dimuat ke tabel pembelian
            `
        
        });
        
}

// BACA ISI FILE EXCEL
function renderImportedData(data) {

    const tbody =
        document.getElementById(
            "purchase-items"
        );

    tbody.innerHTML = "";

    data.forEach(item => {

        const itemData =
            itemsData.find(
                x =>
                x.nama_barang ==
                item.nama_barang
            );

        if (!itemData) {

            console.error(
                "Barang tidak ditemukan:",
                item.nama_barang
            );

            return;
        }

        const subtotal =
            item.qty *
            item.harga_beli;

        const row = `
            <tr>

                <td>

                    <select
                        class="form-control item_id">

                        <option
                            value="${itemData.id}"
                            selected>

                            ${item.nama_barang}

                        </option>

                    </select>

                </td>

                <td>

                    <input
                        type="number"
                        class="form-control qty"
                        value="${item.qty}">

                </td>

                <td>

                    <input
                        type="number"
                        class="form-control harga_beli"
                        value="${item.harga_beli}">

                </td>

                <td class="subtotal">

                    ${subtotal}

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

    });

    calculateGrandTotal();

}

async function savePurchase() {

    // Ambil supplier yang dipilih
    const supplierId = document.getElementById(
        "supplier_id"
    ).value;

    // Ambil tanggal transaksi
    const tanggal = document.getElementById(
        "tanggal"
    ).value;

    // Ambil total pembelian
    const total = document.getElementById(
        "grand-total"
    ).innerText;

    // Menyimpan semua detail barang
    const details = [];

    // Loop setiap baris barang
    document.querySelectorAll(
        "#purchase-items tr"
    ).forEach(row => {

        details.push({

            // ID barang
            item_id: row.querySelector(
                ".item_id"
            ).value,

            // Jumlah barang
            qty: row.querySelector(
                ".qty"
            ).value,

            // Harga beli barang
            harga_beli: row.querySelector(
                ".harga_beli"
            ).value,

            // Total per barang
            subtotal: row.querySelector(
                ".subtotal"
            ).innerText

        });

    });

    Swal.fire({

        title: 'Menyimpan Pembelian...',
    
        allowOutsideClick: false,
    
        didOpen: () => {
    
            Swal.showLoading();
    
        }
    
    });

    // Kirim data ke backend Flask
    const response = await fetch(
        "/purchase/add",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                supplier_id: supplierId,
                tanggal: tanggal,
                total: total,
                details: details

            })
        }
    );

    // Ambil response dari backend
    const result =
    await response.json();

Swal.close();

if (result.status) {

    Swal.fire({

        icon: 'success',

        title: 'Berhasil',

        text: result.message

    }).then(() => {

        location.reload();

    });

} else {

    Swal.fire({

        icon: 'error',

        title: 'Gagal',

        text: result.message

    });

}

    // Tampilkan hasil di console
    console.log(result);


}

// select2
$(document).ready(function () {

    $('#supplier_id').select2({

        placeholder: 'Cari Supplier',

        width: '100%',
        minimumInputLength: 1

    });

});