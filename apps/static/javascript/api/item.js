// # ============================================================== 
// # FUNGSION SAVE ITEMS - START
// # ============================================================== 

async function saveItem() {

    const category_id = document.getElementById("category_id").value;
    const nama_barang = document.getElementById("nama_barang").value;
    const stok = document.getElementById("stok").value;
    const harga_beli = document.getElementById("harga_beli").value;
    const harga_jual = document.getElementById("harga_jual").value;

    const response = await fetch("/item/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            category_id,
            nama_barang,
            stok,
            harga_beli,
            harga_jual
        })
    });

    const result = await response.json();

    if (result.status) {
        location.reload();
    } else {
        alert(result.message);
    }
}
// # ============================================================== 
// # FUNGSION SAVE ITEMS - END
// # ============================================================== 

// # ============================================================== 
// # FUNGSION UPDATE ITEMS - START
// # ============================================================== 

function openEditModal(id,
    category_id,
    nama_barang,
    stok,
    harga_beli,
    harga_jual) {

    document.getElementById("edit_id").value = id;
    document.getElementById("edit_category_id").value = category_id;
    document.getElementById("edit_nama_barang").value = nama_barang;
    document.getElementById("edit_stok").value = stok;
    document.getElementById("edit_harga_beli").value = harga_beli;
    document.getElementById("edit_harga_jual").value = harga_jual;

    let modal = new bootstrap.Modal(
        document.getElementById("editModal")
    );

    modal.show();
}

async function updateItem() {

    const id = document.getElementById("edit_id").value;

    const category_id = document.getElementById("edit_category_id").value;
    const nama_barang = document.getElementById("edit_nama_barang").value;
    const stok = document.getElementById("edit_stok").value;
    const harga_beli = document.getElementById("edit_harga_beli").value;
    const harga_jual = document.getElementById("edit_harga_jual").value;

    const response = await fetch(`/item/update/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            category_id,
            nama_barang,
            stok,
            harga_beli,
            harga_jual
        })
    });

    const result = await response.json();

    if(result.status){
        alert("Data berhasil diupdate");
        location.reload();
    }else{
        alert(result.message);
    }
}
// # ============================================================== 
// # FUNGSION UPDATE ITEMS - END
// # ============================================================== 

// # ============================================================== 
// # FUNGSION DELETE ITEMS - START
// # ============================================================== 

async function deleteItem(id){

    if(!confirm("Yakin hapus data?")){
        return;
    }

    const response = await fetch(`/item/delete/${id}`, {
        method: "DELETE"
    });

    const result = await response.json();

    if(result.status){
        location.reload();
    }else{
        alert(result.message);
    }
}
// # ============================================================== 
// # FUNGSION DELETE ITEMS - END
// # ============================================================== 