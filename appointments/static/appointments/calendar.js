(() => {
  "use strict";
  document.addEventListener("DOMContentLoaded", () => {
    const root = document.getElementById("appointment-schedule");
    if (!root) return;
    const config = JSON.parse(document.getElementById("appointment-calendar-config").textContent);
    const $ = id => document.getElementById(`ac-${id}`);
    const parse = value => new Date(`${value}T12:00:00`);
    const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
    const plus = (d, n) => { const result = new Date(d); result.setDate(result.getDate() + n); return result; };
    const monthStart = d => new Date(d.getFullYear(), d.getMonth(), 1, 12);
    const sunday = d => plus(d, -d.getDay());
    const format = (d, options) => d.toLocaleDateString(undefined, options);
    const minute = time => { const parts = time.split(":").map(Number); return parts[0] * 60 + parts[1] + (parts[2] || 0) / 60; };
    const clock = n => `${String(Math.floor(n / 60) % 24).padStart(2, "0")}:${String(Math.floor(n % 60)).padStart(2, "0")}`;
    const el = (tag, className, text) => {
      const node = document.createElement(tag);
      if (className) node.className = className;
      if (text !== undefined) node.textContent = text;
      return node;
    };
    const button = (className, text, action) => {
      const node = el("button", className, text); node.type = "button";
      node.addEventListener("click", action); return node;
    };
    let selected = parse(config.date);
    let miniMonth = monthStart(selected);
    let view = config.view;
    let controller;
    let timer;
    const today = config.today;
    const pixelsPerMinute = 1.2;
    $("view").value = view;
    $("zone").textContent = `Clinic timezone · ${config.timezone}`;
    if (window.matchMedia("(max-width: 1000px)").matches) root.querySelector("details").open = false;

    function range() {
      const start = view === "month" ? sunday(monthStart(selected)) : view === "week" ? sunday(selected) : selected;
      const length = view === "month" ? 42 : view === "week" ? 7 : 1;
      return {start, end: plus(start, length), days: Array.from({length}, (_, i) => plus(start, i))};
    }
    function mini() {
      $("mini-title").textContent = format(miniMonth, {month: "long", year: "numeric"});
      const fragment = document.createDocumentFragment();
      ["S", "M", "T", "W", "T", "F", "S"].forEach(day => fragment.append(el("span", "ac-mini-weekday", day)));
      const first = sunday(miniMonth);
      const week = sunday(selected);
      for (let i = 0; i < 42; i++) {
        const d = plus(first, i);
        const key = iso(d);
        const b = button("ac-mini-date", d.getDate(), () => { selected = d; miniMonth = monthStart(d); load(); });
        b.setAttribute("aria-label", format(d, {dateStyle: "full"}));
        b.setAttribute("aria-pressed", String(key === iso(selected)));
        if (d.getMonth() !== miniMonth.getMonth()) b.classList.add("ac-outside");
        if (key === today) b.classList.add("ac-is-today");
        if (view === "week" && d >= week && d < plus(week, 7)) b.classList.add("ac-in-week");
        fragment.append(b);
      }
      $("mini").replaceChildren(fragment);
    }
    function showDetails(event, trigger) {
      $("dialog-title").textContent = event.patient;
      $("dialog-status").textContent = event.status;
      $("dialog-status").className = `ac-badge ac-${event.status.toLowerCase()}`;
      $("detail-date").textContent = format(parse(event.date), {dateStyle: "full"});
      const end = minute(event.time) + event.duration;
      $("detail-time").textContent = `${event.time.slice(0, 5)} – ${clock(end)}${end >= 1440 ? " (next day)" : ""} · ${config.timezone}`;
      $("detail-reason").textContent = event.reason;
      $("detail-physician").textContent = event.physician;
      $("duration-note").textContent = event.estimatedDuration ? "This older appointment has no saved duration. Its display length uses the clinic setting, or 30 minutes if unconfigured." : `${event.duration} minute consultation`;
      $("edit").href = event.url;
      $("dialog").showModal();
      $("dialog").addEventListener("close", () => trigger.focus(), {once: true});
    }
    $("close").onclick = () => $("dialog").close();
    $("dialog").addEventListener("click", event => {
      if (event.target !== $("dialog")) return;
      const rect = $("dialog").getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) $("dialog").close();
    });
    function eventButton(event, compact = false) {
      const b = button(`ac-event ac-${event.status.toLowerCase()}${compact ? " ac-compact" : ""}`, undefined, () => showDetails(event, b));
      const name = event.patient;
      const time = event.time.slice(0, 5);
      b.setAttribute("aria-label", `${time}, ${name}, ${event.status}, ${event.physician}`);
      b.title = `${name} · ${time} · ${event.status}`;
      b.append(el("strong", "", name), el("span", "", `${time} · ${event.status}`));
      return b;
    }
    function segmentsFor(events, day) {
      const key = iso(day);
      const yesterday = iso(plus(day, -1));
      return events.flatMap(event => {
        const start = minute(event.time);
        const end = start + event.duration;
        if (event.date === key) return [{event, start, end: Math.min(1440, end)}];
        if (event.date === yesterday && end > 1440) return [{event, start: 0, end: end - 1440}];
        return [];
      }).sort((a, b) => a.start - b.start || b.end - a.end || a.event.id - b.event.id);
    }
    // Divide each overlap group into lanes, including the minimum visual height
    // of short consultations, so every appointment remains clickable.
    function lanes(segments) {
      let group = [];
      let active = [];
      let columns = 0;
      function finish() { group.forEach(item => { item.columns = columns; }); group = []; columns = 0; }
      segments.forEach(item => {
        active = active.filter(other => other.visualEnd > item.start);
        if (!active.length) finish();
        const taken = new Set(active.map(other => other.lane));
        let lane = 0; while (taken.has(lane)) lane++;
        item.lane = lane;
        item.visualEnd = Math.max(item.end, item.start + 34 / pixelsPerMinute);
        columns = Math.max(columns, lane + 1);
        active.push(item); group.push(item);
      });
      finish(); return segments;
    }
    function timeGrid(events, days, keepScroll) {
      const canvas = $("canvas");
      const priorScroll = canvas.querySelector(".ac-time-scroll")?.scrollTop;
      const scroller = el("div", "ac-time-scroll");
      scroller.tabIndex = 0;
      scroller.setAttribute("aria-label", "Hourly calendar; scroll for more times and days");
      const grid = el("div", "ac-time-grid");
      const groups = days.map(d => lanes(segmentsFor(events, d)));
      const maximumLanes = Math.max(1, ...groups.flatMap(g => g.map(s => s.columns)));
      grid.style.setProperty("--ac-days", days.length);
      grid.style.setProperty("--ac-day-width", `${view === "day" ? Math.max(96, maximumLanes * 110) : 96}px`);
      grid.append(el("div", "ac-time-corner", "Time"));
      days.forEach(day => {
        const heading = button("ac-day-heading", undefined, () => { selected = day; view = "day"; $("view").value = view; load(); });
        heading.setAttribute("aria-label", `View ${format(day, {dateStyle: "full"})}`);
        heading.append(el("span", "", format(day, {weekday: "short"})), el("strong", "", day.getDate()));
        if (iso(day) === today) heading.classList.add("ac-is-today");
        grid.append(heading);
      });
      const axis = el("div", "ac-time-axis");
      for (let hour = 0; hour < 24; hour++) {
        const label = el("span", "", `${String(hour).padStart(2, "0")}:00`);
        label.style.top = `${hour * 72}px`; axis.append(label);
      }
      grid.append(axis);
      days.forEach((day, index) => {
        const column = el("div", "ac-day-column");
        column.setAttribute("aria-label", format(day, {dateStyle: "full"}));
        groups[index].forEach(segment => {
          const b = eventButton(segment.event);
          b.style.top = `${segment.start * pixelsPerMinute}px`;
          b.style.height = `${Math.max(34, (segment.end - segment.start) * pixelsPerMinute - 2)}px`;
          b.style.left = `calc(${segment.lane / segment.columns * 100}% + 3px)`;
          b.style.width = `calc(${100 / segment.columns}% - 6px)`;
          if (segment.start === 0 && segment.event.date !== iso(day)) b.title += " · Continued from previous day";
          column.append(b);
        });
        // Convert the current instant to clinic wall time; browser timezone can differ.
        const parts = Object.fromEntries(new Intl.DateTimeFormat("en-GB", {
          timeZone: config.timezone, year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23",
        }).formatToParts(new Date()).map(p => [p.type, p.value]));
        if (iso(day) === `${parts.year}-${parts.month}-${parts.day}`) {
          const line = el("div", "ac-now"); line.setAttribute("aria-label", "Current time");
          line.style.top = `${(Number(parts.hour) * 60 + Number(parts.minute)) * pixelsPerMinute}px`; column.append(line);
        }
        grid.append(column);
      });
      scroller.append(grid); canvas.replaceChildren(scroller);
      const earliest = Math.min(8 * 60, ...groups.flatMap(g => g.map(s => s.start)));
      scroller.scrollTop = keepScroll && priorScroll != null ? priorScroll : Math.max(0, earliest * pixelsPerMinute - 16);
    }
    function monthGrid(events, days) {
      const scroller = el("div", "ac-month-scroll");
      const grid = el("div", "ac-month-grid");
      ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].forEach(name => grid.append(el("div", "ac-month-heading", name)));
      days.forEach(day => {
        const cell = el("div", "ac-month-cell");
        if (day.getMonth() !== selected.getMonth()) cell.classList.add("ac-outside");
        const dateButton = button("ac-month-date", day.getDate(), () => { selected = day; view = "day"; $("view").value = view; load(); });
        dateButton.setAttribute("aria-label", `View ${format(day, {dateStyle: "full"})}`);
        if (iso(day) === today) dateButton.classList.add("ac-is-today");
        cell.append(dateButton);
        const eventsBox = el("div", "ac-month-events");
        segmentsFor(events, day).forEach(s => eventsBox.append(eventButton(s.event, true)));
        cell.append(eventsBox); grid.append(cell);
      });
      scroller.append(grid); $("canvas").replaceChildren(scroller);
    }
    async function load(keepScroll = false) {
      if (controller) controller.abort();
      controller = new AbortController();
      const signal = controller.signal;
      const r = range();
      mini();
      $("title").textContent = view === "day" ? format(selected, {month: "long", day: "numeric", year: "numeric"}) : format(selected, {month: "long", year: "numeric"});
      $("range").textContent = `${format(r.start, {month: "short", day: "numeric"})} – ${format(plus(r.end, -1), {month: "short", day: "numeric", year: "numeric"})}`;
      $("prev").setAttribute("aria-label", `Previous ${view}`);
      $("next").setAttribute("aria-label", `Next ${view}`);
      $("canvas").setAttribute("aria-busy", "true");
      $("message").textContent = "Loading appointments…";
      const url = new URL(config.eventsUrl, location.origin);
      url.searchParams.set("start", iso(r.start)); url.searchParams.set("end", iso(r.end));
      [["status", "status"], ["physician", "physician"], ["search", "q"]].forEach(([id, key]) => {
        if ($(id)?.value) url.searchParams.set(key, $(id).value);
      });
      const page = new URL(location.href); page.searchParams.set("date", iso(selected)); page.searchParams.set("view", view);
      history.replaceState(null, "", page);
      try {
        const response = await fetch(url, {signal, headers: {Accept: "application/json"}});
        if (!response.ok || !response.headers.get("content-type")?.includes("application/json")) throw new Error("Calendar could not be loaded. Check your connection or sign in again, then refresh.");
        const data = await response.json();
        if (signal.aborted) return;
        const shown = new Set(r.days.flatMap(d => segmentsFor(data.events, d).map(s => s.event.id))).size;
        if (view === "month") monthGrid(data.events, r.days); else timeGrid(data.events, r.days, keepScroll);
        $("message").textContent = shown ? `${shown} appointment${shown === 1 ? "" : "s"} · Select an event for details` : "No appointments in this period. Try another date or clear the filters.";
        $("unscheduled").hidden = !data.unscheduled;
      } catch (error) {
        if (error.name === "AbortError") return;
        $("canvas").replaceChildren(); $("unscheduled").hidden = true;
        $("message").textContent = error.message;
      } finally {
        if (!signal.aborted) $("canvas").setAttribute("aria-busy", "false");
      }
    }
    function navigate(direction) {
      if (view === "month") selected = new Date(selected.getFullYear(), selected.getMonth() + direction, 1, 12);
      else selected = plus(selected, direction * (view === "week" ? 7 : 1));
      miniMonth = monthStart(selected); load();
    }
    $("prev").onclick = () => navigate(-1); $("next").onclick = () => navigate(1);
    $("today").onclick = () => { selected = parse(today); miniMonth = monthStart(selected); load(); };
    $("view").onchange = () => { view = $("view").value; load(); };
    $("mini-prev").onclick = () => { miniMonth = new Date(miniMonth.getFullYear(), miniMonth.getMonth() - 1, 1, 12); mini(); };
    $("mini-next").onclick = () => { miniMonth = new Date(miniMonth.getFullYear(), miniMonth.getMonth() + 1, 1, 12); mini(); };
    ["status", "physician"].forEach(id => { if ($(id)) $(id).onchange = () => load(true); });
    if ($("search")) $("search").oninput = () => { clearTimeout(timer); timer = setTimeout(() => load(true), 250); };
    $("refresh").onclick = () => load(true);
    load();
  });
})();
