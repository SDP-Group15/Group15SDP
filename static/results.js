document.addEventListener('DOMContentLoaded', function() {
    const params = new URLSearchParams(window.location.search);
    const geneId = params.get('geneID');
    let currentPage = parseInt(params.get('page')) || 1;

    const resultsTableBody = document.getElementById('resultsTable').querySelector('tbody');
    const currentPageSpan = document.getElementById('currentPage');
    const prevPageButton = document.getElementById('prevPage');
    const nextPageButton = document.getElementById('nextPage');

function fetchResults(page) {
    const params = new URLSearchParams(window.location.search);
    const geneId = params.get('geneID');
    const meshTerm = params.get('meshTerm');
    const geneIDs = params.get('geneIDs');

    let fetchUrl;
    if (geneId) {
        console.log("Gene ID Search: ", geneId);
        fetchUrl = `/searchGene?geneID=${geneId}&page=${page}`;
    } else if (meshTerm) {
        console.log("MeSH Term Search: ", meshTerm);
        fetchUrl = `/searchMesh?meshTerm=${meshTerm}&page=${page}`;
    } else if (geneIDs) {
        console.log("Multiple Genes Search: ", geneIDs);
        fetchUrl = `/searchMultipleGenes?geneIDs=${geneIDs}&page=${page}`;
    } else {
        console.error('No search type specified');
        return;
    }

    console.log("Fetching URL: ", fetchUrl);
    fetch(fetchUrl)
        .then(response => response.json())
        .then(data => {
            populateTable(data.results);
            currentPage = page;
            currentPageSpan.textContent = currentPage;
            // Handle pagination buttons
            prevPageButton.disabled = currentPage === 1;
            nextPageButton.disabled = currentPage >= Math.ceil(data.total / data.per_page);
        })
        .catch(error => console.error('Error:', error));
}


function populateTable(results) {
    resultsTableBody.innerHTML = ''; // Clear existing rows

    results.forEach(result => {
        const row = document.createElement('tr');
        let references = result.references ? result.references.join(', ') : 'No references';
        row.innerHTML = `
            <td>${result.id}</td>
            <td>${result.description}</td>
            <td>${result.score || 'N/A'}</td>
            <td>${result.value || 'N/A'}</td>
            <td>${references}</td>`;
        resultsTableBody.appendChild(row);
    });
}

    prevPageButton.addEventListener('click', () => {
        if (currentPage > 1) fetchResults(currentPage - 1);
    });

    nextPageButton.addEventListener('click', () => {
        fetchResults(currentPage + 1);
    });

    // Initial fetch for page 1 or the specified page
    fetchResults(currentPage);
});