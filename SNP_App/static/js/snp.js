$(document).ready(function () {

    var table = $('#snp_table').DataTable({
        dom: 'lrtip',
        serverSide: true,
        sAjaxSource: "/snp_json/",  // new url
        columns: [
            {
                name: "Rsid", data: 0, render: function (data) {
                    return '<a target="_blank" rel="noopener noreferrer" ' +
                        'href="/snp/details/' + data + '">' + data + '</a>';
                },
            },
            {name: "Chrom", data: 1},
            {name: "Chrom_pos", data: 2},
        ],
        initComplete: function () {
            // Apply the search
            this.api().columns().every(function () {
                var that = this;
                $('input', this.header()).on('keyup change clear', function () {
                    if (that.search() !== this.value) {
                        that.search(this.value).draw();
                    }
                });
                $('input', this.header()).on('click', function (e) {
                    e.stopPropagation();
                });
            });
        },
    });
});