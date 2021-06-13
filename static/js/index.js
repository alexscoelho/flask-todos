$(document).ready(function () {
  let todoName;
  let id;
  let newTodo;
  $(".edit").click(function (event) {
    todoName = $(this).data("name");
    id = $(this).data("id");
    $("#task-name").val(todoName);
    $("#edit").data("id", id);
  });
  $("input").change(function () {
    newTodo = this.value;
  });
  $("#edit").click(function (event) {
    $.ajax({
      type: "PUT",
      dataType: "json",
      url: `/edit/${id}`,
      data: { name: newTodo },
    });
    window.location.reload();
  });
});
