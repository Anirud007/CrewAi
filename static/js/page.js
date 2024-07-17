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
        Agent_name.textContent = 'Crew Name : '

        const instanceText = document.createElement('p');
        instanceText.textContent = `${crw.name}`;

        const del_btn_div = document.createElement('div');
        del_btn_div.className = 'flex-shrink-0'

        const addButton = document.createElement('a');
        addButton.textContent = 'Add Agent'
        addButton.className = 'btn btn-primary my-1';
        addButton.href = `/page/${id}/add_agent`;

        const runbtn = document.createElement('a');
        runbtn.textContent = 'Run Crew';
        runbtn.className = 'btn btn-primary mx-1 my-1';
        runbtn.href = `/crews/${id}/output`
        
        text_div.appendChild(Agent_name);
        text_div.appendChild(instanceText);
        del_btn_div.appendChild(addButton);
        del_btn_div.appendChild(runbtn);
        ins_subDiv.appendChild(text_div);
        ins_subDiv.appendChild(del_btn_div);
        instanceDiv.appendChild(ins_subDiv);

        crw.agents.forEach(agent => {
            const agentsDiv = document.createElement('div');
            agentsDiv.className = 'container';
            const agentText = document.createElement('p');
            agentText.textContent = "Agent -- ";
            agentText.textContent += ` ${agent.role}\n`;
            agentsDiv.appendChild(agentText);
            instanceDiv.appendChild(agentsDiv);
        });

        crewDivlist.appendChild(instanceDiv);
    }
}

document.addEventListener('DOMContentLoaded', fetch_crews);

