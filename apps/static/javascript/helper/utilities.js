// **************************************************************
// GET WORKSHOP OPERATIONAL STATUS | START
// **************************************************************
async function getWorkshopOperationalStatus() {
  try {
    const response = await fetch("/workshop/view", {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    const result = await response.json();

    return String(result?.data?.operational_status || "").toLowerCase();
  } catch (error) {
    console.error("WORKSHOP STATUS ERROR:", error);

    return "";
  }
}
// **************************************************************
// GET WORKSHOP OPERATIONAL STATUS | END
// **************************************************************

// **************************************************************
// PROCESS API RESPONSE | START
// **************************************************************
async function processApiResponse(response) {
  let result = null;

  try {
    result = await response.json();
  } catch (error) {
    console.error("INVALID API RESPONSE:", error);

    swalError("Gagal", "Respons server tidak valid.");

    return null;
  }

  const statusCode = Number(result?.status_code || response.status);

  // LANGGANAN TIDAK AKTIF / KEDALUWARSA
  if (statusCode === 402) {
    swalClose();

    const operationalStatus = await getWorkshopOperationalStatus();

    // Bengkel dinonaktifkan administrator
    if (operationalStatus === "inactive") {
      await swalWorkshopInactive("Bengkel sedang dinonaktifkan oleh administrator. Hubungi administrator untuk mengaktifkannya kembali.");

      return null;
    }

    // Belum berlangganan atau kedaluwarsa
    const confirmation = await swalSubscriptionRequired(result.message);

    if (confirmation.isConfirmed) {
      window.location.href = "/subscription/";
    }

    return null;
  }

  return result;
}
// **************************************************************
// PROCESS API RESPONSE | END
// **************************************************************

// **************************************************************
// GET REQUEST | START
// **************************************************************
async function getRequest(url) {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    return await processApiResponse(response);
  } catch (error) {
    swalError("Gagal", "Tidak dapat terhubung ke server.");

    return null;
  }
}
// **************************************************************
// GET REQUEST | END
// **************************************************************

// **************************************************************
// DATATABLE | START
// **************************************************************
let dataTable = null;

function initDataTable(tableId = "#table1") {
  const table = document.querySelector(tableId);

  if (!table) return;

  if (dataTable) {
    dataTable.destroy();
  }

  dataTable = new simpleDatatables.DataTable(table);
}
// **************************************************************
// DATATABLE | END
// **************************************************************

// **************************************************************
// POST REQUEST | START
// **************************************************************
async function postRequest(url, data) {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    return await processApiResponse(response);
  } catch (error) {
    console.error(error);

    return null;
  }
}
// **************************************************************
// POST REQUEST | END
// **************************************************************

// **************************************************************
// UPLOAD REQUEST | START
// **************************************************************
async function uploadRequest(url, formData) {
  try {
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });

    return await processApiResponse(response);
  } catch (error) {
    swalError("Gagal", "Tidak dapat terhubung ke server.");

    return null;
  }
}
// **************************************************************
// UPLOAD REQUEST | END
// **************************************************************

// **************************************************************
// PUT REQUEST | START
// **************************************************************
async function putRequest(url, data) {
  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    return await processApiResponse(response);
  } catch (error) {
    swalError("Gagal", "Tidak dapat terhubung ke server.");

    return null;
  }
}
// **************************************************************
// PUT REQUEST | END
// **************************************************************

// **************************************************************
// DELETE REQUEST | START
// **************************************************************
async function deleteRequest(url, data) {
  try {
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    return await processApiResponse(response);
  } catch (error) {
    swalError("Gagal", "Tidak dapat terhubung ke server.");

    return null;
  }
}
// **************************************************************
// DELETE REQUEST | END
// **************************************************************

// **************************************************************
// CLEAR FORM | START
// **************************************************************
function clearForm(form) {
  form.reset();
}
// **************************************************************
// CLEAR FORM | END
// **************************************************************

// **************************************************************
// RESET INPUT | START
// **************************************************************
function clearValue(...elements) {
  elements.forEach((element) => {
    element.value = "";
  });
}
// **************************************************************
// RESET INPUT | END
// **************************************************************

// **************************************************************
// CLOSE MODAL | START
// **************************************************************
function closeModal(id) {
  const modalElement = document.getElementById(id);

  if (!modalElement) {
    return;
  }

  let modal = bootstrap.Modal.getInstance(modalElement);

  if (!modal) {
    modal = new bootstrap.Modal(modalElement);
  }

  modal.hide();
}
// **************************************************************
// CLOSE MODAL | END
// **************************************************************

// **************************************************************
// RELOAD TABLE | START
// **************************************************************
async function reloadTable(loadData, renderData) {
  if (dataTable) {
    dataTable.destroy();
    dataTable = null;
  }

  await loadData();

  renderData();

  setTimeout(() => {
    initDataTable();
  }, 100);
}
// **************************************************************
// RELOAD TABLE | END
// **************************************************************

// **************************************************************
// OPEN MODAL | START
// **************************************************************
function openModal(id) {
  const modal = new bootstrap.Modal(document.getElementById(id));

  modal.show();
}
// **************************************************************
// OPEN MODAL | END
// **************************************************************

// **************************************************************
// BUTTON LOADING | START
// **************************************************************
function setButtonLoading(button, loading = true) {
  button.disabled = loading;

  button.innerHTML = loading ? '<span class="spinner-border spinner-border-sm"></span> Loading...' : "Simpan";
}
// **************************************************************
// BUTTON LOADING | END
// **************************************************************

// **************************************************************
// DEBOUNCE | START
// **************************************************************
function debounce(callback, delay = 300) {
  let timer;

  return (...args) => {
    clearTimeout(timer);

    timer = setTimeout(() => {
      callback(...args);
    }, delay);
  };
}
// **************************************************************
// DEBOUNCE | END
// **************************************************************

// **************************************************************
// SLEEP | START
// **************************************************************
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
// **************************************************************
// SLEEP | END
// **************************************************************
