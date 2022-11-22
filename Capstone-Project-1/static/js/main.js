"use strict";

const BASE_URL = "http://localhost:5000";
const $body = $("body");
const $currentUserId = $("#current-user").data("user-id");
const $currentUserFirstAndLastName = $("#current-user").data("user-name");
const $currentUserIsAdmin = $("#current-user").data("is-admin");
const $currentUserIsLoggedIn = $("#current-user").data("is-authenticated");
const $navbar = $("nav");
const $navUsers = $("#navUsers");
const $navTasks = $("#navTasks");
const $navCreateTask = $("#navCreateTask");
const $navLogin = $("#navLogin");
const $navSignup = $("#navSignup");
const $navLogout = $("#navLogout");
const $navMyProfile = $("#navMyProfile");
const $showUserLink = $(".show-user-link");
const $createUserButton = $(".create-user-button");
const $editUserButton = $(".edit-user-button");
const $editUserForm = $("#edit-user-form");
const $deleteUserButton = $(".delete-user-button");
const $createTaskButton = $(".create-task-button");
const $editTaskButton = $(".edit-task-button");
const $deleteTaskButton = $(".delete-task-button");
const $completionStatusButton = $(".completion-status-button");
const $assignTaskButton = $(".assign-task-button");
const $editUserAssignmentButton = $(".edit-user-assignment-button");
const $editTaskAssigmentButton = $(".edit-task-assignment-button");
const $deleteAssignmentButton = $(".delete-assignment-button");
const $dailyReminderButton = $(".daily-reminder-button");
const $remindUserButton = $(".remind-user-button");

async function start() {
	console.debug("start");
	await hideLoggedInUserComponents();
	let isLoggedIn = checkForLoggedInUser();
	let isAdmin;
	if ($currentUserIsAdmin) isAdmin = JSON.parse($currentUserIsAdmin.toLowerCase());
	if (isLoggedIn && isAdmin) showAdminUI();
	else if (isLoggedIn && !isAdmin) showRegularUserUI();
	else showAnonymousUserUI();
}

$(start);

$editUserButton.on("click", async function (evt) {
	evt.preventDefault();
	console.debug("EditUserButton: onSubmit");

	const target = $(evt.target);
	const user_id = target.data("user-id");

	let csrf_token = $("#csrf_token").val();
	let first_name = $("#first_name").val();
	let last_name = $("#last_name").val();
	let username = $("#username").val();
	let email = $("#email").val();
	let phone = $("#phone").val();

	let user = {
		csrf_token: csrf_token,
		first_name: first_name,
		last_name: last_name,
		username: username,
		email: email,
		phone: phone
	};

	const resp = await axios.patch(`${BASE_URL}/users/${user_id}`, user);

	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$deleteUserButton.on("click", async function (evt) {
	evt.preventDefault();
	console.debug("DeleteUserButton: onClick");
	const target = $(evt.target);
	const user_id = target.data("user-id");

	const resp = await axios.delete(`${BASE_URL}/users/${user_id}`);
	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$editTaskButton.on("click", async function (evt) {
	evt.preventDefault();
	console.debug("EditTaskButton: onSubmit");

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
	console.debug("DeleteTaskButton: onClick");
	const target = $(evt.target);
	const task_id = target.data("task-id");
	console.log(task_id);
	const resp = await axios.delete(`${BASE_URL}/tasks/${task_id}`);

	window.location.replace(`${BASE_URL}${resp.data}`);
});

$("input[type=checkbox]").ready(async function () {
	$("#remind_daily").val("");
	$("#notify_admin").val("");
});

$("input[type=checkbox]").change(async function (evt) {
	console.log("current value: ", $(evt.target).val());
	if (this.checked === true) {
		$(evt.target).val("y");
	} else {
		$(evt.target).val("");
	}
});

$editUserAssignmentButton.on("click", async function (evt) {
	evt.preventDefault();
	console.debug("EditUserAssignmentButton: onSubmit");

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
	console.debug("EditUserAssignmentButton: onSubmit");

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
	console.debug("DeleteAssignmentButton: onClick");
	const target = $(evt.target);
	const task_id = target.data("task-id");
	const user_id = target.data("user-id");

	const resp = await axios.delete(`${BASE_URL}/assignments/${user_id}/${task_id}`);

	location.reload();
});

$completionStatusButton.on("click", async function (evt) {
	console.debug("completionStatusButton");
	const target = $(evt.target);
	const task_id = target.data("task-id");
	const assignee_id = target.data("assignee-id");

	const resp1 = await axios.post(`${BASE_URL}/tasks/${task_id}/completed`);
	const resp2 = await axios.post(`${BASE_URL}/notify/${task_id}/${assignee_id}`);

	location.replace(`${BASE_URL}/tasks`);
});
