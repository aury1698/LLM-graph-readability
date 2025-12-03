
    const colorPicker = d => {
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
                return colorOpenAI[1];
            case "mistral-small-3.1-24b":
                return colorMistral[1];
            case "gemini-2.5-flash":
                return colorGemini[1];
            case "glm-4.5v-106b":
                return colorGLM[1];
            default:
                return "#ccc";
        }
    };

// Draw a GROUPED BAR CHART (both for Tasks or Layouts)
// MODIFIED to accept an optional model name for correct color mapping in model-specific charts
function drawGroupedBarChart(containerId, chartData, groupKey, modelNameForColoring = null) {
    d3.select(containerId).select("svg").remove();
    const { data, categories } = chartData;

    // N.B. MARGINS AND DIMENSIONS for the PLOTTING AREA (this time is independent from legend)
    const margin = { top: 40, right: 40, bottom: 65, left: 60 }; 
    const chartTotalWidth = 550; 
    const width = chartTotalWidth - margin.left - margin.right; 
    const height = 350 - margin.top - margin.bottom; 


    const svg = d3.select(containerId).append("svg")
        .attr("width", width + margin.left + margin.right) 
        .attr("height", height + margin.top + margin.bottom)
        .append("g").attr("transform", `translate(${margin.left},${margin.top})`);
    
    // --- COLOUR MAP (needed for the legend) ---
    
    const getColorMap = (categories) => {
        const colorMap = {};
        categories.forEach(category => {
            const key = category.toLowerCase();
            
            // Use the passed-in model name for specific charts, or parse it from the category for the combined chart
            let modelName = modelNameForColoring; 
            if (!modelName) {
                if (key.startsWith('mistral')) modelName = 'mistral';
                else if (key.startsWith('gemini')) modelName = 'gemini';
                else if (key.startsWith('gpt-5')) modelName = 'gpt-5';
                else if (key.startsWith('glm')) modelName = 'glm';
                else modelName = 'unknown';
            }

            const cotMode = key.includes('(cot)') ? 'cot' : 'no_cot';
            
            let llmMode = 'zero_shot'; 
            if (key.includes('few_shot') || key.includes('few-shot')) {
                llmMode = 'few_shot';
            }
            
            colorMap[category] = getGlobalColor(modelName, llmMode, cotMode);
        });
        return colorMap;
    }

    const colorMap = getColorMap(categories);
    const fallbackColor = d3.scaleOrdinal(d3.schemeTableau10);

    const x0 = d3.scaleBand().domain(data.map(d => d[groupKey])).range([0, width]).padding(0.25);
    const x1 = d3.scaleBand().domain(categories).range([0, x0.bandwidth()]).padding(0.1);
    const y = d3.scaleLinear().domain([0, 100]).range([height, 0]);
    
    const group = svg.selectAll(".group").data(data).join("g")
        .attr("class", "group")
        .attr("transform", d => `translate(${x0(d[groupKey])},0)`);

    group.selectAll("rect").data(d => categories.map(key => ({ key, value: d[key] || 0 })))
        .join("rect")
        .attr("x", d => x1(d.key))
        .attr("y", d => y(d.value))
        .attr("width", x1.bandwidth())
        .attr("height", d => height - y(d.value))
        .attr("fill", d => colorMap[d.key] || fallbackColor(d.key))
        .on("mouseover", () => tooltip.style("visibility", "visible"))
        .on("mousemove", (event, d) => {
            tooltip.html(`<b>${d.key}</b><br>Accuracy: ${d.value.toFixed(2)}%`)
                .style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px");
        })
        .on("mouseout", () => tooltip.style("visibility", "hidden"));
        
    svg.append("g").attr("transform", `translate(0, ${height})`).call(d3.axisBottom(x0))
        .selectAll("text").attr("transform", "translate(-10,0)rotate(-45)").style("text-anchor", "end");
    svg.append("g").call(d3.axisLeft(y).ticks(5));
    svg.append("text").attr("class", "axis-label").attr("text-anchor", "middle").attr("y", -margin.left + 20)
        .attr("x", -height / 2).attr("transform", "rotate(-90)").text("Average Accuracy (%)")
        .style("font-size", "23px")

    svg.selectAll(".tick text").style("font-size", "20px")

    return { categories, getColorMap };
}

function drawGroupedViolinChart(containerId, chartData, groupKey, modelNameForColoring = null) {
    d3.select(containerId).select("svg").remove();
    const { data, categories } = chartData;

    const margin = { top: 10, right: 0, bottom: 35, left: 40 }; 
    const chartTotalWidth = 400; 
    const width = chartTotalWidth - margin.left - margin.right; 
    const height = 200 - margin.top - margin.bottom; 

    const svg = d3.select(containerId).append("svg")
        .attr("width", width + margin.left + margin.right) 
        .attr("height", height + margin.top + margin.bottom)
        .append("g").attr("transform", `translate(${margin.left},${margin.top})`);

    if (currentMode === 'bastian') chartData.layouts = ["b+", "b-", "c+", "c-", "m+", "m-", "o+", "o-", "s+", "s-"];
    else if (currentMode === 'aurora') chartData.layouts = ["FD-FR", "FD-K", "POGBa", "POGBb", "PG", "PGS", "SEIS", "Tu"];

    // Assume categories is an array of enum values
    // Create a scale with extra space every two elements and left padding
    const leftPadding = 30; // pixels to pad from the left
    const step = (width - leftPadding) / (-1 + chartData.layouts.length + Math.floor(chartData.layouts.length / 2));
    let positions = [];
    let pos = leftPadding;
    for (let i = 0; i < chartData.layouts.length; i++) {
        positions.push(pos);
        pos += step;
        if (currentMode == "bastian" && (i + 1) % 2 === 0 && i !== chartData.layouts.length - 1) {
            pos += step; // extra space after every two elements
        } else if (currentMode == "aurora"){
            pos += .5*step; // extra space after every three elements
        }
    }
    const enumScale = d3.scaleOrdinal()
        .domain(chartData.layouts)
        .range(positions);

    // draw the x axis
    svg.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(enumScale))
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

    // Y scale
    const yScale = d3.scaleLinear()
        .domain([0, 100])
        .range([height, 0]);
            
    svg.append("g").call(d3.axisLeft(yScale).ticks(5));

    let modelName = modelNameForColoring;
    if (modelName.includes('Mistral')) modelName = 'mistral-small-3.1-24b';
    else if (modelName.includes('Gemini')) modelName = 'gemini-2.5-flash';
    else if (modelName.includes('GPT')) modelName = 'gpt-5-2025-08-07';
    else if (modelName.includes('GLM')) modelName = 'glm-4.5v-106b';
    if (!chartData.models.includes(modelName)) modelName = "gpt-5";

    for (let layout of chartData.layouts) {
        let points = [];
        for (let task in chartData.cells) {
            if (task != "task1") continue;
            points = points.concat(chartData.cells[task][layout][modelName].map(d => d.accuracy));
        }
        
        // draw violin for this layout
        const accuracyData = points.map(d => ({ accuracy: d }));
        
        // Compute kernel density estimation
        const kde = kernelDensityEstimator(kernelEpanechnikov(7), yScale.ticks(40));
        const density = kde(accuracyData.map(d => d.accuracy));
        // Scale for violin width
        const xNum = d3.scaleLinear()
            .domain([0, d3.max(density, d => d[1])])
            .range([0, 13]); // Max width per model
        
        // Draw the violin shape
        svg.append("path")
            .datum(density)
            .attr("transform", `translate(${enumScale(layout)},0)`)
            .attr("fill", colorPicker(modelName))
            .attr("opacity", 1)
            .attr("stroke", "#666")
            .attr("stroke-linejoin", "round")
            .attr("stroke-width", 3)   
            .attr("d", d3.area()
                .x0(d => -xNum(d[1]))
                .x1(d => xNum(d[1]))
                .y(d => yScale(d[0]))
                .curve(d3.curveCatmullRom));
        
        // Draw median line
        const median = d3.median(accuracyData.map(d => d.accuracy));
        let strokeWidth = 3;
        // Compute medians for all layouts for comparison
        const allMedians = chartData.layouts.map(l => {
            let allPoints = [];
            for (let task in chartData.cells) {
                if (task != "task1") continue;
                allPoints = allPoints.concat(chartData.cells[task][l][modelName].map(d => d.accuracy));
            }
            return d3.median(allPoints);
        });
        const maxMedian = d3.max(allMedians);

        // If the median is higher than all other medians and currentMode is 'aurora', draw it red
        let medianColor = "#333";
        if (
            currentMode === "aurora" &&
            accuracyData.length > 0 &&
            median >= maxMedian
        ) {
            medianColor = "#dd0000";
            strokeWidth = 4;
        }

        if (currentMode === "bastian") {
            // For each pair (+/-), check if the difference in median is at least 5
            const layoutPairs = [["b+", "b-"], ["c+", "c-"], ["m+", "m-"], ["o+", "o-"], ["s+", "s-"]];
            for (const [plus, minus] of layoutPairs) {
                if ((layout === plus || layout === minus) && chartData.layouts.includes(plus) && chartData.layouts.includes(minus)) {
                    // Get medians for both layouts
                    let plusPoints = [], minusPoints = [];
                    for (let task in chartData.cells) {
                        if (task != "task1") continue;
                        plusPoints = plusPoints.concat(chartData.cells[task][plus][modelName].map(d => d.accuracy));
                        minusPoints = minusPoints.concat(chartData.cells[task][minus][modelName].map(d => d.accuracy));
                    }
                    const plusMedian = d3.median(plusPoints);
                    const minusMedian = d3.median(minusPoints);
                    if (Math.abs(plusMedian - minusMedian) >= 10) {
                        medianColor = "#dd0000";
                        strokeWidth = 4;
                    }
                }
            }
        }

        svg.append("line")  
            .attr("x1", enumScale(layout) - 1.1 * xNum(d3.max(density, d => d[1])))
            .attr("x2", enumScale(layout) + 1.1 * xNum(d3.max(density, d => d[1])))
            .attr("y1", yScale(median))
            .attr("y2", yScale(median))
            .attr("stroke", medianColor)
            .attr("stroke-width", strokeWidth)
            .style("stroke-linecap", "round")
            .on("mouseover", () => console.log("median", median));
    }

    
}

function drawTasksViolinPlots(container, data){
    console.log(data)
    
    const margin = { top: 10, right: 0, bottom: 35, left: 40 }; 
    const chartTotalWidth = 200; 
    const width = chartTotalWidth - margin.left - margin.right; 
    const height = 150 - margin.top - margin.bottom; 

    const svg = d3.select(container).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

    const tasks = data.tasks;

    const x = d3.scaleBand()
        .domain(tasks)
        .range([0, width])
        .padding(0.3);

    const y = d3.scaleLinear()
        .domain([0, 100])
        .range([height, 0]);

    g.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "rotate(-30)")
        .style("text-anchor", "end");

    g.append("g").call(d3.axisLeft(y).ticks(3));

    function kernelDensityEstimator(kernel, X) {
        return function(V) {
            return X.map(function(x) {
                return [x, d3.mean(V, function(v) { return kernel(x - v); })];
            });
        };
    }
    function kernelEpanechnikov(k) {
        return function(v) {
            v = v / k;
            return Math.abs(v) <= 1 ? 0.75 * (1 - v * v) / k : 0;
        };
    }

    const kdeY = y.ticks(40);

    tasks.forEach((task, i) => {
        const values = Object.values(data.cells[task]).map(d => Object.values(d).flat().map(dd => dd.accuracy)).flat();
        const kde = kernelDensityEstimator(kernelEpanechnikov(7), kdeY);
        const density = kde(values);

        const xNum = d3.scaleLinear()
            .domain([0, d3.max(density, d => d[1])])
            .range([0, x.bandwidth() / 2]);

        g.append("path")
            .datum(density)
            .attr("transform", `translate(${x(task) + x.bandwidth() / 2},0)`)
            .attr("fill", "#69b3a2")
            .attr("stroke", "#333")
            .attr("stroke-width", 2)
            .attr("opacity", 0.8)
            .attr("d", d3.area()
                .x0(d => -xNum(d[1]))
                .x1(d => xNum(d[1]))
                .y(d => y(d[0]))
                .curve(d3.curveCatmullRom)
            );

        const median = d3.median(values);
        g.append("line")
            .attr("x1", x(task) + x.bandwidth() * 0.1)
            .attr("x2", x(task) + x.bandwidth() * 0.9)
            .attr("y1", y(median))
            .attr("y2", y(median))
            .attr("stroke", "#333")
            .attr("stroke-width", 3)
            .style("stroke-linecap", "round");
    });
}

function drawPromptsViolinPlots(container, data){
    console.log(data)
    const margin = { top: 10, right: 0, bottom: 65, left: 30 };
    const chartTotalWidth = 200;
    const width = chartTotalWidth - margin.left - margin.right;
    const height = 150 - margin.top - margin.bottom;


    let prompts = ["Zero-Shot", "Zero-Shot (COT)", "Few-Shot", "Few-Shot (COT)"];
    let tasks = ["task1", "task2", "task3"];    

    draw_a_violin_plot(tasks, undefined, "tasks");
    draw_a_violin_plot(tasks, "Gemini", "tasks");
    draw_a_violin_plot(tasks, "Mistral", "tasks");
    draw_a_violin_plot(tasks, "GPT", "tasks");
    draw_a_violin_plot(tasks, "GLM", "tasks");
    draw_a_violin_plot(prompts, undefined, "prompts");
    draw_a_violin_plot(prompts, "Gemini", "prompts");
    draw_a_violin_plot(prompts, "Mistral", "prompts");
    draw_a_violin_plot(prompts, "GPT", "prompts");
    draw_a_violin_plot(prompts, "GLM", "prompts");

    function draw_a_violin_plot(arr, filterByModel = undefined, key="prompts"){
        const svg = d3.select(container).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);


        if (filterByModel != undefined && filterByModel.includes('Mistral')) filterByModel = 'mistral-small-3.1-24b';
        else if (filterByModel != undefined && filterByModel.includes('Gemini')) filterByModel = 'gemini-2.5-flash';
        else if (filterByModel != undefined && filterByModel.includes('GPT')) filterByModel = 'gpt-5-2025-08-07';
        else if (filterByModel != undefined && filterByModel.includes('GLM')) filterByModel = 'glm-4.5v-106b';
        if (filterByModel!=undefined && !data.models.includes(filterByModel)) filterByModel = "gpt-5";

        const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

        const x = d3.scaleBand()
        .domain(arr)
        .range([0, width])
        .padding(0.3);

        const y = d3.scaleLinear()
            .domain([0, 100])
            .range([height, 0]);

        g.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "rotate(-30)")
        .style("font-size", "13px")
        .style("text-anchor", "end");

        g.append("g").call(d3.axisLeft(y).ticks(3)).selectAll("text").style("font-size", "13px");

        function kernelDensityEstimator(kernel, X) {
            return function(V) {
                return X.map(function(x) {
                    return [x, d3.mean(V, function(v) { return kernel(x - v); })];
                });
            };
        }
        function kernelEpanechnikov(k) {
            return function(v) {
                v = v / k;
                return Math.abs(v) <= 1 ? 0.75 * (1 - v * v) / k : 0;
            };
        }

        const kdeY = y.ticks(40);

        arr.forEach((elem, i) => {
        // Collect all accuracy values for this prompt across all tasks and models
        let values = Object.values(data.cells).map(d => Object.values(d)).flat().map(d => Object.values(d)).flat().flat()
        .filter(d => {
            if (!filterByModel) return true;
            if (filterByModel) return d.rawModelName.includes(filterByModel);
        })
        .filter(d => {
            if (key === "tasks") {
                if (elem === "task1") return d.test.includes("task1");
                if (elem === "task2") return d.test.includes("task2");
                if (elem === "task3") return d.test.includes("task3");
            } else if (key === "prompts") {
                if (elem === "Zero-Shot") return !d.llmMode.includes("Few") && !d.cotMode.includes("No COT");
                if (elem === "Zero-Shot (COT)") return !d.llmMode.includes("Few") && d.cotMode.includes("COT");
                if (elem === "Few-Shot") return d.llmMode.includes("Few") && !d.cotMode.includes("No COT");
                if (elem === "Few-Shot (COT)") return d.llmMode.includes("Few") && d.cotMode.includes("COT");
            }
        }).map(dd => dd.accuracy);

        const kde = kernelDensityEstimator(kernelEpanechnikov(7), kdeY);
        const density = kde(values);

        const xNum = d3.scaleLinear()
            .domain([0, d3.max(density, d => d[1])])
            .range([0, x.bandwidth() / 2]);

        g.append("path")
            .datum(density)
            .attr("transform", `translate(${x(elem) + x.bandwidth() / 2},0)`)
            .attr("fill", (filterByModel) ? colorPicker(filterByModel) : "#69b3a2")
            .attr("stroke", "#333")
            .attr("stroke-width", 2)
            .attr("opacity", 0.8)
            .attr("d", d3.area()
                .x0(d => -xNum(d[1]))
                .x1(d => xNum(d[1]))
                .y(d => y(d[0]))
                .curve(d3.curveCatmullRom)
            );

        const median = d3.median(values);
        g.append("line")
            .attr("x1", x(elem) + x.bandwidth() * 0.1)
            .attr("x2", x(elem) + x.bandwidth() * 0.9)
            .attr("y1", y(median))
            .attr("y2", y(median))
            .attr("stroke", "#333")
            .attr("stroke-width", 3)
            .style("stroke-linecap", "round");
    });
    }
}
