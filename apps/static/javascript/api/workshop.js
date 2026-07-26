// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  await loadWorkshop();

  renderWorkshop();
}
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// FORM SETUP | START
// **************************************************************
const form = {
  id: document.getElementById("workshop_id"),

  logo: document.getElementById("workshop_logo"),

  preview: document.getElementById("preview_logo"),

  name: document.getElementById("workshop_name"),

  email: document.getElementById("workshop_email"),

  phone: document.getElementById("workshop_phone"),

  address: document.getElementById("workshop_address"),

  status: document.getElementById("workshop_status"),
};
// **************************************************************
// FORM SETUP | END
// **************************************************************

// **************************************************************
// GET WORKSHOP | START
// **************************************************************
let workshopData = null;
async function loadWorkshop() {
  const result = await getRequest("/workshop/view");

  if (result.status_code !== 200) {
    await swalError(result.message);

    return;
  }

  workshopData = result.data;
}
// **************************************************************
// GET WORKSHOP | END
// **************************************************************

// **************************************************************
// RENDER WORKSHOP | START
// **************************************************************
function renderWorkshop() {
  if (!workshopData) {
    return;
  }

  form.id.value = workshopData.id ?? "";

  form.name.value = workshopData.workshop_name ?? "";

  form.email.value = workshopData.workshop_email ?? "";

  form.phone.value = workshopData.workshop_phone ?? "";

  form.address.value = workshopData.workshop_address ?? "";

  // Status
  form.status.textContent = workshopData.is_active == 1 ? "Aktif" : "Tidak Aktif";

  form.status.className = workshopData.is_active == 1 ? "badge bg-success fs-6" : "badge bg-danger fs-6";

  // Logo
  if (workshopData.logo) {
    form.preview.src = `/static/images/profiles/${workshopData.logo}`;
  } else {
    form.preview.src = "/static/images/profiles/default-workshop.png";
  }
}
// **************************************************************
// RENDER WORKSHOP | END
// **************************************************************

// **************************************************************
// PREVIEW LOGO | START
// **************************************************************
form.logo.addEventListener("change", previewLogo);

function previewLogo() {
  const file = form.logo.files[0];

  if (!file) return;

  if (!file.type.startsWith("image/")) {
    swalWarning("File harus berupa gambar.");

    form.logo.value = "";

    return;
  }

  form.preview.src = URL.createObjectURL(file);
}
// **************************************************************
// PREVIEW LOGO | END
// **************************************************************

// **************************************************************
// SAVE WORKSHOP | START
// **************************************************************
document.querySelector(".btn-save").addEventListener("click", saveWorkshop);

async function saveWorkshop() {
  const formData = new FormData();

  formData.append("workshop_name", form.name.value.trim());
  formData.append("workshop_email", form.email.value.trim());
  formData.append("workshop_phone", form.phone.value.trim());
  formData.append("workshop_address", form.address.value.trim());

  if (form.logo.files.length > 0) {
    formData.append("logo", form.logo.files[0]);
  }

  swalLoading();

  try {
    const response = await fetch("/workshop/edit", {
      method: "PUT",
      body: formData,
    });

    const result = await response.json();

    swalClose();

    if (response.ok) {
      swalSuccess("Profil bengkel berhasil diperbarui.");

      await loadWorkshop();
    } else {
      swalError(result.message);
    }
  } catch (error) {
    swalClose();
    swalError(error.message);
  }
}
// **************************************************************
// SAVE WORKSHOP | END
// **************************************************************
