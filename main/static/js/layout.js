console.log('JavaScript layout!');

function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
}

function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
}

// DualList
var demo1 = $('select[name="dualListBox"]').bootstrapDualListbox();
$("#demoform").submit(function() {alert($('[name="dualListBox"]').val());
    return false;
});