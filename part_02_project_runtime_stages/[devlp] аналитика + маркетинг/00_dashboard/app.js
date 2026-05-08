const data = window.PIPELINE_DASHBOARD_DATA;

const stageNav = document.getElementById("stage-nav");
const projectMeta = document.getElementById("project-meta");
const panelTop = document.getElementById("panel-top");
const panelContent = document.getElementById("panel-content");

const stage01 = data.stages.find((stage) => stage.id === "01");
const stage02 = data.stages.find((stage) => stage.id === "02");
const stage03 = data.stages.find((stage) => stage.id === "03");
const stage04 = data.stages.find((stage) => stage.id === "04");
const stage05 = data.stages.find((stage) => stage.id === "05");
const stage06 = data.stages.find((stage) => stage.id === "06");
const stage07 = data.stages.find((stage) => stage.id === "07");

const state = {
  stageId: data.stages[0]?.id ?? "01",
  selected01: "summary",
  selected02: stage02?.markups?.[0]?.product_key ?? null,
  selected02PatternId: null,
  selected03: stage03?.matrices?.[0]?.matrix_key ?? null,
  matrixFilter: "all",
  selected04: stage04?.conclusions?.[0]?.product_key ?? null,
  selected05: stage05?.strategies?.[0]?.product_key ?? null,
  selected06: stage06?.funnels?.[0]?.product_key ?? null,
  selected07: stage07?.card_layers?.[0]?.product_key ?? null,
};

const passportMap = new Map(
  (stage01?.passports ?? []).map((passport) => [passport.product_key, passport]),
);

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function roleLabel(role) {
  const labels = {
    hero: "Герой",
    direct_competitors: "Прямой",
    indirect_competitors: "Косвенный",
    project: "Проект",
  };
  return labels[role] ?? role;
}

function humanTitleFromKey(key) {
  const passport = passportMap.get(key);
  if (passport?.brand && passport?.product_name) {
    return `${passport.brand} · ${passport.product_name}`;
  }
  return key
    .replace(/^hero_/, "")
    .replace(/^direct_/, "")
    .replace(/^indirect_/, "")
    .replaceAll("_", " ");
}

function stageCount(stage) {
  if (stage.id === "01") return `${stage.passports.length} паспортов`;
  if (stage.id === "02") return `${stage.markups.length} разметок`;
  if (stage.id === "03") return `${stage.matrices.length} матриц`;
  if (stage.id === "04") return `${stage.conclusions.length} выводов`;
  if (stage.id === "05") return `${stage.strategies.length} стратегий`;
  if (stage.id === "06") return `${stage.funnels.length} воронок`;
  if (stage.id === "07") return `${stage.card_layers.length} слоёв карточки`;
  return "";
}

function matrixKindLabel(kind) {
  const labels = {
    technical: "03a черновик",
    local: "03 рабочая",
    master: "мастер",
  };
  return labels[kind] ?? kind;
}

function render() {
  renderStageRail();
  renderProjectMeta();
  renderPanelTop();
  renderPanelContent();
}

function renderStageRail() {
  stageNav.innerHTML = data.stages
    .map((stage) => {
      const active = stage.id === state.stageId ? "active" : "";
      return `
        <button class="stage-button ${active}" data-stage-id="${stage.id}">
          <span class="stage-id">${escapeHtml(stage.id)}</span>
          <h2 class="stage-title">${escapeHtml(stage.title)}</h2>
          <p class="stage-label">${escapeHtml(stage.label)}</p>
          <p class="stage-count">${escapeHtml(stageCount(stage))}</p>
        </button>
      `;
    })
    .join("");

  stageNav.querySelectorAll(".stage-button").forEach((button) => {
    button.addEventListener("click", () => {
      state.stageId = button.dataset.stageId;
      render();
    });
  });
}

function renderProjectMeta() {
  const counts = data.project.counts;
  projectMeta.innerHTML = `
    <p class="meta-line">Обновлено: ${escapeHtml(data.project.updated_at)}</p>
    <p class="meta-line">Паспорта: ${counts.passports}</p>
    <p class="meta-line">Разметки: ${counts.signal_markups}</p>
    <p class="meta-line">Матрицы: ${counts.matrices}</p>
    <p class="meta-line">Выводы: ${counts.matrix_conclusions ?? 0}</p>
    <p class="meta-line">Стратегии: ${counts.strategies ?? 0}</p>
    <p class="meta-line">Воронки: ${counts.funnels ?? 0}</p>
    <p class="meta-line">Слои карточки: ${counts.card_layers ?? 0}</p>
    <p class="source-path">${escapeHtml(data.project.root)}</p>
  `;
}

function currentStage() {
  return data.stages.find((stage) => stage.id === state.stageId);
}

function renderPanelTop() {
  const stage = currentStage();
  panelTop.innerHTML = `
    <p class="panel-kicker fade-up">${escapeHtml(stage.folder)}</p>
    <h2 class="panel-title fade-up">${escapeHtml(stage.label)}</h2>
    <p class="panel-subtitle fade-up">${escapeHtml(stage.summary)}</p>
  `;
}

function renderPanelContent() {
  const stage = currentStage();
  if (stage.id === "01") {
    renderStage01(stage);
    return;
  }
  if (stage.id === "02") {
    renderStage02(stage);
    return;
  }
  if (stage.id === "03") {
    renderStage03(stage);
    return;
  }
  if (stage.id === "04") {
    renderStage04(stage);
    return;
  }
  if (stage.id === "05") {
    renderStage05(stage);
    return;
  }
  if (stage.id === "06") {
    renderStage06(stage);
    return;
  }
  if (stage.id === "07") {
    renderStage07(stage);
    return;
  }
}

function metricCard(label, value, foot = "") {
  return `
    <article class="metric-card fade-up">
      <p class="metric-label">${escapeHtml(label)}</p>
      <p class="metric-value">${escapeHtml(value)}</p>
      ${foot ? `<p class="metric-foot">${escapeHtml(foot)}</p>` : ""}
    </article>
  `;
}

function section(title, content, note = "") {
  return `
    <section class="panel-section fade-up">
      <div class="section-head">
        <div>
          <h3 class="section-title">${escapeHtml(title)}</h3>
          ${note ? `<p class="small-note">${escapeHtml(note)}</p>` : ""}
        </div>
      </div>
      <div class="section-body">${content}</div>
    </section>
  `;
}

function renderPills(items, active, onClickName) {
  return `
    <div class="subtab-pills">
      ${items
        .map((item) => {
          const selected = item.id === active ? "active" : "";
          return `
            <button class="pill ${selected}" data-handler="${onClickName}" data-id="${escapeHtml(item.id)}">
              ${escapeHtml(item.title)}
              ${item.subtitle ? `<small>${escapeHtml(item.subtitle)}</small>` : ""}
            </button>
          `;
        })
        .join("")}
    </div>
  `;
}

function bindPills() {
  panelContent.querySelectorAll(".pill").forEach((pill) => {
    pill.addEventListener("click", () => {
      const handler = pill.dataset.handler;
      const id = pill.dataset.id;
      if (handler === "stage01") state.selected01 = id;
      if (handler === "stage02") {
        if (state.selected02 !== id) state.selected02PatternId = null;
        state.selected02 = id;
      }
      if (handler === "stage03") {
        if (state.selected03 !== id) state.matrixFilter = "all";
        state.selected03 = id;
      }
      if (handler === "stage04") state.selected04 = id;
      if (handler === "stage05") state.selected05 = id;
      if (handler === "stage06") state.selected06 = id;
      if (handler === "stage07") state.selected07 = id;
      renderPanelContent();
    });
  });
}

function renderTable(rows) {
  if (!rows.length) {
    return `<div class="empty-state">Пока нечего показать.</div>`;
  }
  const headers = Object.keys(rows[0]);
  return `
    <div class="table-shell">
      <table>
        <thead>
          <tr>${headers.map((header) => `<th>${escapeHtml(header)}</th>`).join("")}</tr>
        </thead>
        <tbody>
          ${rows
            .map(
              (row) => `
            <tr>
              ${headers.map((header) => `<td>${escapeHtml(row[header] ?? "")}</td>`).join("")}
            </tr>
          `,
            )
            .join("")}
        </tbody>
      </table>
    </div>
  `;
}

function listBlock(items, emptyLabel = "Пока пусто") {
  if (!items?.length) {
    return `<div class="empty-state">${escapeHtml(emptyLabel)}</div>`;
  }
  const max = Math.max(...items.map((item) => item.reviews || 0), 1);
  return `
    <div class="list-block">
      ${items
        .map((item) => {
          const width = Math.max(8, Math.round(((item.reviews || 0) / max) * 100));
          return `
            <article class="list-item">
              <div class="list-line">
                <div class="list-name">${escapeHtml(item.label)}</div>
                <div class="list-count">${item.reviews || 0}</div>
              </div>
              <div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div>
            </article>
          `;
        })
        .join("")}
    </div>
  `;
}

function bulletList(items, emptyLabel = "Пока пусто") {
  if (!items?.length) {
    return `<div class="empty-state">${escapeHtml(emptyLabel)}</div>`;
  }
  return `
    <div class="list-block">
      ${items
        .map((item) => `<div class="list-item"><div class="list-name">${escapeHtml(item)}</div></div>`)
        .join("")}
    </div>
  `;
}

function flattenSignalPatterns(markup) {
  if (!markup) return [];
  return [
    ...(markup.positives ?? []),
    ...(markup.negatives ?? []),
    ...(markup.scenarios ?? []),
    ...(markup.comparisons ?? []),
  ];
}

function patternIdPreview(ids = []) {
  if (!ids.length) return "Без привязки к ID";
  const preview = ids.slice(0, 6).join(", ");
  const tail = ids.length > 6 ? ` +${ids.length - 6}` : "";
  return `ID отзывов: ${preview}${tail}`;
}

function renderPatternList(items, activeId, emptyLabel = "Пока пусто") {
  if (!items?.length) {
    return `<div class="empty-state">${escapeHtml(emptyLabel)}</div>`;
  }
  return `
    <div class="pattern-stack">
      ${items
        .map((item) => {
          const active = item.id === activeId ? "active" : "";
          const genericBadge = item.generic
            ? `<span class="pattern-badge">слишком общий ярлык</span>`
            : "";
          return `
            <button class="pattern-card ${active}" data-pattern-id="${escapeHtml(item.id)}">
              <div class="pattern-topline">
                <span class="pattern-count">${escapeHtml(String(item.reviews ?? 0))}</span>
                ${genericBadge}
              </div>
              <div class="pattern-label">${escapeHtml(item.label)}</div>
              ${item.example ? `<div class="pattern-example">пример: ${escapeHtml(item.example)}</div>` : ""}
              <div class="pattern-meta">${escapeHtml(patternIdPreview(item.review_ids ?? []))}</div>
            </button>
          `;
        })
        .join("")}
    </div>
  `;
}

function renderPatternFocus(activePattern, shown, total) {
  if (!activePattern) {
    return `
      <div class="focus-panel fade-up">
        <div>
          <p class="pill-label">Трассировка сигнала</p>
          <p class="focus-copy">Нажми на любой паттерн выше, и ниже останутся только те отзывы, где этот сигнал виден.</p>
        </div>
      </div>
    `;
  }
  return `
    <div class="focus-panel fade-up">
      <div>
        <p class="pill-label">Фильтр по сигналу</p>
        <p class="focus-title">${escapeHtml(activePattern.label)}</p>
        ${activePattern.example ? `<p class="focus-copy">Пример из разметки: ${escapeHtml(activePattern.example)}</p>` : ""}
        <p class="focus-copy">Показано ${escapeHtml(String(shown))} из ${escapeHtml(String(total))} отзывов.</p>
      </div>
      <button class="clear-filter" data-clear-pattern="true">Сбросить фильтр</button>
    </div>
  `;
}

function renderSignalEntries(entries, activeLabel = "") {
  if (!entries?.length) return `<div class="signal-entry empty">Нет сигналов</div>`;
  return `
    <div class="signal-entry-stack">
      ${entries
        .map((entry) => {
          const isMatch = activeLabel && entry.label === activeLabel ? "active" : "";
          return `
            <div class="signal-entry ${isMatch}">
              <div class="signal-entry-label">${escapeHtml(entry.label)}</div>
              ${entry.evidence ? `<div class="signal-entry-evidence">${escapeHtml(entry.evidence)}</div>` : ""}
            </div>
          `;
        })
        .join("")}
    </div>
  `;
}

function renderOverlayTable(rows, activePattern) {
  if (!rows.length) {
    return `<div class="empty-state">Нет отзывов для показа.</div>`;
  }
  const activeLabel = activePattern?.label ?? "";
  return `
    <div class="table-shell overlay-table-shell">
      <table class="overlay-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Автор</th>
            <th>Отзыв</th>
            <th>Сигналы</th>
          </tr>
        </thead>
        <tbody>
          ${rows
            .map((row) => `
              <tr class="${activeLabel ? "is-filtered-row" : ""}">
                <td class="overlay-id">${escapeHtml(row.id)}</td>
                <td class="overlay-author">
                  <div>${escapeHtml(row.author || "—")}</div>
                  ${row.date && row.date !== "—" ? `<div class="overlay-date">${escapeHtml(row.date)}</div>` : ""}
                </td>
                <td><div class="overlay-review">${escapeHtml(row.review || "—")}</div></td>
                <td>${renderSignalEntries(row.signals ?? [], activeLabel)}</td>
              </tr>
            `)
            .join("")}
        </tbody>
      </table>
    </div>
  `;
}

function bindSignalPatterns() {
  panelContent.querySelectorAll(".pattern-card").forEach((card) => {
    card.addEventListener("click", () => {
      const id = card.dataset.patternId;
      state.selected02PatternId = state.selected02PatternId === id ? null : id;
      renderPanelContent();
    });
  });

  const clearButton = panelContent.querySelector("[data-clear-pattern='true']");
  if (clearButton) {
    clearButton.addEventListener("click", () => {
      state.selected02PatternId = null;
      renderPanelContent();
    });
  }
}

function compareCard(item) {
  const cleanReviews = item.stats?.B_clean ?? "—";
  const signals = item.stats?.N_signals_total ?? "—";
  const positive = item.positives?.[0]?.label ?? "—";
  const negative = item.negatives?.[0]?.label ?? "—";
  const comparison = item.comparisons?.[0]?.example || item.comparisons?.[0]?.label || "—";
  return `
    <article class="compare-card fade-up">
      <span class="compare-chip">${escapeHtml(roleLabel(item.role))}</span>
      <h4 class="compare-title">${escapeHtml(humanTitleFromKey(item.product_key))}</h4>
      <p class="compare-foot">Clean reviews: ${escapeHtml(cleanReviews)}</p>
      <p class="compare-foot">Signals total: ${escapeHtml(signals)}</p>
      <p class="compare-foot">Top positive: ${escapeHtml(positive)}</p>
      <p class="compare-foot">Top negative: ${escapeHtml(negative)}</p>
      <p class="compare-foot">Top comparison: ${escapeHtml(comparison)}</p>
    </article>
  `;
}

function renderStage01(stage) {
  const priceRows = stage.price_snapshot.rows;
  const summaryCards = `
    <div class="metric-grid">
      ${metricCard("Паспорта", String(stage.passports.length), "Только живые рабочие паспорта")}
      ${metricCard("Герой", "1", "Hero product passport")}
      ${metricCard("Прямые", "2", "Два прямых конкурента")}
      ${metricCard("Косвенные", "2", "Два косвенных конкурента")}
    </div>
  `;

  const compareCards = `
    <div class="compare-grid">
      ${stage.passports
        .map(
          (passport) => `
            <article class="compare-card fade-up">
              <span class="compare-chip">${escapeHtml(roleLabel(passport.role))}</span>
              <h4 class="compare-title">${escapeHtml(humanTitleFromKey(passport.product_key))}</h4>
              <p class="compare-foot">Цена: ${escapeHtml(passport.price)}</p>
              <p class="compare-foot">Объём: ${escapeHtml(passport.volume)}</p>
              <p class="compare-foot">Нужно проверить: ${passport.claims_to_check.length}</p>
              <p class="compare-foot">Неясности: ${passport.missing_or_unclear.length}</p>
            </article>
          `,
        )
        .join("")}
    </div>
  `;

  const pillItems = [
    { id: "summary", title: "Сводка", subtitle: "Цена и все паспорта" },
    ...stage.passports.map((passport) => ({
      id: passport.product_key,
      title: humanTitleFromKey(passport.product_key),
      subtitle: roleLabel(passport.role),
    })),
  ];

  const selectedPassport =
    state.selected01 === "summary"
      ? null
      : stage.passports.find((passport) => passport.product_key === state.selected01);

  let detailContent = compareCards;
  if (selectedPassport) {
    detailContent = `
      <div class="passport-grid">
        <article class="passport-card fade-up">
          <p class="pill-label">Продукт</p>
          <p class="metric-value">${escapeHtml(selectedPassport.product_name)}</p>
          <p class="metric-foot">${escapeHtml(selectedPassport.brand)} · ${escapeHtml(roleLabel(selectedPassport.role))}</p>
          <p class="metric-foot">${escapeHtml(selectedPassport.category)}</p>
        </article>
        <article class="passport-card fade-up">
          <p class="pill-label">Цена и объём</p>
          <p class="metric-value">${escapeHtml(selectedPassport.price)}</p>
          <p class="metric-foot">${escapeHtml(selectedPassport.volume)}</p>
          <p class="metric-foot">${escapeHtml(selectedPassport.unit_price)}</p>
        </article>
        <article class="passport-card fade-up">
          <p class="pill-label">Главный claim</p>
          <p class="metric-foot">${escapeHtml(selectedPassport.seller_main_claim)}</p>
        </article>
      </div>
      <div class="signal-grid">
        <article class="signal-card fade-up">
          <p class="pill-label">Use cases</p>
          ${selectedPassport.declared_use_cases.length
            ? `<div class="list-block">${selectedPassport.declared_use_cases
                .slice(0, 8)
                .map((item) => `<div class="list-item"><div class="list-name">${escapeHtml(item)}</div></div>`)
                .join("")}</div>`
            : `<div class="empty-state">Нет use cases</div>`}
        </article>
        <article class="signal-card fade-up">
          <p class="pill-label">Проверить в отзывах</p>
          ${selectedPassport.claims_to_check.length
            ? `<div class="list-block">${selectedPassport.claims_to_check
                .slice(0, 8)
                .map((item) => `<div class="list-item"><div class="list-name">${escapeHtml(item)}</div></div>`)
                .join("")}</div>`
            : `<div class="empty-state">Пока пусто</div>`}
        </article>
        <article class="signal-card fade-up">
          <p class="pill-label">Опасные overpromises</p>
          ${selectedPassport.possible_overpromises.length
            ? `<div class="list-block">${selectedPassport.possible_overpromises
                .slice(0, 8)
                .map((item) => `<div class="list-item"><div class="list-name">${escapeHtml(item)}</div></div>`)
                .join("")}</div>`
            : `<div class="empty-state">Нет</div>`}
        </article>
        <article class="signal-card fade-up">
          <p class="pill-label">Неясности</p>
          ${selectedPassport.missing_or_unclear.length
            ? `<div class="list-block">${selectedPassport.missing_or_unclear
                .slice(0, 8)
                .map((item) => `<div class="list-item"><div class="list-name">${escapeHtml(item)}</div></div>`)
                .join("")}</div>`
            : `<div class="empty-state">Нет</div>`}
        </article>
      </div>
      <p class="source-path">${escapeHtml(selectedPassport.path)}</p>
    `;
  }

  panelContent.innerHTML = `
    ${section("Stage Summary", summaryCards, "Собрано по папке 01_intake")}
    ${section("Price Snapshot", renderTable(priceRows), "Сводная сравнимая таблица по пяти продуктам")}
    ${section("Паспорта продуктов", renderPills(pillItems, state.selected01, "stage01") + `<div style="height:16px"></div>` + detailContent, "Переключай продукты, чтобы смотреть паспорт человеческими блоками")}
  `;

  bindPills();
}

function renderStage02(stage) {
  const pillItems = stage.markups.map((markup) => ({
    id: markup.product_key,
    title: humanTitleFromKey(markup.product_key),
    subtitle: roleLabel(markup.role),
  }));

  const selected = stage.markups.find((markup) => markup.product_key === state.selected02) || stage.markups[0];
  if (selected) state.selected02 = selected.product_key;

  const stats = selected?.stats ?? {};
  const allPatterns = flattenSignalPatterns(selected);
  const activePattern = allPatterns.find((item) => item.id === state.selected02PatternId) || null;
  if (!activePattern) state.selected02PatternId = null;
  const overlayRows = selected?.overlay_rows ?? [];
  const filteredRows = activePattern
    ? overlayRows.filter((row) => (row.signal_labels ?? []).includes(activePattern.label))
    : overlayRows;
  const genericComparisons = (selected?.comparisons ?? []).filter((item) => item.generic);
  const metrics = `
    <div class="metric-grid">
      ${metricCard("Clean reviews", stats.B_clean ?? "—", "Отзывы после очистки")}
      ${metricCard("Signals total", stats.N_signals_total ?? "—", "Все surviving signals")}
      ${metricCard("Trash", stats.N_trash ?? "—", "Шум и пустые отзывы")}
      ${metricCard("Manual queue", stats.N_manual ?? "—", "Сложные фрагменты")}
    </div>
  `;

  const detail = selected
    ? `
      ${genericComparisons.length
        ? `<div class="diagnostic-note fade-up">Часть сравнений в исходной разметке уже названа слишком общо. Поэтому здесь я показываю не только ярлык, но и живой пример плюс ID отзывов, чтобы конкретика не терялась.</div>`
        : ""}
      <div class="signal-grid">
        <article class="signal-card fade-up">
          <p class="pill-label">Позитив</p>
          ${renderPatternList(selected.positives, state.selected02PatternId, "Нет позитивных паттернов")}
        </article>
        <article class="signal-card fade-up">
          <p class="pill-label">Негатив</p>
          ${renderPatternList(selected.negatives, state.selected02PatternId, "Нет негативных паттернов")}
        </article>
        <article class="signal-card fade-up">
          <p class="pill-label">Сценарии</p>
          ${renderPatternList(selected.scenarios, state.selected02PatternId, "Нет сценариев")}
        </article>
        <article class="signal-card fade-up">
          <p class="pill-label">Сравнения</p>
          ${renderPatternList(selected.comparisons, state.selected02PatternId, "Нет сравнений")}
        </article>
      </div>
      <div style="height:16px"></div>
      ${renderPatternFocus(activePattern, filteredRows.length, overlayRows.length)}
      <div style="height:16px"></div>
      ${renderOverlayTable(filteredRows, activePattern)}
      <p class="source-path">${escapeHtml(selected.path)}</p>
    `
    : `<div class="empty-state">Пока нет разметок.</div>`;

  panelContent.innerHTML = `
    ${section("Сравнение продуктов", `<div class="compare-grid">${stage.markups.map(compareCard).join("")}</div>`, "Быстрый обзор по каждому крему")}
    ${section("Signal Details", renderPills(pillItems, state.selected02, "stage02") + `<div style="height:16px"></div>` + metrics + `<div style="height:16px"></div>` + detail, "Переключай продукт и смотри паттерны без открытия Markdown")}
  `;

  bindPills();
  bindSignalPatterns();
}

function actionPill(action) {
  return `<span class="action-pill action-${escapeHtml(action)}">${escapeHtml(action)}</span>`;
}

function renderMatrixTable(rows, columns = []) {
  if (!rows.length) {
    return `<div class="empty-state">Нет строк для показа.</div>`;
  }

  const fallbackHeaders = Object.keys(rows[0]);
  const headers = columns.length ? columns : fallbackHeaders;

  return `
    <div class="table-shell">
      <table>
        <thead>
          <tr>${headers.map((header) => `<th>${escapeHtml(header)}</th>`).join("")}</tr>
        </thead>
        <tbody>
          ${rows
            .map(
              (row) => `
                <tr>
                  ${headers
                    .map((header) => {
                      const value = row[header] ?? "";
                      if (header === "Technical action" || header === "Статус") {
                        return `<td>${actionPill(value)}</td>`;
                      }
                      return `<td>${escapeHtml(value)}</td>`;
                    })
                    .join("")}
                </tr>
              `,
            )
            .join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderMatrixFilters(matrix) {
  const statuses = Object.keys(matrix?.counts ?? {}).sort();
  const filters = [["all", "Все"], ...statuses.map((status) => [status, status])];
  return `
    <div class="matrix-filter">
      ${filters
        .map(
          ([id, label]) => `
            <button class="filter-chip ${state.matrixFilter === id ? "active" : ""}" data-filter="${id}">
              ${escapeHtml(label)}
            </button>
          `,
        )
        .join("")}
    </div>
  `;
}

function bindMatrixFilters() {
  panelContent.querySelectorAll(".filter-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      state.matrixFilter = chip.dataset.filter;
      renderPanelContent();
    });
  });
}

function renderTinyList(items = []) {
  if (!items.length) return "";
  return `
    <div class="tiny-list">
      ${items.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}
    </div>
  `;
}

function renderSpecialistRouting(specialists = []) {
  if (!specialists.length) {
    return `<div class="empty-state">Специалисты для этого этапа пока не описаны.</div>`;
  }
  return `
    <div class="specialist-flow">
      ${specialists
        .map(
          (specialist) => `
            <article class="specialist-card fade-up">
              <div class="specialist-topline">
                <span class="stage-badge">${escapeHtml(specialist.stage)}</span>
                <span class="role-badge ${escapeHtml(specialist.decision_role)}">${escapeHtml(specialist.decision_role)}</span>
              </div>
              <h4 class="specialist-name">${escapeHtml(specialist.name)}</h4>
              <p class="specialist-authority">${escapeHtml(specialist.authority)}</p>
              <div class="specialist-columns">
                <div>
                  <p class="mini-heading">Что делает</p>
                  ${renderTinyList(specialist.does)}
                </div>
                <div>
                  <p class="mini-heading">Не делает</p>
                  ${renderTinyList(specialist.does_not)}
                </div>
              </div>
              <div class="toolkit-strip">
                <p class="mini-heading">Чемоданчик</p>
                ${(specialist.tools ?? [])
                  .map(
                    (tool) => `
                      <div class="tool-chip">
                        <strong>${escapeHtml(tool.name)}</strong>
                        <span>${escapeHtml(tool.why)}</span>
                      </div>
                    `,
                  )
                  .join("")}
              </div>
              <p class="specialist-impact">${escapeHtml(specialist.influence)}</p>
              <p class="modifier-status">${escapeHtml(specialist.modifier_status)}</p>
              <p class="source-path">${escapeHtml(specialist.profile_path || specialist.toolkit_path || "")}</p>
            </article>
          `,
        )
        .join("")}
    </div>
  `;
}

function renderRoutingNotice(matrix) {
  if (!matrix?.routing_note || matrix.routing_status === "approved_or_not_marked") return "";
  return `
    <div class="routing-notice fade-up">
      <p class="routing-status">${escapeHtml(matrix.routing_status)}</p>
      <p>${escapeHtml(matrix.routing_note)}</p>
    </div>
  `;
}

function renderStage03(stage) {
  const pillItems = stage.matrices.map((matrix) => ({
    id: matrix.matrix_key,
    title: humanTitleFromKey(matrix.product_key),
    subtitle: `${roleLabel(matrix.role)} · ${matrixKindLabel(matrix.matrix_kind)}`,
  }));

  const selected = stage.matrices.find((matrix) => matrix.matrix_key === state.selected03) || stage.matrices[0];
  if (selected) state.selected03 = selected.matrix_key;

  const counts = selected?.counts ?? {};
  const filteredRows = (selected?.rows ?? []).filter((row) => {
    if (state.matrixFilter === "all") return true;
    return row[selected?.status_key] === state.matrixFilter;
  });

  const primaryStatuses = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 4);
  const metrics = `
    <div class="metric-grid">
      ${metricCard("Тип матрицы", matrixKindLabel(selected?.matrix_kind), selected?.title ?? "")}
      ${metricCard("Строк", String(selected?.rows?.length ?? 0), "Все строки выбранного файла")}
      ${primaryStatuses
        .map(([status, count]) => metricCard(status, String(count), "Статус строк"))
        .join("")}
    </div>
  `;

  const anchors = selected?.anchors?.length
    ? `<div class="anchor-grid">${selected.anchors
        .map((anchor) => `<article class="anchor-pill fade-up">${escapeHtml(anchor)}</article>`)
        .join("")}</div>`
    : `<div class="empty-state">Нет visible anchors.</div>`;

  panelContent.innerHTML = `
    ${section("Specialist Routing", renderSpecialistRouting(stage.specialists), "Кто принимает решение, кто даёт input и какие чемоданчики влияют на результат")}
    ${section("Matrix Overview", renderPills(pillItems, state.selected03, "stage03") + `<div style="height:16px"></div>` + renderRoutingNotice(selected) + metrics, "03A — технический черновик; 03B/03C — специалистская сборка")}
    ${section("Visible Anchors", anchors, "То, что покупатель может увидеть и что модифицирует чтение строки")}
    ${section("Candidates Table", renderMatrixFilters(selected) + `<div style="height:16px"></div>` + renderMatrixTable(filteredRows, selected?.columns ?? []) + `<p class="source-path" style="margin-top:14px">${escapeHtml(selected?.path ?? "")}</p>`, "Фильтруй по action/status и читай матрицу как таблицу, а не как стену Markdown")}
  `;

  bindPills();
  bindMatrixFilters();
}

function renderHypotheses(hypotheses = []) {
  if (!hypotheses.length) {
    return `<div class="empty-state">Гипотезы пока не оформлены.</div>`;
  }
  return `
    <div class="compare-grid">
      ${hypotheses
        .map(
          (item) => `
            <article class="compare-card fade-up">
              <span class="compare-chip">${escapeHtml(item.confidence_level || "unknown")}</span>
              <h4 class="compare-title">${escapeHtml(item.id)}</h4>
              <p class="compare-foot"><strong>Опора:</strong> ${escapeHtml(item.based_on || "—")}</p>
              <p class="compare-foot"><strong>Интерпретация:</strong> ${escapeHtml(item.interpretation || "—")}</p>
              <p class="compare-foot"><strong>Зачем важно:</strong> ${escapeHtml(item.why_it_matters || "—")}</p>
            </article>
          `,
        )
        .join("")}
    </div>
  `;
}

function renderStage04(stage) {
  const pillItems = stage.conclusions.map((item) => ({
    id: item.product_key,
    title: humanTitleFromKey(item.product_key),
    subtitle: "hero conclusions",
  }));

  const selected = stage.conclusions.find((item) => item.product_key === state.selected04) || stage.conclusions[0];
  if (selected) state.selected04 = selected.product_key;

  const metrics = `
    <div class="metric-grid">
      ${metricCard("Контракты", String(selected?.perception_ready_contracts?.length ?? 0), "Что уже можно нести дальше")}
      ${metricCard("Не наш покупатель", String(selected?.non_target_buyers?.length ?? 0), "Кому мы не подходим")}
      ${metricCard("Опасные минусы", String(selected?.dangerous_negatives?.length ?? 0), "Что сильнее всего ломает сделку")}
      ${metricCard("Гипотезы", String(selected?.hypotheses?.length ?? 0), "Отдельно от видимых выводов")}
    </div>
  `;

  panelContent.innerHTML = `
    ${section("Specialist Routing", renderSpecialistRouting(stage.specialists), "Owner собирает выводы, input даёт человеческую логику, filter режет то, что рынок не выдержит")}
    ${section("Conclusions Overview", renderPills(pillItems, state.selected04, "stage04") + `<div style="height:16px"></div>` + metrics, "Этап 4 уже не размечает сигналы, а переводит матрицу в читаемые выводы")}
    ${section(
      "Видимые выводы",
      `
        <div class="signal-grid">
          <article class="signal-card fade-up">
            <p class="pill-label">Perception-ready contracts</p>
            ${bulletList(selected?.perception_ready_contracts, "Нет готовых контрактов")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Не наш покупатель</p>
            ${bulletList(selected?.non_target_buyers, "Не выделено")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Терпимые минусы</p>
            ${bulletList(selected?.tolerable_negatives, "Не выделено")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Опасные минусы</p>
            ${bulletList(selected?.dangerous_negatives, "Не выделено")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Claim risks</p>
            ${bulletList(selected?.claim_risks, "Не выделено")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Рыночные нормы</p>
            ${bulletList(selected?.market_norms, "Не выделено")}
          </article>
        </div>
      `,
      "Здесь уже видно, что можно нести дальше, а что только аккуратно интерпретировать",
    )}
    ${section("Интерпретационные гипотезы", renderHypotheses(selected?.hypotheses ?? []), "Гипотезы вынесены отдельно, чтобы не притворяться фактами")}
    ${section(
      "Что передавать дальше",
      `
        <div class="signal-grid">
          <article class="signal-card fade-up">
            <p class="pill-label">Развивать в стратегию</p>
            ${bulletList(selected?.worth_developing, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Тестировать как гипотезу</p>
            ${bulletList(selected?.worth_testing, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Не тащить дальше</p>
            ${bulletList(selected?.do_not_carry, "Пока пусто")}
          </article>
        </div>
        <p class="source-path" style="margin-top:14px">${escapeHtml(selected?.path ?? "")}</p>
      `,
      "Это уже мостик между мастер-матрицей и выбором рекламного направления",
    )}
  `;

  bindPills();
}

function renderStage05(stage) {
  const pillItems = stage.strategies.map((item) => ({
    id: item.product_key,
    title: humanTitleFromKey(item.product_key),
    subtitle: "strategy decision",
  }));

  const selected = stage.strategies.find((item) => item.product_key === state.selected05) || stage.strategies[0];
  if (selected) state.selected05 = selected.product_key;

  const metrics = `
    <div class="metric-grid">
      ${metricCard("Primary", selected?.primary_direction ?? "—", "Основное направление")}
      ${metricCard("Support", selected?.supporting_direction ?? "—", "Поддерживающее направление")}
      ${metricCard("Allowed lines", String(selected?.allowed?.length ?? 0), "Что можно нести без конфликта")}
      ${metricCard("Tradeoffs", String(selected?.tradeoffs?.length ?? 0), "Чем сознательно жертвуем")}
    </div>
  `;

  panelContent.innerHTML = `
    ${section("Specialist Routing", renderSpecialistRouting(stage.specialists), "Owner выбирает пару, input проверяет поведение, filter режет лишнее, variant даёт отдельный ход при необходимости")}
    ${section("Strategy Overview", renderPills(pillItems, state.selected05, "stage05") + `<div style="height:16px"></div>` + metrics, "Здесь уже выбирается рекламное ядро, которое мы понесём в воронку")}
    ${section(
      "Границы стратегии",
      `
        <div class="signal-grid">
          <article class="signal-card fade-up">
            <p class="pill-label">Можно нести</p>
            ${bulletList(selected?.allowed, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Нельзя нести</p>
            ${bulletList(selected?.blocked, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Claim limits</p>
            ${bulletList(selected?.claim_limits, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Category limits</p>
            ${bulletList(selected?.category_limits, "Пока пусто")}
          </article>
        </div>
      `,
      "Это жёсткий коридор, внутри которого должна жить реклама",
    )}
    ${section("Проверка по авторской матрице", renderTable(selected?.strategy_lines ?? []) , "Какие линии допустимы, а какие режем")}
    ${section(
      "Финальный выбор",
      `
        <div class="passport-grid">
          <article class="passport-card fade-up">
            <p class="pill-label">Primary</p>
            <p class="metric-value">${escapeHtml(selected?.primary_direction ?? "—")}</p>
            <p class="metric-foot">${escapeHtml(selected?.why_primary ?? "—")}</p>
          </article>
          <article class="passport-card fade-up">
            <p class="pill-label">Support</p>
            <p class="metric-value">${escapeHtml(selected?.supporting_direction ?? "—")}</p>
            <p class="metric-foot">${escapeHtml(selected?.why_support ?? "—")}</p>
          </article>
          <article class="passport-card fade-up">
            <p class="pill-label">Почему пара работает</p>
            <p class="metric-foot">${escapeHtml(selected?.why_pair_works ?? "—")}</p>
          </article>
        </div>
      `,
      "Не просто что выбрали, а почему это не развалится после отзывов",
    )}
    ${section(
      "Рекламное ядро",
      `
        <div class="signal-grid">
          <article class="signal-card fade-up">
            <p class="pill-label">Strategy core</p>
            ${bulletList(selected?.strategy_core, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Do not do</p>
            ${bulletList(selected?.do_not_do, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Tradeoffs</p>
            ${bulletList(selected?.tradeoffs, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Open questions</p>
            ${bulletList(selected?.open_questions, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Rejected lines</p>
            ${bulletList(selected?.rejected_lines, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Outside style matrix</p>
            ${bulletList(selected?.outside_style_matrix, "Пока пусто")}
          </article>
        </div>
        <p class="source-path" style="margin-top:14px">${escapeHtml(selected?.path ?? "")}</p>
      `,
      "Это уже почти прямой мост к воронке и будущим слайдам",
    )}
  `;

  bindPills();
}

function renderSlideCards(slides = [], kind = "funnel") {
  if (!slides.length) {
    return `<div class="empty-state">Слайды пока не разобраны.</div>`;
  }
  return `
    <div class="compare-grid">
      ${slides
        .map((slide) => {
          if (kind === "funnel") {
            return `
              <article class="compare-card fade-up">
                <span class="compare-chip">Слайд ${escapeHtml(String(slide.number))}</span>
                <h4 class="compare-title">${escapeHtml(slide.title)}</h4>
                <p class="compare-foot"><strong>Роль:</strong> ${escapeHtml(slide.role || "—")}</p>
                <p class="compare-foot"><strong>Вопрос:</strong> ${escapeHtml(slide.buyer_question || "—")}</p>
                <p class="compare-foot"><strong>Механика:</strong> ${escapeHtml(slide.mechanic || "—")}</p>
                <p class="compare-foot"><strong>Visible support:</strong> ${escapeHtml(slide.visible_support || "—")}</p>
                <p class="compare-foot"><strong>Нельзя:</strong> ${escapeHtml(slide.what_not_to_say || "—")}</p>
              </article>
            `;
          }
          return `
            <article class="compare-card fade-up">
              <span class="compare-chip">Слайд ${escapeHtml(String(slide.number))}</span>
              <h4 class="compare-title">${escapeHtml(slide.title)}</h4>
              <p class="compare-foot"><strong>Strict:</strong> ${escapeHtml(slide.copy_strict || "—")}</p>
              <p class="compare-foot"><strong>Bolder:</strong> ${escapeHtml(slide.copy_bolder || "—")}</p>
              <p class="compare-foot"><strong>Subhead:</strong> ${escapeHtml(slide.subhead || "—")}</p>
              <p class="compare-foot"><strong>Visual task:</strong> ${escapeHtml(slide.visual_task || "—")}</p>
              <p class="compare-foot"><strong>Binding:</strong> ${escapeHtml(slide.visible_support_binding || "—")}</p>
              <p class="compare-foot"><strong>Risk:</strong> ${escapeHtml(slide.claim_risk || "—")}</p>
            </article>
          `;
        })
        .join("")}
    </div>
  `;
}

function renderStage06(stage) {
  const pillItems = stage.funnels.map((item) => ({
    id: item.product_key,
    title: humanTitleFromKey(item.product_key),
    subtitle: "funnel architecture",
  }));

  const selected = stage.funnels.find((item) => item.product_key === state.selected06) || stage.funnels[0];
  if (selected) state.selected06 = selected.product_key;

  const metrics = `
    <div class="metric-grid">
      ${metricCard("Primary", selected?.primary_direction ?? "—", "Из strategy decision")}
      ${metricCard("Support", selected?.supporting_direction ?? "—", "Поддерживающее направление")}
      ${metricCard("Слайды", String(selected?.slides?.length ?? 0), "Рабочая длина воронки")}
      ${metricCard("Ready for stage 7", selected?.ready_for_card_layer ?? "no", "Можно ли нести в copy/visual layer")}
    </div>
  `;

  panelContent.innerHTML = `
    ${section("Specialist Routing", renderSpecialistRouting(stage.specialists), "Owner строит порядок убеждения, input держат стратегию и поведение, filter режет шум")}
    ${section("Funnel Overview", renderPills(pillItems, state.selected06, "stage06") + `<div style="height:16px"></div>` + metrics, "Этап 6 отвечает только за маршрут убеждения, не за финальный copy")}
    ${section(
      "Стратегическая рамка",
      `
        <div class="signal-grid">
          <article class="signal-card fade-up">
            <p class="pill-label">Main buyer question</p>
            <div class="list-block"><div class="list-item"><div class="list-name">${escapeHtml(selected?.main_buyer_question ?? "—")}</div></div></div>
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Main buyer fear</p>
            <div class="list-block"><div class="list-item"><div class="list-name">${escapeHtml(selected?.main_buyer_fear ?? "—")}</div></div></div>
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Main reassurance</p>
            <div class="list-block"><div class="list-item"><div class="list-name">${escapeHtml(selected?.main_reassurance_needed ?? "—")}</div></div></div>
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Do not do</p>
            ${bulletList(selected?.do_not_do, "Пока пусто")}
          </article>
        </div>
      `,
      "Это тот коридор, внутри которого разрешено строить слайды",
    )}
    ${section("Сводная таблица слайдов", renderTable(selected?.slides_table ?? []), "Здесь видно роль и механику каждого слайда без деталей")}
    ${section("Детализация по слайдам", renderSlideCards(selected?.slides ?? [], "funnel"), "Каждый слайд закрывает один вопрос, а не всё сразу")}
    ${section(
      "Stress Test",
      `
        <div class="signal-grid">
          <article class="signal-card fade-up">
            <p class="pill-label">Незаменимость</p>
            ${bulletList(selected?.slide_necessity_check, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Дубли</p>
            ${bulletList(selected?.duplicate_check, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Когнитивный шум</p>
            ${bulletList(selected?.cognitive_noise_check, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Хватает ли reassurance</p>
            ${bulletList(selected?.reassurance_sufficiency_check, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Rejected lines check</p>
            ${bulletList(selected?.rejected_lines_check, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Open questions</p>
            ${bulletList(selected?.open_questions, "Пока пусто")}
          </article>
        </div>
        <p class="source-path" style="margin-top:14px">${escapeHtml(selected?.path ?? "")}</p>
      `,
      "Если убрать слайд без потери логики, значит он лишний",
    )}
  `;

  bindPills();
}

function renderStage07(stage) {
  const pillItems = stage.card_layers.map((item) => ({
    id: item.product_key,
    title: humanTitleFromKey(item.product_key),
    subtitle: "card layer",
  }));

  const selected = stage.card_layers.find((item) => item.product_key === state.selected07) || stage.card_layers[0];
  if (selected) state.selected07 = selected.product_key;

  const metrics = `
    <div class="metric-grid">
      ${metricCard("Primary", selected?.primary_direction ?? "—", "Нельзя менять на этапе 7")}
      ${metricCard("Support", selected?.supporting_direction ?? "—", "Поддерживает primary")}
      ${metricCard("Слайды", String(selected?.slides?.length ?? 0), "Locked slide order")}
      ${metricCard("Ready for QA", selected?.ready_for_qa ?? "no", "Можно ли нести в QA")}
    </div>
  `;

  panelContent.innerHTML = `
    ${section("Specialist Routing", renderSpecialistRouting(stage.specialists), "7A пишет copy, 7B задаёт визуальную задачу, 7C собирает всё в одно")}
    ${section("Card Layer Overview", renderPills(pillItems, state.selected07, "stage07") + `<div style="height:16px"></div>` + metrics, "Этап 7 не меняет воронку, а заполняет её словами и visual tasks")}
    ${section(
      "Locked Inputs",
      `
        <div class="signal-grid">
          <article class="signal-card fade-up">
            <p class="pill-label">Locked slide order</p>
            ${bulletList(selected?.locked_slide_order, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Do not do</p>
            ${bulletList(selected?.do_not_do, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Claim limits</p>
            ${bulletList(selected?.claim_limits, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Visual limits</p>
            ${bulletList(selected?.visual_limits, "Пока пусто")}
          </article>
        </div>
      `,
      "Это замок: этап 7 не имеет права ломать эти ограничения",
    )}
    ${section("Сводная таблица слайдов", renderTable(selected?.slides_table ?? []), "Сразу видно headline A/B, visual task и binding")}
    ${section("Slide Copy + Visual", renderSlideCards(selected?.slides ?? [], "card"), "Здесь уже лежит рабочий текст и визуальная задача по каждому слайду")}
    ${section(
      "Integration Check",
      `
        <div class="signal-grid">
          <article class="signal-card fade-up">
            <p class="pill-label">Copy vs visual conflicts</p>
            ${bulletList(selected?.copy_vs_visual_conflicts, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Funnel role preserved</p>
            ${bulletList(selected?.funnel_role_preserved, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Claim risks</p>
            ${bulletList(selected?.claim_risks, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Visual overpromise risks</p>
            ${bulletList(selected?.visual_overpromise_risks, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Need return to stage 6</p>
            ${bulletList(selected?.needs_return_to_stage_6, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Need return to stage 5</p>
            ${bulletList(selected?.needs_return_to_stage_5, "Пока пусто")}
          </article>
          <article class="signal-card fade-up">
            <p class="pill-label">Open questions</p>
            ${bulletList(selected?.open_questions, "Пока пусто")}
          </article>
        </div>
        <p class="source-path" style="margin-top:14px">${escapeHtml(selected?.path ?? "")}</p>
      `,
      "Последняя проверка перед QA: текст, визуал и funnel не должны спорить друг с другом",
    )}
  `;

  bindPills();
}

render();
