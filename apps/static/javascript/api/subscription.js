// **************************************************************
// BASE INITIALIZATION | START
// **************************************************************
document.addEventListener("DOMContentLoaded", init);

async function init() {
  let subscriptionData = await loadSubscriptionStatus();

  const latestStatus = String(subscriptionData?.latest_payment?.transaction_status || "").toLowerCase();

  // Sinkronkan transaksi yang masih pending
  if (latestStatus === "pending") {
    await syncPaymentStatus(false);

    subscriptionData = await loadSubscriptionStatus();
  }

  // Ambil seluruh riwayat pembayaran
  await loadSubscriptionHistory();

  const payButton = document.getElementById("btn_pay_subscription");

  if (payButton) {
    payButton.addEventListener("click", createSubscriptionPayment);
  }
}
// **************************************************************
// BASE INITIALIZATION | END
// **************************************************************

// **************************************************************
// ELEMENT SETUP | START
// **************************************************************
const subscriptionElement = {
  status: document.getElementById("subscription_status"),
  workshopName: document.getElementById("subscription_workshop_name"),
  subscriptionEnd: document.getElementById("subscription_end"),
  remainingDays: document.getElementById("remaining_days"),
  alert: document.getElementById("subscription_alert"),
  message: document.getElementById("subscription_message"),
  payButton: document.getElementById("btn_pay_subscription"),
};

const paymentElement = {
  card: document.getElementById("latest_payment_card"),
  orderId: document.getElementById("latest_order_id"),
  amount: document.getElementById("latest_amount"),
  paymentType: document.getElementById("latest_payment_type"),
  transactionStatus: document.getElementById("latest_transaction_status"),
  paidAt: document.getElementById("latest_paid_at"),
};

const historyElement = {
  total: document.getElementById("subscription_history_total"),
  body: document.getElementById("subscription_history_body"),
};
// **************************************************************
// ELEMENT SETUP | END
// **************************************************************

// **************************************************************
// GET SUBSCRIPTION STATUS | START
// **************************************************************
async function loadSubscriptionStatus() {
  try {
    setSubscriptionLoading(true);

    const response = await fetch("/subscription/status", {
      method: "GET",
      credentials: "same-origin",
    });

    const result = await response.json();

    if (!response.ok || result.status_code !== 200) {
      swalError(result.message || "Gagal mengambil status langganan.");

      return null;
    }

    renderSubscriptionStatus(result.data);

    return result.data;
  } catch (error) {
    console.error(error);

    swalError("Terjadi kesalahan saat mengambil status langganan.");

    return null;
  } finally {
    setSubscriptionLoading(false);
  }
}
// **************************************************************
// GET SUBSCRIPTION STATUS | END
// **************************************************************

// **************************************************************
// SYNC PAYMENT STATUS | START
// **************************************************************
async function syncPaymentStatus(showError = true) {
  try {
    const response = await fetch("/subscription/sync-status", {
      method: "POST",
      credentials: "same-origin",
    });

    const result = await response.json();

    if (!response.ok || result.status_code !== 200) {
      if (showError) {
        swalError(result.message || "Gagal menyinkronkan status pembayaran.");
      }

      return null;
    }

    return result.data;
  } catch (error) {
    console.error(error);

    if (showError) {
      swalError("Terjadi kesalahan saat menyinkronkan pembayaran.");
    }

    return null;
  }
}
// **************************************************************
// SYNC PAYMENT STATUS | END
// **************************************************************

// **************************************************************
// GET PAYMENT HISTORY | START
// **************************************************************
async function loadSubscriptionHistory() {
  try {
    setHistoryLoading();

    const response = await fetch("/subscription/history", {
      method: "GET",
      credentials: "same-origin",
    });

    const result = await response.json();

    if (!response.ok || result.status_code !== 200) {
      renderSubscriptionHistory([]);

      swalError(result.message || "Gagal mengambil riwayat pembayaran.");

      return null;
    }

    renderSubscriptionHistory(result.data?.history || []);

    return result.data;
  } catch (error) {
    console.error("LOAD PAYMENT HISTORY ERROR:", error);

    renderSubscriptionHistory([]);

    return null;
  }
}
// **************************************************************
// GET PAYMENT HISTORY | END
// **************************************************************

// **************************************************************
// RENDER PAYMENT HISTORY | START
// **************************************************************
function renderSubscriptionHistory(history) {
  const payments = Array.isArray(history) ? history : [];

  historyElement.total.textContent = `${payments.length} Transaksi`;

  if (payments.length === 0) {
    historyElement.body.innerHTML = `
      <tr>
        <td
          colspan="6"
          class="text-center text-muted py-4"
        >
          <i class="bi bi-inbox fs-4 d-block mb-2"></i>
          Belum ada riwayat pembayaran.
        </td>
      </tr>
    `;

    return;
  }

  historyElement.body.innerHTML = payments
    .map((payment, index) => {
      const statusClass = getHistoryStatusClass(payment.transaction_status);

      return `
        <tr>
          <td>${index + 1}</td>

          <td>
            ${payment.created_at_format || "-"}
          </td>

          <td>
            <span class="fw-semibold">
              ${payment.order_id || "-"}
            </span>
          </td>

          <td>
            ${payment.payment_type_label || "-"}
          </td>

          <td>
            ${payment.amount_format || "Rp 0"}
          </td>

          <td>
            <span class="badge ${statusClass}">
              ${payment.transaction_status_label || "-"}
            </span>
          </td>
        </tr>
      `;
    })
    .join("");
}
// **************************************************************
// RENDER PAYMENT HISTORY | END
// **************************************************************

// **************************************************************
// HISTORY STATUS CLASS | START
// **************************************************************
function getHistoryStatusClass(status) {
  const transactionStatus = String(status || "").toLowerCase();

  if (transactionStatus === "settlement" || transactionStatus === "capture") {
    return "bg-success";
  }

  if (transactionStatus === "pending") {
    return "bg-warning";
  }

  if (transactionStatus === "cancel" || transactionStatus === "deny" || transactionStatus === "expire") {
    return "bg-danger";
  }

  if (transactionStatus === "refund") {
    return "bg-info";
  }

  return "bg-secondary";
}
// **************************************************************
// HISTORY STATUS CLASS | END
// **************************************************************

// **************************************************************
// RENDER SUBSCRIPTION STATUS | START
// **************************************************************
function renderSubscriptionStatus(data) {
  subscriptionElement.workshopName.textContent = data.workshop_name || "-";

  subscriptionElement.subscriptionEnd.textContent = data.subscription_end_format || "-";

  subscriptionElement.remainingDays.textContent = `${data.remaining_days || 0} Hari`;

  renderSubscriptionBadge(Number(data.subscription_status));

  renderSubscriptionMessage(Number(data.subscription_status), Number(data.remaining_days));

  renderLatestPayment(data.latest_payment);

  const subscriptionStatus = Number(data.subscription_status);

  const remainingDays = Number(data.remaining_days || 0);

  const latestStatus = String(data.latest_payment?.transaction_status || "").toLowerCase();

  if (latestStatus === "pending") {
    subscriptionElement.payButton.disabled = false;

    subscriptionElement.payButton.innerHTML = `
          <i class="bi bi-credit-card me-1"></i>
          Lanjutkan Pembayaran
        `;

    return;
  }

  if (subscriptionStatus === 1 && remainingDays > 7) {
    subscriptionElement.payButton.disabled = true;

    subscriptionElement.payButton.innerHTML = `
          <i class="bi bi-check-circle me-1"></i>
          Langganan Aktif
        `;

    return;
  }

  if (subscriptionStatus === 1 && remainingDays <= 7) {
    subscriptionElement.payButton.disabled = false;

    subscriptionElement.payButton.innerHTML = `
          <i class="bi bi-arrow-repeat me-1"></i>
          Perpanjang Langganan
        `;

    return;
  }

  if (subscriptionStatus === 2) {
    subscriptionElement.payButton.disabled = false;

    subscriptionElement.payButton.innerHTML = `
          <i class="bi bi-arrow-repeat me-1"></i>
          Aktifkan Kembali
        `;

    return;
  }

  subscriptionElement.payButton.disabled = false;

  subscriptionElement.payButton.innerHTML = `
        <i class="bi bi-credit-card me-1"></i>
        Bayar Langganan
      `;
}
// **************************************************************
// RENDER SUBSCRIPTION STATUS | END
// **************************************************************

// **************************************************************
// RENDER SUBSCRIPTION BADGE | START
// **************************************************************
function renderSubscriptionBadge(status) {
  subscriptionElement.status.className = "badge fs-6";

  if (status === 1) {
    subscriptionElement.status.classList.add("bg-success");

    subscriptionElement.status.textContent = "Aktif";

    return;
  }

  if (status === 2) {
    subscriptionElement.status.classList.add("bg-danger");

    subscriptionElement.status.textContent = "Kedaluwarsa";

    return;
  }

  subscriptionElement.status.classList.add("bg-secondary");

  subscriptionElement.status.textContent = "Belum Aktif";
}
// **************************************************************
// RENDER SUBSCRIPTION BADGE | END
// **************************************************************

// **************************************************************
// RENDER SUBSCRIPTION MESSAGE | START
// **************************************************************
function renderSubscriptionMessage(status, remainingDays) {
  subscriptionElement.alert.className = "alert mb-0";

  if (status === 1) {
    subscriptionElement.alert.classList.add("alert-light-success");

    subscriptionElement.message.textContent = `Langganan aktif dengan sisa masa berlaku ${remainingDays} hari.`;

    return;
  }

  if (status === 2) {
    subscriptionElement.alert.classList.add("alert-light-danger");

    subscriptionElement.message.textContent = "Masa langganan sudah berakhir. Silakan lakukan pembayaran untuk mengaktifkan kembali sistem.";

    return;
  }

  subscriptionElement.alert.classList.add("alert-light-warning");

  subscriptionElement.message.textContent = "Langganan belum aktif. Silakan lakukan pembayaran untuk menggunakan seluruh fitur sistem.";
}
// **************************************************************
// RENDER SUBSCRIPTION MESSAGE | END
// **************************************************************

// **************************************************************
// RENDER LATEST PAYMENT | START
// **************************************************************
function renderLatestPayment(payment) {
  if (!payment) {
    paymentElement.card.classList.add("d-none");

    return;
  }

  paymentElement.card.classList.remove("d-none");

  paymentElement.orderId.textContent = payment.order_id || "-";

  paymentElement.amount.textContent = formatRupiah(payment.amount || 0);

  paymentElement.paymentType.textContent = formatPaymentType(payment.payment_type);

  paymentElement.paidAt.textContent = payment.paid_at_format || "-";

  renderTransactionBadge(payment.transaction_status);
}
// **************************************************************
// RENDER LATEST PAYMENT | END
// **************************************************************

// **************************************************************
// RENDER TRANSACTION BADGE | START
// **************************************************************
function renderTransactionBadge(status) {
  const transactionStatus = String(status || "-").toLowerCase();

  paymentElement.transactionStatus.className = "badge";

  if (transactionStatus === "settlement" || transactionStatus === "capture") {
    paymentElement.transactionStatus.classList.add("bg-success");
  } else if (transactionStatus === "pending") {
    paymentElement.transactionStatus.classList.add("bg-warning");
  } else if (transactionStatus === "cancel" || transactionStatus === "deny" || transactionStatus === "expire") {
    paymentElement.transactionStatus.classList.add("bg-danger");
  } else {
    paymentElement.transactionStatus.classList.add("bg-secondary");
  }

  paymentElement.transactionStatus.textContent = formatTransactionStatus(transactionStatus);
}
// **************************************************************
// RENDER TRANSACTION BADGE | END
// **************************************************************

// **************************************************************
// CREATE SUBSCRIPTION PAYMENT | START
// **************************************************************
async function createSubscriptionPayment() {
  try {
    setPaymentLoading(true);

    const response = await fetch("/subscription/create-payment", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        package: "monthly",
      }),
    });

    const result = await response.json();

    if (!response.ok || ![200, 201].includes(result.status_code)) {
      return swalError(result.message || "Gagal membuat transaksi langganan.");
    }

    if (!result.data || !result.data.snap_token) {
      return swalError("Snap Token Midtrans tidak ditemukan.");
    }

    openMidtransSnap(result.data.snap_token);
  } catch (error) {
    console.error(error);

    swalError("Terjadi kesalahan saat membuat pembayaran.");
  } finally {
    setPaymentLoading(false);
  }
}
// **************************************************************
// CREATE SUBSCRIPTION PAYMENT | END
// **************************************************************

// **************************************************************
// OPEN MIDTRANS SNAP | START
// **************************************************************
// **************************************************************
// OPEN MIDTRANS SNAP | START
// **************************************************************
// **************************************************************
// OPEN MIDTRANS SNAP | START
// **************************************************************
function openMidtransSnap(snapToken) {
  if (typeof window.snap === "undefined") {
    return swalError("Midtrans Snap belum berhasil dimuat.");
  }

  window.snap.pay(snapToken, {
    // Pembayaran berhasil
    onSuccess: async function (result) {
      console.log("Payment success:", result);

      const syncResult = await syncPaymentStatus();

      if (!syncResult) {
        return;
      }

      swalSuccess("Pembayaran berhasil dan langganan telah diaktifkan.");

      await loadSubscriptionStatus();
      await loadSubscriptionHistory();
    },

    // Pembayaran masih pending
    onPending: async function (result) {
      console.log("Payment pending:", result);

      await syncPaymentStatus(false);

      swalWarning("Pembayaran belum selesai.");

      await loadSubscriptionStatus();
      await loadSubscriptionHistory();
    },

    // Pembayaran gagal
    onError: async function (result) {
      console.error("Payment error:", result);

      await syncPaymentStatus(false);

      swalError("Pembayaran gagal diproses.");

      await loadSubscriptionStatus();
      await loadSubscriptionHistory();
    },

    // Popup ditutup
    onClose: async function () {
      await syncPaymentStatus(false);

      swalWarning("Pembayaran belum diselesaikan.");

      await loadSubscriptionStatus();
      await loadSubscriptionHistory();
    },
  });
}
// **************************************************************
// OPEN MIDTRANS SNAP | END
// **************************************************************
// **************************************************************
// OPEN MIDTRANS SNAP | END
// **************************************************************
// **************************************************************
// OPEN MIDTRANS SNAP | END
// **************************************************************

// **************************************************************
// PAYMENT TYPE FORMATTER | START
// **************************************************************
function formatPaymentType(paymentType) {
  if (!paymentType) {
    return "-";
  }

  const paymentTypes = {
    bank_transfer: "Transfer Bank",
    credit_card: "Kartu Kredit",
    gopay: "GoPay",
    qris: "QRIS",
    shopeepay: "ShopeePay",
    cstore: "Convenience Store",
    echannel: "Mandiri Bill Payment",
  };

  return paymentTypes[paymentType] || paymentType;
}
// **************************************************************
// PAYMENT TYPE FORMATTER | END
// **************************************************************

// **************************************************************
// TRANSACTION STATUS FORMATTER | START
// **************************************************************
function formatTransactionStatus(status) {
  const statuses = {
    pending: "Menunggu Pembayaran",
    settlement: "Berhasil",
    capture: "Berhasil",
    cancel: "Dibatalkan",
    deny: "Ditolak",
    expire: "Kedaluwarsa",
    refund: "Dikembalikan",
  };

  return statuses[status] || status || "-";
}
// **************************************************************
// TRANSACTION STATUS FORMATTER | END
// **************************************************************

// **************************************************************
// LOADING STATE | START
// **************************************************************
function setSubscriptionLoading(isLoading) {
  if (isLoading) {
    subscriptionElement.status.className = "badge bg-secondary fs-6";

    subscriptionElement.status.textContent = "Memuat...";

    subscriptionElement.payButton.disabled = true;
  }
}

function setPaymentLoading(isLoading) {
  subscriptionElement.payButton.disabled = isLoading;

  if (isLoading) {
    subscriptionElement.payButton.innerHTML = `
      <span
        class="spinner-border spinner-border-sm me-1"
        role="status"
      ></span>
      Memproses...
    `;
  }
}

function setHistoryLoading() {
  if (!historyElement.total || !historyElement.body) {
    return;
  }

  historyElement.total.textContent = "Memuat...";

  historyElement.body.innerHTML = `
    <tr>
      <td
        colspan="6"
        class="text-center text-muted py-4"
      >
        <span
          class="spinner-border spinner-border-sm me-2"
          role="status"
        ></span>

        Memuat riwayat pembayaran...
      </td>
    </tr>
  `;
}
// **************************************************************
// LOADING STATE | END
// **************************************************************
