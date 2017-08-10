/* Cool Javascript Copy to Clipboard Crossbrowser
Version 1.1
Written by Jeff Baker on March 18, 2016
Copyright 2016 by Jeff Baker - 
http://www.seabreezecomputers.com/tips/copy2clipboard.htm
Paste the following javascript call in your HTML web page:

<script type="text/javascript" src="copy2clipboard.js">
</script>

Then use this javascript code to make a button for an element:

make_copy_button(document.getElementById("textbox"));

Or the following html:

<div onclick="select_all_and_copy(this)">This div will copy when clicked on</div>


*/

function tooltip(el, message) {
    var scrollLeft = document.body.scrollLeft || document.documentElement.scrollLeft;
    var scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
    var x = parseInt(el.getBoundingClientRect().left) + scrollLeft + 10;
    var y = parseInt(el.getBoundingClientRect().top) + scrollTop + 10;
    if (!document.getElementById("copy_tooltip")) {
        var tooltip = document.createElement('div');
        tooltip.id = "copy_tooltip";
        tooltip.style.position = "absolute";
        tooltip.style.border = "1px solid black";
        tooltip.style.background = "#dbdb00";
        tooltip.style.opacity = 1;
        tooltip.style.transition = "opacity 0.3s";
        document.body.appendChild(tooltip);
    } else {
        var tooltip = document.getElementById("copy_tooltip")
    }
    tooltip.style.opacity = 1;
    tooltip.style.left = x + "px";
    tooltip.style.top = y + "px";
    tooltip.innerHTML = "";
    setTimeout(function() { tooltip.style.opacity = 0; }, 2000);
}

function select_all_and_copy(el, clicked_element) {
    // Copy textarea, pre, div, etc.
    if (document.body.createTextRange) {
        // IE 
        var textRange = document.body.createTextRange();
        textRange.moveToElementText(el);
        textRange.select();
        textRange.execCommand("Copy");
        el.setCustomValidity('Copied')
        tooltip(el, "Copied!");
    } else if (window.getSelection && document.createRange) {
        // non-IE
        var editable = el.contentEditable; // Record contentEditable status of element
        var readOnly = el.readOnly; // Record readOnly status of element
        el.contentEditable = true; // iOS will only select text on non-form elements if contentEditable = true;
        el.readOnly = false; // iOS will not select in a read only form element
        var range = document.createRange();
        range.selectNodeContents(el);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range); // Does not work for Firefox if a textarea or input
        if (el.nodeName == "TEXTAREA" || el.nodeName == "INPUT")
            el.select(); // Firefox will only select a form element with select()
        if (el.setSelectionRange && navigator.userAgent.match(/ipad|ipod|iphone/i))
            el.setSelectionRange(0, 999999); // iOS only selects "form" elements with SelectionRange
        el.contentEditable = editable; // Restore previous contentEditable status
        el.readOnly = readOnly; // Restore previous readOnly status 
        if (document.queryCommandSupported("copy")) {
            var successful = document.execCommand('copy');
            if (successful) {
                tooltip(el, "Copied!");
                el.setCustomValidity('Copied')
            } else {
                el.setCustomValidity("Press CTRL+C to copy")
                tooltip(el, "Press CTRL+C to copy");
            }
        } else {
            if (!navigator.userAgent.match(/ipad|ipod|iphone|android|silk/i)) {
                el.setCustomValidity("Press Copy")
                tooltip(el, "Press Copy");
            }
        }
    }
} // end function select_all_and_copy(el) 
