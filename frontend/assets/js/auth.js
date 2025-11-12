import { signup, login, saveToken } from "./api.js";

function setMsg(msg, ok=false){
  const el = document.getElementById("authMsg");
  if (el) { el.textContent = msg; el.style.color = ok ? "green" : "crimson"; }
  else alert(msg);
}

function formToObj(form){
  return Object.fromEntries(new FormData(form).entries());
}

// --- Redirect helper ---
function redirectToDashboard(role){
  if (role === "farmer") {
    window.location.href = "dashboard_farmer.html";
  } else if (role === "customer") {
    window.location.href = "dashboard_customer.html";
  }
}

// --- FARMER SIGNUP ---
const farmerSU = document.getElementById("farmerSignUpForm");
if (farmerSU){
  farmerSU.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const payload = formToObj(farmerSU);
    payload.role = "farmer";
    try {
      const res = await signup(payload);
      saveToken(res.token);
      setMsg("Farmer account created ✅ Redirecting...", true);
      setTimeout(()=>redirectToDashboard("farmer"), 1000);
    } catch(err){ setMsg(err.message); }
  });
}

// --- CUSTOMER SIGNUP ---
const customerSU = document.getElementById("customerSignUpForm");
if (customerSU){
  customerSU.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const payload = formToObj(customerSU);
    payload.role = "customer";
    try {
      const res = await signup(payload);
      saveToken(res.token);
      setMsg("Customer account created ✅ Redirecting...", true);
      setTimeout(()=>redirectToDashboard("customer"), 1000);
    } catch(err){ setMsg(err.message); }
  });
}

// --- FARMER LOGIN ---
const farmerLI = document.getElementById("farmerLoginForm");
if (farmerLI){
  farmerLI.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const payload = formToObj(farmerLI);
    try {
      const res = await login(payload);
      saveToken(res.token);
      setMsg("Farmer login successful ✅ Redirecting...", true);
      setTimeout(()=>redirectToDashboard("farmer"), 1000);
    } catch(err){ setMsg(err.message); }
  });
}

// --- CUSTOMER LOGIN ---
const customerLI = document.getElementById("customerLoginForm");
if (customerLI){
  customerLI.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const payload = formToObj(customerLI);
    try {
      const res = await login(payload);
      saveToken(res.token);
      setMsg("Customer login successful ✅ Redirecting...", true);
      setTimeout(()=>redirectToDashboard("customer"), 1000);
    } catch(err){ setMsg(err.message); }
  });
}
