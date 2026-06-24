// =============================================================
// FUNCTION SAVE SERVICE
// =============================================================

async function saveService() {

    const nama_jasa = document.getElementById("nama_jasa").value;
    const biaya_jasa = document.getElementById("biaya_jasa").value;
    const keterangan = document.getElementById("keterangan").value;

    const response = await fetch("/services/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nama_jasa,
            biaya_jasa,
            keterangan
        })
    });

    const result = await response.json();

    if (result.status) {
        location.reload();
    } else {
        alert(result.message);
    }
}

// =============================================================
// FUNCTION UPDATE SERVICE
// =============================================================

function openEditModal(
    id,
    nama_jasa,
    biaya_jasa,
    keterangan
) {

    document.getElementById("edit_id").value = id;

    document.getElementById("edit_nama_jasa").value =
        nama_jasa;

    document.getElementById("edit_biaya_jasa").value =
        biaya_jasa;

    document.getElementById("edit_keterangan").value =
        keterangan;

    let modal = new bootstrap.Modal(
        document.getElementById("editModal")
    );

    modal.show();
}

async function updateService() {

    const id = document.getElementById(
        "edit_id"
    ).value;

    const nama_jasa = document.getElementById(
        "edit_nama_jasa"
    ).value;

    const biaya_jasa = document.getElementById(
        "edit_biaya_jasa"
    ).value;

    const keterangan = document.getElementById(
        "edit_keterangan"
    ).value;

    const response = await fetch(
        `/services/update/${id}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nama_jasa,
                biaya_jasa,
                keterangan
            })
        }
    );

    const result = await response.json();

    if (result.status) {
        alert("Data berhasil diupdate");
        location.reload();
    } else {
        alert(result.message);
    }
}

// =============================================================
// FUNCTION DELETE SERVICE
// =============================================================

async function deleteService(id) {

    if (!confirm("Yakin hapus data?")) {
        return;
    }

    const response = await fetch(
        `/services/delete/${id}`,
        {
            method: "DELETE"
        }
    );

    const result = await response.json();

    if (result.status) {
        location.reload();
    } else {
        alert(result.message);
    }

}