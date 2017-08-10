// Mixing jQuery and Node.js code in the same file? Yes please!
// Requirements
const remote = require('electron').remote;
// JSON data loads
var google_translate_languages = require('./data/translateLanguages.json');

$(function() {
    // // Display some statistics about this computer, using node's os module.
    // var os = require('os');
    // var prettyBytes = require('pretty-bytes');

    // // Demonstrating the os-accessibility of electron
    // $('.stats').append('Number of cpu cores: <span>' + os.cpus().length + '</span>');
    // $('.stats').append('Free memory: <span>' + prettyBytes(os.freemem()) + '</span>');

    // // Electron's UI library. We will need it for later.
    // // var shell = require('shell');
});

// Constants used for the clicking, and the error handling. 
var clicks = 0;
var timer;
var button_released = false;
var dbl_click_delay = 500;
var error_message_delay = 3000;

// mouse down happens on every mouse down
function submit_mouse_down(e) {
    button_released = false;
    clicks++; //count clicks
    // grab the element
    tb = $('#main_ignite_text_box');
    if (clicks === 1) {
        // start a timer to not jump the gun when a double click is coming. 
        timer = setTimeout(function() {
            // if the timer ends, and since it started the button has been released, we count is as a single click. 
            if (button_released) {
                // on the button
                // single click!!
                var newDict = {};
                console.log("single click")
                var text = $('#main_ignite_text_box').text().trim()
                var selectedText = GetSelectedText();
                console.log("text = ", text)
                console.log("selected text = ", selectedText)
                    // debugger
                if (selectedText.length > 0) {
                    var newText = text.replace(selectedText, '<span class="highlightedContent">' + selectedText + '</span>')
                    tb.html(newText);
                    newDict["functions"] = preferencesToDict();
                    newDict["full_text"] = $('#main_ignite_text_box').text().trim();
                    newDict["highlighted_text"] = selectedText;
                    $.when(sendOutDictionary(newDict)).done(function(data) {
                        console.log("got DICT:" + data)
                        renderDivs(data);
                    })
                } else {
                    // display an error (because no text was highlighted) and clear up the text. 
                    $('.error_area').html("No highlighted text!");
                    timer = setTimeout(function() {
                        $('.error_area').html("");
                        tb.html(tb.children("span").html());
                    }, error_message_delay);
                }
            } else {
                // if the button is still down, its a hold
                console.log("hold");
                tb.html('<span class="highlightedContent">' + $('#main_ignite_text_box').text().trim() + '</span>');
                var newDict = {};
                newDict["functions"] = preferencesToDict();
                newDict["full_text"] = $('#main_ignite_text_box').text().trim();
                newDict["highlighted_text"] = $('#main_ignite_text_box').text().trim();

                $.when(sendOutDictionary(newDict)).done(function(data) {
                    console.log("got DICT:" + data)
                    renderDivs(data);
                })

            }
            clicks = 0; //after action performed, reset counter
        }, dbl_click_delay);

    } else {
        //perform double-click action

        // this means timer because theres a click queued from < 500 ms before
        clearTimeout(timer); //prevent single-click action
        console.log("Double Click");
        // separate the text by spaces
        var text = $('#main_ignite_text_box').text().trim().split(' ');
        // drop the last word and store it in a variable
        var last = text.pop();
        // double click means grab last word.
        var newText = text.join(" ") + " " + ('<span class="highlightedContent">' + last + '</span>');
        tb.html(newText);
        var newDict = {};
        newDict["functions"] = preferencesToDict();
        newDict["full_text"] = $('#main_ignite_text_box').text().trim();
        newDict["highlighted_text"] = last;

        $.when(sendOutDictionary(newDict)).done(function(data) {
            console.log("got DICT:" + data)
            renderDivs(data);
        })

        clicks = 0; //after action performed, reset counter
    }
}

function GetSelectedText() {
    if (document.getSelection) { // all browsers, except IE before version 9
        var sel = document.getSelection();
        // sel is a string in Firefox and Opera, 
        // and a selectionRange object in Google Chrome, Safari and IE from version 9
        // the alert method displays the result of the toString method of the passed object
        return String(sel);
    } else {
        if (document.selection) { // Internet Explorer before version 9
            var textRange = document.selection.createRange();
            alert(String(textRange.text));
        }
    }
}

function revert() {
    console.log("reverted");
    button_released = true;
}

function preferencesToDict() {
    var dict = {};
    $('#user_preferences').find('li').each(function() {
        if ($(this).attr("class") == "list-group-item") {
            if ($(this).attr("id") == "list-item-translate") {
                // we add extra attributes to the translate thing since it has "from" and "to" parameters.
                var translateString = String($(this).find("input").attr("id"));
                dict[translateString] = {}
                dict[translateString]["enabled"] = $(this).find("input").is(":checked");
                $(this).children("form").children("select").each(function() {
                    if ($(this).attr("id") == "Translate_From") {
                        // enter this into the dictionary
                        dict[translateString]["from"] = String($(this).val()).toLowerCase();
                    } else if ($(this).attr("id") == "Translate_To") {
                        // enter this into the dictionary
                        dict[translateString]["to"] = String($(this).val()).toLowerCase();
                    } else {
                        throw { name: "NotImplementedError", message: "There is an extra attribute in the translate list-group-item. Not good. Fix it." };
                    }
                });
            } else {
                // translate is the only unique preference at this time, so everything else has the same function:
                dict[String($(this).find("input").attr("id"))] = $(this).find("input").is(":checked");
            }
            console.log(String($(this).find("input").attr("id")) + " has been set to: " + $(this).find("input").is(":checked"));
        }
    });
    return dict;
}

function prepareLanguageDropdowns() {
    var sorted_list = new Array();
    for (var key in google_translate_languages) {
        // debugger
        if (google_translate_languages.hasOwnProperty(key)) {
            sorted_list.push(key)
        }
    }
    sorted_list.sort()
    var translate_from = $('#Translate_From');
    var translate_to = $('#Translate_To');
    sorted_list.forEach(function(language, i) {
        var html = $('<option>' + language + '</option>');
        html.attr('value', language);
        if (language == "Detect") {
            // detect is only for the "from" category and should be at the default and selected by default
            html.attr('selected', 'selected');
            html.clone().prependTo(translate_from);
        } else if (language == "English") {
            // english is in both columns, but is selected by default on the "from" side
            html.attr('selected', 'selected');
            html.clone().prependTo(translate_to);
        } else {
            // everything else is normal
            html.clone().appendTo(translate_from);
            html.clone().appendTo(translate_to);
        }
        // debugger
    });
    translate_from.prop('disabled', true);
    translate_to.prop('disabled', true);
}

function renderDivs(data) {
    $("#returnDataContainer").html(data);
    var divCount = $("#resultsContainer").children().length;
    var divsRendered = 0;

    var returnDataContainer = $("#returnDataContainer");
    //body reference 
    var body = document.getElementsByTagName("body")[0];

    // create elements <table> and a <tbody>
    var tbl = document.createElement("table");
    var tblBody = document.createElement("tbody");

    // cells creation
    while (divCount > 0) {
        // table row creation
        var row = document.createElement("tr");

        for (var i = 0; i < 3; i++) {
            // create element <td> and text node 
            //Make text node the contents of <td> element
            // put <td> at end of the table row
            var cell = document.createElement("td");

            if(divCount == 0)
            {
                break;
            }

            $(cell).html(($("#resultsContainer").children()[divsRendered]));
            row.appendChild(cell);
            divCount -= 1;
        }

        //row added to end of table body
        tblBody.appendChild(row);
    }

    // append the <tbody> inside the <table>
    tbl.appendChild(tblBody);
    // put <table> in the <body>
    $(returnDataContainer).html(tbl);
    // tbl border attribute to 
    tbl.setAttribute("border", "2");
}

function textarea_drop(ev, target) {
    ev.preventDefault();
    $('#main_ignite_text_box').find(".highlightedContent").html($(ev.dataTransfer.getData("text/html"))[1])
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData('text', ev.target.id);
}

function external_link_new_window_from_tag(event) {
    const remote = require('electron').remote;
    const BrowserWindow = remote.BrowserWindow;

    var win = new BrowserWindow({ width: 800, height: 600 });
    win.loadURL($(event).attr("tag"));
    return false;
}

function action_item_click(event) {
    debugger
}


$(document).ready(function() {
    $('.dropdown-menu').on("click", function(e) {
        // stop propagation makes the menu not close when it is clicked (which is the default behavior)
        e.stopPropagation();
    });

    $('#returnDataContainer').on('click', '.actionItem', function(e) {
        $('#main_ignite_text_box').find(".highlightedContent").html(e.target);
    });

    $('.pref_checkbox').change(function(e) {
        // Got the checking done here. 
        preferencesToDict();
        if ($(e.target).attr("id") == "pref_Translate") {
            if (!$(e.target).is(':checked')) {
                $('#Translate_To').prop('disabled', true);
                $('#Translate_From').prop('disabled', true);
            } else {
                $('#Translate_To').prop('disabled', false);
                $('#Translate_From').prop('disabled', false);
            }
        }
    });
    prepareLanguageDropdowns();

});
