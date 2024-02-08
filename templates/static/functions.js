function showText(textId) {
    var textElement = document.getElementById(textId);
    if (textElement.style.display === "none") {
        textElement.style.display = "block";
    } else {
        textElement.style.display = "none";
    }
}

function toggleDropdown(dropdownId) {
    
    var dropdown = document.getElementById(dropdownId);
    if (dropdown.style.display === 'block') {
        dropdown.style.display = 'none';
    } else { // Close all other dropdowns and then make this one appear
        closeAllDropdowns();
        dropdown.style.display = 'block';
    }
}

function filterDropdown(dropdownId) {
var input, filter, ul, a, i;
input = document.getElementById("searchInput");
filter = input.value.toUpperCase();
ul = document.getElementById(dropdownId);

a = ul.getElementsByTagName("a");
for (i = 0; i < a.length; i++) {
    var txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
    } else {
        a[i].style.display = "none";
    }
}
}

document.getElementById('searchButton').addEventListener('click', function() {
    var geneId = document.getElementById('searchInput').value;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/searchGene?geneID=' + encodeURIComponent(geneId), true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            updatePageWithResults(response);
        }
    };
    xhr.send();
});

function updatePageWithResults(results) {
    var resultsDiv = document.getElementById('searchResults');
    resultsDiv.innerHTML = '';

    if (Array.isArray(results)) {
        results.forEach(function(result) {
            // the below line is properties we want to display
            var content = 'ID: ' + result.id + ', Description: ' + result.description + ', Score: ' + result.score + ', References: ' + result.references.join(', ');
            var p = document.createElement('p');
            p.textContent = content;
            resultsDiv.appendChild(p);
        });
    } else {
        // in case the result is not an array (maybe an error message)
        resultsDiv.textContent = results;
    }
}


document.getElementById('searchButton').addEventListener('click', function() {
    var geneId = document.getElementById('searchInput').value;
    window.location.href = '/results.html?geneID=' + encodeURIComponent(geneId) + '&page=1';
});

document.getElementById('meshSearchButton').addEventListener('click', function() {
    var meshTerm = document.getElementById('meshInput').value;
    if (meshTerm) {
        window.location.href = '/static/results.html?meshTerm=' + encodeURIComponent(meshTerm) + '&page=1';
    } else {
        console.log("MeSH term input is empty");
    }


});

document.getElementById('multiGeneSearchButton').addEventListener('click', function() {
    var geneIds = document.getElementById('multiGeneInput').value;
    if (geneIds) {
        window.location.href = '/static/results.html?geneIDs=' + encodeURIComponent(geneIds) + '&page=1';
    } else {
        console.log("Gene IDs input is empty");
    }
});

function closeDropdown(dropdownId) {
    var dropdown = document.getElementById(dropdownId);
    dropdown.style.display = 'none';
}

function closeAllDropdowns() {
    closeDropdown('dropdown1');
    closeDropdown('dropdown2');
    closeDropdown('dropdown3');
    // Add more dropdown IDs here if needed
}
