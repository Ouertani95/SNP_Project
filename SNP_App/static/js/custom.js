$(document).ready(function() {
        let pathname = window.location.pathname;
        $(".nav-link").removeClass("active");
        if (pathname==="/"){
                $("#page-top").addClass("bg-dark text-white");
        }
        else if (pathname==="/phenotype_search/"){
                $("#phenotype_redirect").addClass("active");
        }
        else if (pathname==="/snp_search/"){
                $("#snp_redirect").addClass("active");
        }
        else if (pathname==="/about/"){
                $("#about_redirect").addClass("active");
        }
        else if (pathname==="/services/"){
                $("#services_redirect").addClass("active");
        }
        else if (pathname==="/contact/"){
                $("#contact_redirect").addClass("active");
        }

});