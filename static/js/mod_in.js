async function fetch_crews() {
    const response = await fetch('/crews');
    const crws = await response.json();
    const crewDivlist = document.getElementById('crewDivlist');
    crewDivlist.innerHTML = '';

    for (const [id, crw] of Object.entries(crws)) {

        const instanceDiv = document.createElement('div');
        instanceDiv.className = 'container bg-success bg-opacity-50 py-2 px-4 my-3 border border-success border-2 rounded-3 shadow';

        const ins_subDiv = document.createElement('div');
        ins_subDiv.className = 'd-flex flex-row justify-content-center';

        const text_div = document.createElement('div');
        text_div.className = 'w-100 py-2';

        const Agent_name = document.createElement('strong')
        Agent_name.textContent = 'Crew : '

        const instanceText = document.createElement('p');
        instanceText.textContent = `${crw.name}`;

        const del_btn_div = document.createElement('div');
        del_btn_div.className = 'flex-shrink-1'

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.className = 'btn btn-danger btn';
        deleteButton.onclick = () => deleteCrew(id);

        text_div.appendChild(Agent_name);
        text_div.appendChild(instanceText);
        del_btn_div.appendChild(deleteButton);
        ins_subDiv.appendChild(text_div);
        ins_subDiv.appendChild(del_btn_div);
        instanceDiv.appendChild(ins_subDiv);
        crewDivlist.appendChild(instanceDiv);
    }
}
async function create_crew(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const verbose = document.getElementById('verbose').value;
    const memorisation = document.getElementById('memorisation').value;
    response = await fetch('/crews', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({name, verbose, memorisation })
    });

    if (response.ok) {
        fetch_crews();
        document.getElementById('crews_form').reset();
    }
    else {
        const error = await response.json();
        alert(error.error);
    }
}
async function deleteCrew(id) {
    const response = await fetch(`/crews/${id}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        fetch_crews();
    } else {
        const error = await response.json();
        alert(error.error);
    }
}
document.addEventListener('DOMContentLoaded', fetch_crews);