const state = {
  projects: [],
  selectedProjectId: null,
};

const els = {
  health: document.querySelector("#health"),
  projectCount: document.querySelector("#projectCount"),
  scanCount: document.querySelector("#scanCount"),
  averageScore: document.querySelector("#averageScore"),
  projectForm: document.querySelector("#projectForm"),
  projectName: document.querySelector("#projectName"),
  projectPath: document.querySelector("#projectPath"),
  formError: document.querySelector("#formError"),
  projects: document.querySelector("#projects"),
  refreshButton: document.querySelector("#refreshButton"),
  scanDetails: document.querySelector("#scanDetails"),
  findingsTable: document.querySelector("#findingsTable"),
  severityStats: document.querySelector("#severityStats"),
  reportLink: document.querySelector("#reportLink"),
};

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`;
    try {
      const payload = await response.json();
      message = payload.detail || message;
    } catch (_) {
      // Keep the HTTP status message.
    }
    throw new Error(message);
  }
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return response.json();
  }
  return response.text();
}

async function loadHealth() {
  try {
    const health = await api("/health");
    els.health.textContent = `${health.app}: ${health.status}`;
  } catch (error) {
    els.health.textContent = "Service unavailable";
  }
}

async function loadSummary() {
  const summary = await api("/api/summary");
  els.projectCount.textContent = summary.project_count ?? 0;
  els.scanCount.textContent = summary.scan_count ?? 0;
  els.averageScore.textContent = summary.average_score == null ? "-" : Math.round(summary.average_score);
}

async function loadProjects() {
  state.projects = await api("/api/projects");
  renderProjects();
  await loadSummary();
}

function renderProjects() {
  if (!state.projects.length) {
    els.projects.innerHTML = '<p class="empty">No projects added yet.</p>';
    return;
  }
  els.projects.innerHTML = "";
  for (const project of state.projects) {
    const card = document.createElement("article");
    card.className = "project-card";
    card.innerHTML = `
      <strong>${escapeHtml(project.name)}</strong>
      <div class="project-path">${escapeHtml(project.path)}</div>
      <div class="project-actions">
        <button type="button" data-scan="${project.id}">Scan</button>
        <button type="button" class="secondary" data-history="${project.id}">History</button>
        <button type="button" class="secondary" data-delete="${project.id}">Delete</button>
      </div>
    `;
    els.projects.appendChild(card);
  }
}

async function addProject(event) {
  event.preventDefault();
  els.formError.textContent = "";
  try {
    await api("/api/projects", {
      method: "POST",
      body: JSON.stringify({ name: els.projectName.value.trim(), path: els.projectPath.value.trim() }),
    });
    els.projectForm.reset();
    await loadProjects();
  } catch (error) {
    els.formError.textContent = error.message;
  }
}

async function handleProjectClick(event) {
  const scanId = event.target.dataset.scan;
  const historyId = event.target.dataset.history;
  const deleteId = event.target.dataset.delete;
  if (scanId) {
    await runScan(Number(scanId));
  } else if (historyId) {
    await loadHistory(Number(historyId));
  } else if (deleteId) {
    await deleteProject(Number(deleteId));
  }
}

async function runScan(projectId) {
  els.scanDetails.textContent = "Scanning...";
  try {
    const payload = await api(`/api/projects/${projectId}/scan`, { method: "POST" });
    renderScan(payload);
    await loadSummary();
  } catch (error) {
    els.scanDetails.textContent = error.message;
  }
}

async function loadHistory(projectId) {
  const scans = await api(`/api/projects/${projectId}/scans`);
  if (!scans.length) {
    els.scanDetails.textContent = "No scans for this project.";
    return;
  }
  const latest = await api(`/api/scans/${scans[0].id}`);
  renderScan(latest);
}

async function deleteProject(projectId) {
  await api(`/api/projects/${projectId}`, { method: "DELETE" });
  clearScan();
  await loadProjects();
}

function renderScan(payload) {
  const scan = payload.scan;
  const findings = payload.findings || [];
  const summary = scan.summary_json || {};
  els.scanDetails.innerHTML = `
    <div class="score"><strong>${scan.score ?? "-"}</strong><span class="grade">${escapeHtml(summary.grade || "unknown")}</span></div>
    <p>${findings.length} findings from scan #${scan.id}</p>
    <p>Status: ${escapeHtml(scan.status)}</p>
  `;
  els.reportLink.href = `/api/scans/${scan.id}/report.md`;
  els.reportLink.classList.remove("hidden");
  renderSeverity(summary.severity_counts || {});
  renderFindings(findings);
}

function renderSeverity(counts) {
  els.severityStats.innerHTML = ["error", "warning", "info"]
    .map((severity) => `<span class="pill ${severity}">${severity}: ${counts[severity] || 0}</span>`)
    .join("");
}

function renderFindings(findings) {
  if (!findings.length) {
    els.findingsTable.innerHTML = '<tr><td colspan="5" class="empty">No findings for this scan.</td></tr>';
    return;
  }
  els.findingsTable.innerHTML = findings
    .map(
      (finding) => `
      <tr>
        <td><span class="pill ${escapeHtml(finding.severity)}">${escapeHtml(finding.severity)}</span></td>
        <td>${escapeHtml(finding.rule_id)}</td>
        <td>${escapeHtml(finding.path || "")}</td>
        <td>${escapeHtml(finding.title)}<br /><span class="empty">${escapeHtml(finding.message)}</span></td>
        <td>${escapeHtml(finding.recommendation)}</td>
      </tr>`
    )
    .join("");
}

function clearScan() {
  els.scanDetails.textContent = "No scan selected.";
  els.findingsTable.innerHTML = '<tr><td colspan="5" class="empty">Run a scan to see findings.</td></tr>';
  els.severityStats.innerHTML = "";
  els.reportLink.classList.add("hidden");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

els.projectForm.addEventListener("submit", addProject);
els.projects.addEventListener("click", handleProjectClick);
els.refreshButton.addEventListener("click", loadProjects);

loadHealth();
loadProjects().catch((error) => {
  els.projects.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
});

