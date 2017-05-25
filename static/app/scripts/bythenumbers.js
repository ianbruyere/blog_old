$(document).ready(function () {
    populateAllListItems();
    populateAllMileageListItems()
    totalCostOfSelected();
});

function populateAllMileageListItems() {
    // this is where i populate everything
    // will probably just make this function the sum of the two filters
    // but for now prototyping it out
    //var distance_Data = JSON.parse(distanceData)
    for (var i = 0; i < distanceData.length; i++) {
        // this will loop through everything in the data and append it
        // to the unordered list and set the class as the categorey of the data
        // eg class="Gas" if the category is gas eventually need multiple columns
        var cumulativeMilesTraveled = buildTableColumn(distanceData[i].fields.cumulativeMilesTraveled);
        var checkInPointPlace = buildTableColumn(distanceData[i].fields.checkInPointPlace);
        var state = buildTableColumn(distanceData[i].fields.state);
        var date = buildTableColumn(distanceData[i].fields.date);
        $('#tableMileage tbody').append('<tr class="' + distanceData[i].fields.state + '">'
            + cumulativeMilesTraveled + checkInPointPlace + state + date + '</tr>')
        $('#ddlStateMiles').append('<option>' + state + '</option>');
    }
}

function populateAllListItems() {
    // this is where i populate everything
    // will probably just make this function the sum of the two filters
    // but for now prototyping it out
    var cost_json = JSON.parse(costData)
    for (var i = 0; i < cost_json.length; i++) {
        // this will loop through everything in the data and append it
        // to the unordered list and set the class as the categorey of the data
        // eg class="Gas" if the category is gas eventually need multiple columns
        var cost = buildTableColumn(cost_json[i].fields.cost);
        var category = buildTableColumn(cost_json[i].fields.category);
        var state = buildTableColumn(cost_json[i].fields.state);
        $('#tableCost tbody').append('<tr class="' + cost_json[i].fields.category + ' ' + cost_json[i].fields.state + '">'
            + cost + category + state + '</tr>')
        $('#ddlState').append('<option>' + state + '</option>');
    }
}

function totalCostOfSelected() {
    // this function will tally up the dollar amount of every
    // single item listed below
    $('#overallCost').text(+totalCategoryCost('Camping') + +totalCategoryCost('Gas') + +totalCategoryCost('Entertainment') + +totalCategoryCost('Food') + +totalCategoryCost('Misc'))
}

// making a serires of filters reutrns
function filterByState() {
    unHideTableRows('#tableCost')
    var selectedState = $('#ddlState').find(':selected').text()
    $('#tableCost tbody').find('tr').each(function () {
        
        if (!$(this).hasClass(selectedState) && selectedState != '') {
            this.hidden = true;
        }
    })

    totalCostOfSelected();

}

function unHideTableRows(tableid) {
    $(tableid).find('tr').each(function () {
        this.hidden = false;
    })
}


function totalCategoryCost(nameOfCategory) {
    var total = 0;
    var listItems = $('#tableCost .' + nameOfCategory + ' td:nth-child(1)');
    listItems.each(function () {
        if (!$(this).is(':hidden')) { // if the value is hidden it does not belong in the current total
            var amount = $(this).text()
            amount = amount.replace('$', '');
            total += +amount
        }
    })
    $('#cost' + nameOfCategory).text(total) // update the desired class value
    return total
}

function clearListCostItems() {
    $('#ulCostItems').empty();
}

function buildTableColumn(value) {
    // helps cut down on difficulty reading
    return '<td>' + value + '</td>'; 
}

// might want to bump this up so as not to be page specific
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    tabcontent = $('.tabcontent');
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = 'none';
    }

    tablinks = $('.tablinks');
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(' active', '');
    }

    document.getElementById(tabName).style.display = 'block';
    evt.currentTarget.className += ' active';
}