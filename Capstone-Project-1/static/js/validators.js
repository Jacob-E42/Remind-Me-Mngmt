async function usernameIsUnique(username, prev_username = null) {
	console.debug("usernameIsUnique");

	const resp = await axios.get(`${BASE_URL}/users/usernames`);

	for (let name of resp.data) {
		if (username === name) {
			if (username === prev_username) return true;
			return false;
		}
	}
	return true;
}
