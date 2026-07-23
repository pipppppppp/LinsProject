// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  await loadWorkshop();

  renderWorkshop();
}

// Form ID Setup
const form = {
  name: document.getElementById("workshop_name"),
  phone: document.getElementById("workshop_phone"),
  address: document.getElementById("workshop_address"),
  email: document.getElementById("workshop_email"),
  status: document.getElementById("workshop_status"),
  logo: document.getElementById("workshop_logo"),
  preview: document.getElementById("logo_preview"),
};
// **************************************************************
// BASE INISIALIZATION | END
// **************************************************************


// **************************************************************
// GET WORKSHOP | START
// **************************************************************
// Variable Setup -------------------------------------------------
let workshopData = {};

// Load Data -------------------------------------------------
async function loadWorkshop() {
  const response = await fetch("/workshop/view", {
    method: "GET",
  });

  workshopData = await response.json();
}
// **************************************************************
// GET WORKSHOP | END
// **************************************************************


// **************************************************************
// RENDER DATA | START
// **************************************************************
function renderWorkshop() {
  form.name.value = workshopData.workshop_name ?? "";
  form.phone.value = workshopData.workshop_phone ?? "";
  form.address.value = workshopData.workshop_address ?? "";
  form.email.value = workshopData.workshop_email ?? "";
  form.status.value = workshopData.is_active ?? 1;

  if (workshopData.logo) {
    form.preview.src = `/static/${workshopData.logo}`;
  }
}
// **************************************************************
// RENDER DATA | END
// **************************************************************


// **************************************************************
// SAVE WORKSHOP | START
// **************************************************************
async function saveWorkshop() {
  const body = new FormData();

  body.append("workshop_name", form.name.value);
  body.append("workshop_phone", form.phone.value);
  body.append("workshop_address", form.address.value);
  body.append("workshop_email", form.email.value);
  body.append("is_active", form.status.value);

  if (form.logo.files.length > 0) {
    body.append("logo", form.logo.files[0]);
  }

  const response = await fetch("/workshop/edit", {
    method: "POST",
    body: body,
  });

  const result = await response.json();

  if (result.status) {
    Swal.fire({
      icon: "success",
      title: "Berhasil",
      text: result.message,
    }).then(() => {
      location.reload();
    });
  } else {
    Swal.fire({
      icon: "error",
      title: "Gagal",
      text: result.message,
    });
  }
}

document
  .querySelector(".btn-save")
  .addEventListener("click", saveWorkshop);
// **************************************************************
// SAVE WORKSHOP | END
// **************************************************************


// **************************************************************
// PREVIEW LOGO | START
// **************************************************************
form.logo.addEventListener("change", function () {
  if (this.files.length > 0) {
    form.preview.src = URL.createObjectURL(this.files[0]);
  }
});
// **************************************************************
// PREVIEW LOGO | END
// **************************************************************