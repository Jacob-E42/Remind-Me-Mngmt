"use strict";

const BASE_URL = "http://localhost:5000";
const $body = $("body");
const $currentUserId = $("#current-user").data("user-id");
const $currentUserFirstAndLastName = $("#current-user").data("user-name");
const $currentUserIsAdmin = $("#current-user").data("is-admin");
const $currentUserIsLoggedIn = $("#current-user").data("is-authenticated");
const $editUserForm = $("#edit-user-form");
const $navbar = $("nav");
const $navUsers = $("#navUsers");
const $navTasks = $("#navTasks");
const $navCreateTask = $("#navCreateTask");
const $navLogin = $("#navLogin");
const $navSignup = $("#navSignup");
const $navLogout = $("#navLogout");
const $navMyProfile = $("#navMyProfile");
const $editUserButton = $(".edit-user-button");
const $deleteUserButton = $(".delete-user-button");
const $editTaskButton = $(".edit-task-button");
const $deleteTaskButton = $(".delete-task-button");
const $editUserAssignmentButton = $(".edit-user-assignment-button");
const $editTaskAssigmentButton = $(".edit-task-assignment-button");
const $deleteAssignmentButton = $(".delete-assignment-button");
const $completionStatusButton = $(".completion-status-button");

function hideLoggedInUserComponents() {
	console.debug("hidePageComponents");
	const components = [nav, $navUsers, $navTasks, $navCreateTask, $navLogin, $navSignup, $navLogout, $navMyProfile];
	components.forEach((c) => c.hide());
}

async function start() {
	console.debug("start");
	hideLoggedInUserComponents();
	let isLoggedIn = checkForLoggedInUser();
	let isAdmin;
	if ($currentUserIsAdmin) isAdmin = JSON.parse($currentUserIsAdmin.toLowerCase());
	if (isLoggedIn && isAdmin) showAdminUI();
	else if (isLoggedIn && !isAdmin) showRegularUserUI();
	else showAnonymousUserUI();
}

$(start);

$(".edit-user-button").on("click", async function (evt) {
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

$(".delete-user-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("DeleteUserButton: onClick");
	const target = $(evt.target);
	const user_id = target.data("user-id");

	const resp = await axios.delete(`${BASE_URL}/users/${user_id}`);
	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$(".edit-task-button").on("click", async function (evt) {
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

	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$(".delete-task-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("DeleteTaskButton: onClick");
	const target = $(evt.target);
	const task_id = target.data("task-id");

	const resp = await axios.delete(`${BASE_URL}/tasks/${task_id}`);

	window.location.replace(`${BASE_URL}/${resp.data}`);
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

$(".edit-user-assignment-button").on("click", async function (evt) {
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

$(".edit-task-assignment-button").on("click", async function (evt) {
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

$(".delete-assignment-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("DeleteAssignmentButton: onClick");
	const target = $(evt.target);
	const task_id = target.data("task-id");
	const user_id = target.data("user-id");

	const resp = await axios.delete(`${BASE_URL}/assignments/${user_id}/${task_id}`);

	location.reload();
});

$(".completion-status-button").on("click", async function (evt) {
	console.debug("completion status button");
	const target = $(evt.target);
	const admin_id = target.data("admin-id");
	const task_id = target.data("task-id");

	const resp = await axios.post(`${BASE_URL}/notify/${task_id}/${admin_id}`);
	console.log(resp);
});

$(".completed-tasks-button").on("click", async function (evt) {
	console.debug("Show Completed Tasks: 'click'");
	const user_id = $(".completed-tasks-button").data("user-id");
	const resp = await axios.get(`${BASE_URL}/tasks/${user_id}/completed`);
	completed_tasks = resp.data;
	if (completed_tasks.lenth === 0) return;
	for (let i = 0; i < completed_tasks.length; i++) {
		console.log("completed task: ", completed_tasks[i]);
		html = htmlGenerator(completed_tasks[i], "completed-task");

		// const respHtml = await axios.post(`${BASE_URL}/templates`, {
		// 	headers: { "Content-Type": "application/json" },
		// 	data: { html: html }
		// });
		// console.log(respHtml);
		$("#completed-tasks-list").append(html);
		$("#completed-tasks-container").removeClass("d-none");
	}
});
