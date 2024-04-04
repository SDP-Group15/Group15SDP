document.addEventListener('DOMContentLoaded', function() {
    const params = new URLSearchParams(window.location.search);
    let currentPage = parseInt(params.get('page')) || 1;

    const resultsTableBody = document.getElementById('resultsTable').querySelector('tbody');
    const resultsTableHead = document.getElementById('resultsTable').querySelector('thead')
    const currentPageSpan = document.getElementById('currentPage');
    const prevPageButton = document.getElementById('prevPage');
    const nextPageButton = document.getElementById('nextPage');

function fetchResults(page) {
    // document.getElementById("tableResultsDiv").style.opacity = 0.5;
    const params = new URLSearchParams(window.location.search);
    const geneId = params.get('geneID');
    const meshTerm = params.get('meshTerm');
    const geneIDs = params.get('geneIDs');
    const per_page = params.get('per_page') ?? '20';
    const sort_by = params.get('sort_by') ?? 'p_Value';

    const fetchConfig = {
        method: "GET",
        headers: {
            "content-type": "application/json"
        }
    }

    let fetchUrl;
    if (geneId) {
        // console.log("Gene ID Search: ", geneId);
        fetchUrl = `/searchGene?geneID=${geneId}&page=${page}&per_page=${per_page}&sort_by=${sort_by}`;
    } else if (meshTerm) {
        // console.log("MeSH Term Search: ", meshTerm);
        fetchUrl = `/searchMesh?page=${page}&per_page=${per_page}$sort_by=${sort_by}`;
        fetchConfig.headers = {
            "content-type": "application/json",
            "meshTerm": meshTerm
        }
    } else if (geneIDs) {
        // console.log("Multiple Genes Search: ", geneIDs);
        // sort_by = params.get('sort_by') ?? 4;
        fetchUrl = `/searchMultipleGenes?geneIDs=${geneIDs}&page=${page}&per_page=${per_page}&sort_by=${sort_by}`;
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
    // document.getElementById("tableResultsDiv").style.opacity = 1;
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
        // console.log(typeof(result.pVal));
        row.innerHTML = `
            <td>${result.id}</td>
            <td>${result.mesh}</td>
            <td>${parseFloat(result.pVal).toExponential(2) || 'N/A'}</td>
            <td>${parseFloat(result.enrichment).toFixed(2) || 'N/A'}`;
        row.appendChild(td_reference);
        resultsTableBody.appendChild(row);
    });

    showPage();
    
}

// populate table for multiple gene search
function populateTableMultiple(results) {
    // document.getElementById("tableResultsDiv").style.opacity = 1;
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

    showPage();
    
}

    prevPageButton.addEventListener('click', () => {
        setLoader();
        if (currentPage > 1) fetchResults(currentPage - 1);
    });

    nextPageButton.addEventListener('click', () => {
        setLoader();
        fetchResults(currentPage + 1);
    });

    // Initial fetch for page 1 or the specified page
    fetchResults(currentPage);
});


// functions for loading icon
const tableResultsDiv = document.getElementById('tableResultsDiv').style;
const pagination = document.getElementById('pagination').style;
const loader = document.getElementById('loader').style;

// show the loading icon
function setLoader() {
    tableResultsDiv.opacity = 0.5
    loader.display = "block";  
}

// hide loader and display sections previously hidden
function showPage() {
    loader.display = "none";
    tableResultsDiv.opacity = 1;
    tableResultsDiv.display = "block";
    pagination.display = "block";
}

// function for changing number of results on page
function changeNumResults(numResults) {
    // get current url
    var url = window.location.href;

    // update url with new number of results
    if (url.includes('per_page') ) {
        indexOfPage = url.indexOf('per_page')
        replaceStr = url.substring(indexOfPage, indexOfPage+11)

        url = url.replace(replaceStr, "per_page="+numResults);
    } else {
        url += '&per_page=' + numResults;
    }

    // set window location to new url and fetch results again
    window.location.href = url;
    fetchResults(currentPage);
}

// function to change what value to sort by
function sortByValue(sortValue) {
    // get current url
    var url = window.location.href;

    // update url with new number of results
    if (url.includes('sort_by') ) {
        // need to change to only replace sort_by section
        indexOfPage = url.indexOf('sort_by')
        replaceStr = url.substring(indexOfPage, url.length);

        url = url.replace(replaceStr, "sort_by="+sortValue);
    } else {
        url += '&sort_by=' + sortValue;
    }

    // set window location to new url and fetch results again
    window.location.href = url;
    fetchResults(currentPage);
}
