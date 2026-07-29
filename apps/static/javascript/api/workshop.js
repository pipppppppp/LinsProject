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

  if (!result) {
    return;
  }

  if (result.status_code !== 200) {
    await swalError("Gagal", result.message);

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

  // Status Operasional Workshop
  const statusClasses = {
    active: "bg-success",
    inactive: "bg-secondary",
    unsubscribed: "bg-warning text-dark",
    expired: "bg-danger",
  };

  const operationalStatus = workshopData.operational_status || "inactive";

  form.status.textContent = workshopData.operational_status_label || "Tidak Aktif";

  form.status.className = `
    badge
    ${statusClasses[operationalStatus] || "bg-secondary"}
    fs-6
  `;
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

  let result;

  try {
    swalLoading();

    const response = await fetch("/workshop/edit", {
      method: "PUT",
      body: formData,
    });

    result = await processApiResponse(response);
  } catch (error) {
    await swalError("Gagal", error.message);

    return;
  } finally {
    swalClose();
  }

  if (!result) {
    return;
  }

  if (result.status_code === 200) {
    await swalSuccess("Berhasil", result.message);

    form.logo.value = "";

    await loadWorkshop();

    renderWorkshop();
  } else {
    await swalError("Gagal", result.message);
  }
}
// **************************************************************
// SAVE WORKSHOP | END
// **************************************************************
