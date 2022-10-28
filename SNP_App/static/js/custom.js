$(document).ready(function() {
        let pathname = window.location.pathname;
        $(".nav-link").removeClass("active");
        if (pathname==="/"){
                $("#page-top").addClass("bg-dark text-white");
        }
        else if (pathname==="/phenotype_search/"){
                $("#phenotype_redirect").addClass("active");
                document.title = "Phenotype search";
        }
        else if (pathname==="/snp_search/"){
                $("#snp_redirect").addClass("active");
                $("#snp_table_length").addClass("mb-5");
                document.title = "SNP search";
        }
        else if (pathname==="/about/"){
                $("#about_redirect").addClass("active");
                document.title = "About";
        }
        else if (pathname==="/services/"){
                $("#services_redirect").addClass("active");
                document.title = "Services";
        }
        else if (pathname==="/contact/"){
                $("#contact_redirect").addClass("active");
                document.title = "Contact";
        }

});