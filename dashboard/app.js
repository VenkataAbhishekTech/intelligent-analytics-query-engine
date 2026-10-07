const queryInput =
    document.getElementById("queryInput");

const runButton =
    document.getElementById("runButton");

const buttonText =
    document.getElementById("buttonText");

const buttonLoader =
    document.getElementById("buttonLoader");

const errorCard =
    document.getElementById("errorCard");

const errorMessage =
    document.getElementById("errorMessage");

const resultsSection =
    document.getElementById("resultsSection");

const resultQuery =
    document.getElementById("resultQuery");

const confidenceValue =
    document.getElementById("confidenceValue");

const confidenceFill =
    document.getElementById("confidenceFill");

const explanation =
    document.getElementById("explanation");

const generatedLogic =
    document.getElementById("generatedLogic");

const tableContainer =
    document.getElementById("tableContainer");

const newQueryButton =
    document.getElementById("newQueryButton");

const exampleButtons =
    document.getElementById("exampleButtons");

const statusDot =
    document.getElementById("statusDot");

const statusText =
    document.getElementById("statusText");


async function checkHealth() {

    try {

        const response =
            await fetch("/api/health");

        if (!response.ok) {
            throw new Error(
                "Server unavailable"
            );
        }

        statusDot.classList.add(
            "online"
        );

        statusText.textContent =
            "Engine online";

    } catch (error) {

        statusDot.classList.add(
            "offline"
        );

        statusText.textContent =
            "Engine offline";
    }
}


async function loadExamples() {

    try {

        const response =
            await fetch("/api/examples");

        const data =
            await response.json();

        exampleButtons.innerHTML = "";

        data.examples.forEach(
            function (example) {

                const button =
                    document.createElement(
                        "button"
                    );

                button.className =
                    "example-button";

                button.textContent =
                    example;

                button.addEventListener(
                    "click",
                    function () {

                        queryInput.value =
                            example;

                        queryInput.focus();
                    }
                );

                exampleButtons.appendChild(
                    button
                );
            }
        );

    } catch (error) {

        console.error(
            "Could not load examples:",
            error
        );
    }
}


function setLoading(
    loading
) {

    if (loading) {

        runButton.disabled = true;

        buttonText.textContent =
            "Running...";

        buttonLoader.classList.remove(
            "hidden"
        );

    } else {

        runButton.disabled = false;

        buttonText.textContent =
            "Run Query";

        buttonLoader.classList.add(
            "hidden"
        );
    }
}


function showError(
    message
) {

    errorMessage.textContent =
        message;

    errorCard.classList.remove(
        "hidden"
    );

    resultsSection.classList.add(
        "hidden"
    );
}


function hideError() {

    errorCard.classList.add(
        "hidden"
    );
}


function formatValue(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {
        return "-";
    }

    if (
        typeof value === "number"
    ) {

        if (
            Number.isInteger(value)
        ) {
            return value.toString();
        }

        return value.toFixed(2);
    }

    return String(value);
}


function renderTable(
    rows
) {

    if (
        !rows ||
        rows.length === 0
    ) {

        tableContainer.innerHTML =
            `
            <div class="empty-result">
                The query returned no results.
            </div>
            `;

        return;
    }

    const columns =
        Object.keys(rows[0]);

    let html =
        "<table>";

    html += "<thead>";
    html += "<tr>";

    columns.forEach(
        function (column) {

            html +=
                `<th>${escapeHtml(column)}</th>`;
        }
    );

    html += "</tr>";
    html += "</thead>";

    html += "<tbody>";

    rows.forEach(
        function (row) {

            html += "<tr>";

            columns.forEach(
                function (column) {

                    html +=
                        `<td>${escapeHtml(
                            formatValue(
                                row[column]
                            )
                        )}</td>`;
                }
            );

            html += "</tr>";
        }
    );

    html += "</tbody>";
    html += "</table>";

    tableContainer.innerHTML =
        html;
}


function escapeHtml(
    value
) {

    return String(value)
        .replaceAll(
            "&",
            "&amp;"
        )
        .replaceAll(
            "<",
            "&lt;"
        )
        .replaceAll(
            ">",
            "&gt;"
        )
        .replaceAll(
            '"',
            "&quot;"
        )
        .replaceAll(
            "'",
            "&#039;"
        );
}


function displayResult(
    data
) {

    const result =
        data.data;

    resultQuery.textContent =
        result.query;

    explanation.textContent =
        result.explanation ||
        "No explanation available.";

    generatedLogic.textContent =
        result.generated_logic ||
        "No generated SQL available.";

    const score =
        Number(
            result.confidence_score || 0
        );

    const percentage =
        score <= 1
            ? score * 100
            : score;

    const rounded =
        Math.round(
            percentage
        );

    confidenceValue.textContent =
        `${rounded}%`;

    confidenceFill.style.width =
        `${Math.min(
            Math.max(
                percentage,
                0
            ),
            100
        )}%`;

    renderTable(
        result.result
    );

    hideError();

    resultsSection.classList.remove(
        "hidden"
    );

    resultsSection.scrollIntoView(
        {
            behavior: "smooth",
            block: "start"
        }
    );
}


async function runQuery() {

    const query =
        queryInput.value.trim();

    if (!query) {

        showError(
            "Please enter a natural-language query."
        );

        queryInput.focus();

        return;
    }

    setLoading(true);

    hideError();

    try {

        const response =
            await fetch(
                "/api/query",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        {
                            query: query
                        }
                    )
                }
            );

        const data =
            await response.json();

        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.error ||
                "The query could not be processed."
            );
        }

        displayResult(
            data
        );

    } catch (error) {

        console.error(
            error
        );

        showError(
            error.message ||
            "Something went wrong while processing the query."
        );

    } finally {

        setLoading(false);
    }
}


function resetDashboard() {

    queryInput.value = "";

    hideError();

    resultsSection.classList.add(
        "hidden"
    );

    confidenceValue.textContent =
        "0%";

    confidenceFill.style.width =
        "0%";

    queryInput.focus();

    window.scrollTo(
        {
            top: 0,
            behavior: "smooth"
        }
    );
}


runButton.addEventListener(
    "click",
    runQuery
);


newQueryButton.addEventListener(
    "click",
    resetDashboard
);


queryInput.addEventListener(
    "keydown",
    function (event) {

        if (
            event.ctrlKey &&
            event.key === "Enter"
        ) {

            event.preventDefault();

            runQuery();
        }
    }
);


checkHealth();
loadExamples();