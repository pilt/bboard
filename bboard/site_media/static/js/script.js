/* Author: Simon Pantzare

*/

$(document).ready(function() {
    $('#toggle-alts').click(function() {
        $('#alts').css('display', 'block');
        $(this).css('display', 'none');
    });

    $('input[name=q]').autocomplete({
        source: function(req, add) {
            $.getJSON("", req, add);
        },
        select: function() {
            $('#search-form').submit();
        }
    });

    if ($('#results .no-results').size()) {
        //  No results were found.
        $('#toggle-alts').click();
    }
    else {
        var search = unescape($.url.param("q").replace(/\+/g, ' '));
        $("#results")
            .highlight(search)
            .masonry()
        ;
    }
});
