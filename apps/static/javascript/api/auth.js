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
          signin_prosess(response.data.role);
        }, 500);
      } else {
        swalClose();

        if (response.status_code === 403) {
          swalWarning(response.error, response.message);
        } else {
          swalError(response.error, response.message);
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
        swalSuccess("Registrasi Berhasil", "Silakan login menggunakan akun yang telah didaftarkan.").then(() => {
          window.location.replace("/auth/signin");
        });
      } else {
        swalError("Registrasi Gagal", response.message).then(() => {
          window.location.replace("/auth/signup");
        });
      }
    })
    .catch((error) => {
      swal.fire.close();
      console.error(error);
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
// SIGN IN PROCESS | START
// **************************************************************
function signin_prosess(role) {
  if (role == 0) {
    window.location.replace("/dashboard-administrator/");
  } else if (role == 1) {
    window.location.replace("/dashboard/");
  } else if (role == 2) {
    window.location.replace("/dashboard-cashier/");
  }
}
// **************************************************************
// SIGN IN PROCESS | END
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
