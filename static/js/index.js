$(document).ready(function () {
  let todoName;
  let id;
  let newTodo;
  $(".edit").click(function (event) {
    $("#edit").css("display", "block");
    $(".add-todo").css("display", "none");
    todoName = $(this).data("name");
    id = $(this).data("id");
    $("#task-name").val(todoName);
    $("#edit").data("id", id);
  });
  $("#task-name").change(function () {
    newTodo = this.value;
    console.log(newTodo);
  });
  $("#due-date").change(function () {
    dueDate = this.value;
    console.log(dueDate);
  });
  $("#edit").click(function (event) {
    $.ajax({
      type: "PUT",
      dataType: "json",
      url: `/edit/${id}`,
      data: { name: newTodo, due_date: dueDate },
    });
    window.location.reload();
  });
});
