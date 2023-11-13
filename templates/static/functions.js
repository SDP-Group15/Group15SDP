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
} else {
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