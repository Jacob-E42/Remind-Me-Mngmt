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

$(formatDueTime);

function formatDueTime() {
	for (let time of $("[data-duetime]")) {
		let text = time.dataset.duetime;
		const formattedTime = format24HourTimeString(text);
		time.innerText = formattedTime;
	}
}

function format24HourTimeString(text) {
	let minute = text.slice(-5, -3);
	let hour = parseInt(text.slice(-8, -6));
	let meridiem = hour >= 12 ? "PM" : "AM";
	hour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour;
	return `${hour}:${minute} ${meridiem}`;
}
