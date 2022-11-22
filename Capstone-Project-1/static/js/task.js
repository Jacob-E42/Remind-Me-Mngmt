"use strict";

$editTaskButton.on("click", async function (evt) {
	evt.preventDefault();
	console.debug("editTaskButton");

	const target = $(evt.target);
	const task_id = target.data("task-id");

	let csrf_token = $("#csrf_token").val();
	let title = $("#title").val();
	let description = $("#description").val();
	let resp_type = $("#resp_type").val();
	let due_time = $("#due_time").val();
	let is_completed = $("#is_completed").val();

	let task = {
		csrf_token: csrf_token,
		title: title,
		description: description,
		resp_type: resp_type,
		due_time: due_time,
		is_completed: is_completed
	};
	const resp = await axios.patch(`${BASE_URL}/tasks/${task_id}`, task);
	window.location.replace(`${BASE_URL}${resp.data}`);
});

$deleteTaskButton.on("click", async function (evt) {
	evt.preventDefault();
	console.debug("deleteTaskButton");
	const target = $(evt.target);
	const task_id = target.data("task-id");
	const resp = await axios.delete(`${BASE_URL}/tasks/${task_id}`);
	window.location.replace(`${BASE_URL}${resp.data}`);
});

$completionStatusButton.on("click", async function (evt) {
	console.debug("completionStatusButton");
	const target = $(evt.target);
	const task_id = target.data("task-id");
	const assignee_id = target.data("assignee-id");

	await axios.post(`${BASE_URL}/tasks/${task_id}/completed`);
	await axios.post(`${BASE_URL}/notify/${task_id}/${assignee_id}`);

	location.replace(`${BASE_URL}/tasks`);
});
