const BASE_URL = "http://localhost:5000";
const $editUserForm = $("#edit-user-form");

// async function deleteUser(user_id) {
// 	console.debug("deleteUser");
// 	const resp = await axios.delete(`${BASE_URL}/users/${user_id}`);
// 	const msg = resp.data.delete;
//     console.log(msg)
// 	return msg;
// }

$(".delete-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("DeleteButton: onClick");
	const target = $(evt.target);

	const user_id = target.data("user-id");

	const resp = await axios.delete(`${BASE_URL}/users/${user_id}`);
	const msg = resp.data.delete;
	console.log(msg);

	location.reload(true);
});

$(".edit-user-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("EditButton: onSubmit");

	const target = $(evt.target);
	const user_id = target.data("user-id");

	let csrf_token = $("#csrf_token").val();
	let first_name = $("#first_name").val();
	let last_name = $("#last_name").val();
	let username = $("#username").val();
	let email = $("#email").val();
	let phone = $("#phone").val();

	let obj = {
		csrf_token: csrf_token,
		first_name: first_name,
		last_name: last_name,
		username: username,
		email: email,
		phone: phone
	};

	const resp = await axios.patch(`${BASE_URL}/users/${user_id}`, obj);

	window.location.replace(`${BASE_URL}/${resp.data}`);
});
