"use strict";

$editUserAssignmentButton.on("click", async function (evt) {
	evt.preventDefault();
	console.debug("editUserAssignmentButton");

	const target = $(evt.target);
	const user_id = target.data("user-id");
	const task_id = target.data("task-id");

	let csrf_token = $("#csrf_token").val();
	let remind_daily = $("#remind_daily").val();
	let notify_admin = $("#notify_admin").val();

	let assignment = {
		csrf_token: csrf_token,
		remind_daily: remind_daily,
		notify_admin: notify_admin
	};

	const resp = await axios.patch(`${BASE_URL}/assignments/users/${user_id}/${task_id}`, assignment);
	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$editTaskAssigmentButton.on("click", async function (evt) {
	evt.preventDefault();
	console.debug("editUserAssignmentButton");

	const target = $(evt.target);
	const user_id = target.data("user-id");
	const task_id = target.data("task-id");

	let csrf_token = $("#csrf_token").val();
	let remind_daily = $("#remind_daily").val();
	let notify_admin = $("#notify_admin").val();

	let assignment = {
		csrf_token: csrf_token,
		remind_daily: remind_daily,
		notify_admin: notify_admin
	};

	const resp = await axios.patch(`${BASE_URL}/assignments/tasks/${task_id}/${user_id}`, assignment);
	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$deleteAssignmentButton.on("click", async function (evt) {
	evt.preventDefault();
	console.debug("deleteAssignmentButton");
	const target = $(evt.target);
	const task_id = target.data("task-id");
	const user_id = target.data("user-id");

	await axios.delete(`${BASE_URL}/assignments/${user_id}/${task_id}`);

	location.reload();
});
