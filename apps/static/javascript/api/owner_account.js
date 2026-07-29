// **************************************************************
// API ENDPOINT | START
// **************************************************************
const API = {
  view: "/owner-account/view",
  edit: "/owner-account/edit",
  changePassword: "/owner-account/change-password",
};
// **************************************************************
// API ENDPOINT | END
// **************************************************************

// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  initializeEventListeners();

  await loadOwnerAccount();
}
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// FORM ELEMENTS | START
// **************************************************************
const form = {
  account: document.getElementById("owner_account_form"),
  userId: document.getElementById("user_id"),
  ownerName: document.getElementById("owner_name"),
  username: document.getElementById("username"),
  email: document.getElementById("email"),
  saveAccountButton: document.getElementById("save_account_button"),

  password: document.getElementById("owner_password_form"),
  oldPassword: document.getElementById("old_password"),
  newPassword: document.getElementById("new_password"),
  confirmPassword: document.getElementById("confirm_password"),
  savePasswordButton: document.getElementById("save_password_button"),
};
// **************************************************************
// FORM ELEMENTS | END
// **************************************************************

// **************************************************************
// INITIALIZE EVENT LISTENERS | START
// **************************************************************
function initializeEventListeners() {
  form.account.addEventListener("submit", updateOwnerAccount);

  form.password.addEventListener("submit", changeOwnerPassword);

  document.querySelectorAll(".toggle-password").forEach((button) => {
    button.addEventListener("click", togglePassword);
  });
}
// **************************************************************
// INITIALIZE EVENT LISTENERS | END
// **************************************************************

// **************************************************************
// GET OWNER ACCOUNT | START
// **************************************************************
async function loadOwnerAccount() {
  const result = await getRequest(API.view);

  if (!result) return;

  if (result.status_code !== 200) {
    return swalError(result.message);
  }

  renderOwnerAccount(result.data);
}
// **************************************************************
// GET OWNER ACCOUNT | END
// **************************************************************

// **************************************************************
// RENDER OWNER ACCOUNT | START
// **************************************************************
function renderOwnerAccount(data) {
  if (!data) return;

  form.userId.value = data.id ?? "";
  form.ownerName.value = data.owner_name ?? "";
  form.username.value = data.username ?? "";
  form.email.value = data.email ?? "";
}
// **************************************************************
// RENDER OWNER ACCOUNT | END
// **************************************************************

// **************************************************************
// UPDATE OWNER ACCOUNT | START
// **************************************************************
async function updateOwnerAccount(event) {
  event.preventDefault();

  clearAccountValidation();

  const ownerAccount = {
    owner_name: form.ownerName.value.trim(),
    username: form.username.value.trim(),
    email: form.email.value.trim().toLowerCase(),
  };

  const isValid = validateOwnerAccount(ownerAccount);

  if (!isValid) return;

  setButtonLoading(form.saveAccountButton, true, "Menyimpan...");

  try {
    const result = await putRequest(API.edit, ownerAccount);

    if (!result) return;

    if (result.status_code !== 200) {
      return showRequestError(result);
    }

    swalSuccess(result.message || "Data akun berhasil diperbarui.");

    await loadOwnerAccount();
  } finally {
    setButtonLoading(form.saveAccountButton, false, "Simpan Perubahan", "bi-check-circle");
  }
}
// **************************************************************
// UPDATE OWNER ACCOUNT | END
// **************************************************************

// **************************************************************
// CHANGE OWNER PASSWORD | START
// **************************************************************
async function changeOwnerPassword(event) {
  event.preventDefault();

  clearPasswordValidation();

  const passwordData = {
    old_password: form.oldPassword.value,
    new_password: form.newPassword.value,
    confirm_password: form.confirmPassword.value,
  };

  const isValid = validateOwnerPassword(passwordData);

  if (!isValid) return;

  setButtonLoading(form.savePasswordButton, true, "Menyimpan...");

  try {
    const result = await putRequest(API.changePassword, passwordData);

    if (!result) return;

    if (result.status_code !== 200) {
      return showRequestError(result);
    }

    swalSuccess(result.message || "Password berhasil diperbarui.");

    resetPasswordForm();
  } finally {
    setButtonLoading(form.savePasswordButton, false, "Ubah Password", "bi-shield-lock");
  }
}
// **************************************************************
// CHANGE OWNER PASSWORD | END
// **************************************************************

// **************************************************************
// OWNER ACCOUNT VALIDATION | START
// **************************************************************
function validateOwnerAccount(data) {
  let isValid = true;

  if (!data.owner_name) {
    showInputError(form.ownerName, "Nama owner tidak boleh kosong.");

    isValid = false;
  }

  if (!data.username) {
    showInputError(form.username, "Username tidak boleh kosong.");

    isValid = false;
  }

  if (!data.email) {
    showInputError(form.email, "Email tidak boleh kosong.");

    isValid = false;
  } else if (!isValidEmail(data.email)) {
    showInputError(form.email, "Format email tidak valid.");

    isValid = false;
  }

  return isValid;
}
// **************************************************************
// OWNER ACCOUNT VALIDATION | END
// **************************************************************

// **************************************************************
// OWNER PASSWORD VALIDATION | START
// **************************************************************
function validateOwnerPassword(data) {
  let isValid = true;

  if (!data.old_password) {
    showInputError(form.oldPassword, "Password lama tidak boleh kosong.");

    isValid = false;
  }

  if (!data.new_password) {
    showInputError(form.newPassword, "Password baru tidak boleh kosong.");

    isValid = false;
  }

  if (!data.confirm_password) {
    showInputError(form.confirmPassword, "Konfirmasi password tidak boleh kosong.");

    isValid = false;
  }

  if (data.new_password && data.confirm_password && data.new_password !== data.confirm_password) {
    showInputError(form.confirmPassword, "Konfirmasi password baru tidak sesuai.");

    isValid = false;
  }

  if (data.old_password && data.new_password && data.old_password === data.new_password) {
    showInputError(form.newPassword, "Password baru tidak boleh sama dengan password lama.");

    isValid = false;
  }

  return isValid;
}
// **************************************************************
// OWNER PASSWORD VALIDATION | END
// **************************************************************

// **************************************************************
// EMAIL VALIDATION | START
// **************************************************************
function isValidEmail(email) {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  return pattern.test(email);
}
// **************************************************************
// EMAIL VALIDATION | END
// **************************************************************

// **************************************************************
// SHOW INPUT ERROR | START
// **************************************************************
function showInputError(input, message) {
  input.classList.add("is-invalid");

  const feedback = document.getElementById(`${input.id}_feedback`);

  if (feedback) {
    feedback.textContent = message;
  }
}
// **************************************************************
// SHOW INPUT ERROR | END
// **************************************************************

// **************************************************************
// CLEAR ACCOUNT VALIDATION | START
// **************************************************************
function clearAccountValidation() {
  clearInputError(form.ownerName);
  clearInputError(form.username);
  clearInputError(form.email);
}
// **************************************************************
// CLEAR ACCOUNT VALIDATION | END
// **************************************************************

// **************************************************************
// CLEAR PASSWORD VALIDATION | START
// **************************************************************
function clearPasswordValidation() {
  clearInputError(form.oldPassword);
  clearInputError(form.newPassword);
  clearInputError(form.confirmPassword);
}
// **************************************************************
// CLEAR PASSWORD VALIDATION | END
// **************************************************************

// **************************************************************
// CLEAR INPUT ERROR | START
// **************************************************************
function clearInputError(input) {
  input.classList.remove("is-invalid");

  const feedback = document.getElementById(`${input.id}_feedback`);

  if (feedback) {
    feedback.textContent = "";
  }
}
// **************************************************************
// CLEAR INPUT ERROR | END
// **************************************************************

// **************************************************************
// SHOW REQUEST ERROR | START
// **************************************************************
function showRequestError(result) {
  let message = result.message || "Terjadi kesalahan.";

  if (Array.isArray(result.data)) {
    message = result.data.join("<br>");
  }

  return swalError(message);
}
// **************************************************************
// SHOW REQUEST ERROR | END
// **************************************************************

// **************************************************************
// RESET PASSWORD FORM | START
// **************************************************************
function resetPasswordForm() {
  form.password.reset();

  clearPasswordValidation();

  form.oldPassword.type = "password";
  form.newPassword.type = "password";
  form.confirmPassword.type = "password";

  document.querySelectorAll(".toggle-password i").forEach((icon) => {
    icon.className = "bi bi-eye";
  });
}
// **************************************************************
// RESET PASSWORD FORM | END
// **************************************************************

// **************************************************************
// TOGGLE PASSWORD | START
// **************************************************************
function togglePassword(event) {
  const button = event.currentTarget;
  const targetId = button.dataset.target;
  const input = document.getElementById(targetId);
  const icon = button.querySelector("i");

  if (!input) return;

  const isPassword = input.type === "password";

  input.type = isPassword ? "text" : "password";

  if (icon) {
    icon.className = isPassword ? "bi bi-eye-slash" : "bi bi-eye";
  }
}
// **************************************************************
// TOGGLE PASSWORD | END
// **************************************************************

// **************************************************************
// BUTTON LOADING | START
// **************************************************************
function setButtonLoading(button, isLoading, text, icon = "") {
  if (!button) return;

  button.disabled = isLoading;

  if (isLoading) {
    button.innerHTML = `
          <span
            class="spinner-border spinner-border-sm me-1"
            role="status"
            aria-hidden="true"
          ></span>
          ${text}
        `;

    return;
  }

  button.innerHTML = icon ? `<i class="bi ${icon} me-1"></i>${text}` : text;
}
// **************************************************************
// BUTTON LOADING | END
// **************************************************************
