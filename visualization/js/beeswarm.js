// NEW: Besides the alphabetical order, layouts can now sorted by their Average Accuracy calculated across all tasks and models for that specific layout.
// Order: From BEST average accuracy (leftmost) to WORST average accuracy (rightmost).
function drawBeeswarmMatrix(containerId, cellData, layoutOrder = 'avg_accuracy') {
    // Draw the BEESWARM MATRIX
    d3.select(containerId).select("svg").remove();

    // Define margins and dimensions
    const margin = { top: 40, right: 30, bottom: 60, left: 60 };
    let width = 1600 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    // Adjust width if in "bastian" mode
    if (currentMode === "bastian") width = (width / 8) * 10;

    // Create the main SVG canvas
    const svg = d3.select(containerId).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g").attr("transform", `translate(${margin.left},${margin.top})`);

    // Deconstruct data
    let { tasks, layouts, models, cells } = cellData;

    // --- DYNAMIC COLUMN (LAYOUT) REORDERING LOGIC ---
    if (layoutOrder === 'avg_accuracy') {
        // Calculate the average accuracy across all tasks/models for each layout
        const layoutAvgMap = {};
        layouts.forEach(layout => {
            const vals = [];
            tasks.forEach(t => {
                models.forEach(m => {
                    const arr = (cells[t] && cells[t][layout] && cells[t][layout][m]) || [];
                    arr.forEach(p => vals.push(p.accuracy));
                });
            });
            layoutAvgMap[layout] = vals.length ? d3.mean(vals) : 0;
        });

        // Sort layouts by descending average accuracy (Best to Worst, Left to Right)
        layouts = layouts.slice().sort((a, b) => (layoutAvgMap[b] || 0) - (layoutAvgMap[a] || 0));

    } else if (layoutOrder === 'alphabetical') {
        // Sort layouts alphabetically by their name
        layouts = layouts.slice().sort((a, b) => a.localeCompare(b));
    }
    // --- END DYNAMIC COLUMN REORDERING ---

    // Function to determine point color based on model and ground truth (gt)
    const colorPicker = d => {
        // Define color palettes
        // const colorOpenAI = ["#b2dde6", "#90e0ef", "#00b4d8", "#0077b6", "#090ca0"];
        // const colorMistral = ["#ffd700", "#ffaf01", "#ff8204", "#fa500f", "#e00500"];
        // const colorGemini = ["#fb8cad", "#e75c9d", "#c80d9b", "#bf1a3b", "#910824"];
        // const colorGLM = ["#91f79f", "#53efb6", "#37c18e", "#118e60", "#056355"];
        // Generate 6 progressively darker shades of the original OpenAI blue using d3.interpolateRgb
        // OpenAI blue shades
        const baseColor = d3.rgb("#b2dde6");
        const darkColor = d3.rgb("#090ca0");
        const colorOpenAI = d3.range(0, 6).map(i =>
            d3.interpolateRgb(baseColor, darkColor)(i / 5)
        );

        // Mistral orange shades
        const baseMistral = d3.rgb("#ffd700");
        const darkMistral = d3.rgb("#fa500f");
        const colorMistral = d3.range(0, 6).map(i =>
            d3.interpolateRgb(baseMistral, darkMistral)(i / 5)
        );

        // Gemini pink shades
        const baseGemini = d3.rgb("#fb8cad");
        const darkGemini = d3.rgb("#910824");
        const colorGemini = d3.range(0, 6).map(i =>
            d3.interpolateRgb(baseGemini, darkGemini)(i / 5)
        );

        // GLM green shades
        const baseGLM = d3.rgb("#53efb6");
        const darkGLM = d3.rgb("#056355");
        const colorGLM = d3.range(0, 6).map(i =>
            d3.interpolateRgb(baseGLM, darkGLM)(i / 5)
        );

        

        let i = 0; // Color index based on gt or task specific logic
        if (d.test.includes("task1")) {
            i = parseInt(d.gt.replace('gt', ''), 10) - 1;
        } else if (d.test.includes("task2")) {
            if ((currentMode === "aurora" && d.gt === "gt3") || (currentMode === "bastian" && d.gt === "gt2")) i = 3;
        } else if (d.test.includes("task3")) {
            const diff = parseInt(d.gt.replace('gt', ''), 10);
            if (currentMode === "bastian") {
                if (diff === 3) i = 3;
                else if (diff === 2) i = 2;
            } else if (diff === 3) i = 3;
        }

        // return colorOpenAI[i]

        // Apply color based on model name
        switch (d.rawModelName) {
            case "gpt-5":
            case "gpt-5-2025-08-07":
                return colorOpenAI[i];
            case "mistral-small-3.1-24b":
                return colorMistral[i];
            case "gemini-2.5-flash":
                return colorGemini[i];
            case "glm-4.5v-106b":
                return colorGLM[i];
            default:
                return "#ccc";
        }
    };

    // Layout settings for the matrix
    const cols = layouts.length;
    const rows = tasks.length;
    const cellPadding = 4;
    const cellInnerPadding = 2;

    const cellWidth = width / Math.max(1, cols);
    const cellHeight = height / Math.max(1, rows);

    // Top column labels (layouts) - now in the chosen order
    svg.selectAll(".col-label").data(layouts).join("text")
        .attr("class", "col-label")
        .attr("x", (_, i) => i * cellWidth + cellWidth / 2)
        .attr("y", -10)
        .attr("text-anchor", "middle")
        .style("font-weight", "600")
        .text(d => d);

    // Left row labels (tasks)
    svg.selectAll(".row-label").data(tasks).join("text")
        .attr("class", "row-label")
        .attr("x", -10)
        .attr("y", (_, i) => i * cellHeight + cellHeight / 2)
        .attr("text-anchor", "end")
        .attr("dominant-baseline", "middle")
        .style("font-weight", "600")
        .text(d => d);

    

    // Create a group for each cell
    const cellGroup = svg.selectAll(".matrix-cell")
        .data(
            // Flatten the task x layout structure into an array of cell objects
            tasks.flatMap((t, r) => layouts.map((l, c) => ({ task: t, layout: l, r, c })))
        )
        .join("g")
        .attr("id", d => `cell-${(d.layout || '').replace(/\s+/g, '_')}-${(d.task || '').replace(/\s+/g, '_')}`)
        .attr("class", "matrix-cell")
        .attr("transform", d => `translate(${d.c * cellWidth}, ${d.r * cellHeight})`);

    // Draw cell backgrounds / borders
    cellGroup.append("rect")
        .attr("x", 0).attr("y", 0)
        .attr("width", cellWidth).attr("height", cellHeight)
        .attr("fill", "white");


    // draw internal grid lines between cells, but not on the outer edges of the matrix
    cellGroup.each(function (cellInfo) {
        // TODO: renable/remove early return, for border between cells
        return;

        const g = d3.select(this);

        // Draw horizontal line (except for the last row)
        if (cellInfo.r < tasks.length - 1) {
        g.append("line")
            .attr("x1", 0)
            .attr("x2", cellWidth)
            .attr("y1", cellHeight)
            .attr("y2", cellHeight)
            .attr("stroke", "#ccc")
            .attr("stroke-width", 0.5);
        }

        // Draw vertical line (except for the last column)
        if (cellInfo.c < layouts.length - 1) {
        g.append("line")
            .attr("x1", cellWidth)
            .attr("x2", cellWidth)
            .attr("y1", 0)
            .attr("y2", cellHeight)
            .attr("stroke", "#ccc")
            .attr("stroke-width", 0.5);
        }
    });

    // For each cell, plot beeswarms for all models
    cellGroup.each(function (cellInfo) {
        const g = d3.select(this);

        const innerX = cellPadding;
        const innerY = cellPadding;
        const innerW = cellWidth - cellPadding * 2;
        const innerH = cellHeight - cellPadding * 2;

        // Y-scale for accuracy (0-100)
        const yScale = d3.scaleLinear().domain([0, 100]).range([innerH - cellInnerPadding, cellInnerPadding]);

        // // Add a style tag to hide the cell Y-axis, only showing it for the first cell
        // if (!document.getElementById('hide-cell-y-axis-style')) {
        //     d3.select("head").append("style")
        //         .attr("id", "hide-cell-y-axis-style")
        //         .text(".cell-y-axis { display: none !important; }");
        // }

        // =================================================================
        // --- DYNAMIC MODEL REORDERING (INSIDE CELL) LOGIC ---
        // Now the order of models within each cell can also be dynamic based on layoutOrder
        
        let modelsOrder; 

        if (layoutOrder === 'avg_accuracy') {
            // If average accuracy, compute per-model means for this cell
            const perModelMeans = new Map();
            models.forEach(m => {
                const arr = (cells[cellInfo.task] && cells[cellInfo.task][cellInfo.layout] && cells[cellInfo.task][cellInfo.layout][m]) || [];
                perModelMeans.set(m, arr.length ? d3.mean(arr, d => d.accuracy) : -Infinity);
            });
            // avg_accuracy: sort models by descending mean accuracy
            modelsOrder = models.slice().sort((a, b) => (perModelMeans.get(b) || 0) - (perModelMeans.get(a) || 0));
        
        } else { // 'alphabetical'
            // If alphabetical, keep original order
            modelsOrder = models.slice(); 
        }

        // Local X slot function that uses this cell's model ordering
        const slotXLocal = i => innerX + (i + 0.5) * (innerW / Math.max(1, modelsOrder.length));
        //
        // --- END OF NEW PART ---
        // =================================================================


        // Collect points for this cell using modelsOrder
        const pts = [];
        modelsOrder.forEach((m, mi) => {
            const arr = (cells[cellInfo.task] && cells[cellInfo.task][cellInfo.layout] && cells[cellInfo.task][cellInfo.layout][m]) || [];
            arr.forEach(d => {
                pts.push(Object.assign({}, d, {
                    modelKey: m,
                    modelIndex: mi,
                    targetX: slotXLocal(mi), // Final X position before collision detection
                    targetY: innerY + yScale(d.accuracy), // Final Y position
                    r: 3 // Radius for force simulation
                }));
            });
        });

        // Handle case with no data
        if (pts.length === 0) {
            g.append("text")
                .attr("x", innerX + innerW / 2) 
                .attr("y", innerY + innerH / 2)
                .attr("text-anchor", "middle")
                .attr("dominant-baseline", "middle")
                .attr("fill", "#999")
                .style("font-size", "10px")
                .text("no data");
            return;
        }

        // Run D3 force simulation for beeswarm effect
        const sim = d3.forceSimulation(pts)
            .force("x", d3.forceX(d => d.targetX).strength(1)) // Stick to target X slot
            .force("y", d3.forceY(d => d.targetY).strength(1)) // Stick to target Y accuracy
            .force("collide", d3.forceCollide(d => d.r + 1)) // Prevent overlap
            .stop();

        // Run simulation for fixed number of ticks (80 is typical for quick convergence)
        for (let i = 0; i < 80; ++i) sim.tick();

        /* constrain simulation results inside the inner plotting area */
        // for (const p of pts) {
            // p.x = Math.max(innerX + p.r, Math.min(innerX + innerW - p.r, p.x));
            // p.y = Math.max(innerY + cellInnerPadding + p.r, Math.min(innerY + innerH - cellInnerPadding - p.r, p.y));
        // }


        // Draw accuracy threshold lines
        const thresholds = [25, 50, 75];
        g.selectAll(".threshold-line").data(thresholds).join("line")
            .attr("class", "threshold-line")
            .attr("x1", innerX).attr("x2", innerX + innerW)
            .attr("y1", d => innerY + yScale(d)).attr("y2", d => innerY + yScale(d))
            .attr("stroke", "#bbb").attr("stroke-width", 3)
            // .attr("stroke-dasharray", "4 8")
            .attr("opacity", 0.55)
            .style("stroke-linecap", "round");

        // Add threshold labels (only on the rightmost column)
        if (cellInfo.c === layouts.length - 1) {
            g.selectAll(".threshold-label").data(thresholds).join("text")
                .attr("class", "threshold-label")
                .attr("x", innerX + innerW + 6)
                .attr("y", d => innerY + yScale(d))
                .attr("text-anchor", "start")
                .attr("dominant-baseline", "middle")
                .attr("fill", "#444")
                .style("font-size", "10px")
                .text(d => d + "%");
        }

        // Draw points (circles)
        const points = g.append("g").attr("class", "points")
            .selectAll("circle").data(pts).join("circle")
            .attr("cx", d => d.x).attr("cy", d => d.y).attr("r", d => d.r)
            .attr("fill", d => colorPicker(d))
            .attr("stroke", d => colorPicker(d))
            .attr("stroke-width", 1)
            // Add tooltip handlers (assuming 'tooltip' element is defined elsewhere)
            .on("mouseover", () => tooltip.style("visibility", "visible"))
            .on("mousemove", (event, d) => {
                tooltip.html(`<b>${d.rawModelName}</b><br>${d.llmMode} / ${d.cotMode}<br>Accuracy: ${d.accuracy.toFixed(1)}%<br>Count: ${d.count}<br>${d.test}`)
                    .style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px");
            })
            .on("mouseout", () => tooltip.style("visibility", "hidden"));

        // Draw mean lines per-model
        const means = d3.rollup(pts, v => d3.mean(v, d => d.accuracy), d => d.modelKey);
        const meanGroup = g.append("g").attr("class", "means");
        Array.from(means.entries()).forEach(([m, meanVal]) => {
            const mi = modelsOrder.indexOf(m); // Use model's index in the local order
            const xCenter = slotXLocal(mi);
            const yPos = innerY + yScale(meanVal);
            const lineW = Math.min(innerW / models.length * 0.7, 40);
            meanGroup.append("line")
                .attr("x1", xCenter - lineW / 2).attr("x2", xCenter + lineW / 2)
                .attr("y1", yPos).attr("y2", yPos)
                .attr("stroke", "#666")
                .attr("stroke-width", 6)
                // .attr("stroke-dasharray", "3 6")
                .style("stroke-linecap", "round");
        });

        // // Add model labels (only on the bottom row)
        // if (cellInfo.r === tasks.length - 1) {
        //     const labelGroup = g.append("g").attr("class", "cell-model-labels");
        //     modelsOrder.forEach((m, mi) => {
        //         labelGroup.append("text")
        //             .attr("x", slotXLocal(mi))
        //             .attr("y", innerY + innerH + 20)
        //             .attr("text-anchor", "middle")
        //             .attr("dominant-baseline", "alphabetic")
        //             .style("font-size", "11px")
        //             .style("fill", "#444")
        //             .text(m.replace(/.*?(gemini|mistral|gpt-5|glm).*/i, s => {
        //                 if (/mistral/i.test(s)) return "Mistral";
        //                 if (/gemini/i.test(s)) return "Gemini";
        //                 if (/gpt-5/i.test(s)) return "gpt-5";
        //                 if (/glm/i.test(s)) return "GLM4.5";
        //                 return s;
        //             }));
        //     });
        // }

        // // Add Y-axis to the left of the first column of cells (first row only)
        // if (cellInfo.c === 0 && cellInfo.r === 0) {
        //     const axisG = g.append("g")
        //         .attr("class", "cell-y-axis")
        //         .attr("transform", `translate(${innerX}, ${innerY})`)
        //         .call(d3.axisLeft(yScale).ticks(3).tickSizeOuter(0));
        //     // Add Y-axis label to the first row only
        //     if (cellInfo.r === 0) {
        //         svg.append("text")
        //             .attr("class", "axis-label")
        //             .attr("text-anchor", "end")
        //             .attr("transform", "rotate(-90)")
        //             .attr("y", -margin.left + 20)
        //             .attr("x", -height / 2 + 50);
        //     }
        // }
    });

    // add a button to download all the g as individual svgs with incremental filenames
    d3.select(containerId).append("button")
        .text("Download SVGs")
        .on("click", () => {
            const gElements = d3.selectAll("g.matrix-cell").nodes();
            gElements.forEach((g, i) => {
                // Clone the <g> node
                const gClone = g.cloneNode(true);
                // Remove the translate from the transform attribute
                gClone.removeAttribute("transform");

                // Create a new SVG element and append the <g> node
                const svgElem = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                svgElem.setAttribute("xmlns", "http://www.w3.org/2000/svg");
                svgElem.setAttribute("width", g.getBBox().width || 200);
                svgElem.setAttribute("height", g.getBBox().height || 200);
                svgElem.appendChild(gClone);

                // Serialize the SVG
                const serializer = new XMLSerializer();
                const svgString = serializer.serializeToString(svgElem);
                const blob = new Blob([svgString], { type: "image/svg+xml" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `beeswarm_cell_${i + 1}.svg`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            });
        });
}


function drawViolinPlot(containerId, cellData, layoutOrder = 'avg_accuracy') {
    // using the same logic as drawBeeswarmMatrix for layout ordering, draw a violin plot instead

    // Draw the BEESWARM MATRIX
    d3.select(containerId).select("svg").remove();

    // Define margins and dimensions
    const margin = { top: 40, right: 30, bottom: 60, left: 60 };
    let width = 1600 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    // Adjust width if in "bastian" mode
    if (currentMode === "bastian") width = (width / 8) * 10;

    const colorPicker = d => {
        // Define color palettes
        // const colorOpenAI = ["#b2dde6", "#90e0ef", "#00b4d8", "#0077b6", "#090ca0"];
        // const colorMistral = ["#ffd700", "#ffaf01", "#ff8204", "#fa500f", "#e00500"];
        // const colorGemini = ["#fb8cad", "#e75c9d", "#c80d9b", "#bf1a3b", "#910824"];
        // const colorGLM = ["#91f79f", "#53efb6", "#37c18e", "#118e60", "#056355"];
        // Generate 6 progressively darker shades of the original OpenAI blue using d3.interpolateRgb
        // OpenAI blue shades
        const baseColor = d3.rgb("#90e0ef");
        const darkColor = d3.rgb("#18455f");
        const colorOpenAI = d3.range(0, 6).map(i =>
            d3.interpolateRgb(baseColor, darkColor)(i / 5)
        );

        // Mistral orange shades
        const baseMistral = d3.rgb("#ffd700");
        const darkMistral = d3.rgb("#e00500");
        const colorMistral = d3.range(0, 6).map(i =>
            d3.interpolateRgb(baseMistral, darkMistral)(i / 5)
        );

        // Gemini pink shades
        const baseGemini = d3.rgb("#fb8cad");
        const darkGemini = d3.rgb("#910824");
        const colorGemini = d3.range(0, 6).map(i =>
            d3.interpolateRgb(baseGemini, darkGemini)(i / 5)
        );

        // GLM green shades
        const baseGLM = d3.rgb("#91f79f");
        const darkGLM = d3.rgb("#056355");
        const colorGLM = d3.range(0, 6).map(i =>
            d3.interpolateRgb(baseGLM, darkGLM)(i / 5)
        );

        // Apply color based on model name
        switch (d) {
            case "gpt-5":
            case "gpt-5-2025-08-07":
                return colorOpenAI[2];
            case "mistral-small-3.1-24b":
                return colorMistral[2];
            case "gemini-2.5-flash":
                return colorGemini[2];
            case "glm-4.5v-106b":
                return colorGLM[2];
            default:
                return "#ccc";
        }
    };

    // Create the main SVG canvas
    const svg = d3.select(containerId).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g").attr("transform", `translate(${margin.left},${margin.top})`);

    // Deconstruct data
    let { tasks, layouts, models, cells } = cellData;

    // --- DYNAMIC COLUMN (LAYOUT) REORDERING LOGIC ---
    if (layoutOrder === 'avg_accuracy') {
        // Calculate the average accuracy across all tasks/models for each layout
        const layoutAvgMap = {};
        layouts.forEach(layout => {
            const vals = [];
            tasks.forEach(t => {
                models.forEach(m => {
                    const arr = (cells[t] && cells[t][layout] && cells[t][layout][m]) || [];
                    arr.forEach(p => vals.push(p.accuracy));
                });
            });
            layoutAvgMap[layout] = vals.length ? d3.mean(vals) : 0;
        });

        // Sort layouts by descending average accuracy (Best to Worst, Left to Right)
        layouts = layouts.slice().sort((a, b) => (layoutAvgMap[b] || 0) - (layoutAvgMap[a] || 0));

    } else if (layoutOrder === 'alphabetical') {
        // Sort layouts alphabetically by their name
        layouts = layouts.slice().sort((a, b) => a.localeCompare(b));
    }

    // Layout settings for the matrix
    const cols = layouts.length;
    const rows = tasks.length;
    const cellPadding = 4;
    const cellInnerPadding = 8;

    const cellWidth = width / Math.max(1, cols);
    const cellHeight = height / Math.max(1, rows);

    // Top column labels (layouts) - now in the chosen order
    svg.selectAll(".col-label").data(layouts).join("text")
        .attr("class", "col-label")
        .attr("x", (_, i) => i * cellWidth + cellWidth / 2)
        .attr("y", -10)
        .attr("text-anchor", "middle")
        .style("font-weight", "600")
        .text(d => d);

    // Left row labels (tasks)
    svg.selectAll(".row-label").data(tasks).join("text")
        .attr("class", "row-label")
        .attr("x", -10)
        .attr("y", (_, i) => i * cellHeight + cellHeight / 2)
        .attr("text-anchor", "end")
        .attr("dominant-baseline", "middle")
        .style("font-weight", "600")
        .text(d => d);

    

    // Create a group for each cell
    const cellGroup = svg.selectAll(".matrix-cell-violin")
        .data(
            // Flatten the task x layout structure into an array of cell objects
            tasks.flatMap((t, r) => layouts.map((l, c) => ({ task: t, layout: l, r, c })))
        )
        .join("g")
        .attr("id", d => `cell-${(d.layout || '').replace(/\s+/g, '_')}-${(d.task || '').replace(/\s+/g, '_')}`)
        .attr("class", "matrix-cell-violin")
        .attr("transform", d => `translate(${d.c * cellWidth}, ${d.r * cellHeight})`);

    // // Draw cell backgrounds / borders
    // cellGroup.append("rect")
    //     .attr("x", 0).attr("y", 0)
    //     .attr("width", cellWidth).attr("height", cellHeight)
    //     .attr("fill", "transparent");

    // For each cell, plot violin plots for all models
    cellGroup.each(function (cellInfo) {
        const g = d3.select(this);
        
        const innerX = cellPadding;
        const innerY = cellPadding;
        const innerW = cellWidth - cellPadding * 2;
        const innerH = cellHeight - cellPadding * 2;
        // Y-scale for accuracy (0-100)
        const yScale = d3.scaleLinear().domain([0, 100]).range([innerH - cellInnerPadding, cellInnerPadding]);
        
        // --- DYNAMIC MODEL REORDERING (INSIDE CELL) LOGIC ---
        let modelsOrder;
        if (layoutOrder === 'avg_accuracy') {
            // If average accuracy, compute per-model means for this cell
            const perModelMeans = new Map();
            models.forEach(m => {
                const arr = (cells[cellInfo.task] && cells[cellInfo.task][cellInfo.layout] && cells[cellInfo.task][cellInfo.layout][m]) || [];
                perModelMeans.set(m, arr.length ? d3.mean(arr, d => d.accuracy) : -Infinity);
            });
            // avg_accuracy: sort models by descending mean accuracy
            modelsOrder = models.slice().sort((a, b) => (perModelMeans.get(b) || 0) - (perModelMeans.get(a) || 0));

        } else { // 'alphabetical'
            // If alphabetical, keep original order
            modelsOrder = models.slice();
        }
        // Local X slot function that uses this cell's model ordering
        const slotXLocal = i => innerX + (i + 0.5) * (innerW / Math.max(1, modelsOrder.length));
        //
        // --- END OF NEW PART ---

        const pts = [];
        modelsOrder.forEach((m, mi) => {
            const arr = (cells[cellInfo.task] && cells[cellInfo.task][cellInfo.layout] && cells[cellInfo.task][cellInfo.layout][m]) || [];
            arr.forEach(d => {
                pts.push(Object.assign({}, d, {
                    modelKey: m,
                    modelIndex: mi,
                    targetX: slotXLocal(mi), // Final X position before collision detection
                    targetY: innerY + yScale(d.accuracy), // Final Y position
                    r: 4.5 // Radius for force simulation
                }));
            });
        });

        // Handle case with no data
        if (pts.length === 0) {
            g.append("text")
                .attr("x", innerX + innerW / 2)
                .attr("y", innerY + innerH / 2)
                .attr("text-anchor", "middle")
                .attr("dominant-baseline", "middle")
                .attr("fill", "#999")
                .style("font-size", "10px")
                .text("no data");
            return;
        }

        // Draw violin plots per model
        modelsOrder.forEach((m, mi) => {
            const modelPts = pts.filter(d => d.modelKey === m).map(d => d.accuracy);
            if (modelPts.length === 0) return;
            
            // Compute kernel density estimation
            // Kernel Density Estimator helper functions
            function kernelDensityEstimator(kernel, X) {
                return function (V) {
                    return X.map(function (x) {
                        return [x, d3.mean(V, function (v) { return kernel(x - v); })];
                    });
                };
            }
            function kernelEpanechnikov(k) {
                return function (v) {
                    v = v / k;
                    return Math.abs(v) <= 1 ? 0.75 * (1 - v * v) / k : 0;
                };
            }

            const kde = kernelDensityEstimator(kernelEpanechnikov(7), yScale.ticks(40));
            const density = kde(modelPts);

            // Scale for violin width
            const xNum = d3.scaleLinear()
                .domain([0, d3.max(density, d => d[1])])
                .range([0, innerW / modelsOrder.length / 2 * 0.8]); // Max width per model
                
            // Draw the violin shape
            const violinG = g.append("g").attr("class", "violin-plot");
            violinG.append("path")
                .datum(density)
                .attr("transform", `translate(${slotXLocal(mi)},0)`)
                .attr("fill", colorPicker(m) || "#ccc")
                .attr("opacity", 0.7)
                .attr("stroke", "#333")
                .attr("stroke-width", 2)
                .style("stroke-linejoin", "round")
                .style("stroke-linecap", "round")
                .attr("d", d3.area()
                    .x0(d => -xNum(d[1]))
                    .x1(d => xNum(d[1]))
                    .y(d => innerY + yScale(d[0]))
                    .curve(d3.curveCatmullRom)
                );

            // Draw median line
            const median = d3.median(modelPts);
            violinG.append("line")
                .attr("x1", slotXLocal(mi) - xNum(d3.max(density, d => d[1])))
                .attr("x2", slotXLocal(mi) + xNum(d3.max(density, d => d[1])))
                .attr("y1", innerY + yScale(median))
                .attr("y2", innerY + yScale(median))
                .attr("stroke", "#666")
                .attr("stroke-width", 2)
                // .attr("stroke-dasharray", "4 4")
                .style("stroke-linecap", "round");
        }
        );
        
    })
}

function drawSingleViolinPlots(containerId, rawData, currentMode) {
    // list all Model Names present in rawData
    const modelNames = Array.from(new Set(rawData.map(d => d["Model Name"])));

    for (let model of modelNames) {
        const modelData = rawData.filter(d => d["Model Name"] === model);
    
        // append an svg to the container
        let svg = d3.select(containerId).append("svg")
            .attr("width", 400)
            .attr("height", 300)
            .append("g")
            .attr("transform", "translate(50,20)");

        // draw a violin plot split by layout, using the distribution of accuracy
        const layouts = ["b-", "b+", "c-", "c+", "m-", "m+", "o-", "o+", "s-", "s+"];

        for (let layout of layouts) {
            let layoutData = modelData.filter(d => d["Layout"].includes(layout));
            layoutData = layoutData.filter(d => d["Task"].includes("task1"));
            
            // group layoutData by layout and COT mode
            const groupedData = d3.group(layoutData, d => d["Layout"], d => d["COT Mode"]);

            // now for every group produce the average accuracy based on Correct Prediction (True/False)
            const accuracyData = [];
            for (let [layout, cotMap] of groupedData) {
                for (let [cotMode, records] of cotMap) {
                    const correctCount = records.filter(d => d["Correct Prediction (True/False)"] === "True").length;
                    const totalCount = records.length;
                    const accuracy = (correctCount / totalCount) * 100;
                    accuracyData.push({
                        layout: layout,
                        cotMode: cotMode,
                        accuracy: accuracy
                    });
                }
            }

            console.log(`Model: ${model}, Layout: ${layout}`, accuracyData);

            // now draw the violin plot for this layout
            // Y-scale for accuracy (0-100)
            const yScale = d3.scaleLinear().domain([0, 100]).range([250, 0]);

            const kde = kernelDensityEstimator(kernelEpanechnikov(7), yScale.ticks(40));
            const density = kde(accuracyData.map(d => d.accuracy));

            // Scale for violin width
            const xNum = d3.scaleLinear()
                .domain([0, d3.max(density, d => d[1])])
                .range([0, 10]); // Max width per model
                
            // Draw the violin shape
            svg.append("path")
                .datum(density)
                .attr("transform", `translate(${layouts.indexOf(layout) * 30 + 30},0)`)
                .attr("fill", "#69b3a2")
                .attr("opacity", 0.7)
                .attr("stroke", "#333")
                .attr("stroke-width", 2)
                .style("stroke-linejoin", "round")
                .style("stroke-linecap", "round")
                .attr("d", d3.area()
                    .x0(d => -xNum(d[1]))
                    .x1(d => xNum(d[1]))
                    .y(d => yScale(d[0]))
                    .curve(d3.curveCatmullRom)
                );

            // Draw median line
            const median = d3.median(accuracyData.map(d => d.accuracy));
            svg.append("line")  
                .attr("x1", layouts.indexOf(layout) * 30 + 30 - xNum(d3.max(density, d => d[1])))
                .attr("x2", layouts.indexOf(layout) * 30 + 30 + xNum(d3.max(density, d => d[1])))
                .attr("y1", yScale(median))
                .attr("y2", yScale(median))
                .attr("stroke", "#666")
                .attr("stroke-width", 2)
                // .attr("stroke-dasharray", "4 4")
                .style("stroke-linecap", "round");

        }

        // title with the name of the model
            svg.append("text")
                .attr("x", 100)
                .attr("y", -5)
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .style("font-weight", "600")
                .text(`${model}`);
    } 
}

// Compute kernel density estimation
            function kernelDensityEstimator(kernel, X) {
                return function (V) {
                    return X.map(function (x) {
                        return [x, d3.mean(V, function (v) { return kernel(x - v); })];
                    });
                };
            }
            function kernelEpanechnikov(k) {
                return function (v) {
                    v = v / k;
                    return Math.abs(v) <= 1 ? 0.75 * (1 - v * v) / k : 0;
                };
            }