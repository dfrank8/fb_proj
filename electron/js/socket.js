routes = {
    "logi": // go out on this route
    {
        "functions": {
            "define": {
                "active": true
            },
            "thesaurus": {
                "active": true
            },
            "wiki": {
                "active": true
            }
        }
    },

    "__uniqueDeveloperID__": // go out on this route
    {
        "functions": {
            "thesaurus": {
                "active": true
            },
            "gif": {
                "active": true
            }
        }
    }
}

var host = "localhost";
var apiRoute = "portal"
var apiVersion = "v1"
var port = "5001";

function sendOutDictionary(query) {

    var route = "http://" + host + ":" + port + "/" + apiRoute + "/" + apiVersion + "/logi";
    console.log(query)
    return $.ajax({
            queryType: "POST",
            url: route,
            data: JSON.stringify(query),
            contentType: 'application/json',
            success: function(data, textStatus, jqXHR)
            {
            	return data;
            }
        })
        .done(function(data) {
            return data;
        })
        .fail(function(error) {
        	debugger
            alert("error");
        })
}
