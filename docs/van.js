// $(document).ready(function() {
//   $("#sidebarCollapse").on("click", function() {
//     $("#sidebar").toggleClass("active");
//   });
// });

$(document).ready(function() {
  $("#sidebar").mCustomScrollbar({
    theme: "minimal"
  });

  $("#sidebarCollapse").on("click", function() {
    $("#sidebar, #content").toggleClass("active");
    $(".collapse.in").toggleClass("in");
    $("a[aria-expanded=true]").attr("aria-expanded", "false");
  });
});
