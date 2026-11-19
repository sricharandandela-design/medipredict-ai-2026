
let allSymptoms = [];
let selectedSymptoms = [];

async function loadSymptoms() {
    const symptomList = document.getElementById("symptomList");

    try {
        const response = await fetch("/symptoms");

        if (!response.ok) {
            throw new Error("Could not load symptoms");
        }

        const data = await response.json();
        allSymptoms = data.symptoms || [];

        displaySymptoms(allSymptoms);

        document.getElementById("totalSymptoms").textContent =
            allSymptoms.length;

        document.getElementById("modelStatus").textContent = "Ready";

        updateSelectedCount();

    } catch (error) {
        symptomList.textContent = "Unable to load symptoms.";
        document.getElementById("modelStatus").textContent = "Unavailable";
    }
}

function displaySymptoms(symptoms) {
    const symptomList = document.getElementById("symptomList");
    symptomList.innerHTML = "";

    symptoms.forEach(symptom => {
        const label = document.createElement("label");
        label.className = "symptom-option";

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.value = symptom;
        checkbox.checked = selectedSymptoms.includes(symptom);

        checkbox.addEventListener("change", function () {
            if (this.checked) {
                selectedSymptoms.push(symptom);
            } else {
                selectedSymptoms = selectedSymptoms.filter(
                    item => item !== symptom
                );
            }

            updateSelectedCount();
        });

        label.appendChild(checkbox);
        label.appendChild(
            document.createTextNode(symptom.replace(/_/g, " "))
        );

        symptomList.appendChild(label);
    });
}

function filterSymptoms() {
    const search = document.getElementById("symptomSearch")
        .value.toLowerCase().trim();

    const filtered = allSymptoms.filter(symptom =>
        symptom.replace(/_/g, " ").includes(search)
    );

    displaySymptoms(filtered);
}

function updateSelectedCount() {
    document.getElementById("selectedCount").textContent =
        "Selected Symptoms: " + selectedSymptoms.length;

    document.getElementById("selectedStat").textContent =
        selectedSymptoms.length;

    const summary = document.getElementById("selectedSummary");

    if (selectedSymptoms.length === 0) {
        summary.textContent = "No symptoms selected yet.";
        return;
    }

    summary.innerHTML = `
        <strong>Your Selected Symptoms:</strong><br>
        ${selectedSymptoms.map(symptom =>
            `<span>${escapeHTML(symptom.replace(/_/g, " "))}</span>`
        ).join("")}
    `;
}

function resetSymptoms() {
    selectedSymptoms = [];

    document.getElementById("symptomSearch").value = "";
    document.getElementById("result").innerHTML = "";

    displaySymptoms(allSymptoms);
    updateSelectedCount();
}

async function predictDisease() {
    const resultDiv = document.getElementById("result");

    if (selectedSymptoms.length === 0) {
        resultDiv.textContent = "Please select at least one symptom.";
        return;
    }

    resultDiv.textContent = "Analyzing your symptoms...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                symptoms: selectedSymptoms
            })
        });

        const data = await response.json();

        if (!response.ok) {
            resultDiv.textContent = data.error || "Prediction failed.";
            return;
        }

        const conditions = data.top_conditions || [];

        const conditionCards = conditions.map((condition, index) => `
            <div class="top-condition-card">
                <div class="condition-rank">#${index + 1}</div>
                <div class="condition-details">
                    <h3>${escapeHTML(condition.disease)}</h3>
                    <p>Model score: ${Number(condition.score).toFixed(2)}%</p>
                    <div class="score-track">
                        <div class="score-fill"
                             style="width:${Math.min(100, Math.max(0, Number(condition.score) || 0))}%">
                        </div>
                    </div>
                </div>
            </div>
        `).join("");

        const precautions = (data.precautions || [])
            .map(item => `<li>${escapeHTML(item)}</li>`)
            .join("");

        resultDiv.innerHTML = `
            <div class="prediction-result">
                <h3>✚ Top 3 Possible Conditions</h3>

                <div class="top-conditions">
                    ${conditionCards}
                </div>

                <h4>About the Top-Ranked Condition</h4>
                <p>${escapeHTML(data.description)}</p>

                <h4>General Dataset Precautions</h4>
                <ul>
                    ${precautions || "<li>No information available.</li>"}
                </ul>

                <p class="disclaimer">
                    ${escapeHTML(data.message)}
                    Model scores are not medical probabilities.
                    Consult a qualified healthcare professional.
                </p>
            </div>
        `;

    } catch (error) {
        resultDiv.textContent = "Unable to connect to the server.";
    }
}

function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
}

document.addEventListener("DOMContentLoaded", loadSymptoms);
