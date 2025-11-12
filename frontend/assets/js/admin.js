import { getAdminStats, getAllUsers, getAllCrops } from "./api.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    // 1️⃣ Load quick stats
    const stats = await getAdminStats();
    document.getElementById("farmerCount").textContent = stats.farmers;
    document.getElementById("customerCount").textContent = stats.customers;
    document.getElementById("cropCount").textContent = stats.crops;

    // 2️⃣ Populate demand table
    const tbody = document.querySelector("#demandTable tbody");
    tbody.innerHTML = "";
    stats.demand.forEach(d => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${d.crop}</td>
        <td>${d.farmers}</td>
        <td>${d.quantity}</td>
        <td>${d.demand_level}</td>`;
      tbody.appendChild(tr);
    });

    // 3️⃣ View buttons
    const tableContainer = document.getElementById("tableContainer");
    const table = document.getElementById("adminTable");
    const title = document.getElementById("tableTitle");

    document.getElementById("viewFarmersBtn").onclick = async () => {
      title.textContent = "👨‍🌾 All Farmers";
      const data = await getAllUsers("farmer");
      renderTable(data, ["id", "username", "village", "district", "state", "contact"]);
      tableContainer.classList.remove("hidden");
    };
    document.getElementById("viewCustomersBtn").onclick = async () => {
      title.textContent = "🧑‍🤝‍🧑 All Customers";
      const data = await getAllUsers("customer");
      renderTable(data, ["id", "username"]);
      tableContainer.classList.remove("hidden");
    };
    document.getElementById("viewCropsBtn").onclick = async () => {
      title.textContent = "🌾 All Crops";
      const data = await getAllCrops();
      renderTable(data, ["id", "farmer_name", "crop", "quantity", "harvest_date", "district"]);
      tableContainer.classList.remove("hidden");
    };

    function renderTable(rows, cols){
      table.innerHTML = "";
      const thead = table.createTHead();
      const trHead = thead.insertRow();
      cols.forEach(c => trHead.insertCell().textContent = c.toUpperCase());
      const tbody = table.createTBody();
      rows.forEach(r=>{
        const tr = tbody.insertRow();
        cols.forEach(c => tr.insertCell().textContent = r[c] ?? "");
      });
    }
  } catch(err){
    console.error(err);
    alert("Error loading admin data");
  }
});
