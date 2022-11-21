"use strict";

let currentUser;

function checkForLoggedInUser() {
	console.debug("chedkForLoggedInUser");
	let loggedIn = $currentUserIsLoggedIn;
	if (loggedIn === "False") {
		return false;
	} else {
		currentUser = $currentUserFirstAndLastName;
		return true;
	}
}

function showAdminUI() {
	console.debug("showAdminUI");
	showRegularUserComponents();
	showAdminComponents();
}

function showRegularUserUI() {
	console.debug("showRegularUserUI");
	showRegularUserComponents();
}

function showAnonymousUserUI() {
	console.debug("showAnonymousUserUI");
}

function showRegularUserComponents() {
	console.debug("ShowRegularUserComponents");
	const components = [nav, $navUsers, $navTasks, $navLogout, $navMyProfile];
	components.forEach((c) => c.show());
}

function showAdminComponents() {
	console.debug("ShowAdminComponents");
	const components = [$navCreateTask];
	components.forEach((c) => c.show());
}

function showAnonymousUserComponents() {
	console.debug("ShowAnonymousUserComponents");
	const components = [];
	components.forEach((c) => c.show());
}
