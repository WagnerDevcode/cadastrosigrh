document
  .getElementById("register-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const code = event.target.elements.code.value;
    const description = event.target.elements.description.value;

    // Verifica se ambos os campos estão preenchidos
    if (!code || !description) {
      alert("Both fields are required.");
      return;
    }

    // Cria o objeto a ser enviado
    const data = { code, description };

    try {
      // Envia os dados via POST como JSON
      const response = await fetch("/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      if (response.ok) {
        alert(result.message);
        event.target.reset(); // Limpa o formulário após o registro
      } else {
        alert(`Error: ${result.message}`);
      }
    } catch (error) {
      alert("An error occurred: " + error.message);
    }
  });

// Adiciona evento para pesquisa
document
  .getElementById("search-box")
  .addEventListener("input", async function (event) {
    const description = event.target.value;

    if (description) {
      try {
        const response = await fetch(
          `/search?description=${encodeURIComponent(description)}`
        );
        const results = await response.json();
        displayResults(results);
      } catch (error) {
        console.error("Error fetching search results:", error);
      }
    } else {
      document.getElementById("search-results").innerHTML = ""; // Limpa resultados se a pesquisa estiver vazia
    }
  });

// Função para exibir resultados da pesquisa
function displayResults(results) {
  const resultsContainer = document.getElementById("search-results");
  resultsContainer.innerHTML = ""; // Limpa resultados anteriores

  results.forEach((result) => {
    const div = document.createElement("div");
    div.className = "result-item";
    div.textContent = `Code: ${result.code}, Description: ${result.description}`;
    resultsContainer.appendChild(div);
  });

  if (results.length === 0) {
    resultsContainer.innerHTML = "<p>No results found.</p>";
  }
}
