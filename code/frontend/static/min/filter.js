// its better to use class, than id  when manupulation of multiple similar elements is needed
// define vars x and y for t_current_stock class and t_cs_editable class
console.log('filters.js loaded')
let tr = document.getElementsByClassName("table_row");
let tid = document.getElementsByClassName("t_id");
let tpn = document.getElementsByClassName("t_part_name");
let tpt = document.getElementsByClassName("t_part_type");
let tms = document.getElementsByClassName("t_min_stock");
let tcs = document.getElementsByClassName("t_current_stock");

let i,j,k;

function filter(){

    fpn = document.getElementById('fiPartName').value;
    fpt = document.getElementById('fiPartType').value;
    // console.log(fpt == "");
    for (i=0; i<= (tr.length); i++) {
        
        if (fpn != ""){
            if ( String(tpn[i].innerHTML.toLowerCase()).includes(fpn.toLowerCase()) == false ) {
                // console.log(i)
                tr[i].style.display = "none";
            }

        }

        if (fpt != ""){
            if (String(tpt[i].innerHTML.toLowerCase()) != fpt.toLowerCase()) {
                // console.log(i)
                tr[i].style.display = "none";
            }

        }
    }


}

function filter_revert(){
    console.log(tr.length)
    for (i=1; i < (tr.length+1); i++) {
        // console.log(i);
        tr[i].style.display = "block";
        
    }
}

// cs in update, clear stands for commited stock from page
// function to switch the table with data to table with mix of data and input cells
function update() {
    // its better to use class, than id  when manupulation of multiple similar elements is needed
// define lets x and y for t_min_stock class and t_ms_editable class
    let x = document.getElementsByClassName("t_min_stock");
    let y = document.getElementsByClassName("t_ms_editable");
    let i;
    // loop over the length of t_min_stock class, for each element in t_min_stock class hide the element
    // for each element in t_ms_editable class, make them visible to enter value
    for (i=0; i < x.length; i++) {
        x[i].style.display = "none";
        y[i].style.display ="block";
    
    }
}

// function to switch table with input cells to just display data
// Clears the data inputs in the input cells and reverts back to default display.
function cell_clear() {
    console.log('clear() called')
    let x = document.getElementsByClassName("t_min_stock");
    let y = document.getElementsByClassName("t_ms_editable");
    let i;
    for (i=0; i < x.length; i++) {

        y[i].value = "";
        // delay(100)
        x[i].style.display = "block";
        y[i].style.display ="none";
        
    }
}

function file_check() {
    let file = document.getElementById('file');
    console.log(file.value.length);
    if (file.value.length>0) {
        let form = document.getElementById('file_form');
        form.submit();
    }
    else {
        alert('File not selected!')
    }
}

function update_check() {
    let quantity = document.getElementsByClassName("t_ms_editable");
    let form = document.getElementById("min_update");
    let i=0;

    for (i; i< quantity.length; i++) {

        if (quantity[i].value !== "") {
            return form.submit();
            
        }
    }

    return alert("Please enter new quantity before commiting!");
}
