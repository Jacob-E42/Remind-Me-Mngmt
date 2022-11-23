$(setCheckBoxes);

function setCheckBoxes() {
	console.debug("setCheckboxes");
	$("#remind_daily").val("");
	$("#notify_admin").val("");
}

$checkboxes.change(async function (evt) {
	console.debug("changeCheckboxes");
	if (this.checked === true) {
		$(evt.target).val("y");
	} else {
		$(evt.target).val("");
	}
});

$(formatDueTime);

function formatDueTime() {
	console.debug("formatDueTime");
	for (let time of $("[data-duetime]")) {
		let text = time.dataset.duetime;
		const formattedTime = format24HourTimeString(text);
		time.innerText = formattedTime;
	}
}

function format24HourTimeString(text) {
	console.debug("format24HourTimeString");
	let minute = text.slice(-5, -3);
	let hour = parseInt(text.slice(-8, -6));
	let meridiem = hour >= 12 ? "PM" : "AM";
	hour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour;
	return `${hour}:${minute} ${meridiem}`;
}

$(getMyTasks);

async function getMyTasks() {
	console.debug("getMyTasks");
	if (window.location.pathname === "/") {
		const userId = $("#current-user").data("user-id");
		const resp = await axios.get(`${BASE_URL}/users/${userId}/tasks`);

		for (let task of resp.data) {
			let html = `<div>
			<h5>
				<a href="/tasks/${task.id}" class="text-decoration-none"><span class="text-dark">
					${task.title} - ${task.id} - ${task.is_completed ? "Completed" : "Incomplete"}</span></a> 
			</h5></div>`;

			$myTasks.append(html);
		}
	}
	return;
}
