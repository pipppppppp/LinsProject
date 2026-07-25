// **************************************************************
// SUCCESS ALERT | START
// **************************************************************
function swalSuccess(title = "Berhasil", text = "") {
  return Swal.fire({
    icon: "success",
    title: title,
    text: text,
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
function swalError(title = "Gagal", text = "") {
  return Swal.fire({
    icon: "error",
    title: title,
    text: text,
  });
}
// **************************************************************
// ERROR ALERT | END
// **************************************************************

// **************************************************************
// WARNING ALERT | START
// **************************************************************
function swalWarning(title = "Peringatan", text = "") {
  return Swal.fire({
    icon: "warning",
    title: title,
    text: text,
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
function swalLoading(
  title = "Tunggu Sebentar...",
  text = "Permintaan kamu sedang diproses."
) {
  Swal.fire({
    title: title,
    text: text,
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

// **************************************************************
// CONFIRM ALERT | START
// **************************************************************
async function swalConfirm(title, text, confirmText = "Ya") {
  return await Swal.fire({
    title: title,
    text: text,
    icon: "question",
    showCancelButton: true,
    confirmButtonText: confirmText,
    cancelButtonText: "Batal",
  });
}
// **************************************************************
// CONFIRM ALERT | END
// **************************************************************
