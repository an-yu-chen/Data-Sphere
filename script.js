
const colours = {
  teal: "#087f78",
  blue: "#457b9d",
  gold: "#d59b36",
  rose: "#b75d68",
  grey: "#9aabad"
};

const layoutBase = {
  paper_bgcolor: "#ffffff",
  plot_bgcolor: "#ffffff",
  font: {
    family: "Inter, Arial, sans-serif",
    color: "#314750",
    size: 12
  },
  margin: { l: 55, r: 20, t: 20, b: 50 },
  xaxis: {
    title: "Patent grant year",
    gridcolor: "#edf1f2"
  },
  yaxis: {
    gridcolor: "#edf1f2"
  },
  hovermode: "x unified",
  legend: {
    orientation: "h",
    y: -0.25
  }
};

function readCSV(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = () => {
      const lines = reader.result.trim().split(/\r?\n/);
      const headers = lines[0].split(",").map(x => x.trim());

      const records = lines.slice(1).map(line => {
        const values = line.split(",");
        const row = {};

        headers.forEach((header, index) => {
          const value = values[index];
          row[header] =
            value === undefined || value.trim() === ""
              ? null
              : Number.isNaN(Number(value))
                ? value.trim()
                : Number(value);
        });

        return row;
      });

      resolve(records);
    };

    reader.onerror = reject;
    reader.readAsText(file);
  });
}

function requireColumns(data, columns) {
  if (!data.length) {
    throw new Error("The CSV contains no data rows.");
  }

  const missing = columns.filter(
    column => !(column in data[0])
  );

  if (missing.length) {
    throw new Error("Missing columns: " + missing.join(", "));
  }
}

function createLineChart(elementId, data, series, yTitle, percentage = false) {
  const traces = series.map(item => ({
    x: data.map(row => row.YearOfPatentGrant),
    y: data.map(row => percentage ? row[item.key] * 100 : row[item.key]),
    name: item.name,
    type: "scatter",
    mode: "lines",
    line: { width: 2.7 },
    connectgaps: false
  }));

  Plotly.newPlot(
    elementId,
    traces,
    {
      ...layoutBase,
      yaxis: {
        ...layoutBase.yaxis,
        title: yTitle,
        ticksuffix: percentage ? "%" : ""
      }
    },
    {
      responsive: true,
      displaylogo: false
    }
  );
}

function createBarChart(elementId, data, key, name, yTitle) {
  Plotly.newPlot(
    elementId,
    [{
      x: data.map(row => row.YearOfPatentGrant),
      y: data.map(row => row[key]),
      type: "bar",
      name,
      marker: { color: colours.teal }
    }],
    {
      ...layoutBase,
      yaxis: {
        ...layoutBase.yaxis,
        title: yTitle
      }
    },
    {
      responsive: true,
      displaylogo: false
    }
  );
}

function renderPatentCharts(data) {
  requireColumns(data, [
    "YearOfPatentGrant",
    "patent_count",
    "female_inventor_patent_share",
    "science_using_patent_share",
    "mean_female_ratio",
    "mean_male_ratio",
    "mean_unknown_gender_ratio",
    "average_team_size",
    "average_originality",
    "average_generality"
  ]);

  data.sort((a, b) =>
    a.YearOfPatentGrant - b.YearOfPatentGrant
  );

  createBarChart(
    "patentChart",
    data,
    "patent_count",
    "Patent count",
    "Number of patents"
  );

  createLineChart(
    "femaleChart",
    data,
    [{
      key: "female_inventor_patent_share",
      name: "Patents with female inventors"
    }],
    "Share of patents",
    true
  );

  createLineChart(
    "scienceChart",
    data,
    [{
      key: "science_using_patent_share",
      name: "Patents using science"
    }],
    "Share of patents",
    true
  );

  createLineChart(
    "genderChart",
    data,
    [
      { key: "mean_female_ratio", name: "Female" },
      { key: "mean_male_ratio", name: "Male" },
      { key: "mean_unknown_gender_ratio", name: "Unknown gender" }
    ],
    "Mean inventor share",
    true
  );

  createLineChart(
    "teamChart",
    data,
    [{
      key: "average_team_size",
      name: "Average team size"
    }],
    "Mean team size"
  );

  createLineChart(
    "innovationChart",
    data,
    [
      { key: "average_originality", name: "Originality" },
      { key: "average_generality", name: "Generality" }
    ],
    "Mean indicator"
  );
}

function renderScienceCharts(data) {
  requireColumns(data, [
    "YearOfPatentGrant",
    "science_patent_count",
    "mean_female_science_share",
    "mean_male_science_share"
  ]);

  data.sort((a, b) =>
    a.YearOfPatentGrant - b.YearOfPatentGrant
  );

  createLineChart(
    "scienceGenderChart",
    data.map(row => ({
      ...row,
      YearOfPatentGrant: row.YearOfPatentGrant
    })),
    [
      {
        key: "mean_female_science_share",
        name: "Female-authored science"
      },
      {
        key: "mean_male_science_share",
        name: "Male-authored science"
      }
    ],
    "Mean share",
    true
  );
}

document.getElementById("patentFile")
  .addEventListener("change", async event => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      const data = await readCSV(file);
      renderPatentCharts(data);

      document.getElementById("uploadStatus").textContent =
        `Loaded ${data.length} annual patent records.`;
    } catch (error) {
      document.getElementById("uploadStatus").textContent =
        "Could not load patent data: " + error.message;
    }
  });

document.getElementById("scienceFile")
  .addEventListener("change", async event => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      const data = await readCSV(file);
      renderScienceCharts(data);

      document.getElementById("uploadStatus").textContent +=
        ` Loaded ${data.length} annual science records.`;
    } catch (error) {
      document.getElementById("uploadStatus").textContent =
        "Could not load science data: " + error.message;
    }
  });

// --------------------------------------------------
// PATENT–PUBLICATION KNOWLEDGE NETWORK
// --------------------------------------------------

document.getElementById("networkFile")
  .addEventListener("change", async event => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      const edges = await readCSV(file);
      renderNetwork(edges);

      document.getElementById("networkStatus").textContent =
        `Loaded ${edges.length} patent–publication relationships.`;
    } catch (error) {
      document.getElementById("networkStatus").textContent =
        "Could not load network: " + error.message;
    }
  });

function renderNetwork(edges) {
  requireColumns(edges, ["source", "target"]);

  const nodesMap = new Map();
  const cleanEdges = [];

  edges.forEach(row => {
    const source = String(row.source);
    const target = String(row.target);

    if (!source || !target || source === "null" || target === "null") {
      return;
    }

    // Prefixes keep patent and publication identifiers distinct.
    const sourceId = "patent:" + source;
    const targetId = "publication:" + target;

    if (!nodesMap.has(sourceId)) {
      nodesMap.set(sourceId, {
        id: sourceId,
        label: source,
        type: "Patent",
        degree: 0
      });
    }

    if (!nodesMap.has(targetId)) {
      nodesMap.set(targetId, {
        id: targetId,
        label: target,
        type: "Publication",
        degree: 0
      });
    }

    const weight = Number(row.weight) || 1;

    cleanEdges.push({
      source: sourceId,
      target: targetId,
      weight
    });

    nodesMap.get(sourceId).degree += 1;
    nodesMap.get(targetId).degree += 1;
  });

  const nodes = Array.from(nodesMap.values());

  const patents = nodes.filter(node => node.type === "Patent");
  const papers = nodes.filter(node => node.type === "Publication");

  document.getElementById("nodeCount").textContent =
    nodes.length.toLocaleString();

  document.getElementById("edgeCount").textContent =
    cleanEdges.length.toLocaleString();

  document.getElementById("patentNodes").textContent =
    patents.length.toLocaleString();

  document.getElementById("paperNodes").textContent =
    papers.length.toLocaleString();

  renderNetworkGraph(nodes, cleanEdges);
  renderCentralityTable(nodes);
}

function renderNetworkGraph(nodes, edges) {
  const container = document.getElementById("networkGraph");
  container.innerHTML = "";

  const width = container.clientWidth || 900;
  const height = 480;

  const svg = d3.select(container)
    .append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`);

  const simulationNodes = nodes.map(node => ({ ...node }));
  const simulationLinks = edges.map(edge => ({ ...edge }));

  const simulation = d3.forceSimulation(simulationNodes)
    .force("link", d3.forceLink(simulationLinks)
      .id(node => node.id)
      .distance(45)
      .strength(0.25))
    .force("charge", d3.forceManyBody().strength(-65))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide(9));

  const link = svg.append("g")
    .selectAll("line")
    .data(simulationLinks)
    .join("line")
    .attr("class", "network-link")
    .attr("stroke-width", edge =>
      Math.max(0.5, Math.min(3, edge.weight))
    );

  const node = svg.append("g")
    .selectAll("circle")
    .data(simulationNodes)
    .join("circle")
    .attr("class", "network-node")
    .attr("r", node =>
      Math.min(10, 3 + Math.sqrt(node.degree))
    )
    .attr("fill", node =>
      node.type === "Patent" ? colours.teal : colours.gold
    )
    .append("title")
    .text(node =>
      `${node.type}: ${node.label}\nDegree: ${node.degree}`
    );

  const circles = svg.selectAll("circle");

  circles.call(
    d3.drag()
      .on("start", (event, node) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        node.fx = node.x;
        node.fy = node.y;
      })
      .on("drag", (event, node) => {
        node.fx = event.x;
        node.fy = event.y;
      })
      .on("end", (event, node) => {
        if (!event.active) simulation.alphaTarget(0);
        node.fx = null;
        node.fy = null;
      })
  );

  simulation.on("tick", () => {
    link
      .attr("x1", edge => edge.source.x)
      .attr("y1", edge => edge.source.y)
      .attr("x2", edge => edge.target.x)
      .attr("y2", edge => edge.target.y);

    circles
      .attr("cx", node => node.x)
      .attr("cy", node => node.y);
  });
}

function renderCentralityTable(nodes) {
  const sorted = [...nodes]
    .sort((a, b) => b.degree - a.degree)
    .slice(0, 15);

  const html = `
    <table>
      <thead>
        <tr>
          <th>Node type</th>
          <th>Identifier</th>
          <th>Degree</th>
        </tr>
      </thead>
      <tbody>
        ${sorted.map(node => `
          <tr>
            <td>${node.type}</td>
            <td>${escapeHTML(node.label)}</td>
            <td>${node.degree}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;

  document.getElementById("centralityTable").innerHTML = html;
}

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  })[char]);
}
