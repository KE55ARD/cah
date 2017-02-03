function clog(txt)
{
  console.log(txt);
}

$(document).ready(function() {

  //Request permission on page load
  document.addEventListener('DOMContentLoaded', function () {
    if (Notification.permission !== "granted") {
      Notification.requestPermission();
    }
  });

  dropsearch();

});
