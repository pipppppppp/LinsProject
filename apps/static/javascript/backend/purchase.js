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

function savePurchase() {

    console.log("Simpan Pembelian");

}

function removeRow(button){

    button.closest("tr").remove();

    calculateGrandTotal();

}