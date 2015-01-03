$( document ).ready(function() {
    $('a[data-tracking]').click(function(e) {
        var track = e.target.attributes["data-tracking"].value.split(":");
        var target = e.target.target;

        if (target == "_blank") {
            ga('send', 'event', track[0], track[1], track[2]);
            return true;
        } else {
            var href = e.target.href;
            ga('send', 'event', track[0], track[1], track[2], {
                'hitCallback' : function() {
                        window.location = href;
                }
            });
            return false;
        }
    })
})