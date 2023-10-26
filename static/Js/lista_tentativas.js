function searchData() {
    var input = document.getElementById("data-search");
    var filter = input.value.toUpperCase();
    var table = document.querySelector(".excel-table");
    var tr = table.getElementsByTagName("tr");

    for (var i = 0; i < tr.length; i++) {
        var td = tr[i].getElementsByTagName("td")[4]; // Assume que a data está na quinta coluna

        if (td) {
            var txtValue = td.textContent || td.innerText;

            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}