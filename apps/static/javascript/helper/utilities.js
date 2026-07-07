// **************************************************************
// GET REQUEST | START
// **************************************************************
async function getRequest(url) {
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  return await response.json();
}
// **************************************************************
// GET REQUEST | END
// **************************************************************

// **************************************************************
// POST REQUEST | START
// **************************************************************
async function postRequest(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return await response.json();
}
// **************************************************************
// POST REQUEST | END
// **************************************************************

// **************************************************************
// PUT REQUEST | START
// **************************************************************
async function putRequest(url, data) {
  const response = await fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return await response.json();
}
// **************************************************************
// PUT REQUEST | END
// **************************************************************

// **************************************************************
// DELETE REQUEST | START
// **************************************************************
async function deleteRequest(url) {
  const response = await fetch(url, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });

  return await response.json();
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
  await loadData();

  renderData();
}
// **************************************************************
// RELOAD TABLE | END
// **************************************************************
