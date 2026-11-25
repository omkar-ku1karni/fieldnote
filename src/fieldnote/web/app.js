const $ = (s) => document.querySelector(s);
const form = $("#ask"), q = $("#q"), go = $("#go");

const KIND = { page: "Manual figure", text: "Manual text", call: "Support call", photo: "Job photo",
               register: "Equipment register", photo_caption: "Job photo (caption only)" };

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// Models sometimes write units as LaTeX ($5\text{ }\mu\text{F}$) even when told not to.
function unlatex(t) {
  return t.replace(/\\text\{([^}]*)\}/g, "$1").replace(/\\mu\s*/g, "µ").replace(/\\(pm)\s*/g, "±")
          .replace(/\\(?:,|;|\s)/g, " ").replace(/\$([^$\n]{1,80})\$/g, "$1").replace(/\s{2,}/g, " ");
}

// Just enough markdown: paragraphs, lists, **bold**, and the [S#] citation tags. Escapes everything else.
function render(md) {
  md = unlatex(md);
  const inline = (t) => esc(t)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\[(S\d+(?:\s*[,;]\s*S\d+)*)\]/g, (_, tags) =>
      tags.split(/\s*[,;]\s*/).map((t) => `<button type="button" class="cite" data-tag="${t}" aria-label="Show source ${t}">${t}</button>`).join(""));
  const out = [];
  let list = null;
  for (const raw of md.split("\n")) {
    const line = raw.trim();
    const bullet = line.match(/^[-*•]\s+(.*)/), num = line.match(/^\d+[.)]\s+(.*)/);
    if (bullet || num) {
      const tag = bullet ? "ul" : "ol";
      if (!list || list.tag !== tag) { if (list) out.push(`</${list.tag}>`); out.push(`<${tag}>`); list = { tag }; }
      out.push(`<li>${inline((bullet || num)[1])}</li>`);
      continue;
    }
    if (list) { out.push(`</${list.tag}>`); list = null; }
    if (line) {
      let html = inline(line.replace(/^#+\s*/, ""));
      if (!out.length) {  // lead: only the first sentence gets the display type
        const m = html.match(/^(.+?[.!?](?:\s*<button[^>]*>S\d+<\/button>)*\.?)(\s+[\s\S]*)?$/);
        html = m ? `<span class="lead">${m[1]}</span>${m[2] || ""}` : `<span class="lead">${html}</span>`;
      }
      out.push(`<p>${html}</p>`);
    }
  }
  if (list) out.push(`</${list.tag}>`);
  return out.join("");
}

function ts(s) { s = Math.max(0, s); return `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`; }

function sourceHTML(s, cited) {
  const chip = `<span class="cite ${cited ? "" : "uncited"}">${s.tag}</span>`;
  let body = "";
  if (s.modality === "page") {
    body = `<figure><img src="/media/${esc(s.image)}" alt="${s.figure ? "Figure" : "Page"} from ${esc(s.label)}" loading="${cited ? "eager" : "lazy"}">
      <figcaption>${esc(s.label)}.${s.figure ? " Check the value against the figure." : ""}</figcaption></figure>
      <div class="actions"><button type="button" data-page="/media/${esc(s.page_image)}">Open the whole page</button></div>`;
  } else if (s.modality === "photo") {
    const a = s.attribution || {};
    body = `<figure class="photo"><img src="/media/${esc(s.image)}" alt="Job site photo, ${esc(s.label)}" loading="${cited ? "eager" : "lazy"}">
      <figcaption>${esc(a.creator || "Unknown author")}, ${esc(a.license || "")}${a.source ? `, <a href="${esc(a.source)}" target="_blank" rel="noopener">source</a>` : ""}</figcaption></figure>`;
  } else if (s.modality === "call") {
    const segs = [...(s.text || "").matchAll(/\[(\d+):(\d+)\]\s*([^\[]*)/g)].map((m) => ({ t: +m[1] * 60 + +m[2], text: m[3].trim() }));
    const near = segs.filter((g) => g.t >= s.start - 1 && g.t <= s.end + 1);
    const quote = (near.length ? near : segs.slice(0, 3)).map((g) => `<span class="ts">${ts(g.t)}</span> ${esc(g.text)}`).join("<br>");
    body = `<audio controls preload="metadata" src="/api/clip/${esc(s.call_id)}?start=${s.start}&end=${s.end}"></audio>
      <blockquote>${quote}</blockquote>
      ${segs.length > near.length ? `<details class="full"><summary>Show the whole call</summary><blockquote>${
        segs.map((g) => `<span class="ts">${ts(g.t)}</span> ${esc(g.text)}`).join("<br>")}</blockquote></details>` : ""}`;
  } else {
    body = `<p class="snippet">${esc((s.text || "").slice(0, 420))}${(s.text || "").length > 420 ? "…" : ""}</p>`;
  }
  return `<li class="source ${cited ? "cited" : ""}" id="src-${s.tag}">
    <div class="source-head">${chip}<span class="source-label">${esc(s.label)}</span>
    <span class="source-kind">${s.modality === "page" ? (s.figure ? "Manual figure" : "Manual page") : (KIND[s.modality] || "")}</span></div>${body}</li>`;
}

function traceHTML(d) {
  const t = d.timings || {};
  const rows = [
    ["Model", `${d.model} (${d.provider})`],
    ["Search", `${t.search_ms ?? "?"} ms`],
    ["Generation", `${t.llm_ms ?? "?"} ms`],
    ["Total", `${t.total_ms ?? "?"} ms`],
    ["Evidence shown to the model", `${d.sources.length} items, ${d.sources.filter((s) => s.modality === "page" || s.modality === "photo").length} as images`],
  ];
  return `<dl>${rows.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join("")}</dl>`;
}

async function ask(question) {
  q.value = question;
  go.disabled = true;
  $("#result").hidden = false;
  $("#status").className = "status";
  $("#status").textContent = "Searching manuals, calls and photos…";
  ["#answer", "#sources", "#meta"].forEach((s) => ($(s).innerHTML = ""));
  $("#evidence-title").hidden = true; $("#trace").hidden = true;
  try {
    const r = await fetch("/api/ask", { method: "POST", headers: { "Content-Type": "application/json" },
                                         body: JSON.stringify({ question }) });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || `The server returned ${r.status}.`);
    $("#status").textContent = "";
    $("#answer").innerHTML = render(d.answer);
    const cited = new Set(d.cited);
    const used = d.sources.filter((s) => cited.has(s.tag)), rest = d.sources.filter((s) => !cited.has(s.tag));
    $("#sources").innerHTML = used.map((s) => sourceHTML(s, true)).join("") + (rest.length
      ? `<li class="also"><details><summary>Also retrieved, not used in the answer (${rest.length})</summary>
         <ol class="sources">${rest.map((s) => sourceHTML(s, false)).join("")}</ol></details></li>` : "");
    $("#evidence-title").hidden = !d.sources.length;
    $("#meta").textContent = `Answered in ${(d.timings.total_ms / 1000).toFixed(1)} s. Tap a yellow tag to see its source.`;
    $("#trace-body").innerHTML = traceHTML(d);
    $("#trace").hidden = false;
    history.replaceState(null, "", `?q=${encodeURIComponent(question)}`);
  } catch (e) {
    $("#status").className = "status error";
    $("#status").textContent = e.message;
  } finally {
    go.disabled = false;
  }
}

form.addEventListener("submit", (e) => { e.preventDefault(); if (q.value.trim()) ask(q.value.trim()); });
q.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); } });

document.addEventListener("click", (e) => {
  const cite = e.target.closest("button.cite");
  if (cite) {
    const el = document.getElementById(`src-${cite.dataset.tag}`);
    if (el) {
      el.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
      el.classList.remove("flash"); void el.offsetWidth; el.classList.add("flash");
    }
  }
  const page = e.target.closest("[data-page]");
  if (page) { $("#viewer-img").src = page.dataset.page; $("#viewer-img").alt = "Full manual page"; $("#viewer").showModal(); }
});

fetch("/api/examples").then((r) => r.json()).then((ex) => {
  $("#examples").innerHTML = ex.map((x, i) =>
    `<button type="button" data-i="${i}">${esc(x.q.length > 70 ? x.q.slice(0, 68) + "…" : x.q)}<small>${esc(x.why)}</small></button>`).join("");
  $("#examples").addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) ask(ex[b.dataset.i].q); });
  const pre = new URLSearchParams(location.search).get("q");
  if (pre) ask(pre);
});
