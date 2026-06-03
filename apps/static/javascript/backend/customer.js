// # ============================================================== 
// # FUNGSION SAVE CUSTOMERS - START
// # ============================================================== 

async function saveCustomer() {

    const nama = document.getElementById("nama").value;
    const alamat = document.getElementById("alamat").value;
    const telepon = document.getElementById("telepon").value;

    const response = await fetch("/customer/add", {
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
// # FUNGSION SAVE CUSTOMERS - END
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

// # ============================================================== 
// # FUNGSION UPDATE CUSTOMERS - START
// # ============================================================== 

async function updateCustomer(id) {

    const nama = document.getElementById("edit_nama").value;
    const alamat = document.getElementById("edit_alamat").value;
    const telepon = document.getElementById("edit_telepon").value;

    const response = await fetch(`/customer/update/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nama: nama,
            alamat: alamat,
            telepon: telepon
        })
    });

    // const result = await response.json();
    const result = await response.text();
    console.log(result);

    if(result.status){
        alert("Data berhasil diupdate");
        location.reload();
    }else{
        alert(result.message);
    }
}
// # ============================================================== 
// # FUNGSION UPDATE CUSTOMERS - START
// # ============================================================== 

