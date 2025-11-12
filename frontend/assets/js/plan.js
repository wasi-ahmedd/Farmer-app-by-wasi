import { createPlan, myPlans } from "./api.js";

/* Expected IDs (no visual change):
   - #planForm  (crop, quantity, sow_date, harvest_date, state, district, taluk, village)
   - #planMsg
   - #myPlansTable  (tbody element to render rows)
*/

function setPlanMsg(msg, ok=false){
  const el = document.getElementById("planMsg");
  if (el) { el.textContent = msg; el.style.color = ok ? "green" : "crimson"; }
  else console.log(msg);
}

const planForm = document.getElementById("planForm");
if (planForm){
  planForm.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const data = Object.fromEntries(new FormData(planForm).entries());
    try {
      if (!data.quantity) throw new Error("quantity required");
      await createPlan(data);
      setPlanMsg("Plan saved ✅", true);
      planForm.reset();
      renderMyPlans();
    } catch(err){ setPlanMsg(err.message); }
  });
}

async function renderMyPlans(){
  const tbody = document.querySelector("#myPlansTable");
  if (!tbody) return;
  try{
    const plans = await myPlans();
    tbody.innerHTML = plans.map(p => `
      <tr>
        <td>${p.crop}</td>
        <td>${p.quantity}</td>
        <td>${p.sow_date}</td>
        <td>${p.harvest_date}</td>
        <td>${p.village}, ${p.taluk}, ${p.district}</td>
      </tr>
    `).join("");
  }catch(e){
    // not logged in as farmer, ignore
  }
}
renderMyPlans();
