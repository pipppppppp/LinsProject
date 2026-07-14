// **************************************************************
// BASE INISIALIZATION | START
// **************************************************************
// Form ID Setup
const signinForm = {
   usermail: document.getElementById("usermail"),
   password: document.getElementById("password"),
};
// Form SIGNUP
const signupForm = {
   username: document.getElementById("username"),
   email: document.getElementById("email"),
   password: document.getElementById("password"),
   confirmPassword: document.getElementById("confirm_password"),
   workshopName: document.getElementById("workshop_name"),
   workshopAddress: document.getElementById("workshop_address"),
   workshopPhone: document.getElementById("workshop_phone"),
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
// SIGN UP | START
// **************************************************************
async function signup() {

   // Request Data ----------------------------------------
   const username = document.getElementById("username").value.trim();
   const email = document.getElementById("email").value.trim();
   const password = document.getElementById("password").value;
   const confirmPassword = document.getElementById("confirm_password").value;
   const workshopName = document.getElementById("workshop_name").value.trim();
   const workshopAddress = document.getElementById("workshop_address").value.trim();
   const workshopPhone = document.getElementById("workshop_phone").value.trim();

   // Validation ----------------------------------------
   if (
       username === "" ||
       email === "" ||
       password === "" ||
       confirmPassword === "" ||
       workshopName === "" ||
       workshopAddress === "" ||
       workshopPhone === ""
   ) {

       Swal.fire({
           icon: "warning",
           title: "Peringatan",
           text: "Semua data wajib diisi.",
           confirmButtonColor: "#435ebe"
       });

       return;
   }

   // Loading ----------------------------------------
   Swal.fire({
       title: "Memproses...",
       text: "Sedang membuat akun...",
       allowOutsideClick: false,
       didOpen: () => {
           Swal.showLoading();
       }
   });

   try {

       const response = await fetch("/auth/signup/account", {
           method: "POST",
           headers: {
               "Content-Type": "application/json"
           },
           body: JSON.stringify({
               username: username,
               email: email,
               password: password,
               retype_password: confirmPassword,
               workshop_name: workshopName,
               workshop_address: workshopAddress,
               workshop_phone: workshopPhone
           })
       });

       Swal.close();

       const result = await response.json();

       if (response.ok) {

           await Swal.fire({
               icon: "success",
               title: "Registrasi Berhasil",
               text: "Silakan login menggunakan akun Anda.",
               timer: 1500,
               showConfirmButton: false
           });

           window.location.href = "/auth/signin";
           return;
       }

       Swal.fire({
           icon: "error",
           title: "Registrasi Gagal",
           text: result.message,
           confirmButtonColor: "#435ebe"
       });

   } catch (error) {

       Swal.close();

       Swal.fire({
           icon: "error",
           title: "Server Error",
           text: "Terjadi kesalahan pada server.",
           confirmButtonColor: "#435ebe"
       });

       console.error(error);

   }

}

document.getElementById("signup_form").addEventListener("submit", signin_process);
// **************************************************************
// SIGN UP | END
// **************************************************************