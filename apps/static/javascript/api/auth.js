// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
// Form ID Setup
const form = {
   usermail: document.getElementById("usermail"),
   password: document.getElementById("password"),
};

const reg_form = {
   username: document.getElementById("usermail"),
   email: document.getElementById("usermail"),
   password: document.getElementById("password"),
   retype_password: document.getElementById("password"),
   workshop_name: document.getElementById("workshop_name"),
   workshop_phone: document.getElementById("workshop_phone"),
   workshop_address: document.getElementById("workshop_address"),
};
// **************************************************************
// BASE INISIALIZATION | END
// **************************************************************

// **************************************************************
// SIGN IN PROCESS | START
// **************************************************************
function signin_process(e) {
   e.preventDefault();
   const { usermail, password } = form;

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
      text: "Permintaan kamu sedang diproses",
      button: false,
   });

   // Request API
   fetch(API, request_options)
      .then((http_response) => http_response.json())
      .then((response) => {
         if (response.status_code == 200) {
            swal.fire({
               title: "Login berhasil",
               icon: "success",
            }).then((result) => {
               window.location.replace("/dashboard/");
            });
         } else {
            swal.fire({
               title: `${response.description}`,
               icon: "error",
               buttons: "Kembali",
            }).then((result) => {
               window.location.replace("/auth/signin");
            });
         }
      })
      .catch((error) => {
         swal.fire.close();
         console.error(error);
      });
}
document.getElementById("signin_form").addEventListener("submit", signin_process);
// **************************************************************
// SIGN IN PROCESS | END
// **************************************************************

// **************************************************************
// SIGN IN PROCESS | START
// **************************************************************
function signup_process(e) {
   e.preventDefault();
   const { usermail, password } = form;

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
                  title: "Login berhasil",
                  icon: "success",
               })
               .then((result) => {
                  window.location.replace("/dashboard/");
               });
         } else {
            swal
               .fire({
                  title: `${response.description}`,
                  icon: "error",
                  buttons: "Kembali",
               })
               .then((result) => {
                  window.location.replace("/auth/signin");
               });
         }
      })
      .catch((error) => {
         swal.fire.close();
         console.error(error);
      });
}
document.getElementById("signup_form").addEventListener("submit", signup_process);
// **************************************************************
// SIGN IN PROCESS | END
// **************************************************************
