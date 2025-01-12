document.addEventListener("DOMContentLoaded", () => {
    const queryInput = document.getElementById("query-input");
    const submitBtn = document.getElementById("submit-btn");
    const responseSection = document.getElementById("response-section");
    const summary = document.getElementById("summary");
    const sourcesList = document.getElementById("sources-list");
    const errorMessage = document.getElementById("error-message");

    const API_URL = "http://localhost:9000/query"; // Adjust to your backend URL

    submitBtn.addEventListener("click", async() => {
        const query = queryInput.value.trim();

        if (!query) {
            showError("Please enter a question.");
            return;
        }

        hideError();
        responseSection.classList.add("hidden");
        submitBtn.disabled = true;

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query }),
            });

            if (!response.ok) {
                throw new Error("Error connecting to the server.");
            }

            const data = await response.json();
            if (data.error) {
                throw new Error(data.error);
            }

            displayResponse(data);
        } catch (error) {
            showError(error.message);
        } finally {
            submitBtn.disabled = false;
        }
    });

    function displayResponse(data) {
        summary.textContent = data.summary;

        sourcesList.innerHTML = "";
        data.sources.forEach((source) => {
            const listItem = document.createElement("li");
            listItem.textContent = `Source: ${source.source}, Chunk: ${source.chunk_index}`;
            sourcesList.appendChild(listItem);
        });

        responseSection.classList.remove("hidden");
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove("hidden");
    }

    function hideError() {
        errorMessage.classList.add("hidden");
        errorMessage.textContent = "";
    }
});