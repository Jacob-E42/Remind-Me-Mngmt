"use strict";

let currentUser;

function checkForLoggedInUser() {
	console.debug("chedkForLoggedInUser");
	let loggedIn = JSON.parse($currentUserIsLoggedIn);
	if (loggedIn) {
		currentUser = $currentUserFirstAndLastName;
		return true;
	} else return false;
}

function showAdminUI() {
	return "hi";
}

function showRegularUserUI() {
	return "hi";
}

function showAnonymousUserUI() {
	return "hi";
}
