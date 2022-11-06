$(document).ready(function () {
    $('#phenotype_table').DataTable({
        serverSide: true,
        sAjaxSource: "/pheno_json/",  // new url
        columns: [
            {
                data: 0, render: function (data) {
                    return '<a target="_blank" rel="noopener noreferrer" ' +
                        'href="/phenotype/details/' + data + '">' + data + '</a>';
                },
            }
        ],
    });
});