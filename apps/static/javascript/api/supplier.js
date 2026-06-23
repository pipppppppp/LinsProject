// # ============================================================== 
// # FUNGSION SAVE SUPPLIER - START
// # ============================================================== 

async function saveSupplier() {

    const nama = document.getElementById("nama").value;
    const alamat = document.getElementById("alamat").value;
    const telepon = document.getElementById("telepon").value;

    const response = await fetch("/supplier/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nama,
            alamat,
            telepon
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
// # FUNGSION SAVE SUPPLIER - END
// # ============================================================== 

// # ============================================================== 
// # FUNGSION UPDATE SUPPLIER - START
// # ============================================================== 

function openEditModal(id, nama, alamat, telepon) {

    document.getElementById("edit_id").value = id;
    document.getElementById("edit_nama").value = nama;
    document.getElementById("edit_alamat").value = alamat;
    document.getElementById("edit_telepon").value = telepon;

    let modal = new bootstrap.Modal(
        document.getElementById("editModal")
    );

    modal.show();
}

async function updateSupplier() {

    const id = document.getElementById("edit_id").value;

    const nama = document.getElementById("edit_nama").value;
    const alamat = document.getElementById("edit_alamat").value;
    const telepon = document.getElementById("edit_telepon").value;

    console.log("UPDATE ID =", id);

    const response = await fetch(`/supplier/update/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nama,
            alamat,
            telepon
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
// # FUNGSION UPDATE SUPPLIER - END
// # ============================================================== 

// # ============================================================== 
// # FUNGSION DELETE SUPPLIER - START
// # ============================================================== 

async function deleteSupplier(id){

    if(!confirm("Yakin hapus data?")){
        return;
    }

    const response = await fetch(`/supplier/delete/${id}`, {
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
// # FUNGSION DELETE SUPPLIER - END
// # ============================================================== 