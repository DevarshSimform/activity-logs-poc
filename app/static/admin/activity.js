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

  const EVENT_LABELS = {
    "profile.updated": {
      action: "Updated profile",
      badge: "Profile",
    },
    "task.created": {
      action: "Created task",
      badge: "Task",
    },
    "task.updated": {
      action: "Updated task",
      badge: "Task",
    },
    "task.deleted": {
      action: "Deleted task",
      badge: "Task",
    },
    "subtask.created": {
      action: "Created subtask",
      badge: "Subtask",
    },
    "subtask.updated": {
      action: "Updated subtask",
      badge: "Subtask",
    },
    "subtask.deleted": {
      action: "Deleted subtask",
      badge: "Subtask",
    },
  };

  function renderActivity(event) {
    if (!event || !event.event_type) return;

    const config = EVENT_LABELS[event.event_type];

    // Skip unknown events safely
    if (!config) return;

    const rowId = `details-${event.event_id}`;
    const changes =
      event.event_type === "profile.updated"
        ? Object.keys(event.payload?.changes || {})
        : [];

    const changesText = changes.length ? changes.join(", ") : "—";

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${new Date(event.occurred_at).toLocaleTimeString()}</td>
      <td>${event.actor?.email ?? "Unknown"}</td>
      <td>
        ${config.action}
        <span class="badge bg-secondary ms-1">${config.badge}</span>
      </td>
      <td>
        ${changes.length
          ? `<span class="badge changes-badge">${changesText}</span>`
          : "—"}
      </td>
      <td>
        <button class="btn btn-sm btn-outline-primary"
                data-bs-toggle="collapse"
                data-bs-target="#${rowId}">
          View
        </button>
      </td>
    `;

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
