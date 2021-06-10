$(document).ready(function () {
  $(".edit").click(function (event) {
    todoName = $(this).data("name");
    id = $(this).data("id");
    $("#task-name").val(todoName);
    $("#edit").data("id", id);
    $("#edit").attr("href", `/edit/${id}`);
  });
});
