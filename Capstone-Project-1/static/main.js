const BASE_URL = "http://localhost:5000";
const $editUserForm = $("#edit-user-form");

// async function deleteUser(user_id) {
// 	console.debug("deleteUser");
// 	const resp = await axios.delete(`${BASE_URL}/users/${user_id}`);
// 	const msg = resp.data.delete;
//     console.log(msg)
// 	return msg;
// }

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

$("#incomplete-tasks-button").on("click", async function (evt) {
	console.debug("Show Incomplete Tasks: 'click'");
	const user_id = $("#incomplete-tasks-button").data("user-id");
	const resp = await axios.get(`${BASE_URL}/tasks/${user_id}/incomplete`);
	incomplete_tasks = resp.data;
	if (incomplete_tasks.lenth === 0) return;
	for (let i = 0; i < incomplete_tasks.length; i++) {
		console.log("incompleted task: ", incomplete_tasks[i]);
		html = htmlGenerator(incomplete_tasks[i], "incomplete-task");
		$("#incomplete-tasks-list").append(html);
		$("#incomplete-tasks-container").removeClass("d-none");
	}
});

$("#upcoming-tasks-button").on("click", async function (evt) {
	console.debug("Show Upcoming Tasks: 'click'");
	const user_id = $("#upcoming-tasks-button").data("user-id");
	const resp = await axios.get(`${BASE_URL}/tasks/${user_id}/upcoming`);
	upcoming_tasks = resp.data;
	if (upcoming_tasks.lenth === 0) return;
	for (let i = 0; i < upcoming_tasks.length; i++) {
		console.log("completed task: ", upcoming_tasks[i]);
		html = htmlGenerator(upcoming_tasks[i], "upcoming-task");
		$("#upcoming-tasks-list").append(html);
		$("#upcoming-tasks-container").removeClass("d-none");
	}
});

function htmlGenerator(obj, code) {
	if (code === "completed-task") {
		return `<li class="card">
		<div class="card-body">
			<div class="card-title">
				<h4>
					<span class="badge text-bg-dark fw-bold">
						<a href="{{url_for('show_task', id=task.id)}}" class="">${obj.title}</a>
					</span>
					<span class="badge bg-secondary fw-semibold">${obj.due_time}</span>
					<span class="m-3 fw-semibold">${obj.is_completed ? "Complete" : "Incomplete"}</span>
				</h4>
			</div>
			<form class="card-text" action="#" method="post">
				<div class="row">
					<div class="col">
						<button
							formaction="{{url_for('edit_completed_status', id=task.id)}}"
							class="btn btn-primary completion-status-button"
							data-admin-id="{{current_user.id}}"
							data-task-id="${obj.id}">
							Mark complete
						</button>
						<button
							class="btn btn-secondary"
							formaction="{{url_for('show_edit_user_assignment', user_id=user.id, task_id=task.id)}}"
							formmethod="get">
							Edit Assignment
						</button>
						<button class="btn btn-info" formaction="{{url_for('assign_user_to_task', id=task.id)}}" formmethod="get">
							Reassign
						</button>
						<button class="btn btn-warning" formaction="{{url_for('remind_for_task', task_id=task.id)}}">
							Remind
						</button>
						<button
							class="btn btn-danger delete-assignment-button"
							data-task-id="{{task.id}}"
							data-user-id="{{user.id}}"
							formaction="{{url_for('remind_for_task', task_id=task.id)}}">
							Delete Assignment
						</button>
					</div>
				</div>
			</form>
		</div>
	</li>`;
	}
}
