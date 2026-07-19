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

    return await response.json();
  } catch (error) {
    swalError("Tidak dapat terhubung ke server.");

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

    return await response.json();
  } catch (error) {
    swalError("Tidak dapat terhubung ke server.");

    return null;
  }
}
// **************************************************************
// POST REQUEST | END
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

    return await response.json();
  } catch (error) {
    swalError("Tidak dapat terhubung ke server.");

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

    return await response.json();
  } catch (error) {
    swalError("Tidak dapat terhubung ke server.");

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
  bootstrap.Modal.getInstance(document.getElementById(id)).hide();
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
