document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.getElementById("activity-table-body");

  if (!tableBody) {
    console.error("❌ activity-table-body not found");
    return;
  }

  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("Admin token missing. Please login again.");
    return;
  }

  const protocol = location.protocol === "https:" ? "wss" : "ws";
  const wsUrl = `${protocol}://${location.host}${window.ADMIN_WS_URL}?token=${token}`;

  const socket = new WebSocket(wsUrl);

  socket.onopen = () => console.log("🟢 Admin WebSocket connected");

  socket.onmessage = (message) => {
    try {
      const data = JSON.parse(message.data);
      const activityEvent = data.event ?? data.value ?? data; // safe extraction
      renderActivity(activityEvent);
    } catch (err) {
      console.error("Invalid WS message:", err);
    }
  };


  function renderActivity(event) {
    // Defensive guard
    if (!event || !event.event_type) return;
    if (event.event_type !== "profile.updated") return;

    const rowId = `details-${event.event_id}`;
    const changes = Object.keys(event.payload?.changes || {});
    const changesText = changes.length ? changes.join(", ") : "—";

    // Main table row
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${new Date(event.occurred_at).toLocaleTimeString()}</td>
      <td>${event.actor?.email ?? "Unknown"}</td>
      <td>Updated profile</td>
      <td>${changes.length ? `<span class="badge changes-badge">${changesText}</span>` : "—"}</td>
      <td>
        <button class="btn btn-sm btn-outline-primary" data-bs-toggle="collapse" data-bs-target="#${rowId}">
          View
        </button>
      </td>
    `;

    // Details row
    const detailsTr = document.createElement("tr");
    detailsTr.innerHTML = `
      <td colspan="5" class="p-0">
        <div id="${rowId}" class="collapse">
          <div class="p-3">
            <div class="mb-2"><b>Request ID:</b> ${event.request_id}</div>
            <div class="mb-2"><b>IP Address:</b> ${event.meta?.ip_address ?? "-"}</div>
            <div class="mb-2"><b>User Agent:</b> ${event.meta?.user_agent ?? "-"}</div>
            <div class="mt-3">
              <b>Raw Event</b>
              <pre>${JSON.stringify(event, null, 2)}</pre>
            </div>
          </div>
        </div>
      </td>
    `;

    tableBody.prepend(detailsTr);
    tableBody.prepend(tr);
  }

});
