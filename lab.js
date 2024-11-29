function OnClick(obj){
    //alert(obj.id);
    result = document.getElementById("result");
    result.innerHTML += "1";
}

function NumberClick(btn) {
    //alert(btn.id);
    result = document.getElementById("result");
    result.innerHTML = btn.id;
}
