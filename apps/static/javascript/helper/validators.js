// **************************************************************
// REQUIRED VALIDATION | START
// **************************************************************
function required(value, message) {
  if (value.trim() === "") {
    swalWarning(message);
    return false;
  }

  return true;
}
// **************************************************************
// REQUIRED VALIDATION | END
// **************************************************************

// **************************************************************
// PHONE VALIDATION | START
// **************************************************************
function phone(phoneNumber) {
  const regex = /^[0-9]{6,16}$/;

  if (!regex.test(phoneNumber)) {
    swalWarning("Nomor telepon tidak valid.");
    return false;
  }

  return true;
}
// **************************************************************
// PHONE VALIDATION | END
// **************************************************************

// **************************************************************
// PLATE NUMBER VALIDATION | START
// **************************************************************
function plate(plateNumber) {
  const regex = /^[A-Za-z0-9\s-]{5,15}$/;

  if (!regex.test(plateNumber)) {
    swalWarning("Plat nomor tidak valid.");
    return false;
  }

  return true;
}
// **************************************************************
// PLATE NUMBER VALIDATION | END
// **************************************************************

// **************************************************************
// NUMBER VALIDATION | START
// **************************************************************
function number(value, message) {
  if (isNaN(value)) {
    swalWarning(message);
    return false;
  }

  return true;
}
// **************************************************************
// NUMBER VALIDATION | END
// **************************************************************

// **************************************************************
// YEAR VALIDATION | START
// **************************************************************
function year(vehicleYear) {
  const currentYear = new Date().getFullYear();

  if (isNaN(vehicleYear)) {
    swalWarning("Tahun kendaraan harus berupa angka.");
    return false;
  }

  if (vehicleYear < 1980 || vehicleYear > currentYear) {
    swalWarning("Tahun kendaraan tidak valid.");
    return false;
  }

  return true;
}
// **************************************************************
// YEAR VALIDATION | END
// **************************************************************

// **************************************************************
// PRICE VALIDATION | START
// **************************************************************
function price(value, message) {
  if (isNaN(value) || Number(value) < 0) {
    swalWarning(message);
    return false;
  }

  return true;
}
// **************************************************************
// PRICE VALIDATION | END
// **************************************************************

// **************************************************************
// STOCK VALIDATION | START
// **************************************************************
function stock(value) {
  if (isNaN(value) || Number(value) < 0) {
    swalWarning("Stok tidak valid.");
    return false;
  }

  return true;
}
// **************************************************************
// STOCK VALIDATION | END
// **************************************************************

// **************************************************************
// CUSOMER VALIDATION | START
// **************************************************************
function validateCustomer(customer) {
  if (!required(customer.customer_name, "Nama customer wajib diisi")) return false;

  if (!required(customer.customer_address, "Alamat wajib diisi")) return false;

  if (!required(customer.customer_phone, "Nomor telepon wajib diisi")) return false;

  if (!phone(customer.customer_phone)) return false;

  return true;
}
// **************************************************************
// CUSOMER VALIDATION | END
// **************************************************************
