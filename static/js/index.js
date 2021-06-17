$(document).ready(function () {
  let todoName;
  let id;
  // let newTodo;
  $(".edit").click(function (event) {
    $("#edit").css("display", "block");
    $(".add-todo").css("display", "none");
    todoName = $(this).data("name");
    id = $(this).data("id");
    $("#task-name").val(todoName);
    $("#edit").data("id", id);
  });
  $("#task-name").change(function () {
    todoName = this.value;
    console.log(todoName);
  });
  $("#due-date").change(function () {
    dueDate = this.value;
    console.log(dueDate);
  });
  $("#edit").click(function (event) {
    console.log(todoName, dueDate);
    $.ajax({
      type: "PUT",
      dataType: "json",
      url: `/edit/${id}`,
      data: { name: todoName, due_date: dueDate },
    });
    window.location.reload();
  });
});
