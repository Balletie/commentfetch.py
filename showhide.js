function getFirstChild(el) {
    var firstChild = el.firstChild;
    while (firstChild != null && firstChild.nodeType == 3) { // skip TextNodes
        firstChild = firstChild.nextSibling;
    }
    return firstChild;
}

function getNextSibling(e) {
    while (e && (e = e.nextSibling)) {
        if (e.nodeType == 1) {
            return e
        }
    }
    return undefined
}

function hideAll() {
    hide_nested = document.querySelectorAll(".root>.allnested");
    hide_rootmd = document.querySelectorAll(".root>.md");
    for (var i = 0; i < hide_nested.length; i++) {
        hide_nested[i].style.display = "none";
        hide_rootmd[i].style.display = "none";
    }
    getFirstChild(document.body).innerHTML = "Show All";
    getFirstChild(document.body).setAttribute("onclick", "return showAll()");
    return true;
}

function showAll() {
    show_nested = document.querySelectorAll(".root>.allnested");
    show_rootmd = document.querySelectorAll(".root>.md");
    for (var i = 0; i < hide_nested.length; i++) {
        show_nested[i].style.display = "block";
        show_rootmd[i].style.display = "block";
    }
    getFirstChild(document.body).innerHTML = "Hide All";
    getFirstChild(document.body).setAttribute("onclick", "return hideAll()");
    return true;
}

function hide(e) {
    pre = e.parentNode;
    md = getNextSibling(pre);
    md.style.display = "none";
    allnested = getNextSibling(md);
    allnested.style.display = "none";
    e.innerHTML = "Show";
    e.setAttribute("onclick", "return show(this)");
    return true
}

function show(e) {
    pre = e.parentNode;
    md = getNextSibling(pre);
    md.style.display = "block";
    allnested = getNextSibling(md);
    allnested.style.display = "block";
    e.innerHTML = "Hide";
    e.setAttribute("onclick", "return hide(this)");
    return true
}
