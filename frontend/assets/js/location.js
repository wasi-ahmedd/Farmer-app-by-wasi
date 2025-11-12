export async function loadStateDistrictDropdown(stateId, districtId) {
  const stateSelect = document.getElementById(stateId);
  const districtSelect = document.getElementById(districtId);

  const response = await fetch("assets/data/india_states_districts.json");
  const data = await response.json();

  const states = data.states;
  stateSelect.innerHTML = "<option value=''>Select State</option>";
  districtSelect.innerHTML = "<option value=''>Select District</option>";

  // Load all states
  states.forEach((s) => {
    const option = document.createElement("option");
    option.value = s.state;
    option.textContent = s.state;
    stateSelect.appendChild(option);
  });

  // When state changes, load districts
  stateSelect.addEventListener("change", () => {
    const selectedState = states.find((s) => s.state === stateSelect.value);
    districtSelect.innerHTML = "<option value=''>Select District</option>";

    if (selectedState) {
      selectedState.districts.forEach((d) => {
        const option = document.createElement("option");
        option.value = d;
        option.textContent = d;
        districtSelect.appendChild(option);
      });
    }
  });
}
