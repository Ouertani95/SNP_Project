$(document).ready(function() {
        let pathname = window.location.pathname;
        if (pathname !== "/"){
                $("#home_redirect").removeClass("active");
                if (pathname==="/phenotype_search/"){
                        $("#phenotype_redirect").addClass("active");
                        document.title = "Phenotype search";
                }
                else if (pathname==="/snp_search/"){
                        $("#snp_redirect").addClass("active");
                        document.title = "SNP search";
                }
        }
});