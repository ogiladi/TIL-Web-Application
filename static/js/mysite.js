// base page functions

$(document).ready(function() {
  $('.fadein').css('visibility', 'visible').hide().fadeIn(3000);
});

function openNav() {
  $('#mySidenav').css('width', '250px');
}

function closeNav() {
  $('#mySidenav').css('width', '0');
}
