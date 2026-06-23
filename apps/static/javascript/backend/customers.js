// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);
async function init() {
   await loadCustomers();

   renderTable();
}

// Form ID Setup
const form = {
   title: document.getElementById("modal_label"),
   id: document.getElementById("customer_id"),
   name: document.getElementById("customer_name"),
   address: document.getElementById("customer_address"),
   phone: document.getElementById("customer_phone"),
};
// **************************************************************
// BASE INISIALIZATION | END
// **************************************************************

// **************************************************************
// RENDER DATA TABLES | START
// **************************************************************
// Variable Setup -------------------------------------------------
let customersData = [];

// Get Data -------------------------------------------------
async function loadCustomers() {
   const response = await fetch("/customer/view");
   customersData = await response.json();
}

// Load Data -------------------------------------------------
function renderTable() {
   let html = "";

   customersData.forEach((customer, index) => {
      html += `
            <tr>
                <td>${index + 1}</td>
                <td>${customer.name}</td>
                <td>${customer.address}</td>
                <td>${customer.phone}</td>
                <td>
                    <span class="badge bg-success"> Aktif </span>
                </td>
                <td>
                    <button
                        class="btn btn-warning btn-sm btn-edit" 
                        data-bs-toggle="modal" 
                        data-bs-target="customer_modal"
                        data-id="${customer.id}"> Edit
                    </button>
                    <button
                        class="btn btn-danger btn-sm btn-delete"
                        data-id="${customer.id}"> Hapus
                    </button>
                </td>
            </tr>
        `;
   });

   document.getElementById("customer_table").innerHTML = html;
}
// **************************************************************
// RENDER DATA TABLES | END
// **************************************************************

// **************************************************************
// SAVE CUSTOMER | START
// **************************************************************
async function saveCustomer() {
   const customer_id = form.id.value;
   const customer_name = form.name.value;
   const customer_address = form.address.value;
   const customer_phone = form.phone.value;

   let response;
   if (!customer_id) {
      response = await fetch("/customer/add", {
         method: "POST",
         headers: {
            "Content-Type": "application/json",
         },
         body: JSON.stringify({
            customer_name: customer_name,
            customer_address: customer_address,
            customer_phone: customer_phone,
         }),
      });
   } else {
      response = await fetch(`/customer/update/${customer_id}`, {
         method: "PUT",
         headers: {
            "Content-Type": "application/json",
         },
         body: JSON.stringify({
            customer_name: customer_name,
            customer_address: customer_address,
            customer_phone: customer_phone,
         }),
      });
   }

   const result = await response.json();
   if (result.status) {
      Swal.fire({
         icon: "success",
         title: "Berhasil",
         text: "Member berhasil ditambahkan",
         timer: 1500,
         showConfirmButton: false,
      });

      const option = new Option(result.nama, result.customer_id, true, true);

      $("#customer_id").append(option).trigger("change");

      const modal = bootstrap.Modal.getInstance(document.getElementById("inlineForm"));

      modal.hide();

      document.getElementById("nama").value = "";
      document.getElementById("alamat").value = "";
      document.getElementById("telepon").value = "";
   } else {
      Swal.fire({
         icon: "error",
         title: "Gagal",
         text: result.message,
      });
   }
}
document.querySelector(".btn-save").addEventListener("click", saveCustomer);
// **************************************************************
// SAVE CUSTOMER | END
// **************************************************************


// **************************************************************
// UPDATE & DELETE CUSTOMER | START 
// **************************************************************
document.getElementById("customer_table").addEventListener("click", handleTableClick);
async function handleTableClick(e) {
   const id = Number(e.target.dataset.id);
   if (e.target.classList.contains("btn-edit")) {
      // proses edit
      const customer = customersData.find((p) => p.id === id);

      form.title.textContent = "Ubah Pelanggan";
      form.id.value = customer.id;
      form.name.value = customer.name;
      form.address.value = customer.address;
      form.phone.value = customer.phone;
   } else if (e.target.classList.contains("btn-delete")) {
      // proses delete
      if (!confirm("Yakin hapus data?")) {
         return;
      }

      const response = await fetch(`/customer/delete/${id}`, {
         method: "DELETE",
      });

      const result = await response.json();

      if (result.status) {
         location.reload();
      } else {
         alert(result.message);
      }
   }
}
// **************************************************************
// UPDATE & DELETE CUSTOMER | END 
// **************************************************************
