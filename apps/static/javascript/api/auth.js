// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
// Form ID Setup
const signinForm = {
  usermail: document.getElementById("usermail"),
  password: document.getElementById("password"),
};
// **************************************************************
// BASE INISIALIZATION | END
// **************************************************************

// **************************************************************
// SIGN IN PROCESS | START
// **************************************************************
function signin_process(e) {
  e.preventDefault();
  const { usermail, password } = signinForm;

  // Set API Request Configuration
  const API = "/auth/signin/account";
  const my_headers = new Headers();
  const raw = JSON.stringify({
    usermail: usermail.value,
    password: password.value,
  });

  my_headers.append("Content-Type", "application/json");
  const request_options = {
    method: "POST",
    headers: my_headers,
    body: raw,
    redirect: "follow",
  };

  // Tampilkan loading langsung
  swalLoading("Tunggu Sebentar...", "Permintaan kamu sedang diproses.");
  fetch(API, request_options)
    .then((http_response) => http_response.json())

    .then((response) => {
      console.log("LOGIN RESPONSE:", response);
      if (response.status_code == 200) {
        // Biarkan loading terlihat sebentar
        console.log("LOGIN BERHASIL");
        console.log(response.data);
        localStorage.setItem("username", response.data.name);
        setTimeout(() => {
          signin_redirect(response.data.role);
        }, 500);
      } else {
        swalClose();

        if (response.status_code === 403) {
          swalWarning("Akun Tidak Dapat Digunakan", response.message);
        } else {
          swalError("Login Gagal", response.message);
        }
      }
    })
    .catch((error) => {
      swalClose();
      console.error(error);
      swalError("Login Gagal", "Terjadi kesalahan pada server.");
    });
}
const signin = document.getElementById("signin_form");
if (signin) {
  signin.addEventListener("submit", signin_process);
}
// document.getElementById("signin_form").addEventListener("submit", signin_process);
// **************************************************************
// SIGN IN PROCESS | END
// **************************************************************

// **************************************************************
// SIGN UP PROCESS | START
// **************************************************************
const reg_form = {
  owner_name: document.getElementById("owner_name"),
  username: document.getElementById("username"),
  email: document.getElementById("email"),
  password: document.getElementById("password"),
  retype_password: document.getElementById("retype_password"),
  workshop_name: document.getElementById("workshop_name"),
  workshop_address: document.getElementById("workshop_address"),
  workshop_phone: document.getElementById("workshop_phone"),
};
function signup_process(e) {
  e.preventDefault();
  const { owner_name, username, email, password, retype_password, workshop_name, workshop_phone, workshop_address } = reg_form;

  // Set API Request Configuration
  const API = "/auth/signup/account";
  const my_headers = new Headers();
  const raw = JSON.stringify({
    owner_name: owner_name.value,
    username: username.value,
    email: email.value,
    password: password.value,
    retype_password: retype_password.value,
    workshop_name: workshop_name.value,
    workshop_phone: workshop_phone.value,
    workshop_address: workshop_address.value,
  });

  my_headers.append("Content-Type", "application/json");
  const request_options = {
    method: "POST",
    headers: my_headers,
    body: raw,
    redirect: "follow",
  };

  // Set Loading UI
  swalLoading("Tunggu Sebentar...", "Permintaan kamu sedang diproses.");

  // Request API
  fetch(API, request_options)
    .then((http_response) => http_response.json())
    .then((response) => {
      if (response.status_code == 200) {
        swalSuccess("Registrasi Berhasil", "Registrasi berhasil. Silakan periksa email untuk melakukan verifikasi akun.").then(() => {
          window.location.replace("/auth/signin");
        });
      } else {
        swalClose();

        swalError("Registrasi Gagal", response.message);
      }
    })
    .catch((error) => {
      swalClose();
      console.error(error);

      swalError("Registrasi Gagal", "Terjadi kesalahan pada server.");
    });
}
const signup = document.getElementById("signup_form");
if (signup) {
  signup.addEventListener("submit", signup_process);
}
// document.getElementById("signup_form").addEventListener("submit", signup_process);
// **************************************************************
// SIGN UP PROCESS | END
// **************************************************************

// **************************************************************
// SIGN IN REDIRECT | START
// **************************************************************
function signin_redirect(role) {
  if (role == 0) {
    window.location.replace("/dashboard-administrator/");
  } else if (role == 1) {
    window.location.replace("/dashboard/");
  } else if (role == 2) {
    window.location.replace("/dashboard-cashier/");
  }
}
// **************************************************************
// SIGN IN REDIRECT | END
// **************************************************************

// **************************************************************
// FORGOT PASSWORD PROCESS | START
// **************************************************************
const forgotPasswordForm = {
  email: document.getElementById("email"),
};

function forgot_password_process(e) {
  e.preventDefault();

  const { email } = forgotPasswordForm;

  // Set API Request Configuration
  const API = "/auth/forgot-password";
  const my_headers = new Headers();

  const raw = JSON.stringify({
    email: email.value,
  });

  my_headers.append("Content-Type", "application/json");

  const request_options = {
    method: "POST",
    headers: my_headers,
    body: raw,
    redirect: "follow",
  };

  // Set Loading UI
  swalLoading("Tunggu Sebentar...", "Link reset password sedang dikirim.");

  // Request API
  fetch(API, request_options)
    .then((http_response) => http_response.json())
    .then((response) => {
      if (response.status_code == 200) {
        swalSuccess("Email Berhasil Dikirim", response.message).then(() => {
          window.location.replace("/auth/signin");
        });
      } else {
        swalClose();

        swalError("Gagal Mengirim Email", response.message);
      }
    })
    .catch((error) => {
      swalClose();
      console.error(error);

      swalError("Gagal Mengirim Email", "Terjadi kesalahan pada server.");
    });
}

const forgotPassword = document.getElementById("forgot_password_form");

if (forgotPassword) {
  forgotPassword.addEventListener("submit", forgot_password_process);
}
// **************************************************************
// FORGOT PASSWORD PROCESS | END
// **************************************************************

// **************************************************************
// RESET PASSWORD PROCESS | START
// **************************************************************
const resetPasswordForm = {
  token: document.getElementById("reset_token"),
  password: document.getElementById("new_password"),
  retype_password: document.getElementById("retype_password"),
};

function reset_password_process(e) {
  e.preventDefault();

  const { token, password, retype_password } = resetPasswordForm;

  // Password Validation
  if (password.value !== retype_password.value) {
    swalError("Reset Password Gagal", "Konfirmasi password tidak sesuai.");

    return;
  }

  // Set API Request Configuration
  const API = `/auth/reset-password/${encodeURIComponent(token.value)}`;

  const my_headers = new Headers();

  const raw = JSON.stringify({
    password: password.value,
    retype_password: retype_password.value,
  });

  my_headers.append("Content-Type", "application/json");

  const request_options = {
    method: "PUT",
    headers: my_headers,
    body: raw,
    redirect: "follow",
  };

  // Set Loading UI
  swalLoading("Tunggu Sebentar...", "Password sedang diperbarui.");

  // Request API
  fetch(API, request_options)
    .then((http_response) => http_response.json())
    .then((response) => {
      if (response.status_code == 200) {
        swalSuccess("Password Berhasil Diubah", response.message).then(() => {
          window.location.replace("/auth/signin");
        });
      } else {
        swalClose();

        swalError("Reset Password Gagal", response.message);
      }
    })
    .catch((error) => {
      swalClose();
      console.error(error);

      swalError("Reset Password Gagal", "Terjadi kesalahan pada server.");
    });
}

const resetPassword = document.getElementById("reset_password_form");

if (resetPassword) {
  resetPassword.addEventListener("submit", reset_password_process);
}
// **************************************************************
// RESET PASSWORD PROCESS | END
// **************************************************************

// **************************************************************
// SIGN OUT PROCESS | START
// **************************************************************
async function logout_process(event) {
  event.preventDefault();

  const result = await swalConfirm("Logout", "Apakah Anda yakin ingin keluar dari aplikasi?", "Ya, Logout");

  if (result.isConfirmed) {
    await swalSuccess("Anda telah keluar dari aplikasi.");

    window.location.href = "/auth/signout";
  }
}

const logout = document.getElementById("logout");

if (logout) {
  logout.addEventListener("click", logout_process);
}
// **************************************************************
// SIGN OUT PROCESS | END
// **************************************************************
