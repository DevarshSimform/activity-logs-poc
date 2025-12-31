document.getElementById("loginForm").onsubmit = async (e) => {
  e.preventDefault();

  const form = new FormData(e.target);

  const res = await fetch("/api/v1/auth/login/admin", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: form.get("username"),
      password: form.get("password"),
    }),
  });

  if (!res.ok) {
    alert("Invalid credentials");
    return;
  }

  const data = await res.json();
  localStorage.setItem("access_token", data.access_token);

  // Proper redirect
  window.location.href = "/activity";
};
