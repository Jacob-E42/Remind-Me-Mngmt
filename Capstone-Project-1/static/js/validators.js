async function usernameIsUnique(username) {
	console.debug("usernameIsUnique");
	const resp = await axios.get(`${BASE_URL}/users/usernames`);
	if (username in resp.data) {
		return false;
	} else {
		return true;
	}
}
