const BASE_URL = "http://localhost:5000";

async function deleteUser(user_id) {
	console.debug("deleteUser");
	const resp = await axios.delete(`${BASE_URL}/users/${user_id}`);
	const msg = resp.data.delete;
	return msg;
}

$(".delete-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("DeleteButton: onSubmit");
	const target = $(evt.target);

	const user_id = target.data("user-id");

	const resp = deleteUser(user_id);
	console.log(resp);
	location.reload(true);
});
