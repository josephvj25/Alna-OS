function saveTextAsFile()
{      

    var textToWrite = document.getElementById("inputTextToSave").value;

    var textFileAsBlob = new Blob([textToWrite], {type:'text/plain'});

    var fileNameToSaveAs = "myNewFile.txt";
    
;

    var downloadLink = document.createElement("a");

    downloadLink.download = fileNameToSaveAs;

    downloadLink.innerHTML = "My Hidden Link";
    

    window.URL = window.URL || window.webkitURL;
          

    downloadLink.href = window.URL.createObjectURL(textFileAsBlob);

    downloadLink.onclick = destroyClickedElement;
// make sure the link is hidden.
    downloadLink.style.display = "none";
// add the link to the DOM
    document.body.appendChild(downloadLink);
    
// click the new link
    downloadLink.click();
}

function destroyClickedElement(event)
{
// remove the link from the DOM
    document.body.removeChild(event.target);
}
