document.addEventListener('DOMContentLoaded', function() {
    const params = new URLSearchParams(window.location.search);
    let currentPage = parseInt(params.get('page')) || 1;

    const resultsTableBody = document.getElementById('resultsTable').querySelector('tbody');
    const resultsTableHead = document.getElementById('resultsTable').querySelector('thead')
    const currentPageSpan = document.getElementById('currentPage');
    const prevPageButton = document.getElementById('prevPage');
    const nextPageButton = document.getElementById('nextPage');

function fetchResults(page) {
    const params = new URLSearchParams(window.location.search);
    const geneId = params.get('geneID');
    const meshTerm = params.get('meshTerm');
    const geneIDs = params.get('geneIDs');
    const fetchConfig = {
        method: "GET",
        headers: {
            "content-type": "application/json"
        }
    }

    let fetchUrl;
    if (geneId) {
        // console.log("Gene ID Search: ", geneId);
        fetchUrl = `/searchGene?geneID=${geneId}&page=${page}`;
    } else if (meshTerm) {
        // console.log("MeSH Term Search: ", meshTerm);
        fetchUrl = `/searchMesh?page=${page}`;
        fetchConfig.headers = {
            "content-type": "application/json",
            "meshTerm": meshTerm
        }
    } else if (geneIDs) {
        // console.log("Multiple Genes Search: ", geneIDs);
        fetchUrl = `/searchMultipleGenes?geneIDs=${geneIDs}&page=${page}`;
    } else {
        console.error('No search type specified');
        return;
    }

    // console.log("Fetching URL: ", fetchUrl);
    // fetch api
    fetch(fetchUrl, fetchConfig)
        .then(response => response.json())
        .then(data => {
            if ( fetchUrl.includes("MultipleGenes") ) {
                populateTableMultiple(data.results);
            } else {
                populateTable(data.results);
            }
            // populateTable(data.results);
            currentPage = page;
            currentPageSpan.textContent = currentPage;
            // Handle pagination buttons
            prevPageButton.disabled = currentPage === 1;
            nextPageButton.disabled = currentPage >= Math.ceil(data.total / data.per_page);
        })
        .catch(error => console.error('Error:', error));
}

// populate table for gene search and mesh search
function populateTable(results) {
    resultsTableBody.innerHTML = ''; // Clear existing rows
    resultsTableHead.innerHTML = ''; // Clear existing rows

    const row = document.createElement('tr');
    row.innerHTML = `
        <th>ID</th>
        <th>MeSH Term</th>
        <th>pVal</th>
        <th>Enrichment</th>
        <th>References</th>`;
    resultsTableHead.appendChild(row);

    results.forEach(result => {
        const row = document.createElement('tr');
        let baseUrl = 'https://pubmed.ncbi.nlm.nih.gov/';
        var references = result.references ? result.references.join(',') : 'No references';
        references = baseUrl + references;

        // create a new hyperlink element
        var articleLink = document.createElement('a');
        articleLink.setAttribute('href', references);
        articleLink.setAttribute('target', '_blank');
        articleLink.innerHTML = "Show articles";
        // create new table data cell element
        var td_reference = document.createElement('td');
        td_reference.appendChild(articleLink); // append hyperlink to table cell
        console.log(typeof(result.pVal));
        row.innerHTML = `
            <td>${result.id}</td>
            <td>${result.mesh}</td>
            <td>${parseFloat(result.pVal).toExponential(2) || 'N/A'}</td>
            <td>${parseFloat(result.enrichment).toFixed(2) || 'N/A'}`;
        row.appendChild(td_reference);
        resultsTableBody.appendChild(row);
    });
}

// populate table for multiple gene search
function populateTableMultiple(results) {
    resultsTableBody.innerHTML = ''; // Clear existing rows
    resultsTableHead.innerHTML = ''; // Clear existing rows

    const row = document.createElement('tr');
    row.innerHTML = `
        <th>Combined pVals</th>
        <th>MeSH Term</th>
        <th>Num Genes</th>
        <th>Genes</th>`;
    resultsTableHead.appendChild(row);

    results.forEach(result => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${parseFloat(result.combined_pval).toExponential(2) || 'N/A'}</td>
            <td>${result.mesh}</td>
            <td>${result.num_genes || 'N/A'}</td>
            <td>${result.genes || 'N/A'}`;
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


// functions for loading icon

function setLoader() {
    document.getElementById("tableResultsDiv").style.opacity = 0.5;
    document.getElementById("loader").style.display = "block";
    setTimeout(showPage, 6100);
}

function showPage() {
    document.getElementById("loader").style.display = "none";
    document.getElementById("tableResultsDiv").style.opacity = 1;
    document.getElementById("tableResultsDiv").style.display = "block";
}