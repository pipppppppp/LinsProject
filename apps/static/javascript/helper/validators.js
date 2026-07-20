// **************************************************************
// REQUIRED VALIDATION | START
// **************************************************************
function required(value, message) {

  if (value === null || value === undefined) {
      swalWarning(message);
      return false;
  }

  if (String(value).trim() === "") {
      swalWarning(message);
      return false;
  }

  return true;
}
// **************************************************************
// REQUIRED VALIDATION | END
// **************************************************************

// **************************************************************
// EMAIL VALIDATION | START
// **************************************************************
function email(emailAddress) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!regex.test(emailAddress)) {
    swalWarning("Email tidak valid.");
    return false;
  }

  return true;
}
// **************************************************************
// EMAIL VALIDATION | END
// **************************************************************

// **************************************************************
// PASSWORD VALIDATION | START
// **************************************************************
function password(password) {
  if (password.length < 8) {
    swalWarning("Password minimal 8 karakter.");
    return false;
  }

  return true;
}
// **************************************************************
// PASSWORD VALIDATION | END
// **************************************************************

// **************************************************************
// CONFIRM PASSWORD | START
// **************************************************************
function confirmPassword(password, confirmPassword) {
  if (password !== confirmPassword) {
    swalWarning("Konfirmasi password tidak sama.");
    return false;
  }

  return true;
}
// **************************************************************
// CONFIRM PASSWORD | END
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
// POSITIVE NUMBER | START
// **************************************************************
function positiveNumber(value, message) {
  if (Number(value) <= 0) {
    swalWarning(message);
    return false;
  }

  return true;
}
// **************************************************************
// POSITIVE NUMBER | END
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

// **************************************************************
// VEHICLE VALIDATION | START
// **************************************************************
function validateVehicle(vehicle) {
  if (!required(vehicle.plate_number, "Plat nomor wajib diisi")) return false;

  if (!plate(vehicle.plate_number)) return false;

  if (!required(vehicle.vehicle_brand, "Merek kendaraan wajib diisi")) return false;

  if (!required(vehicle.vehicle_type, "Tipe kendaraan wajib diisi")) return false;

  if (!required(vehicle.vehicle_year, "Tahun kendaraan wajib diisi")) return false;

  if (!year(vehicle.vehicle_year)) return false;

  if (!required(vehicle.vehicle_color, "Warna kendaraan wajib diisi")) return false;

  return true;
}
// **************************************************************
// VEHICLE VALIDATION | END
// **************************************************************

// **************************************************************
// CATEGORY VALIDATION | START
// **************************************************************
function validateCategory(category) {
  if (!required(category.category_name, "Nama kategori wajib diisi")) {
    return false;
  }

  return true;
}
// **************************************************************
// CATEGORY VALIDATION | END
// **************************************************************

// **************************************************************
// SUPPLIER VALIDATION | START
// **************************************************************
// **************************************************************
// SUPPLIER VALIDATION | START
// **************************************************************
function validateSupplier(supplier) {
  if (!required(supplier.name, "Nama supplier wajib diisi")) return false;

  if (!required(supplier.address, "Alamat wajib diisi")) return false;

  if (!required(supplier.phone, "Nomor telepon wajib diisi")) return false;

  if (!phone(supplier.phone)) return false;

  return true;
}
// **************************************************************
// SUPPLIER VALIDATION | END
// **************************************************************

// **************************************************************
// PRODUCT VALIDATION | START
// **************************************************************
function validateProduct(product) {

  if (!required(product.product_name, "Nama barang wajib diisi")) return false;

  if (!required(product.price, "Harga jual wajib diisi")) return false;

  if (!price(product.price, "Harga jual tidak valid")) return false;

  if (!required(product.purchase, "Harga beli wajib diisi")) return false;

  if (!price(product.purchase, "Harga beli tidak valid")) return false;

  if (!required(product.stock, "Stok wajib diisi")) return false;

  if (!stock(product.stock)) return false;

  return true;
}
// **************************************************************
// PRODUCT VALIDATION | END
// **************************************************************

// **************************************************************
// SERVICE VALIDATION | START
// **************************************************************
function validateService(service) {

  if (!required(service.name, "Nama jasa wajib diisi")) return false;

  if (!required(service.service_fee, "Biaya jasa wajib diisi")) return false;

  if (!price(service.service_fee, "Biaya jasa tidak valid")) return false;

  return true;
}
// **************************************************************
// SERVICE VALIDATION | END
// **************************************************************