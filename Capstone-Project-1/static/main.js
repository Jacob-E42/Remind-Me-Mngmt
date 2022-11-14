const BASE_URL = "http://localhost:5000";
const user_id = $("#user_id");

async function deleteUser(user) {
	console.debug("deleteUser");
	const resp = await axios.delete(`${BASE_URL}/users/${user.id}`);
	const msg = resp.data.delete;
}

$(".delete-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("DeleteButton: onSubmit");

	deleteUser(user_id);
});
