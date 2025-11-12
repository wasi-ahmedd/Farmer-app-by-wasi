import { searchCrops } from "./api.js";

/* Expected IDs:
   - #searchInput
   - #searchBtn
   - #resultsContainer
*/

function planCard(p){
  const f = p.farmer || {};
  return `
    <div class="card" style="padding:12px; border:1px solid #e6e6e6; border-radius:12px; margin-bottom:10px;">
      <div><b>${p.crop}</b> • ${p.quantity} kg</div>
      <div>Harvest: ${p.harvest_date} | Sown: ${p.sow_date}</div>
      <div>Location: ${p.village}, ${p.taluk}, ${p.district}, ${p.state}</div>
      <div>Farmer: @${f.username || "unknown"} ${f.contact ? " • Contact: " + f.contact : ""}</div>
    </div>
  `;
}

async function doSearch(){
  const q = document.getElementById("searchInput")?.value || "";
  const container = document.getElementById("resultsContainer");
  if (!container) return;
  container.innerHTML = "Searching...";
  try{
    const rows = await searchCrops(q);
    if (!rows.length){ container.innerHTML = "No matching farmers found."; return; }
    container.innerHTML = rows.map(planCard).join("");
  }catch(err){
    container.innerHTML = "Error: " + err.message;
  }
}

const btn = document.getElementById("searchBtn");
if (btn) btn.addEventListener("click", doSearch);

const input = document.getElementById("searchInput");
if (input) input.addEventListener("keydown", (e)=>{ if (e.key==="Enter") doSearch(); });
