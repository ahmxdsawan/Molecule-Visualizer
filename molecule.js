



// document.addEventListener("DOMContentLoaded", function () {
//     const moleculeSelect = document.getElementById("molecule-select");
//     moleculeSelect.addEventListener("change", () => {
//         const selectedMolecule = moleculeSelect.value;

//         switch (selectedMolecule) {
//             case "water":
//                 document.getElementById("svg-container").innerHTML = waterSVG;
//                 break;
//             case "caffeine":
//                 document.getElementById("svg-container").innerHTML = caffeineSVG;
//                 break;
//             case "isopentanol":
//                 document.getElementById("svg-container").innerHTML = isopentanolSVG;
//                 break;
//             // case :
//             //     document.getElementById("svg-container").innerHTML = "";
//             default:
//                 document.getElementById("svg-container").innerHTML = "";
//                 break;
//         }
//     });
// });


// function addTableRow() {
//     var element_number = $('#element_number').val();
//     var element_code = $('#element_code').val();
//     var element_name = $('#element_name').val();
//     var color1 = $('#color1').val();
//     var color2 = $('#color2').val();
//     var color3 = $('#color3').val();
//     var radius = $('#radius').val();

//     var row = $('<tr>');
//     var col1 = $('<td>').text(element_number);
//     var col2 = $('<td>').text(element_code);
//     var col3 = $('<td>').text(element_name);
//     var col4 = $('<td>').text(color1);
//     var col5 = $('<td>').text(color2);
//     var col6 = $('<td>').text(color3);
//     var col7 = $('<td>').text(radius);
//     var col8 = document.createElement('td');

//     var btn = document.createElement('button');

//     btn.innerHTML = 'Remove';
//     btn.type = 'button';

//     btn.onclick = function() {
//       $(this).closest('tr').remove();
//       saveTableData();
//     };

//     col8.appendChild(btn);
//     row.append(col1, col2, col3, col4, col5, col6, col7, col8);

//     $('#elements-table').append(row);
//     saveTableData();
//   }

function addTableRow() {
  var element_number = $('#element_number').val();
  var element_code = $('#element_code').val();
  var element_name = $('#element_name').val();
  var color1 = $('#color1').val();
  var color2 = $('#color2').val();
  var color3 = $('#color3').val();
  var radius = $('#radius').val();

  var row = $('<tr>');
  var col1 = $('<td>').text(element_number);
  var col2 = $('<td>').text(element_code);
  var col3 = $('<td>').text(element_name);
  var col4 = $('<td>').text(color1);
  var col5 = $('<td>').text(color2);
  var col6 = $('<td>').text(color3);
  var col7 = $('<td>').text(radius);
  var col8 = document.createElement('td');

  var btn = document.createElement('button');

  btn.innerHTML = 'Remove';
  btn.action_type = 'remove-list'
  btn.type = 'button';
  btn.id = 'remove-element-button'; // add id attribute

  btn.type = 'button';
  console.log("Hello world!");


  btn.onclick = function () {

    var row = $(this).closest('tr');
    var elementNumber = $(tr).find('td input:eq(0)').val()
    console.log("Hello world!");


    $.post('/add_remove.html', {
      id: 'remove-element-button',
      action_type: 'remove-list',
      element_number: elementNumber
    }, function (response) {

      console.log(response);
      row.remove();
    });
  };

  col8.appendChild(btn);
  row.append(col1, col2, col3, col4, col5, col6, col7, col8);

  $('#elements-table').append(row);
  saveTableData();
}


function saveTableData() {
  var data = [];
  $('#elements-table tbody tr').each(function (index, element) {
    var tds = $(this).find('td');
    var row = {
      element_number: $(tds[0]).text(),
      element_code: $(tds[1]).text(),
      element_name: $(tds[2]).text(),
      color1: $(tds[3]).text(),
      color2: $(tds[4]).text(),
      color3: $(tds[5]).text(),
      radius: $(tds[6]).text()
    };
    data.push(row);
  });
  localStorage.setItem('elements-table', JSON.stringify(data));
}

function loadTableData() {
  var data = JSON.parse(localStorage.getItem('elements-table'));
  if (data) {
    for (var i = 0; i < data.length; i++) {
      var row = $('<tr>');
      var col1 = $('<td>').text(data[i].element_number);
      var col2 = $('<td>').text(data[i].element_code);
      var col3 = $('<td>').text(data[i].element_name);
      var col4 = $('<td>').text(data[i].color1);
      var col5 = $('<td>').text(data[i].color2);
      var col6 = $('<td>').text(data[i].color3);
      var col7 = $('<td>').text(data[i].radius);
      var col8 = document.createElement('td');

      var btn = document.createElement('button');

      btn.innerHTML = 'Remove';
      btn.type = 'button';
      btn.name = 'action_type'
      btn.value = 'button';
      btn.id = 'remove-element-button'; // add id attribute

      btn.onclick = function () {

        $(this).closest('tr').remove();
        var row = $(this).closest('tr');
        var elementNumber = row.find('td:first').text();

        $.post('/add_remove.html', {
          id: 'remove-element-button',
          action_type: 'remove-list',
          elementNumber: elementNumber
        }, function (response) {
          console.log(response);
          row.remove();
        });
        saveTableData();
      };

      //saveTableData();

      col8.appendChild(btn);
      row.append(col1, col2, col3, col4, col5, col6, col7, col8);

      $('#elements-table').append(row);

    }
  }
}

$(document).ready(function () {
  loadTableData();
});

$(document).ready(function () {
  $('#molecule-select').on('change', function () {
    var selectedMolecule = $(this).val();
    var svgContent = $('option[value="' + selectedMolecule + '"]').data('svg');
    $('#svg-container').html(svgContent);
  });
});

