// # ============================================================== 
// # FUNGSION SAVE CATEGORY - START
// # ============================================================== 
async function saveCategory() {

    const category =
        document.getElementById("category").value;

    const response = await fetch("/category/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            category: category
        })
    });

    const result = await response.json();

    if(result.status){
        alert(result.message);
        location.reload();
    }
}
// # ============================================================== 
// # FUNGSION SAVE CATEGORY - END
// # ============================================================== 

// # ============================================================== 
// # FUNGSION UPDATE CATEGORY - START
// # ============================================================== 

function openEditModal(id, category) {
    document.getElementById("edit_id").value = id;
    document.getElementById("edit_category").value = category;

    let modal = new bootstrap.Modal(
        document.getElementById("editModal")
    );

    modal.show();
}

async function updateCategory() {

    const id = document.getElementById("edit_id").value;

    const category =
        document.getElementById("edit_category").value;

    const response = await fetch(`/category/update/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            category
        })
    });

    const result = await response.json();

    if(result.status){
        alert(result.message);
        location.reload();
    }else{
        alert(result.message);
    }
}
// # ============================================================== 
// # FUNGSION UPDATE CATEGORY - END
// # ============================================================== 

// # ============================================================== 
// # FUNGSION DELETE CATEGORY - START
// # ============================================================== 

async function deleteCategory(id){

    if(!confirm("Yakin hapus data?")){
        return;
    }

    const response = await fetch(`/category/delete/${id}`, {
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
// # FUNGSION DELETE CATEGORY - END
// # ============================================================== 