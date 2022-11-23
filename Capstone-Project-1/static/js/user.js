"use strict";

$createUserButton.on("click", async function (evt) {
	console.debug("createUserButton");

	let username = $("#username").val();

	if (!(await usernameIsUnique(username))) {
		await axios.post(`${BASE_URL}/flash`, {"msg": "That username is already taken."});
		window.location.reload();
	}
});

$editUserButton.on("click", async function (evt) {
	evt.preventDefault();
	console.debug("editUserButton");

	const target = $(evt.target);
	const user_id = target.data("user-id");
	const prev_username = target.data("username");

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
	if (!(await usernameIsUnique(username, prev_username))) {
		await axios.post(`${BASE_URL}/flash`, {"msg": "That username is already taken."});
		window.location.reload();
	} else {
		const resp = await axios.patch(`${BASE_URL}/users/${user_id}`, user);
		window.location.replace(`${BASE_URL}${resp.data}`);
	}
});

$deleteUserButton.on("click", async function (evt) {
	evt.preventDefault();
	console.debug("deleteUserButton");
	const target = $(evt.target);
	const user_id = target.data("user-id");

	const resp = await axios.delete(`${BASE_URL}/users/${user_id}`);
	console.log(resp.data);
	window.location.replace(`${BASE_URL}/users`);
});
