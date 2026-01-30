const EVENTS_API = "/api/get_events";
const REFRESH_INTERVAL = 15000; // 15s

async function fetchEvents() {
    try {
        const response = await fetch(EVENTS_API);
        const events = await response.json();
        renderEvents(events);
    } catch (error) {
        console.error("Failed to fetch events:", error);
    }
}

/* ---------- Helpers ---------- */

function formatTimestamp(isoString) {
    const date = new Date(isoString);

    const options = {
        day: "numeric",
        month: "long",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
        timeZone: "UTC",
        timeZoneName: "short"
    };

    return date.toLocaleString("en-GB", options);
}

function buildMessage(event) {
    const author = event.author;
    const to = event.to_branch;
    const from = event.from_branch;
    const timestamp = formatTimestamp(event.timestamp["$date"]);

    switch (event.action) {
        case "PUSH":
            return `${author} pushed to ${to} on ${timestamp}`;

        case "PULL_REQUEST":
            return `${author} submitted a pull request from ${from} to ${to} on ${timestamp}`;

        case "MERGE":
            return `${author} merged branch ${from} to ${to} on ${timestamp}`;

        default:
            return `${author} performed ${event.action} on ${timestamp}`;
    }
}

/* ---------- Render ---------- */

function renderEvents(events) {
    const container = document.getElementById("events");

    if (!events || events.length === 0) {
        container.innerHTML = "<p>No events yet.</p>";
        return;
    }

    container.innerHTML = "";

    events.forEach(event => {
        const div = document.createElement("div");
        div.className = "event";

        const message = buildMessage(event);

        div.innerHTML = `<p>${message}</p>`;

        container.appendChild(div);
    });
}

/* ---------- Init ---------- */

fetchEvents();
setInterval(fetchEvents, REFRESH_INTERVAL);
