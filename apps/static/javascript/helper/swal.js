// **************************************************************
// SUCCESS ALERT | START
// **************************************************************
function swalSuccess(message) {
   return Swal.fire({
      icon: "success",
      title: "Berhasil",
      text: message,
      timer: 1500,
      showConfirmButton: false,
   });
}
// **************************************************************
// SUCCESS ALERT | END
// **************************************************************

// **************************************************************
// ERROR ALERT | START
// **************************************************************
function swalError(message) {
   return Swal.fire({
      icon: "error",
      title: "Gagal",
      text: message,
   });
}
// **************************************************************
// ERROR ALERT | END
// **************************************************************

// **************************************************************
// WARNING ALERT | START
// **************************************************************
function swalWarning(message) {
   return Swal.fire({
      icon: "warning",
      title: "Peringatan",
      text: message,
   });
}
// **************************************************************
// WARNING ALERT | END
// **************************************************************

// **************************************************************
// DELETE ALERT | START
// **************************************************************
async function swalDelete() {
   return await Swal.fire({
      title: "Hapus Data?",
      text: "Data yang dihapus tidak dapat dikembalikan.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Ya, Hapus",
      cancelButtonText: "Batal",
   });
}
// **************************************************************
// DELETE ALERT | END
// **************************************************************

// **************************************************************
// LOADING ALERT | START
// **************************************************************
function swalLoading(message = "Memproses...") {

      Swal.fire({
          title: message,
          allowOutsideClick: false,
          didOpen: () => {
              Swal.showLoading();
          },
      });
  
  }
  // **************************************************************
  // LOADING ALERT | END
  // **************************************************************
  
  // **************************************************************
// CLOSE LOADING | START
// **************************************************************
function swalClose() {
      Swal.close();
  }
  // **************************************************************
  // CLOSE LOADING | END
  // **************************************************************