// Functions for dropdowns

function toggleDropdown(dropdownId) {
    var dropdown = document.getElementById(dropdownId);
    if (dropdown.style.display === 'block') {
        dropdown.style.display = 'none';
    } else { // Close all other dropdowns and then make this one appear
        closeAllDropdowns();
        dropdown.style.display = 'block';
    }
}

// closes all dropdowns
function closeAllDropdowns() {
    closeDropdown('dropdown1');
    closeDropdown('dropdown2');
    closeDropdown('dropdown3');
    // Add more dropdown IDs here if needed
}

// closes a single dropdown
function closeDropdown(dropdownId) {
    var dropdown = document.getElementById(dropdownId);
    dropdown.style.display = 'none';
}

// Functions to copy dropdown lists into the search input

// copies gene into search bar
function copyGeneToInput(){
    var sel = document.getElementById("geneSelections");
    var val = sel.options[sel.selectedIndex].value;
    document.getElementById("searchInput").value = val;
}

// copies mesh into search bar
function copyMeshToInput(){
    var sel = document.getElementById("meshSelections");
    var val = sel.options[sel.selectedIndex].value;
    document.getElementById("meshInput").value = val;
}

// copies multiple genes into search bar and formats them properly
function copyMultipleGenesToInput(){
    var sel = document.getElementById("multipleGeneSelections");
    var val = sel.options[sel.selectedIndex].value;
    var userInput = document.getElementById("multiGeneInput");
    if (userInput.value == ""){
        userInput.value = val;
    } else {
        userInput.value += ',' + val;
    }
}

// Functions to go to results page

// goes to results for gene-id search
document.getElementById('searchButton').addEventListener('click', function() {
    var geneId = document.getElementById('searchInput').value;
    window.location.href = '/static/results.html?geneID=' + encodeURIComponent(geneId);
});

// goes to results for mesh search
document.getElementById('meshSearchButton').addEventListener('click', function() {
    var meshTerm = document.getElementById('meshInput').value;
    if (meshTerm) {
        window.location.href = '/static/results.html?meshTerm=' + encodeURIComponent(meshTerm);
    } else {
        console.log("MeSH term input is empty");
    }


});

// goes to results for multiple gene id search
document.getElementById('multiGeneSearchButton').addEventListener('click', function() {
    var geneIds = document.getElementById('multiGeneInput').value;
    if (geneIds) {
        window.location.href = '/static/results.html?geneIDs=' + encodeURIComponent(geneIds);
    } else {
        console.log("Gene IDs input is empty");
    }
});