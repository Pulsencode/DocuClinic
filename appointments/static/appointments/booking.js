(() => {
  "use strict";
  document.addEventListener("DOMContentLoaded", () => {
    const calendar = document.getElementById("booking-calendar");
    if (!calendar) return;
    const doctor = document.getElementById("id_physician");
    const dateField = document.getElementById("id_date");
    const timeField = document.getElementById("id_time");
    const grid = document.getElementById("booking-grid");
    const status = document.getElementById("booking-status");
    const selection = document.getElementById("booking-selection");
    const form = document.getElementById("appointment_form");
    const details = [...form.querySelectorAll("fieldset")].filter(f =>
      f.querySelector("#id_patient, #id_consultation_fee"));
    let selected = dateField.value && timeField.value ? `${dateField.value}|${timeField.value.slice(0, 8)}` : null;
    let week = parseDate(dateField.value || calendar.dataset.today);
    let controller;
    let dragging = false;
    let lastDoctor = doctor.value;
    week.setDate(week.getDate() - (week.getDay() + 6) % 7);
    dateField.closest("fieldset").hidden = true;
    function parseDate(value) { return new Date(`${value}T12:00:00`); }
    function iso(value) {
      return `${value.getFullYear()}-${String(value.getMonth() + 1).padStart(2, "0")}-${String(value.getDate()).padStart(2, "0")}`;
    }
    function label(value, options) { return value.toLocaleDateString(undefined, options); }
    function gate() { details.forEach(f => { f.hidden = !selected; }); }
    function clear() {
      selected = null;
      dateField.value = "";
      timeField.value = "";
      selection.textContent = "No time selected";
      gate();
    }
    function choose(button) {
      selected = button.dataset.slot;
      [dateField.value, timeField.value] = selected.split("|");
      grid.querySelectorAll("button[data-slot]").forEach(b => b.setAttribute("aria-pressed", String(b === button)));
      selection.textContent = `${label(parseDate(dateField.value), {weekday: "long", month: "long", day: "numeric", year: "numeric"})} · ${button.textContent}`;
      gate();
    }
    async function render() {
      if (controller) controller.abort();
      controller = new AbortController();
      const signal = controller.signal;
      grid.replaceChildren();
      gate();
      const end = new Date(week); end.setDate(end.getDate() + 6);
      document.getElementById("booking-week").textContent = `${label(week, {month: "short", day: "numeric"})} – ${label(end, {month: "short", day: "numeric", year: "numeric"})}`;
      document.getElementById("booking-duration").textContent = "";
      if (!doctor.value) { clear(); status.textContent = "Select a doctor to see their available days and times."; return; }
      status.textContent = "Loading available times…";
      const url = new URL(calendar.dataset.url, window.location.origin);
      url.searchParams.set("physician", doctor.value);
      url.searchParams.set("start", iso(week));
      try {
        const response = await fetch(url, {signal, headers: {Accept: "application/json"}});
        if (!response.ok) {
          const data = response.headers.get("content-type")?.includes("application/json") ? await response.json() : null;
          throw new Error(data?.error || "Availability could not be loaded. Check your booking, staff-directory and availability permissions, then refresh.");
        }
        const data = await response.json();
        if (signal.aborted) return;
        document.getElementById("booking-duration").textContent = `${data.duration} min · ${data.timezone}`;
        const table = document.createElement("table");
        table.className = "booking-table";
        const caption = table.createCaption(); caption.textContent = "Available consultation times"; caption.className = "booking-sr-only";
        const head = table.createTHead().insertRow();
        const corner = document.createElement("th"); corner.textContent = "Time"; head.append(corner);
        data.days.forEach(day => {
          const th = document.createElement("th"); th.scope = "col";
          th.textContent = label(parseDate(day.date), {weekday: "short", day: "numeric", month: "short"});
          head.append(th);
        });
        const times = [...new Set(data.days.flatMap(d => d.slots.map(s => s.start)))].sort();
        let selectedButton = null;
        const body = table.createTBody();
        times.forEach(time => {
          const row = body.insertRow();
          const th = document.createElement("th"); th.scope = "row"; th.textContent = time.slice(0, 5); row.append(th);
          data.days.forEach(day => {
            const cell = row.insertCell();
            const slot = day.slots.find(s => s.start === time);
            if (!slot) { cell.className = "booking-unavailable"; return; }
            const button = document.createElement("button"); button.type = "button";
            button.dataset.slot = `${day.date}|${slot.start}`;
            button.textContent = `${slot.start.slice(0, 5)} – ${slot.end.slice(0, 5)}`;
            button.setAttribute("aria-label", `${day.date}, ${button.textContent}`);
            button.setAttribute("aria-pressed", "false");
            if (button.dataset.slot === selected) selectedButton = button;
            button.addEventListener("click", () => choose(button));
            button.addEventListener("pointerdown", e => {
              if (e.button !== 0 || e.pointerType === "touch") return;
              dragging = true; e.preventDefault(); choose(button);
            });
            button.addEventListener("pointerenter", () => { if (dragging) choose(button); });
            cell.append(button);
          });
        });
        grid.append(table);
        if (selectedButton) choose(selectedButton);
        else if (selected) clear();
        status.textContent = times.length ? "Select a free time below. Shaded areas are unavailable." : "No available times this week. Try another week or doctor.";
      } catch (error) {
        if (error.name === "AbortError") return;
        clear(); status.textContent = error.message;
      }
    }
    document.addEventListener("pointerup", () => { dragging = false; });
    window.addEventListener("blur", () => { dragging = false; });
    function doctorChanged() {
      if (doctor.value === lastDoctor) return;
      lastDoctor = doctor.value; clear(); render();
    }
    doctor.addEventListener("change", doctorChanged);
    if (window.django?.jQuery) window.django.jQuery(doctor).on("change", doctorChanged);
    document.getElementById("booking-prev").onclick = () => { clear(); week.setDate(week.getDate() - 7); render(); };
    document.getElementById("booking-next").onclick = () => { clear(); week.setDate(week.getDate() + 7); render(); };
    document.getElementById("booking-today").onclick = () => {
      clear(); week = parseDate(calendar.dataset.today); week.setDate(week.getDate() - (week.getDay() + 6) % 7); render();
    };
    document.getElementById("booking-refresh").onclick = render;
    form.addEventListener("submit", event => {
      if (!selected) { event.preventDefault(); status.textContent = "Choose a doctor and an available calendar time before saving."; calendar.scrollIntoView({behavior: "smooth"}); }
    });
    render();
  });
})();
