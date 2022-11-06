$(document).ready(function () {
    $("#page-top").addClass("bg-dark");
});

new Autocomplete('#autocomplete', {
    search: input => {
        const url = "/pheno_autocomplete/?search=" + input
        return new Promise(resolve => {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    resolve(data.payload)
                })
        })
    },
    getResultValue: result => result.trait,
    renderResult: (result, props) => `
                            <li ${props}>
                              <div class="text-start">
                                ${result.trait}
                              </div>
                            </li>
                          `,
    autoSelect: true,
    onSubmit: result => {
        window.open('/phenotype/details/' + result.trait + '/', "_self")
    }
})