"use strict";

let currentUser;

async function hideLoggedInUserComponents() {
	console.debug("hidePageComponents");
	const components = [
		$navbar,
		$navUsers,
		$navTasks,
		$navCreateTask,
		$navLogin,
		$navSignup,
		$navLogout,
		$navMyProfile,
		$createUserButton,
		$dailyReminderButton,
		$editUserButton,
		$assignTaskButton,
		$remindUserButton,
		$deleteUserButton,
		$showUserLink
	];
	components.forEach((c) => c.hide());
}

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

function showAdminComponents() {
	console.debug("ShowAdminComponents");
	const components = [
		$navCreateTask,
		$createUserButton,
		$dailyReminderButton,
		$editUserButton,
		$assignTaskButton,
		$remindUserButton,
		$deleteUserButton,
		$showUserLink
	];
	components.forEach((c) => c.show());
}

function showRegularUserComponents() {
	console.debug("ShowRegularUserComponents");
	const components = [$navbar, $navUsers, $navTasks, $navLogout, $navMyProfile];
	components.forEach((c) => c.show());
}

function showAnonymousUserComponents() {
	console.debug("ShowAnonymousUserComponents");
	const components = [];
	components.forEach((c) => c.show());
}
