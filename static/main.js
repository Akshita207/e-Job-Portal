$(document).ready(function(){
  $('#modal-btn').click(function(){
    $('.ui.modal').modal('show');
  })
})

$(document).ready(function(){
  $('#close-modal-btn').click(function(){
    $('.ui.modal').modal('hide');
  })
})

function viewEmp(className) {
  let classN = '.' + className;
  $(classN).modal('show');
}

function hideEmp(className) {
  let classN = '.' + className;
  $(classN).modal('hide');
}

let ach = 1;
function addAchievementField(ctr) {
  if (ctr == 0 && ach == 1) {
    ach = parseInt(ctr) + 1;
  } 
  else if (ctr > 0 && ach == 1) {
    ach = parseInt(ctr);
  }
  let achievementFields = document.getElementById("id_achievements");
  let newField = document.createElement("div");
  newField.className = "id_achievement";
  newField.innerHTML = `
    <textarea name="achievement${ach}" cols="40" rows="10" value="" id="achievement${ach}"></textarea>
    <button class="btn btn-info" type="button" onclick="removeAchievementField(this)">Remove</button>
  `;
  achievementFields.appendChild(newField);
  ach += 1;
}

function removeAchievementField(field) {
  let achievementFields = document.getElementById("id_achievements");
  let fieldContainer = field.parentNode;
  achievementFields.removeChild(fieldContainer);
  let childs = document.querySelectorAll('[id^="achievement"]');
  for (let i=0; i<childs.length; i++) {
    childs[i].id = "achievement" + i;
    childs[i].name = "achievement" + i;
  }
}

let ed = 1;
function addEducationField(ctr) {
  if (ctr == 0 && ed == 1) {
    ed = parseInt(ctr) + 1;
  } 
  else if (ctr > 0 && ed == 1) {
    ed = parseInt(ctr);
  }
  let educationFields = document.getElementById("educationFields");
  let newField = document.createElement("div");
  newField.className = `educationField educationField${ed}`;
  newField.innerHTML = `
    <label>Degree:</label>
    <input type="text" name="ed-degree-${ed}" id="ed-degree-${ed}">
    <label>University:</label>
    <input type="text" name="ed-university-${ed}" id="ed-university-${ed}">
    <label>Year:</label>
    <input type="number" name="ed-year-${ed}" id="ed-year-${ed}">
    <button class="btn btn-info" type="button" onclick="removeEducationField(this)">Remove</button>
  `;
  educationFields.appendChild(newField);
  ed += 1;
}

function removeEducationField(field) {
  let educationFields = document.getElementById("educationFields");
  let fieldContainer = field.parentNode;
  educationFields.removeChild(fieldContainer);
  let childs = document.querySelectorAll('[class^="educationField"]');
  for (let i=0; i<childs.length; i++) {
    childs[i].class = "educationField educationField" + i;
    let inputObj = childs[i].getElementsByTagName('INPUT');
    for (let j=0; j<inputObj.length; j++) {
      if (inputObj[j].id.includes('degree')) {
        inputObj[j].id = 'ed-degree-' + i;
        inputObj[j].name = 'ed-degree-' + i;
      }
      else if (inputObj[j].id.includes('university')) {
        inputObj[j].id = 'ed-university-' + i;
        inputObj[j].name = 'ed-university-' + i;
      }
      else if (inputObj[j].id.includes('year')) {
        inputObj[j].id = 'ed-year-' + i;
        inputObj[j].name = 'ed-year-' + i;
      } 
    }
  }
}

let wrk = 1;
function addWorkField(ctr) {
  if (ctr == 0 && wrk == 1) {
    wrk = parseInt(ctr) + 1;
  } 
  else if (ctr > 0 && wrk == 1) {
    wrk = parseInt(ctr);
  }
  let workFields = document.getElementById("workFields");
  let newField = document.createElement("div");
  newField.className = `workField workField${wrk}`;
  newField.innerHTML = `
    <label>Company:</label>
    <input type="text" name="wrk-company-${wrk}" id="wrk-company-${wrk}">
    <label>Title:</label>
    <input type="text" name="wrk-title-${wrk}" id="wrk-title-${wrk}">
    <label>Start Date:</label>
    <input type="date" name="wrk-sdate-${wrk}" id="wrk-sdate-${wrk}">
    <label>End Date: (Do not select end date if still working there.)</label>
    <input type="date" name="wrk-edate-${wrk}" id="wrk-edate-${wrk}">
    <button class="btn btn-info" type="button" onclick="removeWorkField(this)">Remove</button>
  `;
  workFields.appendChild(newField);
  wrk += 1;
}

function removeWorkField(field) {
  let workFields = document.getElementById("workFields");
  let fieldContainer = field.parentNode;
  workFields.removeChild(fieldContainer);
  let childs = document.querySelectorAll('[class^="workField"]');
  for (let i=0; i<childs.length; i++) {
    childs[i].class = "workField workField" + i;
    let inputObj = childs[i].getElementsByTagName('INPUT');
    for (let j=0; j<inputObj.length; j++) {
      if (inputObj[j].id.includes('company')) {
        inputObj[j].id = 'wrk-company-' + i;
        inputObj[j].name = 'wrk-company-' + i;
      } 
      else if (inputObj[j].id.includes('title')) {
        inputObj[j].id = 'wrk-title-' + i;
        inputObj[j].name = 'wrk-title-' + i;
      } 
      else if (inputObj[j].id.includes('sdate')) {
        inputObj[j].id = 'wrk-sdate-' + i;
        inputObj[j].name = 'wrk-sdate-' + i;
      } 
      else if (inputObj[j].id.includes('edate')) {
        inputObj[j].id = 'wrk-edate-' + i;
        inputObj[j].name = 'wrk-edate-' + i;
      } 
    }
  }
}