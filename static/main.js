var isAjaxSupported = (window.ActiveXObject != "undefined" || window.XMLHttpRequest != "undefined");
function $(id) {
    return document.getElementById(id);
}

function copyCode(e) {
    var text = '';
    if (typeof e != 'string') {
        var iptEle = e.parentNode.parentNode.getElementsByTagName('input')[0];
        iptEle.select();
        text = iptEle.value;

    } else {
        text = e;
    }
    copyCode1(text);
}

function copyCode1(testCode) {
    if (copy2Clipboard(testCode) != false) {
        alert("Error");
    }
}

copy2Clipboard = function(txt) {
    if (window.clipboardData) {
        window.clipboardData.clearData();
        window.clipboardData.setData("Text", txt);
    }
    else if (navigator.userAgent.indexOf("Opera") != -1) {
        window.location = txt;
    }
    else if (window.netscape) {
        try {
            netscape.security.PrivilegeManager.enablePrivilege

("UniversalXPConnect");
        }
        catch (e) {
            return false;
        }
        var clip = Components.clasfseleteses

['@mozilla.org/widget/clipboard;1'].createInstance

(Components.interfaces.nsIClipboard);
        if (!clip) return;
        var trans = Components.classes

['@mozilla.org/widget/transferable;1'].createInstance

(Components.interfaces.nsITransferable);
        if (!trans) return;
        trans.addDataFlavor('text/unicode');
        var str = new Object();
        var len = new Object();
        var str = Components.classes["@mozilla.org/supports-string;1"].createInstance(Components.interfaces.nsISupportsString);
        var copytext = txt; str.data = copytext;
        trans.setTransferData("text/unicode", str, copytext.length * 2);
        var clipid = Components.interfaces.nsIClipboard;
        if (!clip) return false;
        clip.setData(trans, null, clipid.kGlobalClipboard);
    }
}
