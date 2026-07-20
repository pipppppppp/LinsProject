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

  // Set Loading UI
  swal.fire({
    title: "Tunggu Sebentar..",
    text: "Permintaan kamu sedang diproses.",
    button: false,
  });

  // Request API
  fetch(API, request_options)
    .then((http_response) => http_response.json())
    .then((response) => {
      console.log(response);
      console.log("Role:", response.role);
      console.log("Data:", response.data);

      if (response.status_code == 200) {
        swal
          .fire({
            title: "Login berhasil",
            icon: "success",
          })
          .then((result) => {
            const role = response.data.role;

            console.log(role);

            if (role == 0) {
              window.location.replace("/administrator/dashboard");
            } else if (role == 1) {
              window.location.replace("/dashboard/");
            } else if (role == 2) {
              window.location.replace("/cashier/");
            }
          });
      } else {
        if (response.status_code === 403) {
          swal.fire({
            title: response.error,
            text: response.message,
            icon: "warning",
          });
        } else {
          swal.fire({
            title: response.error,
            text: response.message,
            icon: "error",
          });
        }
      }
    })
    .catch((error) => {
      swal.fire.close();
      console.error(error);
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
  const {owner_name, username, email, password, retype_password, workshop_name, workshop_phone, workshop_address } = reg_form;

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
  swal.fire({
    title: "Tunggu Sebentar..",
    text: "Permintaan kamu sedang diproses",
    button: false,
  });

  // Request API
  fetch(API, request_options)
    .then((http_response) => http_response.json())
    .then((response) => {
      if (response.status_code == 200) {
        swal
          .fire({
            title: "Registrasi berhasil",
            icon: "success",
          })
          .then((result) => {
            window.location.replace("/auth/signin");
          });
      } else {
        swal
          .fire({
            title: response.message,
            icon: "error",
            buttons: "Kembali",
          })
          .then((result) => {
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
